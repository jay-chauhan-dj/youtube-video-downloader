import os
from yt_dlp import YoutubeDL
import sys
from urllib.parse import urlparse, parse_qs

# Unicode icons for improved UI
FOLDER_ICON = "📁"
CHECK_ICON = "✅"
BACK_ICON = "🔙"
PLUS_ICON = "➕"
VIDEO_ICON = "🎬"
AUDIO_ICON = "🎧"
PROGRESS_ICON = "⏳"
SUCCESS_ICON = "✅"

# Supported file extensions for media files
AUDIO_EXTENSIONS = {'.mp3', '.wav', '.aac', '.flac', '.m4a'}
VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.mov', '.flv'}

def list_directories(path):
    """List all directories in the specified path."""
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def list_media_files(path):
    """List all audio and video files in the specified path with relevant icons."""
    media_files = []
    for filename in os.listdir(path):
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in AUDIO_EXTENSIONS:
            media_files.append(f"{AUDIO_ICON} {filename}")
        elif file_ext in VIDEO_EXTENSIONS:
            media_files.append(f"{VIDEO_ICON} {filename}")
    return media_files

def get_save_location(base_path):
    """Navigate folders within the base path and create new folders if needed."""
    current_path = base_path
    while True:
        print(f"\n{FOLDER_ICON} Current: {current_path}")
        media_files = list_media_files(current_path)
        if media_files:
            print("\n--- Media Files ---")
            for file in media_files:
                print(f" {file}")
            print("------------------")
        else:
            print("\n(No media files found)")

        directories = list_directories(current_path)
        print("\n--- Folders ---")
        for idx, folder in enumerate(directories):
            print(f" {idx + 1}. {FOLDER_ICON} {folder}")
        print(f" {len(directories) + 1}. {PLUS_ICON} New Folder")
        print(f" {len(directories) + 2}. {BACK_ICON} Parent Folder")
        print(f" {len(directories) + 3}. {CHECK_ICON} Select Here")
        print("------------------")

        try:
            choice = int(input("Choose a number: "))
        except ValueError:
            print("❌ Invalid input, enter a number.")
            continue

        if choice == len(directories) + 1:
            new_folder_name = input("New folder name: ")
            new_folder_path = os.path.join(current_path, new_folder_name)
            os.makedirs(new_folder_path, exist_ok=True)
            print(f"{CHECK_ICON} Created '{new_folder_name}'")
            current_path = new_folder_path
        elif choice == len(directories) + 2:
            current_path = os.path.dirname(current_path)
        elif choice == len(directories) + 3:
            return current_path
        elif 1 <= choice <= len(directories):
            current_path = os.path.join(current_path, directories[choice - 1])
        else:
            print("❌ Invalid choice, try again.")

def show_progress_bar(d):
    """Display a progress bar for the download process."""
    if d['status'] == 'downloading':
        total = d.get('total_bytes', 0)
        downloaded = d.get('downloaded_bytes', 0)
        percentage = (downloaded / total) * 100 if total > 0 else 0
        bar_length = 30
        progress = int(percentage / (100 / bar_length))
        progress_bar = '#' * progress + '-' * (bar_length - progress)
        sys.stdout.write(f"\r{PROGRESS_ICON} Downloading: [{progress_bar}] {percentage:.2f}%")
        sys.stdout.flush()
    elif d['status'] == 'finished':
        print(f"\n{SUCCESS_ICON} Download complete.")

def is_playlist(url):
    """Check if the URL contains a playlist parameter."""
    query = parse_qs(urlparse(url).query)
    return 'list' in query

def get_unique_filename(path, filename, ext):
    """Generate a unique filename if a file with the same name already exists."""
    original_path = os.path.join(path, f"{filename}{ext}")
    if not os.path.exists(original_path):
        return original_path  # No conflict, return the original path

    # If conflict exists, offer to rename or generate a unique filename
    choice = input("File already exists. Rename manually? (y/n): ").strip().lower()
    if choice == 'y':
        new_name = input("Enter new name (without extension): ").strip()
        return os.path.join(path, f"{new_name}{ext}")
    else:
        count = 1
        while True:
            new_path = os.path.join(path, f"{filename} ({count}){ext}")
            if not os.path.exists(new_path):
                return new_path
            count += 1

def download_youtube_content():
    """Download YouTube content based on user's choice of video or audio."""
    base_path = os.path.expanduser("~/Desktop/youtube")
    if not os.path.exists(base_path):
        os.makedirs(base_path)
        print(f"{CHECK_ICON} Created base directory '{base_path}'")

    # Input URL and check if it's a playlist
    url = input("Enter YouTube URL: ").strip()
    if not url.startswith("http"):
        url = "https://" + url

    if is_playlist(url):
        print("\n📋 This URL is part of a playlist.")
        playlist_choice = input("Download entire playlist? (y/n): ").strip().lower()
        if playlist_choice == 'n':
            url = url.split('&')[0]  # Remove playlist parameters for single video

    # Selection of download type
    print(f"\n{VIDEO_ICON} Video or {AUDIO_ICON} Audio?")
    print(" 1. 🎬 Video")
    print(" 2. 🎧 Audio")
    choice = input("Choose (1 or 2): ").strip()

    # Set format code based on selection
    if choice == '1':
        formats = ['mp4', 'mkv', 'mov', 'flv']
        print("\n--- Video Formats ---")
        for idx, fmt in enumerate(formats, start=1):
            print(f" {idx}. {VIDEO_ICON} {fmt}")
        print("--------------------")
        try:
            format_choice = int(input("Choose format: "))
            selected_format = formats[format_choice - 1]
        except (ValueError, IndexError):
            print("❌ Invalid format choice.")
            return
        format_code = f"bestvideo[ext={selected_format}]+bestaudio/best[ext={selected_format}]"
        file_extension = f".{selected_format}"

    elif choice == '2':
        formats = ['mp3', 'wav', 'aac', 'flac', 'm4a']
        print("\n--- Audio Formats ---")
        for idx, fmt in enumerate(formats, start=1):
            print(f" {idx}. {AUDIO_ICON} {fmt}")
        print("--------------------")
        try:
            format_choice = int(input("Choose format: "))
            selected_format = formats[format_choice - 1]
        except (ValueError, IndexError):
            print("❌ Invalid format choice.")
            return
        format_code = 'bestaudio'
        file_extension = f".{selected_format}"

    else:
        print("❌ Invalid choice.")
        return

    # Choose to keep original name or use custom name with conflict handling
    use_original_name = input("Keep original name? (y/n): ").strip().lower()
    save_location = get_save_location(base_path)
    if use_original_name == 'y':
        output_template = os.path.join(save_location, "%(title)s.%(ext)s")
    else:
        file_name = input("Enter custom file name (without extension): ")
        output_template = get_unique_filename(save_location, file_name, file_extension)

    # yt-dlp options
    ydl_opts = {
        'format': format_code,
        'outtmpl': output_template,
        'progress_hooks': [show_progress_bar],
        'quiet': True,
    }

    # Add postprocessor for audio conversion
    if choice == '2':
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': selected_format,
            'preferredquality': '192',
        }]

    print(f"\n{PROGRESS_ICON} Downloading...")
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\n{CHECK_ICON} Download complete in '{output_template}'")
    except Exception as e:
        print(f"❌ Download failed: {e}")

# Run the main function
download_youtube_content()
