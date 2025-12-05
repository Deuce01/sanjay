# How to Install on DreamHost Shared Hosting

This system is built to work specifically with DreamHost's Python support. Since you are on shared hosting, there are 3 simple steps to get it running.

**Files Required:**
Upload all files from the Matrimony_Video_Generator folder to your website's folder (e.g., yourdomain.com).

## Step 1: Enable Passenger (The Web Server)

1. Log in to your DreamHost Panel.
2. Go to Websites > Manage Websites.
3. Click Manage next to your domain.
4. Click Web Options.
5. Scroll down to "Web Server Settings" and check the box "Passenger (Ruby/Python/Node)".
6. Click Save Changes.

## Step 2: Install Libraries (The One-Time Setup)

Since shared hosting doesn't have all libraries pre-installed, you need to run one command.
If you are not comfortable with this, you can ask DreamHost Support to "Install the requirements.txt into a virtual environment for my domain".

**If doing it yourself via SSH:**

1. Login to SSH.
2. Navigate to your folder: `cd yourdomain.com`
3. Create a python environment: `python3 -m venv venv`
4. Activate it: `source venv/bin/activate`
5. Install the tools: `pip install -r requirements.txt`

## Step 3: Turn on the Worker (The Cron Job)

This is what processes the videos in the background.

1. In the DreamHost Panel, go to Advanced > Cron Jobs.
2. Click Add New Cron Job.
3. User: Select your username.
4. Command: `cd /home/YOUR_USERNAME/yourdomain.com && python3 worker.py`
   (Replace YOUR_USERNAME and yourdomain.com with your actual details)
5. Run Every: Select "Custom" and type `*/2` in the Minutes box (runs every 2 minutes).
6. Click Add.

**That's it!**
- Visit yourdomain.com to see the upload page.
- Upload an Excel file.
- The Cron Job will pick it up within 2 minutes and process your videos.

## Important Notes

### File Structure on DreamHost
```
~/yoursite.com/
├── passenger_wsgi.py    # WSGI entry point
├── .htaccess           # Apache configuration
├── app.py              # Flask application
├── worker.py           # Background processor
├── requirements.txt    # Dependencies
├── venv/              # Virtual environment
├── uploads/           # Upload directory
├── outputs/           # Output directory
└── assets/            # Static assets
```

### FFmpeg Installation
DreamHost may not have FFmpeg. Install locally:
```bash
# Download FFmpeg static build
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
tar -xf ffmpeg-release-amd64-static.tar.xz
mv ffmpeg-*-static/ffmpeg ~/bin/
```

Update `video_generator.py`:
```python
FFMPEG_PATH = os.path.expanduser("~/bin/ffmpeg")
# Use FFMPEG_PATH in subprocess calls
```

### Background Worker
DreamHost shared hosting doesn't support long-running processes. Options:

**Option 1: Cron Job**
```bash
# Add to crontab
*/5 * * * * cd ~/yoursite.com && source venv/bin/activate && python worker.py
```

**Option 2: On-Demand Processing**
Remove threading from `app.py` and process jobs synchronously.

### Memory Limitations
- Shared hosting has memory limits
- Reduce video quality if needed
- Process one profile at a time

## Configuration Updates

### Update app.py for DreamHost
```python
# Remove threading for shared hosting
# Comment out worker thread code
# if not worker_running:
#     worker_running = True
#     threading.Thread(target=process_jobs, daemon=True).start()
```

### Update paths for shared hosting
```python
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')
DATABASE = os.path.join(BASE_DIR, 'jobs.db')
```

## Troubleshooting

### 500 Internal Server Error
- Check error logs: `tail ~/logs/yoursite.com/http/error.log`
- Verify Python path in .htaccess
- Check file permissions

### Import Errors
- Ensure virtual environment is activated
- Verify all dependencies installed
- Check Python version compatibility

### Database Issues
- Ensure SQLite is available
- Check database file permissions
- Initialize database properly

### Video Generation Fails
- Install FFmpeg in ~/bin/
- Update FFmpeg path in code
- Check memory usage

## Performance Optimization

### Reduce Resource Usage
```python
# Smaller video resolution
VIDEO_WIDTH = 512
VIDEO_HEIGHT = 512

# Lower quality settings
'-crf', '28'  # Higher CRF = lower quality
```

### File Cleanup
```python
# Clean old files regularly
import glob
import time

def cleanup_old_files():
    for folder in ['uploads', 'outputs']:
        files = glob.glob(f"{folder}/*")
        for file in files:
            if time.time() - os.path.getctime(file) > 3600:  # 1 hour
                os.remove(file)
```

## Alternative: VPS Hosting
For better performance, consider DreamHost VPS:
- Full root access
- Install FFmpeg system-wide
- Run background workers
- More memory and CPU

## Support
- DreamHost Knowledge Base
- Check hosting limits
- Monitor resource usage