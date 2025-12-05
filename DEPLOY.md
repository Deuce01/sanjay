# Render Deployment Guide

## Prerequisites
- GitHub account
- Render account (free tier available)
- Code pushed to GitHub repository

## Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Create Render Service
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select the `sanjay` repository

### 3. Configure Service
**Basic Settings:**
- Name: `matrimony-video-generator`
- Environment: `Python 3`
- Build Command: `pip install -r requirements.txt`
- Start Command: `python app.py`

**Advanced Settings:**
- Auto-Deploy: `Yes`
- Instance Type: `Free` (or `Starter` for better performance)

### 4. Environment Variables
Add these in Render dashboard:
```
PYTHON_VERSION=3.9.16
PORT=10000
```

### 5. Deploy
Click "Create Web Service" and wait for deployment.

## Important Notes

### FFmpeg Installation
Render includes FFmpeg by default, so no additional setup needed.

### File Storage
- Render has ephemeral storage
- Uploaded files and generated videos are temporary
- Consider using external storage for production

### Database
- SQLite works for development
- For production, consider PostgreSQL addon

### Performance
- Free tier has limitations (512MB RAM, sleeps after 15min)
- Upgrade to Starter ($7/month) for better performance

## Post-Deployment

### Access Your App
Your app will be available at:
```
https://matrimony-video-generator.onrender.com
```

### Monitor Logs
View logs in Render dashboard to debug issues.

### Custom Domain (Optional)
Add custom domain in Render dashboard settings.

## Troubleshooting

### Build Failures
- Check Python version compatibility
- Verify all dependencies in requirements.txt
- Review build logs in Render dashboard

### Runtime Issues
- Check application logs
- Verify environment variables
- Test locally first

### Memory Issues
- Reduce video quality settings
- Process fewer profiles per batch
- Upgrade to higher tier

## Production Optimizations

### Security
```python
# Add to app.py
import os
if os.environ.get('RENDER'):
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
```

### Database
```python
# Use PostgreSQL for production
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///jobs.db')
```

### File Storage
```python
# Use cloud storage
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
OUTPUT_FOLDER = os.environ.get('OUTPUT_FOLDER', 'outputs')
```

## Scaling Considerations
- Use background job queue (Redis + Celery)
- Implement file cleanup policies
- Add rate limiting
- Use CDN for video delivery