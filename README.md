# yt-dlp GUI

A modern, user-friendly desktop application for downloading videos from YouTube and other sites using [`yt-dlp`](https://github.com/yt-dlp/yt-dlp).

Built with **Python** and **CustomTkinter**, this app provides a clean interface for:
- Fetching video metadata (title, formats, subtitles),
- Selecting download presets or custom formats,
- Configuring advanced options (subtitles, thumbnails),

---

## Features

- **Auto-detect video info** — just paste a URL
- **Format presets**: MP4 1080p, MP3, AAC, WebM, etc.
- **Manual format selection** from all available streams
- **Subtitles**: download and select languages
- **Thumbnail**: download, convert (JPG/PNG/WebP), embed into video
- **Select output folder**
- **Error handling** with clear messages

---

##️ Requirements

- Python 3.13+
- `yt-dlp` (installed automatically or manually)
- FFmpeg (for format conversion and embedding thumbnails)

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/yt-dlp-gui.git
cd yt-dlp-gui
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

The app will auto-download yt-dlp if not found, but you can also install it manually: 
```bash
pip install yt-dlp
```
### 3. Install FFmpeg
- Windows: Download from https://www.gyan.dev/ffmpeg/builds/
- macOS: ```brew install ffmpeg```
- Linux: ```sudo apt install ffmpeg```

Ensure ffmpeg is in your PATH.

---

## Usage
Run the application:
```bash
python main.py
```
1. **Paste a YouTube (or supported site) URL.**
2. **Wait for video info to load.**
3. **Choose format, subtitles, thumbnail options.**
4. **Click Download Video.**

All downloads are saved to the selected folder.

---

## Testing
The project includes unit tests for core logic (flags, utils, controller):
```bash
pytest
```
Requires: `pytest`

## Project Structure
```
yt-dlp-gui/
├── main.py                 # Entry point
├── data/
├── logs/
├── src/
│   ├── core/               # Business logic (runner, flags, config)
│   ├── controller/         # AppController (orchestrates logic)
│   └── view/               # UI components (MainWindow, panels)
│   └── app.py
├── tests/                  # Unit tests
├── requirements.txt
├── pyproject.toml
└── README.md
```
