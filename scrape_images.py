import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def download_images(url, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    print(f"Fetching {url}...")
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')
    
    # Also find background images in divs/sections if possible, but let's stick to img tags first
    
    downloaded = 0
    for i, img in enumerate(images):
        src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
        if not src:
            continue
            
        img_url = urljoin(url, src)
        parsed = urlparse(img_url)
        
        # Skip small icons/logos typically SVG or very small, but let's grab everything for now
        if not parsed.netloc:
            continue
            
        filename = os.path.basename(parsed.path)
        if not filename:
            filename = f"image_{i}.jpg"
            
        # Clean up query params from filename if any
        if '?' in filename:
            filename = filename.split('?')[0]
            
        # Ensure it has an extension
        if not any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']):
            filename = f"image_{i}.jpg"
            
        save_path = os.path.join(save_dir, filename)
        
        # Skip if already downloaded
        if os.path.exists(save_path):
            continue
            
        print(f"Downloading {img_url}...")
        try:
            img_data = requests.get(img_url, headers={'User-Agent': 'Mozilla/5.0'}).content
            with open(save_path, 'wb') as f:
                f.write(img_data)
            downloaded += 1
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")
            
    print(f"Successfully downloaded {downloaded} images to {save_dir}")

if __name__ == "__main__":
    website_url = "https://jasperschut.nl/"
    assets_dir = "/Users/jorikschut/Documents/Projecten-sites/Jasper Schut/src/assets"
    public_dir = "/Users/jorikschut/Documents/Projecten-sites/Jasper Schut/public/images"
    
    # Let's save to public for easier access in Astro without import hassle for a gallery
    download_images(website_url, public_dir)
