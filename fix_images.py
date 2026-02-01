import os
import re
import requests
import time

# Configura les rutes
md_path = r'C:\Users\froca\.gemini\antigravity\brain\7ed35962-f64e-49f5-9c88-cb6afd678662\pla_jardineria_palautordera.md'
fixed_md_path = r'C:\Users\froca\.gemini\antigravity\brain\7ed35962-f64e-49f5-9c88-cb6afd678662\pla_jardineria_palautordera_fixed.md'

def get_wikimedia_images(flower_name, limit=3):
    headers = {'User-Agent': 'GardenPlannerFixer/1.0 (contact: info@example.com)'}
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": f"{flower_name} flower",
        "gsrnamespace": 6,
        "gsrlimit": limit,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }
    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        urls = []
        for page_id in pages:
            info = pages[page_id].get("imageinfo", [{}])[0]
            if "url" in info:
                urls.append(info["url"])
        return urls
    except Exception as e:
        print(f"Error buscant {flower_name}: {e}")
        return []

def fix_markdown():
    if not os.path.exists(md_path):
        print("Error: fitxer MD no trobat.")
        return

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Dividir el fitxer per flors (###)
    parts = re.split(r'(### \d+\. .*?\n)', content)
    new_content = parts[0]
    
    flower_count = 0
    for i in range(1, len(parts), 2):
        header = parts[i]
        body = parts[i+1]
        
        # Extreure el nom del header
        name_match = re.search(r'### \d+\. (.*?) \((.*?)\)', header)
        if not name_match:
             # Provar format sense parèntesis
             name_match = re.search(r'### \d+\. (.*)', header)
        
        if name_match:
            flower_name = name_match.group(1).strip()
            scientific_name = name_match.group(2).strip() if len(name_match.groups()) > 1 else flower_name
            
            print(f"Fixant {flower_name} ({flower_count+1}/125)...")
            # Buscar noves imatges
            new_imgs = get_wikimedia_images(scientific_name)
            if not new_imgs: # Reintentar amb el nom comú si el científic falla
                 new_imgs = get_wikimedia_images(flower_name)
            
            # Reemplaçar les imatges antigues en el body
            # Busquem el bloc d'imatges: ![desc](url)
            old_img_pattern = r'!\[.*?\]\(.*?\)'
            
            if new_imgs:
                img_markdown = "\n".join([f"![{flower_name} {idx+1}]({url})" for idx, url in enumerate(new_imgs)])
                # Substituïm TOTES les imatges velles d'aquest bloc per les noves
                body_no_imgs = re.sub(old_img_pattern, "", body)
                # Afegim les noves al final del bloc d'imatges o després d'Amazon
                if "Imatges:" in body_no_imgs:
                    new_body = body_no_imgs.replace("Imatges:", f"Imatges:\n{img_markdown}")
                else:
                    new_body = body_no_imgs + f"\n*   **Imatges:**\n{img_markdown}\n"
            else:
                new_body = body
            
            new_content += header + new_body
            flower_count += 1
            time.sleep(0.1) # Respectar l'API
        else:
            new_content += header + body

    with open(fixed_md_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"FET! Markdown fixat a: {fixed_md_path}")

if __name__ == "__main__":
    fix_markdown()
