# Setup Guide

## Prerequisites

1. **Python 3.8+**
2. **FFmpeg** (for video processing)
3. **Git** (optional, for version control)

## Installation Steps

### 1. Clone/Download Project
```bash
git clone https://github.com/Deuce01/sanjay.git
cd sanjay
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg

**Windows:**
1. Download from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to system PATH
4. Verify: `ffmpeg -version`

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

### 4. Verify Assets
Ensure these files exist in `assets/`:
- `font_bold.ttf`
- `font_regular.ttf` 
- `template-background.jpg`
- `VN20251008_150305.mp3`

### 5. Initialize Database
```bash
python -c "from app import init_db; init_db()"
```

### 6. Run Application
```bash
python app.py
```

### 7. Access Web Interface
Open browser: http://127.0.0.1:5000

## Directory Structure After Setup
```
sanjay/
├── uploads/        # Created automatically
├── outputs/        # Created automatically  
├── jobs.db         # Created on first run
└── temp_video_*/   # Temporary (auto-cleaned)
```

## Testing

### Test with Sample Data
Create `test.xlsx` with columns:
- Profile url: https://www.freeindianmatrimony.com/...
- Background music URL: (optional)

Upload through web interface and monitor logs.

## Production Deployment

### Security Checklist
- [ ] Change default host from 127.0.0.1
- [ ] Add authentication if needed
- [ ] Set up HTTPS
- [ ] Configure firewall rules
- [ ] Set up log rotation
- [ ] Monitor disk space for uploads/outputs

### Performance Tuning
- [ ] Increase worker threads if needed
- [ ] Set up database backups
- [ ] Configure reverse proxy (nginx)
- [ ] Set up monitoring (logs, metrics)

### Environment Variables
```bash
export FLASK_ENV=production
export DATABASE_URL=sqlite:///jobs.db
export UPLOAD_FOLDER=/path/to/uploads
export OUTPUT_FOLDER=/path/to/outputs
```

## Troubleshooting Setup

### Python Import Errors
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### FFmpeg Issues
```bash
# Test FFmpeg installation
ffmpeg -version

# Windows PATH issues
echo %PATH%
# Should include FFmpeg bin directory
```

### Permission Errors
```bash
# Linux/macOS
chmod +x app.py
sudo chown -R $USER:$USER .

# Windows
# Run as Administrator if needed
```

### Database Issues
```bash
# Reset database
rm jobs.db
python -c "from app import init_db; init_db()"
```

### Port Already in Use
```bash
# Find process using port 5000
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # macOS/Linux

# Kill process or change port in app.py
app.run(host='127.0.0.1', port=5001)
```