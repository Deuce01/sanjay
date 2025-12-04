import os
import sqlite3
import pandas as pd
import time
import shutil
import zipfile

# Import our custom modules
from scraper import get_profile_data
from video_generator import generate_video_from_profile

# Configuration
DATABASE = 'jobs.db'
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def process_job(job_id, input_file):
    print(f"--- Processing Job: {job_id} ---")
    
    # Create a temp working dir for this job's videos
    job_output_dir = os.path.join(OUTPUT_FOLDER, job_id)
    os.makedirs(job_output_dir, exist_ok=True)
    
    video_files_created = []
    
    try:
        df = pd.read_excel(input_file)
        
        # --- Format 1: URLs ---
        if 'Profile url' in df.columns:
            print("Detected Format 1: Scraping URLs...")
            
            for index, row in df.iterrows():
                profile_url = row['Profile url']
                music_url = row.get('Background music URL')
                print(f"Row {index}: Scraping {profile_url}...")
                
                try:
                    profile_data = get_profile_data(profile_url)
                    
                    if not profile_data:
                        print(f"Skipping row {index}: Scraper returned no data.")
                        continue
                    
                    if music_url:
                        profile_data['background_music_url'] = music_url
                    
                    output_filename = os.path.join(job_output_dir, f"video_{index}.mp4")
                    generate_video_from_profile(profile_data, output_filename)
                    
                    if os.path.exists(output_filename):
                        video_files_created.append(output_filename)
                    
                except Exception as e:
                    print(f"Failed to process row {index}: {e}")

        # --- Format 2: Direct Data ---
        elif 'Profile Name' in df.columns:
            print("Detected Format 2: Using direct data...")
            
            for index, row in df.iterrows():
                print(f"Processing row {index}: {row.get('Profile Name', 'Unknown')}")
                try:
                    profile_data = {
                        "profile_name": row.get("Profile Name", "N/A"),
                        "age": str(row.get("Age", "N/A")),
                        "marital_status": row.get("Marital Status", "N/A"),
                        "mother_tongue": row.get("Mother Toungue", "N/A"),
                        "religion": row.get("Religion", "N/A"),
                        "country": row.get("Country", "N/A"),
                        "education": row.get("Education", "N/A"),
                        "occupation": row.get("Occupation", "N/A"),
                        "about": row.get("Profile description", "N/A"),
                        "profile_picture": row.get("Photos URL"),
                        "background_music_url": row.get("Background music URL"),
                        "additional_data": {
                            "profile_url": "No URL Provided",
                            "star_sign": "", 
                            "food_habit": "",
                            "smoking_habit": "",
                            "drinking_habit": ""
                        }
                    }
                    
                    output_filename = os.path.join(job_output_dir, f"video_{index}.mp4")
                    generate_video_from_profile(profile_data, output_filename)
                    
                    if os.path.exists(output_filename):
                        video_files_created.append(output_filename)

                except Exception as e:
                    print(f"Failed to process row {index}: {e}")

        # --- Finalize ---
        if video_files_created:
            zip_filename = f"{job_id}.zip"
            zip_filepath = os.path.join(OUTPUT_FOLDER, zip_filename)
            
            print(f"Zipping {len(video_files_created)} videos...")
            with zipfile.ZipFile(zip_filepath, 'w') as zf:
                for file in video_files_created:
                    zf.write(file, os.path.basename(file))
            
            shutil.rmtree(job_output_dir) # Cleanup raw videos
            return "COMPLETED", zip_filepath
        else:
            print("No videos created.")
            return "FAILED", None

    except Exception as e:
        print(f"Job {job_id} failed: {e}")
        return "FAILED", None

def main_worker_loop():
    print("Worker loop started. Waiting for jobs...")
    while True:
        try:
            db = get_db()
            job = db.execute('SELECT * FROM jobs WHERE status = ? LIMIT 1', ('PENDING',)).fetchone()
            
            if job:
                job_id = job['id']
                input_file = job['input_file']
                
                db.execute('UPDATE jobs SET status = ? WHERE id = ?', ('PROCESSING', job_id))
                db.commit()
                
                status, output_path = process_job(job_id, input_file)
                
                db.execute('UPDATE jobs SET status = ?, output_file = ? WHERE id = ?', (status, output_path, job_id))
                db.commit()
            
            db.close()
        except Exception as e:
            print(f"Worker loop error: {e}")
        
        time.sleep(5)

if __name__ == "__main__":
    main_worker_loop()