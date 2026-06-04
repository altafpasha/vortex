import os
import threading
import uuid
from functools import wraps
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

DOWNLOAD_DIR = "/app/downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

VORTEX_PASSWORD = os.environ.get('VORTEX_PASSWORD', '')
active_tokens = set()

downloads = {}
playlist_jobs = {}

PRESETS = [
    {'id': 'video_best', 'label': 'Best Quality', 'type': 'video', 'ext': 'mp4', 'badge': 'AUTO'},
    {'id': 'video_1080', 'label': '1080p',        'type': 'video', 'ext': 'mp4', 'badge': 'MP4'},
    {'id': 'video_720',  'label': '720p',          'type': 'video', 'ext': 'mp4', 'badge': 'MP4'},
    {'id': 'video_480',  'label': '480p',          'type': 'video', 'ext': 'mp4', 'badge': 'MP4'},
    {'id': 'video_360',  'label': '360p',          'type': 'video', 'ext': 'mp4', 'badge': 'MP4'},
    {'id': 'audio_mp3',  'label': 'MP3',           'type': 'audio', 'ext': 'mp3', 'badge': 'AUDIO'},
    {'id': 'audio_m4a',  'label': 'M4A',           'type': 'audio', 'ext': 'm4a', 'badge': 'AUDIO'},
    {'id': 'audio_wav',  'label': 'WAV',           'type': 'audio', 'ext': 'wav', 'badge': 'LOSSLESS'},
]

def _vfmt(h):
    # language_preference>=0 excludes auto-dubbed tracks, prefers original audio
    return (
        f'bestvideo[height<={h}][ext=mp4]+bestaudio[language_preference>=0][ext=m4a]/'
        f'bestvideo[height<={h}][ext=mp4]+bestaudio[ext=m4a]/'
        f'bestvideo[height<={h}]+bestaudio[language_preference>=0]/'
        f'bestvideo[height<={h}]+bestaudio/'
        f'best[height<={h}]/best'
    )

_BEST_AUDIO = 'bestaudio[language_preference>=0]/bestaudio/best'

FORMAT_MAP = {
    'video_best': {'format': 'bestvideo[ext=mp4]+bestaudio[language_preference>=0][ext=m4a]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best', 'merge': 'mp4'},
    'video_1080': {'format': _vfmt(1080), 'merge': 'mp4'},
    'video_720':  {'format': _vfmt(720),  'merge': 'mp4'},
    'video_480':  {'format': _vfmt(480),  'merge': 'mp4'},
    'video_360':  {'format': _vfmt(360),  'merge': 'mp4'},
    'audio_mp3':  {'format': _BEST_AUDIO, 'convert': 'mp3'},
    'audio_m4a':  {'format': _BEST_AUDIO, 'convert': 'm4a'},
    'audio_wav':  {'format': _BEST_AUDIO, 'convert': 'wav'},
}

LANG_NAMES = {
    'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
    'hi': 'Hindi', 'ja': 'Japanese', 'ko': 'Korean', 'pt': 'Portuguese',
    'ru': 'Russian', 'zh': 'Chinese', 'ar': 'Arabic', 'it': 'Italian',
    'tr': 'Turkish', 'pl': 'Polish', 'nl': 'Dutch', 'sv': 'Swedish',
    'id': 'Indonesian', 'th': 'Thai', 'vi': 'Vietnamese', 'uk': 'Ukrainian',
    'cs': 'Czech', 'ro': 'Romanian', 'hu': 'Hungarian', 'fi': 'Finnish',
    'da': 'Danish', 'no': 'Norwegian', 'ms': 'Malay', 'bn': 'Bengali',
    'ta': 'Tamil', 'te': 'Telugu', 'ml': 'Malayalam', 'mr': 'Marathi',
    'pa': 'Punjabi', 'gu': 'Gujarati', 'kn': 'Kannada', 'ur': 'Urdu',
}

def lang_name(code):
    if not code:
        return code
    base = code.split('-')[0].lower()
    return LANG_NAMES.get(base, code.upper())


# ── Auth ──────────────────────────────────────────────────────────────────────

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not VORTEX_PASSWORD:
            return f(*args, **kwargs)
        token = request.headers.get('X-Auth-Token', '')
        if token not in active_tokens:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated


