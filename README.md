## Installation
```bash
pip3 install yt-dlp
```

## Requirements
- Python 3.x
- yt-dlp
- FFmpeg

### Installing Python
**macOS/Linux:** `brew install python` or download from [python.org](https://python.org)

**Windows:** Download from [python.org](https://python.org) — check "Add Python to PATH" during install

### Installing FFmpeg (required for MP3)

**macOS**
```bash
brew install ffmpeg
```

**Windows**
```powershell
winget install ffmpeg
```

**Linux**
```bash
sudo apt install ffmpeg
```

**Manual (Windows only):**
1. Download from https://www.gyan.dev/ffmpeg/builds/
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your system PATH
4. Restart terminal

## Usage

**macOS/Linux**
```bash
python3 downloader.py
```
**Windows**
```bash
python downloader.py
```
