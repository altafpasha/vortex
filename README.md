# VORTEX — Media Extractor
> Internal YouTube downloader for content creators. Not for redistribution.

## Configuration

Before starting, copy the example environment file and configure your settings:
```bash
cp example.env .env
```
Open `.env` and set your `VORTEX_PASSWORD`. If left empty, the application will run without password protection (open access).

## Quick Start

```bash
# Clone / copy this folder, set up your .env, then start the containers:
docker compose up --build -d

# Open browser to http://localhost:8080
```

## Features
- Paste any YouTube URL → auto-fetches video metadata + thumbnail
- Choose video quality (360p → 1080p+) or audio format (MP3/M4A/WAV)
- Real-time download progress with speed + ETA
- Local file library with one-click downloads
- ffmpeg handles merging video+audio and audio conversion

## Stack
- **Backend**: Python + Flask + yt-dlp + ffmpeg
- **Frontend**: Vanilla HTML/CSS (cyberpunk UI, no framework needed)
- **Proxy**: nginx (routes /api/ to Flask)
- **Container**: Docker Compose

## Downloaded Files
Files saved to `./downloads/` on the host (bind mount).

## Stop
```bash
docker compose down
```

## Update yt-dlp (if YouTube breaks)
```bash
docker compose exec backend pip install -U yt-dlp
docker compose restart backend
```
