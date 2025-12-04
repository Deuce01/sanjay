import requests
from bs4 import BeautifulSoup
import re

# --- Helper Logic ---

def extract_name(soup, text):
    # Try text-shadow style (specific to this site)
    for h3 in soup.find_all('h3'):
        if 'text-shadow' in h3.get('style', ''):
            name = h3.get_text().strip()
            if len(name) > 2: return name
    # Fallback
    for tag in ['h1', 'h2', 'h3']:
        el = soup.find(tag)
        if el:
            name = el.get_text().strip()
            if 2 < len(name) < 50: return name
    return "N/A"

def extract_field_from_iconbox(soup, keyword):
    """Generic extractor for the icon-leftbox structure"""
    for box in soup.find_all('div', class_='icon-leftbox'):
        strong = box.find('strong')
        if strong and keyword in strong.get_text():
            return box.get_text().replace(strong.get_text(), '').strip()
    return "N/A"

def extract_education(soup):
    edu_data = {}
    for box in soup.find_all('div', class_='icon-leftbox'):
        strong = box.find('strong')
        if strong:
            label = strong.get_text()
            if 'Education Category' in label:
                edu_data['cat'] = box.get_text().replace('Education Category', '').strip()
            elif 'Education Level' in label:
                edu_data['lvl'] = box.get_text().replace('Education Level', '').strip()
    
    if edu_data:
        lvl = edu_data.get('lvl', '')
        cat = edu_data.get('cat', '')
        if lvl and cat: return f"{lvl} in {cat}"
        return lvl or cat
    return "N/A"

def extract_about(soup):
    for h4 in soup.find_all('h4'):
        text = h4.get_text().strip()
        if 'looking' in text.lower() and len(text) > 10:
            return text
    # Fallback to quotes/about me section
    for h6 in soup.find_all('h6'):
        if 'About Me' in h6.get_text():
            q = h6.find_next('div', class_='quotes')
            if q and q.find('h4'): return q.find('h4').get_text().strip()
    return "N/A"

def extract_additional_data(soup, url):
    data = {'profile_url': url}
    
    # Try to find the canonical profile URL in the page
    found_url = False
    try:
        body = soup.find('body')
        if body:
            # Attempting to follow the specific div structure provided earlier
            divs = body.find_all('div', recursive=False)
            if len(divs) >= 3:
                div2 = divs[2].find_all('div', recursive=False)[1]
                p = div2.find_all('p', recursive=False)[0]
                href = p.find('a').get('href', '')
                if href: 
                    data['profile_url'] = href
                    found_url = True
    except:
        pass

    if not found_url:
        for a in soup.find_all('a'):
            href = a.get('href', '')
            if 'freeindianmatrimony.com' in href and href != '#':
                data['profile_url'] = href
                break

    # Extract other fields
    mappings = {
        'Star Sign': 'star_sign', 'Moon Sign': 'moon_sign', 'Height': 'height',
        'Weight': 'weight', 'Food Habit': 'food_habit', 
        'Smoking Habit': 'smoking_habit', 'Drinking Habit': 'drinking_habit'
    }
    
    for box in soup.find_all('div', class_='icon-leftbox'):
        strong = box.find('strong')
        if strong:
            label = strong.get_text()
            val = box.get_text().replace(label, '').strip()
            for key, field in mappings.items():
                if key in label:
                    data[field] = val
                    
    return data

# --- Main Scraper Function ---
def get_profile_data(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        # 1. Profile Picture
        profile_pic = None
        # Try complex path first
        try:
            body = soup.find('body')
            target_div = body.find_all('div', recursive=False)[2].find_all('div', recursive=False)[1].find_all('div', recursive=False)[0]
            src = target_div.find('img').get('src', '')
            if src and 'no_avatar' not in src: profile_pic = src
        except:
            pass
        
        # Fallback for picture
        if not profile_pic:
            for img in soup.find_all('img'):
                src = img.get('src', '')
                if 'uploads' in src and any(x in src.lower() for x in ['.jpg', '.jpeg', '.png']):
                    profile_pic = src
                    break
        
        text = soup.get_text()
        
        data = {
            'profile_name': extract_name(soup, text),
            'age': extract_field_from_iconbox(soup, 'Age').replace('Years', '').strip(), # Clean up 'Years' if present
            'gender': extract_field_from_iconbox(soup, 'Gender'), # Or use text analysis fallback
            'marital_status': extract_field_from_iconbox(soup, 'Marital Status'),
            'mother_tongue': extract_field_from_iconbox(soup, 'Mother Tongue'),
            'religion': extract_field_from_iconbox(soup, 'Religion'),
            'caste': extract_field_from_iconbox(soup, 'Caste'),
            'country': extract_field_from_iconbox(soup, 'Country'),
            'education': extract_education(soup),
            'occupation': extract_field_from_iconbox(soup, 'Occupation'),
            'about': extract_about(soup),
            'profile_picture': profile_pic,
            'additional_data': extract_additional_data(soup, url)
        }

        # Validation
        if data['profile_name'] == "N/A" and data['profile_picture'] is None:
            return None # Failed to scrape meaningful data

        return data

    except Exception as e:
        print(f"Scraper Exception for {url}: {e}")
        return None