# File path: youtube_downloader.py

import os
from pytube import YouTube, Playlist
import shutil
import sys

# Default base location for downloads
BASE_DIR = os.path.expanduser('~/Desktop/Songs')


def list_files_and_folders(directory: str):
    """List files and folders in the given directory."""
    print(f"\nListing files and folders in: {directory}")
    with os.scandir(directory) as entries:
        for entry in entries:
            print(f"{'[Folder]' if entry.is_dir() else '[File]'} {entry.name}")


def create_folder(directory: str):
    """Create a new folder in the given directory."""
    folder_name = input("Enter the name of the new folder: ")
    new_folder_path = os.path.join(directory, folder_name)
    try:
        os.makedirs(new_folder_path, exist_ok=True)
        print(f"Folder created: {new_folder_path}")
        return new_folder_path
    except Exception as e:
        print(f"Error creating folder: {e}")
        return directory


def select_folder(base_dir: str):
    """Select an existing folder or create a new one."""
    while True:
        list_files_and_folders(base_dir)
        choice = input("\nOptions:\n1. Select an existing folder\n2. Create a new folder\n3. Use the current location\n4. Go back\nSelect: ")
        if choice == '1':
            folder_name = input("Enter the name of the folder: ")
            selected_folder = os.path.join(base_dir, folder_name)
            if os.path.isdir(selected_folder):
                return selected_folder
            else:
                print("Invalid folder name. Try again.")
        elif choice == '2':
            return create_folder(base_dir)
        elif choice == '3':
            return base_dir
        elif choice == '4':
            return None
        else:
            print("Invalid choice. Try again.")


def download_video(youtube_video: YouTube, file_format: str, destination: str):
    """Download video in the selected format."""
    print(f"Downloading: {youtube_video.title}")
    try:
        # Get video streams matching the file format
        stream = youtube_video.streams.filter(file_extension=file_format).get_highest_resolution()
        if stream is None:
            print(f"No video streams found for the selected format {file_format}")
            return
        stream.download(output_path=destination)
        print("Video download completed!")
    except Exception as e:
        print(f"Error downloading video: {e}")


def download_audio(youtube_video: YouTube, file_format: str, destination: str):
    """Download audio in the selected format."""
    print(f"Downloading: {youtube_video.title}")
    try:
        # Fetch audio-only streams and select the first available one
        stream = youtube_video.streams.filter(only_audio=True).first()
        
        if stream is None:
            print("No audio stream found!")
            return

        # Download the audio stream
        out_file = stream.download(output_path=destination)

        # Rename and convert if needed
        base, ext = os.path.splitext(out_file)
        new_file = base + f'.{file_format}'
        
        # Handle conversion if not mp4 audio (e.g., convert to mp3, wav, etc.)
        if file_format != 'mp4':
            shutil.move(out_file, new_file)

        print(f"Audio download completed as {new_file}!")
    except Exception as e:
        print(f"Error during audio download: {e}")


def get_video_or_audio(url: str, file_type: str, file_format: str, destination: str):
    """Fetch YouTube video object and handle download based on type."""
    try:
        youtube_video = YouTube(url)

        if file_type == "audio":
            download_audio(youtube_video, file_format, destination)
        else:
            download_video(youtube_video, file_format, destination)
    except Exception as e:
        print(f"Error fetching YouTube video: {e}")


def main():
    print("Welcome to the YouTube Downloader!")

    # Ask for YouTube URL
    video_url = input("Enter the YouTube video URL (supports single videos, not full playlists): ")

    # Check if it's a playlist URL and select the first video
    if 'playlist' in video_url:
        playlist = Playlist(video_url)
        print(f"Playlist detected. Downloading the first video: {playlist.video_urls[0]}")
        video_url = playlist.video_urls[0]

    # Ask for file type (audio or video)
    file_type = input("Do you want to download Audio or Video? (type 'audio' or 'video'): ").strip().lower()

    # Ask for file format based on file type
    if file_type == 'audio':
        file_format = input("Select audio format (mp3, wav, m4a): ").strip().lower()
    elif file_type == 'video':
        file_format = input("Select video format (mp4, mov): ").strip().lower()
    else:
        print("Invalid file type. Exiting.")
        return

    # Ensure the base directory exists
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    # Folder selection process
    destination = select_folder(BASE_DIR)
    if destination is None:
        print("No folder selected. Exiting.")
        return

    # Download the selected file
    get_video_or_audio(video_url, file_type, file_format, destination)


if __name__ == "__main__":
    main()
