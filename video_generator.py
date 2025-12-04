import os
import shutil
import subprocess
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps
import uuid

# --- Configuration ---
ASSET_DIR = "assets"
TEMPLATE_BG = os.path.join(ASSET_DIR, "template-background.jpg")
FONT_BOLD_FILE = os.path.join(ASSET_DIR, "font_bold.ttf")
FONT_REGULAR_FILE = os.path.join(ASSET_DIR, "font_regular.ttf")

# Settings
SCENE_DURATION = 4
VIDEO_WIDTH = 1024
VIDEO_HEIGHT = 1024
CX = VIDEO_WIDTH // 2
TEXT_COLOR_DARK = "#5D4037"
TEXT_COLOR_LIGHT = "#7A5549"

def create_scene_image(profile, scene_number, temp_dir):
    img = Image.open(TEMPLATE_BG).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # Fonts
    try:
        font_h1 = ImageFont.truetype(FONT_BOLD_FILE, 65)
        font_h2 = ImageFont.truetype(FONT_BOLD_FILE, 40)
        font_p = ImageFont.truetype(FONT_REGULAR_FILE, 35)
        font_link = ImageFont.truetype(FONT_REGULAR_FILE, 25) 
    except IOError:
        print("Error: Fonts not found.")
        return None

    # Profile Picture
    pfp_y = 220
    pfp_size = 300
    try:
        pic_path = os.path.join(temp_dir, "profile_pic.jpg")
        
        # Download if not exists
        if not os.path.exists(pic_path) and profile.get("profile_picture"):
             with open(pic_path, "wb") as f:
                f.write(requests.get(profile["profile_picture"]).content)

        if os.path.exists(pic_path):
            pfp = Image.open(pic_path).convert("RGBA")
            mask = Image.new("L", (pfp_size, pfp_size), 0)
            ImageDraw.Draw(mask).ellipse((0, 0, pfp_size, pfp_size), fill=255)
            pfp_circular = ImageOps.fit(pfp, mask.size, centering=(0.5, 0.5))
            pfp_circular.putalpha(mask)
            img.paste(pfp_circular, (CX - (pfp_size // 2), pfp_y), pfp_circular)
    except Exception as e:
        print(f"PFP Error: {e}")

    # Layout Coordinates
    # Gap increased to 80px as requested
    y_name = pfp_y + pfp_size + 80 
    # URL moved below name as requested
    y_url = y_name + 60 
    y_col_start = y_url + 70 

    # Data Extraction
    url_text = profile.get("additional_data", {}).get("profile_url", "")
    name = profile["profile_name"]
    name_alt = f"{profile.get('additional_data', {}).get('star_sign', '')} / {name}"
    
    # Common Elements (Name & URL)
    display_name = name if scene_number == 1 else name_alt
    draw.text((CX, y_name), display_name, font=font_h1, fill=TEXT_COLOR_DARK, anchor="ms")
    draw.text((CX, y_url), url_text, font=font_link, fill=TEXT_COLOR_LIGHT, anchor="ms")

    # Scene Specifics
    col1 = 320
    col2 = 704
    
    if scene_number == 1:
        draw.text((col1, y_col_start), "AGE", font=font_h2, fill=TEXT_COLOR_DARK, anchor="ms")
        draw.text((col1, y_col_start + 45), f"{profile.get('age', 'N/A')} Years", font=font_p, fill=TEXT_COLOR_LIGHT, anchor="ms")
        
        draw.text((col2, y_col_start), "RELIGION", font=font_h2, fill=TEXT_COLOR_DARK, anchor="ms")
        draw.text((col2, y_col_start + 45), profile.get("religion", "N/A"), font=font_p, fill=TEXT_COLOR_LIGHT, anchor="ms")
        
        y_row2 = y_col_start + 120
        draw.text((col1, y_row2), "MARITAL STATUS", font=font_h2, fill=TEXT_COLOR_DARK, anchor="ms")
        draw.text((col1, y_row2 + 45), profile.get("marital_status", "N/A"), font=font_p, fill=TEXT_COLOR_LIGHT, anchor="ms")
        
        draw.text((col2, y_row2), "MOTHER TONGUE", font=font_h2, fill=TEXT_COLOR_DARK, anchor="ms")
        draw.text((col2, y_row2 + 45), profile.get("mother_tongue", "N/A"), font=font_p, fill=TEXT_COLOR_LIGHT, anchor="ms")

    elif scene_number == 2:
        draw.text((CX, y_col_start), "EDUCATION", font=font_h2, fill=TEXT_COLOR_DARK, anchor="ms")
        draw.text((CX, y_col_start + 45), profile.get("education", "N/A"), font=font_p, fill=TEXT_COLOR_LIGHT, anchor="ms")
        
        y_row2 = y_col_start + 120
        draw.text((CX, y_row2), "OCCUPATION", font=font_h2, fill=TEXT_COLOR_DARK, anchor="ms")
        draw.text((CX, y_row2 + 45), profile.get("occupation", "N/A"), font=font_p, fill=TEXT_COLOR_LIGHT, anchor="ms")

    elif scene_number == 3:
        draw.text((CX, y_col_start), "Lifestyle", font=font_h2, fill=TEXT_COLOR_DARK, anchor="ms")
        y = y_col_start + 60
        draw.text((CX, y), profile.get("additional_data", {}).get("food_habit", ""), font=font_p, fill=TEXT_COLOR_LIGHT, anchor="ms")
        draw.text((CX, y + 50), profile.get("additional_data", {}).get("smoking_habit", ""), font=font_p, fill=TEXT_COLOR_LIGHT, anchor="ms")
        draw.text((CX, y + 100), profile.get("additional_data", {}).get("drinking_habit", ""), font=font_p, fill=TEXT_COLOR_LIGHT, anchor="ms")

    elif scene_number == 4:
        draw.text((CX, y_col_start), "About me", font=font_h2, fill=TEXT_COLOR_DARK, anchor="ms")
        about = profile.get("about", "")
        lines = [about[i:i+45] for i in range(0, len(about), 45)]
        y = y_col_start + 60
        for line in lines:
            draw.text((CX, y), line, font=font_p, fill=TEXT_COLOR_LIGHT, anchor="ms")
            y += 45
        draw.text((CX, y + 30), profile.get("country", ""), font=font_p, fill=TEXT_COLOR_LIGHT, anchor="ms")

    outfile = os.path.join(temp_dir, f"scene-{scene_number}.png")
    img.save(outfile)
    return outfile

def generate_video_from_profile(profile_json, output_filename):
    temp_dir = f"temp_video_{uuid.uuid4()}"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Audio Handling
    music_file = os.path.join(temp_dir, "music.mp3")
    has_music = False
    
    if profile_json.get("background_music_url"):
        try:
            with open(music_file, "wb") as f:
                f.write(requests.get(profile_json["background_music_url"]).content)
            has_music = True
        except:
            print("Failed to download music, using silence.")

    if not has_music:
        # Create silent track
        try:
            subprocess.run([
                'ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono',
                '-t', str(SCENE_DURATION * 4), '-q:a', '9', '-acodec', 'mp3',
                '-y', music_file
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            return None # Critical failure if ffmpeg fails

    try:
        scenes = []
        for i in range(1, 5):
            s = create_scene_image(profile_json, i, temp_dir)
            if not s: raise Exception(f"Failed to create scene {i}")
            scenes.append(s)

        # Video Stitching
        offset1 = SCENE_DURATION - 0.5
        offset2 = (SCENE_DURATION * 2) - 0.5
        offset3 = (SCENE_DURATION * 3) - 0.5
        total = SCENE_DURATION * 4

        cmd = [
            'ffmpeg',
            '-loop', '1', '-t', str(SCENE_DURATION), '-i', scenes[0],
            '-loop', '1', '-t', str(SCENE_DURATION), '-i', scenes[1],
            '-loop', '1', '-t', str(SCENE_DURATION), '-i', scenes[2],
            '-loop', '1', '-t', str(SCENE_DURATION), '-i', scenes[3],
            '-i', music_file,
            '-filter_complex',
            f"[0:v][1:v]xfade=transition=fade:duration=0.5:offset={offset1}[v1];"
            f"[v1][2:v]xfade=transition=fade:duration=0.5:offset={offset2}[v2];"
            f"[v2][3:v]xfade=transition=fade:duration=0.5:offset={offset3}[v3];"
            f"[4:a]aloop=loop=-1:size=2e+09[a]",
            '-map', '[v3]', '-map', '[a]',
            '-c:v', 'libx264', '-c:a', 'aac', '-pix_fmt', 'yuv420p',
            '-r', '24', '-t', str(total), '-y', output_filename
        ]
        
        subprocess.run(cmd, check=True)

    except Exception as e:
        print(f"Video Gen Error: {e}")
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)