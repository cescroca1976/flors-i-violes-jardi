import os
import requests

base_dir = os.getcwd()
img_dir = os.path.join(base_dir, "img")
if not os.path.exists(img_dir): os.makedirs(img_dir)

# NOVES URLs (UNSPLASH - Més fiables per descàrrega)
TARGETS = {
    "dicentra.jpg": "https://images.unsplash.com/photo-1596436647226-25d2d480e478?auto=format&fit=crop&w=800&q=80",
    "lupinus.jpg": "https://images.unsplash.com/photo-1563297746-b6ae43292418?auto=format&fit=crop&w=800&q=80",
    "helleborus.jpg": "https://images.unsplash.com/photo-1644336043552-652f4eb275f0?auto=format&fit=crop&w=800&q=80",
    "impatiens.jpg": "https://images.unsplash.com/photo-1620063264426-38d5d431c360?auto=format&fit=crop&w=800&q=80",
    "petunia.jpg": "https://images.unsplash.com/photo-1559437188-375fd3697e07?auto=format&fit=crop&w=800&q=80",
    "physostegia.jpg": "https://images.unsplash.com/photo-1628193859089-de688a2dd782?auto=format&fit=crop&w=800&q=80",
    "chelone.jpg": "https://images.unsplash.com/photo-1629837943542-a8c9e421379e?auto=format&fit=crop&w=800&q=80"
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

print("--- BAIXANT PHOTOS UNSPLASH A LOCAL ---")
for name, url in TARGETS.items():
    path = os.path.join(img_dir, name)
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                f.write(r.content)
            print(f"[OK] {name} baixada.")
        else:
            print(f"[ERROR] {name}: {r.status_code}")
    except Exception as e:
        print(f"[ERROR] {name}: {e}")
