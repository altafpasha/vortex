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
║              MEDIA EXTRACTOR  //  v3.1                       ║
║         Personal YouTube Downloader — Self Hosted            ║
╚══════════════════════════════════════════════════════════════╝
```

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)
![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-FF0000?style=flat-square&logo=youtube&logoColor=white)
![nginx](https://img.shields.io/badge/nginx-proxy-009639?style=flat-square&logo=nginx&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-20_LTS-339933?style=flat-square&logo=nodedotjs&logoColor=white)
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
- [YouTube Authentication](#youtube-authentication)
- [Auto-Sync Browser Extension](#auto-sync-browser-extension)
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
│  🤖 BOT DETECTION BYPASS                                    │
│     • PO Token generation via bgutil-ytdlp-pot-provider     │
│     • Multi-client fallback: web → mweb → ios → android     │
│     • Cookie upload UI — paste or upload cookies.txt        │
│     • Auto-Sync Extension — cookies refresh automatically   │
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
│  VORTEX      MEDIA EXTRACTOR // v3.1          ● SYSTEM ONLINE   │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ FILES        │  │ STORAGE      │  │ ACTIVE       │          │
│  │     12       │  │   847 MB     │  │     1        │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                 │
│  00 // YT AUTH COOKIES ────────────────────────────────────     │
│  [ ✓ COOKIES ACTIVE — Updated 05/06/2026 ]  [✕ REMOVE]         │
│  [ 📋 UPLOAD cookies.txt ]  [ ⬇ AUTO-SYNC EXTENSION ]          │
│                                                                 │
│  01 // SAVE LOCATION ──────────────────────────────────────     │
│  [ 📁 CHOOSE FOLDER ]   📂 Downloads  ✕                         │
│                                                                 │
│  02 // TARGET URL ──────────────────────────────────────── ✕    │
│  ┌─────────────────────────────────────────┐ ┌───────────┐     │
│  │  https://youtube.com/watch?v=...        │ │  ANALYZE  │     │
│  └─────────────────────────────────────────┘ └───────────┘     │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ ▓▓▓▓▓  Video Title Here                                 │   │
│  │ ▓▓▓▓▓  CHANNEL: Example   DURATION: 4:32   VIEWS: 2.1M  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  03 // SELECT FORMAT ──────────────────────────────────────     │
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
                     https://vortex.codesec.me
                              │
                    ┌─────────▼──────────┐
                    │       nginx         │
                    │   (reverse proxy)   │
                    └────┬──────────┬────┘
                         │          │ /api/*
                    ┌────▼────┐  ┌──▼───────────────────────────┐
                    │  Static │  │    Gunicorn + Flask            │
                    │  HTML   │  │  (1 worker · 4 threads)       │
                    └─────────┘  │                               │
                                 │  yt-dlp                       │
                                 │   ├─ bgutil PO token plugin   │
                                 │   ├─ cookies.txt (optional)   │
                                 │   └─► ffmpeg                  │
                                 └──────────┬────────────────────┘
                                            │ bind mount
                                    ┌───────▼────────┐
                                    │  ./downloads/  │
                                    │  (host folder) │
                                    └────────────────┘

  Chrome/Firefox (user's device)
  ┌────────────────────────────┐
  │  Vortex Cookie Sync ext.   │  ── auto-POST cookies ──►  /api/cookies/upload
  │  (syncs every 6 hours)     │
  └────────────────────────────┘
```

