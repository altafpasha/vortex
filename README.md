```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    ██╗   ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗     ║
║    ██║   ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝     ║
║    ██║   ██║██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝      ║
║    ╚██╗ ██╔╝██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗      ║
║     ╚████╔╝ ╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗     ║
║      ╚═══╝   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝     ║
║                                                              ║
║              MEDIA EXTRACTOR  //  v3.0                       ║
║         Personal YouTube Downloader — Self Hosted            ║
╚══════════════════════════════════════════════════════════════╝
```

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)
![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-FF0000?style=flat-square&logo=youtube&logoColor=white)
![nginx](https://img.shields.io/badge/nginx-proxy-009639?style=flat-square&logo=nginx&logoColor=white)
![License](https://img.shields.io/badge/License-Private-red?style=flat-square)

**A self-hosted, password-protected media downloader with a full dashboard UI.**  
Download YouTube videos and playlists in any format — from laptop or mobile.

</div>

---

## Table of Contents

- [Features](#features)
- [UI Preview](#ui-preview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Format Options](#format-options)
- [Playlist Download](#playlist-download)
- [API Reference](#api-reference)
- [File Management](#file-management)
- [Updating](#updating)
- [Troubleshooting](#troubleshooting)
- [Stack](#stack)

---

## Features

```
┌─────────────────────────────────────────────────────────────┐
│  ⚡ CORE                                                     │
│     • Paste any YouTube URL — metadata fetched automatically │
│     • Playlist detection — download entire playlists        │
│     • Real-time progress bar with speed + ETA display       │
│     • 4× parallel fragment downloads for maximum speed      │
│     • Original audio track always selected (no auto-dub)    │
│                                                             │
│  🎛  FORMAT SUPPORT                                         │
│     • Video  → Best Quality / 1080p / 720p / 480p / 360p   │
│     • Audio  → MP3 / M4A / WAV (ffmpeg conversion)         │
│     • All video output merged to MP4                        │
│                                                             │
│  🔐 SECURITY                                                │
│     • Password protection via .env                          │
│     • Session token stored in browser localStorage          │
│     • All API endpoints require auth token                  │
│     • Open access mode when no password is set              │
│                                                             │
│  📁 FILE MANAGEMENT                                         │
│     • Browser folder picker — choose where files save       │
│     • Auto-download to browser Downloads on mobile          │
│     • Local library with per-file delete + Clear All        │
│     • Storage stats on dashboard (files, MB used)           │
│                                                             │
│  🐳 PRODUCTION READY                                        │
│     • Gunicorn WSGI server (not Flask dev server)           │
│     • nginx reverse proxy with /api/ routing                │
│     • Docker Compose — single command deploy                │
│     • Works on laptop + mobile browser                      │
└─────────────────────────────────────────────────────────────┘
```

---

## UI Preview

```
┌─────────────────────────────────────────────────────────────────┐
│  VORTEX      MEDIA EXTRACTOR // v3.0          ● SYSTEM ONLINE   │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ FILES        │  │ STORAGE      │  │ ACTIVE       │          │
│  │     12       │  │   847 MB     │  │     1        │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                 │
│  00 // SAVE LOCATION ──────────────────────────────────────     │
│  [ 📁 CHOOSE FOLDER ]   📂 Downloads  ✕                         │
│                                                                 │
│  01 // TARGET URL ──────────────────────────────────────── ✕    │
│  ┌─────────────────────────────────────────┐ ┌───────────┐     │
│  │  https://youtube.com/watch?v=...        │ │  ANALYZE  │     │
│  └─────────────────────────────────────────┘ └───────────┘     │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ ▓▓▓▓▓  Video Title Here                                 │   │
│  │ ▓▓▓▓▓  CHANNEL: Example   DURATION: 4:32   VIEWS: 2.1M  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  02 // SELECT FORMAT ──────────────────────────────────────     │
│  ┌──────────────────────────┐                                   │
│  │  📹 VIDEO  │  🎵 AUDIO  │                                   │
│  └──────────────────────────┘                                   │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │Best ✦AUTO│ │ 1080p MP4│▌│  720p MP4│ │  480p MP4│           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    ⚡  EXTRACT                            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  03 // EXTRACTION PROGRESS ────────────────────────────────     │
│  Video Title Here...                          [ DOWNLOADING ]   │
│  ████████████████████░░░░░░░░░░  63.4%                          │
│  PROGRESS: 63.4%   SPEED: 8.2 MB/s   ETA: 12s   SIZE: 248 MB   │
│                                                                 │
│  // LOCAL LIBRARY ──────────────────────── [ 🗑 CLEAR ALL ]     │
│  ┌────┬────────────────────────────────┬────────┬──────────┐    │
│  │ MP4│ Video Title.mp4               │ 248 MB │ [↓] [✕] │    │
│  │ MP3│ Audio Track.mp3               │ 8.4 MB │ [↓] [✕] │    │
│  └────┴────────────────────────────────┴────────┴──────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Architecture

```
                        Browser / Mobile
                              │
                     http://HOST:8080
                              │
                    ┌─────────▼──────────┐
                    │       nginx         │
                    │   (reverse proxy)   │
                    └────┬──────────┬────┘
                         │          │ /api/*
                    ┌────▼────┐  ┌──▼───────────────────────┐
                    │  Static │  │    Gunicorn + Flask        │
                    │  HTML   │  │  (1 worker · 4 threads)   │
                    └─────────┘  │                           │
                                 │  yt-dlp  ──►  ffmpeg      │
                                 │  in-memory download state  │
                                 └──────────┬────────────────┘
                                            │ bind mount
                                    ┌───────▼────────┐
                                    │  ./downloads/  │
                                    │  (host folder) │
                                    └────────────────┘
```

---

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Docker | 24+ | [Install Docker](https://docs.docker.com/get-docker/) |
| Docker Compose | v2 | Bundled with Docker Desktop |
| Port `8080` | free | Configurable in `docker-compose.yml` |

> **No Python, Node, or ffmpeg required on the host** — everything runs inside containers.

---

## Installation

**1. Get the project**

```bash
git clone https://github.com/altafpasha/vortex.git vortex-ytdl
cd vortex-ytdl
```

**2. Set your password**

```bash
# Open .env and fill in your password
VORTEX_PASSWORD=your_secure_password_here
```

> Leave `VORTEX_PASSWORD=` empty for open access (no login screen shown).

**3. Start**

```bash
docker compose up --build -d
```

**4. Open**

```
http://localhost:8080
```

The login screen appears automatically if a password is configured.

---

## Configuration

All settings live in `.env` at the project root:

```env
# ─────────────────────────────────────────────────
#  VORTEX  ·  Environment Configuration
# ─────────────────────────────────────────────────

# Access password. Leave empty = no login required.
VORTEX_PASSWORD=your_secure_password
```

> ⚠️ `.env` is in `.gitignore` — it is never committed to git.

### Change the port

Edit `docker-compose.yml`:

```yaml
ports:
  - "9090:80"    # change 8080 to any free port
```

### Change the download folder

```yaml
volumes:
  - /your/custom/path:/app/downloads    # absolute path on host
```

---

## Usage

### Download a single video

```
1.  Open  http://localhost:8080
2.  Log in with your password
3.  Paste a YouTube URL into the input
4.  Click  ANALYZE
5.  Select video quality or audio format
6.  Click  ⚡ EXTRACT
7.  File saves to your Downloads folder automatically
```

### Choose a custom save folder *(desktop only)*

```
1.  Click  📁 CHOOSE FOLDER
2.  Pick any folder on your computer
3.  All downloads save there silently — no dialog each time
```

> On **mobile**, files save to the phone's default Downloads folder automatically.  
> Folder picker works in Chrome, Edge, and Opera on desktop.

### Access from mobile

Find your computer's local IP, then open on any phone/tablet:

```
http://192.168.x.x:8080
```

Find your IP:

```powershell
# Windows
ipconfig

# Mac / Linux
ip addr show
```

---

## Format Options

### Video

| Option | Resolution | Container |
|--------|-----------|-----------|
| Best Quality | Highest available | MP4 |
| 1080p | 1920 × 1080 | MP4 |
| 720p | 1280 × 720 | MP4 |
| 480p | 854 × 480 | MP4 |
| 360p | 640 × 360 | MP4 |

### Audio

| Option | Format | Bitrate |
|--------|--------|---------|
| MP3 | `.mp3` | 192 kbps |
| M4A | `.m4a` | Best available |
| WAV | `.wav` | Lossless |

> **Original audio is always used.** Auto-dubbed and dubbed tracks are excluded automatically via `language_preference >= 0` in the yt-dlp format selector.

---

## Playlist Download

```
1.  Paste a YouTube playlist URL
    e.g. youtube.com/playlist?list=PLxxxxxxxx

2.  Click  ANALYZE
    → App detects the playlist and lists all video titles

3.  Select a format

4.  Click  ⚡ EXTRACT PLAYLIST
    → Live progress shows  X / total  and current video name

5.  Files are saved to  downloads/<playlist-name>/
```

> Videos that fail within a playlist are skipped automatically — the rest continue downloading.

---

## API Reference

All endpoints require the header:

```
X-Auth-Token: <token>
```

Token is returned by `/api/login`. Omit the header only for `/api/login`, `/api/auth/check`, and `/health`.

### Auth

| Method | Endpoint | Body | Returns |
|--------|----------|------|---------|
| `GET` | `/api/auth/check` | — | `{ auth_required: bool }` |
| `POST` | `/api/login` | `{ password }` | `{ token, ok }` |
| `POST` | `/api/logout` | — | `{ ok }` |

### Download

| Method | Endpoint | Body | Returns |
|--------|----------|------|---------|
| `POST` | `/api/info` | `{ url }` | Metadata + format list |
| `POST` | `/api/download` | `{ url, preset_id }` | `{ download_id }` |
| `GET` | `/api/status/:id` | — | Progress object |
| `GET` | `/api/file/:id` | — | File (attachment) |

### Playlist

| Method | Endpoint | Body | Returns |
|--------|----------|------|---------|
| `POST` | `/api/playlist/download` | `{ url, preset_id }` | `{ job_id }` |
| `GET` | `/api/playlist/status/:id` | — | Job progress |

### Library

| Method | Endpoint | Returns |
|--------|----------|---------|
| `GET` | `/api/downloads` | File list + stats |
| `GET` | `/api/file/direct/:name` | File (attachment) |
| `DELETE` | `/api/file/delete/:name` | `{ ok }` |
| `DELETE` | `/api/clear` | `{ ok, deleted }` |

### Preset IDs

| `preset_id` | Description |
|-------------|-------------|
| `video_best` | Best available MP4 |
| `video_1080` | 1080p MP4 |
| `video_720` | 720p MP4 |
| `video_480` | 480p MP4 |
| `video_360` | 360p MP4 |
| `audio_mp3` | MP3 · 192 kbps |
| `audio_m4a` | M4A · best bitrate |
| `audio_wav` | WAV · lossless |

---

## File Management

### In-app controls

| Button | Action |
|--------|--------|
| **↓ GET** | Download file to browser |
| **✕** | Delete file (no confirmation) |
| **🗑 CLEAR ALL** | Delete all files instantly |

### On the filesystem

```
vortex-ytdl/
└── downloads/
    ├── Video Title.mp4
    ├── Audio Track.mp3
    └── My Playlist/
        ├── 01 - Episode One.mp4
        └── 02 - Episode Two.mp4
```

---

## Updating

### Update yt-dlp only *(no rebuild needed)*

```bash
docker compose exec backend pip install -U yt-dlp
docker compose restart backend
```

### Full rebuild *(after code changes)*

```bash
docker compose down
docker compose up --build -d
```

### Stop / Start

```bash
docker compose down        # stop containers
docker compose up -d       # start (no rebuild)
```

---

## Troubleshooting

### "Requested format is not available"

YouTube changes formats regularly. Update yt-dlp:

```bash
docker compose exec backend pip install -U yt-dlp
docker compose restart backend
```

### "Sign in to confirm you're not a bot" / YouTube Blocks

YouTube aggressively blocks automated requests. Vortex v3.0 includes several built-in countermeasures (Deno JS runtime, rate limiting, user-agent spoofing), but you may still need to provide your YouTube cookies:

**Step 1 — Export your cookies**

1. Install [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) in Chrome/Edge
2. Go to `youtube.com` and sign in (use a throwaway account if possible)
3. Click the extension icon → **Export** → save as `cookies.txt`

**Step 2 — Place the file**

Copy the exported `cookies.txt` into the `./downloads/` folder (which is already mounted into the container):

```
vortex-ytdl/
├── downloads/
│   └── cookies.txt     ← place it here
├── docker-compose.yml
├── .env
└── ...
```

**Step 3 — Restart**

```bash
docker compose restart backend
```

The backend automatically detects and uses the cookies file on the next request. No rebuild needed.

> ⚠️ **Important:** Cookies expire. If you start seeing bot errors again, re-export a fresh `cookies.txt`, drop it in `./downloads/`, and restart.



### Can't access from mobile / another device

Allow port `8080` through your firewall:

```powershell
# Windows
netsh advfirewall firewall add rule name="VORTEX" dir=in action=allow protocol=TCP localport=8080
```

### Login page loops after entering password

Clear the site's `localStorage` in browser DevTools → Application → Local Storage, then reload.

### Download stuck at "PROCESSING / ENCODING"

ffmpeg is merging video + audio streams — normal for large files. Allow 30–60 seconds before assuming failure.

### View live container logs

```bash
docker compose logs -f backend     # backend logs
docker compose logs -f frontend    # nginx logs
```

---

## Stack

```
┌────────────────────────────────────────────────────────┐
│  Layer           Technology          Purpose            │
├────────────────────────────────────────────────────────┤
│  Media download  yt-dlp (latest)     Stream extraction  │
│  Post-process    ffmpeg              Merge · convert    │
│  Language        Python 3.12         Backend runtime    │
│  Framework       Flask 3.0           HTTP API           │
│  WSGI server     Gunicorn 22         Production server  │
│  Reverse proxy   nginx               Request routing    │
│  Frontend        Vanilla HTML/CSS    No build step      │
│  Containers      Docker Compose      Orchestration      │
└────────────────────────────────────────────────────────┘
```

---

<div align="center">

```
// FOR PERSONAL USE ONLY //
```

**VORTEX** is a private, self-hosted tool.  
Do not redistribute or use to download copyrighted content without permission.

</div>
