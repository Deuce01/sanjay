# Loom Demo Script - Matrimony Video Generator

## Opening (30 seconds)
**"Hi! I'm going to show you the Matrimony Video Generator - an automated system that creates personalized video profiles from Excel data. Let me walk you through how it works."**

*Show desktop with project folder open*

## Setup Demo (45 seconds)
**"First, let me start the application. I just run python app.py and it starts both the web server and background worker automatically."**

*Open terminal, type: `python app.py`*
*Show terminal output: "Running on http://127.0.0.1:5000"*

**"Now I'll open the web interface in my browser."**

*Open browser, navigate to http://127.0.0.1:5000*
*Show clean upload interface*

## Excel File Demo (60 seconds)
**"The system accepts two types of Excel files. Let me show you both formats."**

*Open Excel or show sample files*

**"Format 1 uses matrimony website URLs - the system scrapes profile data automatically."**
*Show Excel with columns: Profile url, Background music URL*

**"Format 2 uses direct profile data - name, age, religion, education, etc."**
*Show Excel with columns: Profile Name, Age, Religion, Education, etc.*

**"For this demo, I'll use Format 1 with URLs."**

## Upload Process (90 seconds)
**"Now I'll upload the Excel file and watch the magic happen."**

*Click "Choose File", select Excel file*
*Click "Start Job"*

**"Notice how the page automatically shows the processing status with real-time logs."**

*Point to status display and logs section*

**"The logs show timestamps, progress indicators, and exactly what's happening:"**
*Read a few log entries as they appear*
- **"Started processing job"**
- **"Found X profiles to process"** 
- **"Scraping profile URLs"**
- **"Video created successfully"**

**"The page refreshes automatically every 10 seconds, so I don't need to do anything."**

## Processing Explanation (60 seconds)
**"Behind the scenes, here's what's happening:"**

*Show file structure while processing continues*

**"The scraper extracts profile data from matrimony websites, downloads profile pictures, and the video generator creates 4-scene videos:"**
- **"Scene 1: Basic info like age and religion"**
- **"Scene 2: Education and occupation"** 
- **"Scene 3: Lifestyle preferences"**
- **"Scene 4: About section and location"**

**"Each video is 16 seconds long with smooth transitions and background music."**

## Completion Demo (45 seconds)
**"Look - the job just completed! The status changed to 'Job Complete' and I can now download the ZIP file."**

*Click "Download ZIP"*
*Show ZIP file downloading*

**"Let me extract and show you the generated videos."**

*Extract ZIP, open one of the MP4 files*
*Play video showing the 4 scenes with profile data*

## Video Showcase (60 seconds)
**"Here's the final result - a professional matrimony video with:"**
*Point out features as video plays*
- **"Profile picture in a circular frame"**
- **"Clean typography with the template background"**
- **"Smooth scene transitions"**
- **"Background music"**
- **"All profile data beautifully laid out"**

**"The system processed multiple profiles and created individual videos for each one, all automatically."**

## Key Features Summary (30 seconds)
**"Key features that make this powerful:"**
- **"Automatic web scraping from matrimony sites"**
- **"Real-time progress tracking with detailed logs"**
- **"Batch processing of multiple profiles"**
- **"Professional video templates"**
- **"No manual intervention needed"**
- **"Single command to start everything"**

## Closing (15 seconds)
**"That's the Matrimony Video Generator - from Excel file to professional videos in minutes, completely automated. Perfect for matrimony agencies or anyone creating profile videos at scale."**

*Show final ZIP file with multiple videos*

---

## Demo Tips

### Before Recording:
- [ ] Prepare sample Excel file with 3-5 profiles
- [ ] Test the complete flow once
- [ ] Clear browser cache/history
- [ ] Close unnecessary applications
- [ ] Set up good lighting and audio

### During Recording:
- [ ] Speak clearly and at moderate pace
- [ ] Use mouse cursor to highlight important elements
- [ ] Pause briefly when switching between screens
- [ ] Show actual video output, not just the interface

### Sample Excel Data:
```
Profile url: https://www.freeindianmatrimony.com/10500/...
Profile url: https://www.freeindianmatrimony.com/10501/...
Profile url: https://www.freeindianmatrimony.com/10502/...
```

### Backup Plan:
If live demo fails, have pre-recorded video files ready to show the final output.

**Total Demo Time: ~6 minutes**