import os
import requests

# Estem executant des de C:\Users\froca\Documents\jardi-palautordera
base_dir = os.getcwd()
img_dir = os.path.join(base_dir, "img")

if not os.path.exists(img_dir):
    os.makedirs(img_dir)
    print(f"Creat directori: {img_dir}")

TARGETS = {
    "dicentra.jpg": "https://upload.wikimedia.org/wikipedia/commons/8/87/Dicentra-spectabilis.jpg",
    "lupinus.jpg": "https://upload.wikimedia.org/wikipedia/commons/e/ea/Lupinus_polyphyllus.JPG",
    "helleborus.jpg": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Helleborus_orientalis._Lenteroos_04.JPG",
    "impatiens.jpg": "https://upload.wikimedia.org/wikipedia/commons/2/23/Impatiens_Walleriana_Red.jpg",
    "petunia.jpg": "https://upload.wikimedia.org/wikipedia/commons/3/36/Petunia_x_hybrida_a1.JPG",
    "physostegia.jpg": "https://upload.wikimedia.org/wikipedia/commons/e/ec/Physostegia_virginiana_9622.jpg",
    "chelone.jpg": "https://upload.wikimedia.org/wikipedia/commons/a/a2/Chelone_obliqua_02.jpg"
}

headers = {'User-Agent': 'Mozilla/5.0'}

print(f"Començant descàrrega a {img_dir}...")

for name, url in TARGETS.items():
    path = os.path.join(img_dir, name)
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                f.write(r.content)
            print(f"[OK] {name} ({os.path.getsize(path)} bytes)")
        else:
            print(f"[ERROR] {name} - Status {r.status_code}")
    except Exception as e:
        print(f"[EXCEPCIO] {name}: {e}")

print("Finalitzat.")
