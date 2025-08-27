import os
import uuid
from yt_dlp import YoutubeDL
from urllib.parse import urlparse, parse_qs

def download_media(url, download_type, media_format, is_playlist=False, custom_filename=None, progress_hook=None):
    """
    Downloads media from YouTube based on provided options.
    Saves the file to a temporary directory and returns the path.
    """
    # Create a temporary directory for downloads if it doesn't exist
    temp_dir = 'temp_downloads'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Determine yt-dlp options based on download type
    if download_type == 'video':
        format_code = f"bestvideo[ext={media_format}]+bestaudio/best[ext={media_format}]"
        file_extension = f".{media_format}"
    elif download_type == 'audio':
        format_code = 'bestaudio'
        file_extension = f".{media_format}"
    else:
        raise ValueError("Invalid download type specified.")

    # Handle filename
    if custom_filename:
        # Use custom filename, ensuring it has the correct extension
        filename_base = os.path.splitext(custom_filename)[0]
        output_template = os.path.join(temp_dir, f"{filename_base}{file_extension}")
    else:
        # Use a unique ID for the filename to avoid conflicts and use original title later
        unique_id = str(uuid.uuid4())
        output_template = os.path.join(temp_dir, f"{unique_id}.%(ext)s")

    # yt-dlp options
    ydl_opts = {
        'format': format_code,
        'outtmpl': output_template,
        'noplaylist': not is_playlist,
        'quiet': True,
    }

    # Add progress hook if provided
    if progress_hook:
        ydl_opts['progress_hooks'] = [progress_hook]

    # Add postprocessor for audio conversion
    if download_type == 'audio':
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': media_format,
            'preferredquality': '192',
        }]

    # Start download
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded_path = ydl.prepare_filename(info)

            # If no custom name, rename the file to its original title
            if not custom_filename:
                original_title = info.get('title', 'download')
                final_filename = os.path.join(temp_dir, f"{original_title}{file_extension}")
                # Ensure the final filename is unique
                count = 1
                base, ext = os.path.splitext(final_filename)
                while os.path.exists(final_filename):
                    final_filename = f"{base} ({count}){ext}"
                    count += 1

                os.rename(downloaded_path, final_filename)
                return final_filename

            return downloaded_path

    except Exception as e:
        print(f"Error during download: {e}")
        return None