@app.route('/api/auth/check', methods=['GET'])
def auth_check():
    """Returns whether a password is required."""
    return jsonify({'auth_required': bool(VORTEX_PASSWORD)})


@app.route('/api/login', methods=['POST'])
def login():
    if not VORTEX_PASSWORD:
        return jsonify({'token': 'open', 'ok': True})
    data = request.json or {}
    if data.get('password') == VORTEX_PASSWORD:
        token = str(uuid.uuid4())
        active_tokens.add(token)
        return jsonify({'token': token, 'ok': True})
    return jsonify({'error': 'Invalid password'}), 401


@app.route('/api/logout', methods=['POST'])
def logout():
    token = request.headers.get('X-Auth-Token', '')
    active_tokens.discard(token)
    return jsonify({'ok': True})


# ── Progress hooks ────────────────────────────────────────────────────────────

def make_progress_hook(download_id):
    def hook(d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            percent = (downloaded / total * 100) if total else 0
            downloads[download_id].update({
                'status': 'downloading',
                'percent': round(percent, 1),
                'speed': d.get('speed', 0),
                'eta': d.get('eta', 0),
                'downloaded': downloaded,
                'total': total,
            })
        elif d['status'] == 'finished':
            downloads[download_id].update({
                'status': 'processing',
                'percent': 100,
                'filepath': d['filename'],
            })
        elif d['status'] == 'error':
            downloads[download_id]['status'] = 'error'
    return hook


# ── Info / analyze ────────────────────────────────────────────────────────────

@app.route('/api/info', methods=['POST'])
@require_auth
def get_info():
    data = request.json or {}
    url = data.get('url', '').strip()
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True, 'extract_flat': 'in_playlist'}) as ydl:
            info = ydl.extract_info(url, download=False)

        # ── Playlist ──
        if info.get('_type') == 'playlist':
            entries = []
            for e in (info.get('entries') or []):
                if e:
                    entries.append({
                        'title': e.get('title', 'Unknown'),
                        'url': e.get('url') or e.get('webpage_url', ''),
                        'thumbnail': e.get('thumbnail', ''),
                        'duration': e.get('duration', 0),
                    })
            return jsonify({
                'type': 'playlist',
                'title': info.get('title', 'Playlist'),
                'uploader': info.get('uploader', ''),
                'count': len(entries),
                'entries': entries[:100],
                'formats': PRESETS,
            })

        # ── Single video ──
        return jsonify({
            'type': 'video',
            'title': info.get('title', 'Unknown'),
            'thumbnail': info.get('thumbnail', ''),
            'duration': info.get('duration', 0),
            'uploader': info.get('uploader', ''),
            'view_count': info.get('view_count', 0),
            'formats': PRESETS,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Single download ───────────────────────────────────────────────────────────

@app.route('/api/download', methods=['POST'])
@require_auth
def start_download():
    data = request.json or {}
    url = data.get('url', '').strip()
    preset_id = data.get('preset_id', 'video_best')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    preset = FORMAT_MAP.get(preset_id, FORMAT_MAP['video_best'])
    download_id = str(uuid.uuid4())
    downloads[download_id] = {'status': 'starting', 'percent': 0}

    def run():
        try:
            fmt = preset['format']
            ydl_opts = {
                'format': fmt,
                'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
                'progress_hooks': [make_progress_hook(download_id)],
                'quiet': True,
                'no_warnings': True,
                'concurrent_fragment_downloads': 4,
            }

            if 'merge' in preset:
                ydl_opts['merge_output_format'] = preset['merge']

            if 'convert' in preset:
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': preset['convert'],
                    'preferredquality': '192',
                }]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                if 'convert' in preset:
                    base = os.path.splitext(filename)[0]
                    filename = f"{base}.{preset['convert']}"
                downloads[download_id].update({
                    'status': 'done',
                    'filename': os.path.basename(filename),
                    'filepath': filename,
                    'title': info.get('title', ''),
                })
        except Exception as e:
            downloads[download_id].update({'status': 'error', 'error': str(e)})

    threading.Thread(target=run, daemon=True).start()
    return jsonify({'download_id': download_id})


# ── Playlist download ─────────────────────────────────────────────────────────

