FROM python:3.12-slim

# Install ffmpeg, curl, gnupg for Node.js setup
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    unzip \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20 LTS — required by bgutil-ytdlp-pot-provider for PO token generation
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Deno — yt-dlp needs a JS runtime to solve YouTube's signature challenges
RUN curl -fsSL https://deno.land/install.sh | DENO_INSTALL=/usr/local sh

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Force yt-dlp to absolute latest (nightly fixes for YouTube changes)
RUN pip install -U yt-dlp

COPY app.py .

RUN mkdir -p /app/downloads

EXPOSE 5000

# 1 worker + 4 threads keeps in-memory download state consistent across requests
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "4", "--timeout", "600", "app:app"]
