
# 🎬 YouTube Video & Audio Downloader 🎧

A Python script for downloading YouTube videos or audio files in various formats, with flexible options for file naming, format, and download location. Includes automatic filename conflict resolution to prevent overwriting existing files. 📂

---

## 📋 Features

- **Download YouTube Videos** 🎥 in formats like `.mp4`, `.mkv`, etc.
- **Download Audio Files** 🎶 in formats like `.mp3`, `.wav`, `.m4a`, etc.
- Flexible **File Naming Options** 📝 — use original title or custom.
- **Conflict-Free Naming** 🆕 with auto-incremented file names.
- **Progress Bar** ⏳ for easy download tracking.

---

## 🚀 Getting Started

### Prerequisites

Ensure **Python** and **pip** are installed. You can check by running:
```bash
python --version
pip --version
```

### Install Required Libraries

Install the required Python packages with:
```bash
pip install yt-dlp
```

### Install FFmpeg for Audio Conversions

FFmpeg is necessary for converting audio formats:
- **Linux**: `sudo apt install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Windows**: [Download FFmpeg](https://ffmpeg.org/download.html) and add it to your PATH.

---

## 📂 Folder Setup

The base download folder is set to:
```plaintext
~/Desktop/youtube
```
This folder is created automatically if it doesn’t exist.

---

## 📥 Usage

### Run the Script
To start the downloader, run:
```bash
python youtube.py
```

### Download Options
1. **Enter YouTube URL** 🔗
   - If the URL is a playlist, the script will prompt you to choose between downloading the entire playlist or a single video.

2. **Choose Download Type** 🎥 or 🎧
   - **1**: Video
   - **2**: Audio

3. **Select Format** 🎞️
   - Video formats include `.mp4`, `.mkv`, `.mov`, and `.flv`.
   - Audio formats include `.mp3`, `.wav`, `.aac`, `.flac`, and `.m4a`.

4. **Set File Name** 📝
   - Choose to keep the original YouTube title or enter a custom file name.
   - If a file with the same name exists, the script prompts for renaming or appends numbers to create unique filenames automatically.

5. **Select Save Location** 📂
   - Choose a folder within the base directory, create new folders, or go back to parent folders as needed.

6. **Track Progress** ⏳
   - The download progress bar shows real-time status with `#####------ 50%`.

---

## 🎉 Example Usage

### Downloading a Video

1. Run:
   ```bash
   python youtube.py
   ```
2. Enter the **YouTube URL**.
3. Choose **Video (1)**.
4. Select the desired format (e.g., `.mp4`).
5. Choose to keep the original title or set a custom file name.
6. Select the save location.
7. Watch the progress bar as the file downloads.

### Downloading an Audio File

1. Run:
   ```bash
   python youtube.py
   ```
2. Enter the **YouTube URL**.
3. Choose **Audio (2)**.
4. Select the desired format (e.g., `.mp3`).
5. Choose to keep the original title or set a custom file name.
6. Select the save location.
7. Watch the progress bar as the file downloads.

---

## 🛠️ Troubleshooting

### FFmpeg Not Found
If FFmpeg is missing or not found:
- Ensure it’s installed and added to your system’s PATH.
- [FFmpeg Installation Guide](https://ffmpeg.org/download.html).

### yt-dlp Errors
If `yt-dlp` encounters issues, try updating it:
```bash
pip install -U yt-dlp
```

---

## 💡 Tips

- **Manual Rename**: If a file with the same name exists, you can manually rename it or let the script append a number automatically.
- **Playlist Detection**: Automatically detects playlists and prompts for downloading either the entire playlist or a single video.
- **Audio Quality**: Audio downloads are set to 192 kbps for optimal quality.

---

## 🤝 Contributions

Feel free to contribute by opening pull requests or reporting issues.

## 👤 Author Information

**Author**: Jay Chauhan  
**Website**: [www.dj-jay.in](http://www.dj-jay.in)  
**Email**: contact@dj-jay.in  
**Contact Number**: +91 93134 40532

## 📜 License

This project is licensed under the MIT License.

---

Happy downloading! 🎉📥