@app.route('/api/playlist/download', methods=['POST'])
@require_auth
def download_playlist():
    data = request.json or {}
    url = data.get('url', '').strip()
    preset_id = data.get('preset_id', 'video_best')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    preset = FORMAT_MAP.get(preset_id, FORMAT_MAP['video_best'])
    job_id = str(uuid.uuid4())
    playlist_jobs[job_id] = {
        'status': 'starting', 'total': 0, 'done': 0,
        'errors': 0, 'current': '', 'percent': 0,
    }

    def run():
        try:
            completed = [0]
            total_count = [0]

            def progress_hook(d):
                if d['status'] == 'finished':
                    completed[0] += 1
                    pct = (completed[0] / total_count[0] * 100) if total_count[0] else 0
                    playlist_jobs[job_id].update({
                        'done': completed[0],
                        'percent': round(pct, 1),
                        'status': 'downloading',
                    })
                elif d['status'] == 'downloading':
                    title = d.get('info_dict', {}).get('title', '')
                    if title:
                        playlist_jobs[job_id]['current'] = title

            # Get total count first
            with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True}) as ydl:
                pinfo = ydl.extract_info(url, download=False)
                total_count[0] = len(pinfo.get('entries') or [])
                playlist_jobs[job_id]['total'] = total_count[0]

            ydl_opts = {
                'format': preset['format'],
                'outtmpl': os.path.join(DOWNLOAD_DIR, '%(playlist_title)s/%(title)s.%(ext)s'),
                'progress_hooks': [progress_hook],
                'quiet': True,
                'no_warnings': True,
                'ignoreerrors': True,
                'concurrent_fragment_downloads': 4,
            }
            if 'merge' in preset:
                ydl_opts['merge_output_format'] = preset['merge']
            if 'convert' in preset:
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': preset['convert'],
                    'preferredquality': '192',
                }]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            playlist_jobs[job_id].update({'status': 'done', 'percent': 100})
        except Exception as e:
            playlist_jobs[job_id].update({'status': 'error', 'error': str(e)})

    threading.Thread(target=run, daemon=True).start()
    return jsonify({'job_id': job_id})


@app.route('/api/playlist/status/<job_id>')
@require_auth
def playlist_status(job_id):
    return jsonify(playlist_jobs.get(job_id, {'status': 'not_found'}))


# ── File serving & library ────────────────────────────────────────────────────

@app.route('/api/status/<download_id>')
@require_auth
def get_status(download_id):
    return jsonify(downloads.get(download_id, {'status': 'not_found'}))


@app.route('/api/file/<download_id>')
@require_auth
def serve_file(download_id):
    info = downloads.get(download_id)
    if not info or info.get('status') != 'done':
        return jsonify({'error': 'File not ready'}), 404
    filepath = info.get('filepath')
    if not filepath or not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    return send_file(filepath, as_attachment=True, download_name=info.get('filename'))


@app.route('/api/downloads')
@require_auth
def list_downloads():
    files = []
    total_size = 0
    for fname in os.listdir(DOWNLOAD_DIR):
        fpath = os.path.join(DOWNLOAD_DIR, fname)
        if os.path.isfile(fpath):
            size = os.path.getsize(fpath)
            total_size += size
            files.append({'name': fname, 'size': size, 'modified': os.path.getmtime(fpath)})
    files.sort(key=lambda x: x['modified'], reverse=True)
    return jsonify({'files': files, 'total_size': total_size, 'count': len(files)})


@app.route('/api/file/direct/<filename>')
@require_auth
def serve_direct(filename):
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'Not found'}), 404
    return send_file(filepath, as_attachment=True)


@app.route('/api/file/delete/<filename>', methods=['DELETE'])
@require_auth
def delete_file(filename):
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({'ok': True})
    return jsonify({'error': 'Not found'}), 404


@app.route('/api/clear', methods=['DELETE'])
@require_auth
def clear_all():
    count = 0
    for fname in os.listdir(DOWNLOAD_DIR):
        fpath = os.path.join(DOWNLOAD_DIR, fname)
        if os.path.isfile(fpath):
            os.remove(fpath)
            count += 1
    downloads.clear()
    return jsonify({'ok': True, 'deleted': count})


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