---

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Docker | 24+ | [Install Docker](https://docs.docker.com/get-docker/) |
| Docker Compose | v2 | Bundled with Docker Desktop |
| Port `8080` | free | Configurable in `docker-compose.yml` |

> **No Python, Node, ffmpeg, or browser required on the host** — everything runs inside containers.

---

## Installation

**1. Get the project**

```bash
git clone https://github.com/altafpasha/vortex-ytdl.git vortex-ytdl
cd vortex-ytdl
```

**2. Set your password**

```bash
cp example.env .env
# Edit .env and fill in your password
VORTEX_PASSWORD=your_secure_password_here
```

> Leave `VORTEX_PASSWORD=` empty for open access (no login screen).

**3. Build and start**

```bash
docker compose up --build -d
```

> First build takes ~3–5 minutes — it installs Node.js 20, Deno, ffmpeg, and the yt-dlp PO token plugin.

**4. Open**

```
http://localhost:8080
```

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

> ⚠️ `.env` is in `.gitignore` — never committed to git.

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

## YouTube Authentication

Vortex v3.1 includes a multi-layer bot detection bypass:

```
Layer 1 — PO Token (automatic, no setup)
  bgutil-ytdlp-pot-provider generates a cryptographic
  Proof-of-Origin token for every request using Node.js.

Layer 2 — Player client fallback (automatic)
  Tries web → mweb → ios → android clients in order.

Layer 3 — YouTube cookies (required for VPS/datacenter IPs)
  Datacenter IPs are fully blocked by YouTube without a real
  browser session. A signed-in cookies.txt resolves this.
```

### Option A — Auto-Sync Extension *(recommended, permanent)*

Install the bundled browser extension once. Cookies refresh every 6 hours automatically.  
See [Auto-Sync Browser Extension](#auto-sync-browser-extension).

### Option B — Manual upload via the UI

1. Install [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) in Chrome/Firefox
2. Sign into YouTube
3. Click the extension → **Export** → save `cookies.txt`
4. In Vortex → `00 // YT AUTH COOKIES` → click **📋 UPLOAD cookies.txt**
5. Status turns green: **✓ COOKIES ACTIVE**

### Option C — File drop on VPS

```bash
scp cookies.txt user@your-vps:~/vortex-ytdl/downloads/cookies.txt
docker compose restart backend
```

> Cookies expire roughly every 2 weeks. Option A refreshes them automatically — recommended for VPS deployments.

---

## Auto-Sync Browser Extension

Vortex ships a Chrome/Firefox extension that silently keeps your YouTube cookies fresh on the server — no manual export ever needed again.

### How it works

```
1. Extension runs in Chrome/Firefox on your PC or laptop
2. When you browse YouTube while signed in, it reads your session cookies
3. Every 6 hours it logs into Vortex and uploads a fresh cookies.txt
4. The VPS always has valid cookies — bot detection stays bypassed forever
```

### One-time setup (~30 seconds)

**Step 1 — Download**

In the Vortex web UI → `00 // YT AUTH COOKIES` → click **⬇ AUTO-SYNC EXTENSION**.  
This downloads `vortex-cookie-sync.zip`. Unzip it.

**Step 2 — Install in Chrome / Edge**

1. Open `chrome://extensions`
2. Enable **Developer mode** (toggle, top right)
3. Click **Load unpacked** → select the unzipped folder

**Step 3 — Configure**

1. Click the **VORTEX** extension icon in the Chrome toolbar
2. Enter **Server URL** — e.g. `https://vortex.codesec.me`
3. Enter **Vortex Password** — same password used to log into the web UI
4. Click **SAVE & SYNC NOW**

The popup shows **✓ Synced at ...** — done.

**Install in Firefox**

1. Open `about:debugging` → **This Firefox**
2. Click **Load Temporary Add-on** → select `manifest.json` from the unzipped folder

> Firefox requires re-loading temporary extensions after each browser restart. Chrome is recommended for permanent background sync.

### Sync schedule

| Trigger | When |
|---------|------|
| First install | Immediately |
| Visiting YouTube | Every page load |
| Background alarm | Every 6 hours |
| Manual | Click → SAVE & SYNC NOW |

---

## Usage

### Download a single video

```
1.  Open  http://localhost:8080  (or your VPS URL)
2.  Log in with your password
3.  Paste a YouTube URL
4.  Click  ANALYZE
5.  Select video quality or audio format
6.  Click  ⚡ EXTRACT
7.  File saves to your Downloads folder automatically
```

### Choose a custom save folder *(desktop only)*

```
1.  Click  📁 CHOOSE FOLDER
2.  Pick any folder on your computer
3.  All downloads save there silently — no prompt each time
```

> On **mobile**, files save to the phone's Downloads folder automatically.  
> Folder picker works in Chrome, Edge, and Opera on desktop.

### Access from mobile

Find your local IP, then open on any device:

```
http://192.168.x.x:8080
```

```powershell
ipconfig        # Windows
ip addr show    # Linux / Mac
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

> **Original audio is always used.** Auto-dubbed tracks are excluded automatically via `language_preference >= 0` in the yt-dlp format selector.

---

## Playlist Download

```
1.  Paste a YouTube playlist URL
    e.g. youtube.com/playlist?list=PLxxxxxxxx

2.  Click  ANALYZE
    → Playlist detected, all video titles listed

3.  Select a format

4.  Click  ⚡ EXTRACT PLAYLIST
    → Live progress: X / total  +  current video name

5.  Files saved to  downloads/<playlist-name>/
```

> Videos that fail are skipped automatically — the rest continue.

---

## API Reference

All endpoints require the header:

```
X-Auth-Token: <token>
```

Token is returned by `/api/login`. Omit only for `/api/login`, `/api/auth/check`, and `/health`.

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

### Cookies

| Method | Endpoint | Body | Returns |
|--------|----------|------|---------|
| `GET` | `/api/cookies/status` | — | `{ present, modified, size }` |
| `POST` | `/api/cookies/upload` | `file` (multipart `.txt`) | `{ ok }` |
| `DELETE` | `/api/cookies/delete` | — | `{ ok }` |

### Extension

| Method | Endpoint | Returns |
|--------|----------|---------|
| `GET` | `/api/extension/download` | `vortex-cookie-sync.zip` |

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

### "Sign in to confirm you're not a bot"

YouTube blocks requests from VPS/datacenter IPs without a real browser session. Fix in order of preference:

**1. Install the Auto-Sync Extension** *(permanent fix)*  
See [Auto-Sync Browser Extension](#auto-sync-browser-extension). Cookies stay fresh automatically.

**2. Upload cookies.txt manually via the UI**  
`00 // YT AUTH COOKIES` → **📋 UPLOAD cookies.txt**  
Export from Chrome using the "Get cookies.txt LOCALLY" extension while signed into YouTube.

**3. Drop file directly on the VPS**
```bash
scp cookies.txt user@vps:~/vortex-ytdl/downloads/cookies.txt
docker compose restart backend
```

> Cookies expire every ~2 weeks. The Auto-Sync Extension handles this automatically.

### "Requested format is not available"

Update yt-dlp to the latest nightly:

```bash
docker compose exec backend pip install -U yt-dlp
docker compose restart backend
```

### Can't access from mobile / another device

Allow the port through your firewall:

```powershell
# Windows
netsh advfirewall firewall add rule name="VORTEX" dir=in action=allow protocol=TCP localport=8080
```

```bash
# Linux / VPS
ufw allow 8080/tcp
```

### Login loops after entering password

Clear `localStorage` in browser DevTools → Application → Local Storage → clear site data → reload.

### Download stuck at "PROCESSING / ENCODING"

ffmpeg is merging video + audio — normal for large files. Wait 30–60 seconds before treating as failure.

### View live container logs

```bash
docker compose logs -f backend     # yt-dlp output + errors
docker compose logs -f frontend    # nginx access log
docker compose logs -f             # all containers
```

---

## Stack

```
┌──────────────────────────────────────────────────────────────┐
│  Layer              Technology                Purpose         │
├──────────────────────────────────────────────────────────────┤
│  Media download     yt-dlp (latest nightly)   Stream extract │
│  PO token gen.      bgutil-ytdlp-pot-provider  Bot bypass    │
│  PO token bridge    yt-dlp-get-pot             Plugin API    │
│  JS runtime         Node.js 20 LTS             bgutil engine │
│  JS challenges      Deno                        Sig. solving  │
│  Post-process       ffmpeg                      Merge/convert │
│  Language           Python 3.12                Backend       │
│  Framework          Flask 3.0                  HTTP API      │
│  WSGI server        Gunicorn 22                Prod server   │
│  Reverse proxy      nginx                      Routing       │
│  Frontend           Vanilla HTML / CSS / JS    No build step │
│  Cookie sync        Chrome/Firefox extension   Auto-refresh  │
│  Containers         Docker Compose             Orchestration │
└──────────────────────────────────────────────────────────────┘
```

---

<div align="center">

```
// FOR PERSONAL USE ONLY //
```

**VORTEX** is a private, self-hosted tool.  
Do not redistribute or use to download copyrighted content without permission.

</div>
