# YouTube Video Downloader Web UI

This project provides a web-based user interface for downloading YouTube videos and audio. It is built with Flask and uses `yt-dlp` as the backend for handling downloads.

## Features

-   **Web-Based Interface:** Easy-to-use UI for downloading videos without command-line interaction.
-   **Video & Audio Downloads:** Choose to download the full video or extract audio only.
-   **Multiple Formats:**
    -   Video: MP4, MKV, MOV, FLV
    -   Audio: MP3, WAV, AAC, FLAC, M4A
-   **Playlist Support:** Option to download an entire YouTube playlist. (Note: The current implementation downloads all files from a playlist to the server and serves them one by one. For a better experience, this could be improved to zip the playlist files.)
-   **Custom Filenames:** Specify a custom name for your downloaded files.
-   **Real-time Progress:** A progress bar provides real-time feedback on the download status.

## Local Setup (for Development)

Follow these steps to run the application on your local machine.

### 1. Prerequisites

-   Python 3.6+
-   `pip` (Python package installer)
-   `ffmpeg` (Required by `yt-dlp` for audio conversion and merging formats)
    -   **On macOS (via Homebrew):** `brew install ffmpeg`
    -   **On Debian/Ubuntu:** `sudo apt-get install ffmpeg`
    -   **On Windows (via Chocolatey):** `choco install ffmpeg`

### 2. Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    # On Windows, use: `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Running the Application

1.  **Start the Flask server:**
    ```bash
    python app.py
    ```

2.  **Access the application:**
    Open your web browser and navigate to `http://127.0.0.1:5000`.

## Deployment Guide (Ubuntu with Nginx & Gunicorn)

This guide explains how to deploy the application on an Ubuntu server.

### 1. Prerequisites

-   An Ubuntu server (20.04 or newer recommended).
-   A non-root user with `sudo` privileges.
-   `nginx` installed and configured.
-   A domain name pointed at your server's IP address (optional, but recommended for production).

### 2. Server Setup

1.  **Update package lists:**
    ```bash
    sudo apt-get update
    ```

2.  **Install Python, pip, and Nginx:**
    ```bash
    sudo apt-get install -y python3 python3-pip python3-venv nginx
    ```

3.  **Install FFmpeg:**
    ```bash
    sudo apt-get install -y ffmpeg
    ```

### 3. Project Setup

1.  **Clone your project:**
    ```bash
    git clone <repository-url> /var/www/your-project
    cd /var/www/your-project
    ```

2.  **Create a virtual environment:**
    ```bash
    sudo python3 -m venv venv
    ```

3.  **Activate the virtual environment and install dependencies:**
    ```bash
    source venv/bin/activate
    pip install -r requirements.txt
    ```
    *Note: You may need to run `sudo` with `pip` if you encounter permission issues, or preferably, set the correct permissions for your user on the `/var/www/your-project` directory.*

4.  **Install Gunicorn:**
    ```bash
    pip install gunicorn
    ```

5.  **Test Gunicorn:**
    From your project directory (`/var/www/your-project`), run the following command to test if Gunicorn can serve your app. `app:app` refers to the `app` object inside the `app.py` file.
    ```bash
    gunicorn --workers 3 --bind unix:youtube-downloader.sock -m 007 app:app
    ```
    This will create a Unix socket file (`youtube-downloader.sock`) in your project directory. Press `Ctrl+C` to stop.

### 4. Create a Gunicorn Systemd Service

Create a systemd service file to manage the Gunicorn process.

1.  **Create the service file:**
    ```bash
    sudo nano /etc/systemd/system/youtube-downloader.service
    ```

2.  **Add the following content.** Replace `<your-user>` with your username.
    ```ini
    [Unit]
    Description=Gunicorn instance to serve YouTube Downloader
    After=network.target

    [Service]
    User=<your-user>
    Group=www-data
    WorkingDirectory=/var/www/your-project
    Environment="PATH=/var/www/your-project/venv/bin"
    ExecStart=/var/www/your-project/venv/bin/gunicorn --workers 3 --bind unix:youtube-downloader.sock -m 007 app:app

    [Install]
    WantedBy=multi-user.target
    ```

3.  **Start and enable the service:**
    ```bash
    sudo systemctl start youtube-downloader
    sudo systemctl enable youtube-downloader
    ```

4.  **Check the status:**
    ```bash
    sudo systemctl status youtube-downloader
    ```

### 5. Configure Nginx as a Reverse Proxy

Configure Nginx to forward web traffic to the Gunicorn socket.

1.  **Create an Nginx server block file:**
    ```bash
    sudo nano /etc/nginx/sites-available/youtube-downloader
    ```

2.  **Add the following configuration.** Replace `your_domain.com` with your domain or server IP address.
    ```nginx
    server {
        listen 80;
        server_name your_domain.com www.your_domain.com;

        location / {
            include proxy_params;
            proxy_pass http://unix:/var/www/your-project/youtube-downloader.sock;
        }
    }
    ```

3.  **Enable the site by creating a symbolic link:**
    ```bash
    sudo ln -s /etc/nginx/sites-available/youtube-downloader /etc/nginx/sites-enabled
    ```

4.  **Test the Nginx configuration for syntax errors:**
    ```bash
    sudo nginx -t
    ```

5.  **Restart Nginx to apply the changes:**
    ```bash
    sudo systemctl restart nginx
    ```

Your application should now be accessible at your domain or IP address.
