import os
import shutil
import glob

# Origens i Destins
source_dir = r"C:\Users\froca\.gemini\antigravity\playground"
dest_dir = r"C:\Users\froca\Documents\jardi-palautordera\img"

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

print(f"--- MOVENT IMATGES DE {source_dir} A {dest_dir} ---")

# Normalització de noms (detectem pel contingut del nom original)
# Mapa: 'part_del_nom_original': 'nom_final_standard.jpg'
rename_map = {
    'chelone': 'chelone.jpg',
    'lupinus': 'lupinus.jpg',
    'petunia': 'petunia.jpg',
    'physostegia': 'physostegia.jpg',
    'dicentra': 'dicentra.jpg',
    'impatiens': 'impatiens.jpg',
    'helleborus': 'helleborus.jpg',
    'roos': 'helleborus.jpg' # Per si el nom era 'Lenteroos...'
}

# Llista tots els JPGs source
files = glob.glob(os.path.join(source_dir, "*.*"))
for f in files:
    if f.lower().endswith(('.jpg', '.jpeg')):
        basename = os.path.basename(f)
        lower_name = basename.lower()
        
        # Mirem si coincideix amb alguna flor
        final_name = basename # Per defecte el mateix nom
        for search_key, target_name in rename_map.items():
            if search_key in lower_name:
                final_name = target_name
                break
        
        dest_path = os.path.join(dest_dir, final_name)
        
        try:
            shutil.copy2(f, dest_path)
            print(f"Copiat: {basename} -> {final_name}")
        except Exception as e:
            print(f"Error copiant {basename}: {e}")

print("Transferència completada. Contingut actual de IMG:")
print(os.listdir(dest_dir))
