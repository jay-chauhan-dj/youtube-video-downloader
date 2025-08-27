from flask import Flask, render_template, request, jsonify, send_file, after_this_request
import os
import uuid
import threading
from youtube import download_media

app = Flask(__name__)

# In-memory dictionary to store task status
# In a production environment, you would use a more robust solution like Redis or a database.
tasks = {}

def run_download(task_id, url, download_type, media_format, is_playlist, custom_filename):
    """The function that will be executed in a background thread."""

    def progress_hook(d):
        """Updates the task progress."""
        if d['status'] == 'downloading':
            # yt-dlp provides progress as a float from 0 to 1
            progress = d.get('_percent_str', '0%')
            # remove the ANSI color codes
            progress = ''.join(filter(str.isdigit, progress))
            if progress:
                tasks[task_id]['progress'] = int(float(progress))
            tasks[task_id]['status'] = 'downloading'
        elif d['status'] == 'finished':
            tasks[task_id]['status'] = 'processing' # Renaming and post-processing can take time

    try:
        filepath = download_media(
            url,
            download_type,
            media_format,
            is_playlist,
            custom_filename,
            progress_hook=progress_hook
        )
        if filepath and os.path.exists(filepath):
            tasks[task_id]['status'] = 'finished'
            tasks[task_id]['filepath'] = filepath
            tasks[task_id]['progress'] = 100
        else:
            raise Exception("File not found after download.")
    except Exception as e:
        tasks[task_id]['status'] = 'error'
        tasks[task_id]['error'] = str(e)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def start_download_task():
    """Starts a download task in the background."""
    data = request.json
    url = data.get('url')
    download_type = data.get('download_type')
    is_playlist = data.get('playlist', False)
    custom_filename = data.get('filename')

    if download_type == 'video':
        media_format = data.get('video_format')
    else:
        media_format = data.get('audio_format')

    if not url or not download_type or not media_format:
        return jsonify({'error': 'Missing required parameters'}), 400

    task_id = str(uuid.uuid4())
    tasks[task_id] = {'status': 'starting', 'progress': 0}

    thread = threading.Thread(
        target=run_download,
        args=(task_id, url, download_type, media_format, is_playlist, custom_filename)
    )
    thread.start()

    return jsonify({'task_id': task_id})

@app.route('/progress/<task_id>')
def get_progress(task_id):
    """Returns the progress of a download task."""
    task = tasks.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task)

@app.route('/file/<task_id>')
def get_file(task_id):
    """Sends the downloaded file to the client."""
    task = tasks.get(task_id)
    if not task or task['status'] != 'finished':
        return jsonify({'error': 'File not ready or task not found'}), 404

    filepath = task.get('filepath')
    if not filepath or not os.path.exists(filepath):
        return jsonify({'error': 'File not found on server'}), 404

    @after_this_request
    def cleanup(response):
        try:
            os.remove(filepath)
            del tasks[task_id]
        except Exception as e:
            app.logger.error(f"Error cleaning up file for task {task_id}: {e}")
        return response

    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    # Ensure temp_downloads directory exists
    if not os.path.exists('temp_downloads'):
        os.makedirs('temp_downloads')
    app.run(host='0.0.0.0', port=5000, debug=True)
