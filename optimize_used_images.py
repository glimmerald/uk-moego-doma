import os
import json
import re
from PIL import Image

def get_used_images():
    used = set()
    
    # 1. Parse index.vue
    with open('app/pages/index.vue', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all /images/... (JPG/PNG)
    matches = re.findall(r"'/images/([^']+\.(?:jpg|jpeg|png))'", content)
    for m in matches:
        used.add(f"/images/{m}")
        
    matches2 = re.findall(r'"/images/([^"]+\.(?:jpg|jpeg|png))"', content)
    for m in matches2:
        used.add(f"/images/{m}")

    # 2. Parse cities.json
    with open('app/data/cities.json', 'r', encoding='utf-8') as f:
        cities = json.load(f)
        
    for city in cities:
        for complex in city.get('complexes', []):
            img = complex.get('image', '')
            if img.startswith('/images/'):
                used.add(img)

    return used

used_images = get_used_images()
print(f"Found {len(used_images)} unique images used in code.")

DEST_DIR = 'app/public/optimized'
if not os.path.exists(DEST_DIR):
    os.makedirs(DEST_DIR)

replacements = {} # old_path -> new_path

for img_path in used_images:
    # img_path is like /images/Фасад/DSC04411.jpg
    # real path on disk is app/public + img_path
    
    disk_path = f"app/public{img_path}"
    
    # We will flatten them into /optimized/ or keep structure?
    # Let's keep structure but inside optimized
    rel_path = img_path.replace('/images/', '')
    # Change extension to webp
    webp_rel_path = os.path.splitext(rel_path)[0] + '.webp'
    
    out_path = os.path.join(DEST_DIR, webp_rel_path)
    out_dir = os.path.dirname(out_path)
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    if os.path.exists(disk_path):
        try:
            with Image.open(disk_path) as im:
                # Convert to RGB if needed
                if im.mode in ("RGBA", "P"):
                    im = im.convert("RGB")
                    
                # Resize if it's too large (max 1920x1920)
                im.thumbnail((1920, 1920), Image.Resampling.LANCZOS)
                
                im.save(out_path, 'WEBP', quality=80)
            
            # The new URL path will be /optimized/...
            replacements[img_path] = f"/optimized/{webp_rel_path}"
        except Exception as e:
            print(f"Error processing {disk_path}: {e}")
    else:
        print(f"Warning: File not found on disk: {disk_path}")

print(f"Optimized {len(replacements)} images.")

# Now replace in files
with open('app/pages/index.vue', 'r', encoding='utf-8') as f:
    index_content = f.read()

for old_p, new_p in replacements.items():
    index_content = index_content.replace(old_p, new_p)
    
with open('app/pages/index.vue', 'w', encoding='utf-8') as f:
    f.write(index_content)

with open('app/data/cities.json', 'r', encoding='utf-8') as f:
    cities_content = f.read()

for old_p, new_p in replacements.items():
    cities_content = cities_content.replace(old_p, new_p)

with open('app/data/cities.json', 'w', encoding='utf-8') as f:
    f.write(cities_content)
    
print("Code updated!")
