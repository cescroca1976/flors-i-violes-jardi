import os
import re
import json

# Configura les rutes
md_path = r'C:\Users\froca\.gemini\antigravity\brain\7ed35962-f64e-49f5-9c88-cb6afd678662\pla_jardineria_palautordera_fixed.md'
html_path = r'C:\Users\froca\Desktop\jardi_palautordera_dashboard.html'

def generate_dashboard():
    if not os.path.exists(md_path):
        print("Error: No es troba el fitxer Markdown.")
        return

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Estructura de dades per zones
    zones = []
    current_zone = None
    
    # Dividir per zones
    sections = re.split(r'## ZONA ', content)
    
    for section in sections[1:]: # Ignorar el pròleg
        lines = section.split('\n')
        zone_header = lines[0].strip()
        zone_title = "ZONA " + zone_header
        
        # Extreure flors d'aquesta zona
        flowers = []
        flower_blocks = re.split(r'### \d+\. ', section)
        
        for block in flower_blocks[1:]:
            block_lines = block.split('\n')
            name = block_lines[0].strip()
            
            # Descripció (linia següent)
            desc = ""
            amazon = "#"
            images = []
            
            for line in block_lines[1:]:
                line = line.strip()
                if line.startswith('*   **Amazon:**') or line.startswith('* **Amazon:**'):
                    amazon_match = re.search(r'\[.*?\]\((.*?)\)', line)
                    if amazon_match:
                        amazon = amazon_match.group(1)
                elif line.startswith('![') and '](' in line:
                    img_match = re.search(r'!\[.*?\]\((.*?)\)', line)
                    if img_match:
                        images.append(img_match.group(1))
                elif line and not line.startswith('*') and not line.startswith('---'):
                    if not desc: desc = line
            
            flowers.append({
                "name": name,
                "desc": desc,
                "amazon": amazon,
                "images": images[:3]
            })
            
        zones.append({
            "title": zone_title,
            "flowers": flowers
        })

    # Generar HTML
    html_template = f"""
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="referrer" content="no-referrer">
    <title>Dashboard Jardí Palautordera</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #2d5a27;
            --accent: #e67e22;
            --bg: #f4f7f6;
            --card: #ffffff;
            --text: #333;
        }}
        body {{
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 0;
        }}
        header {{
            background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1466692476868-aef1dfb1e735?auto=format&fit=crop&w=1200&q=80');
            background-size: cover;
            background-position: center;
            color: white;
            text-align: center;
            padding: 60px 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .zone-section {{
            margin-bottom: 50px;
        }}
        .zone-title {{
            border-bottom: 3px solid var(--primary);
            padding-bottom: 10px;
            margin-bottom: 30px;
            color: var(--primary);
            font-size: 2em;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 25px;
        }}
        .flower-card {{
            background: var(--card);
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 20px rgba(0,0,0,0.05);
            transition: transform 0.3s ease;
            display: flex;
            flex-direction: column;
        }}
        .flower-card:hover {{
            transform: translateY(-5px);
        }}
        .image-container {{
            position: relative;
            height: 200px;
            display: flex;
            overflow-x: auto;
            scroll-snap-type: x mandatory;
            background: #eee;
        }}
        .image-container img {{
            height: 100%;
            min-width: 100%;
            object-fit: cover;
            scroll-snap-align: start;
        }}
        .content {{
            padding: 20px;
            flex-grow: 1;
        }}
        .content h3 {{
            margin: 0 0 10px 0;
            color: var(--primary);
        }}
        .content p {{
            font-size: 0.9em;
            color: #666;
            height: 40px;
            overflow: hidden;
        }}
        .buy-btn {{
            display: block;
            background: var(--primary);
            color: white;
            text-align: center;
            text-decoration: none;
            padding: 12px;
            margin: 0 20px 20px 20px;
            border-radius: 8px;
            font-weight: 600;
            transition: background 0.3s;
        }}
        .buy-btn:hover {{
            background: #1e3f1b;
        }}
        .nav-sticky {{
            position: sticky;
            top: 0;
            background: white;
            padding: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 100;
            text-align: center;
        }}
        .nav-sticky a {{
            margin: 0 10px;
            text-decoration: none;
            color: var(--primary);
            font-weight: 600;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <header>
        <h1>Jardí de Santa Maria de Palautordera</h1>
        <p>Proposta de 125 Varietats de Flors per a Primavera</p>
    </header>

    <div class="nav-sticky">
        {"".join([f'<a href="#zone{i}">{z["title"].split(":")[0]}</a>' for i, z in enumerate(zones)])}
    </div>

    <div class="container">
        {"".join([f'''
        <div class="zone-section" id="zone{i}">
            <h2 class="zone-title">{z["title"]}</h2>
            <div class="grid">
                {"".join([f'''
                <div class="flower-card">
                    <div class="image-container">
                        {"".join([f'<img src="{img}" alt="{f["name"]}" loading="lazy">' for img in f["images"]])}
                    </div>
                    <div class="content">
                        <h3>{f["name"]}</h3>
                        <p>{f["desc"]}</p>
                    </div>
                    <a href="{f["amazon"]}" target="_blank" class="buy-btn">Comprar a Amazon</a>
                </div>
                ''' for f in z["flowers"]])}
            </div>
        </div>
        ''' for i, z in enumerate(zones)])}
    </div>
</body>
</html>
    """

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"Dashboard generat a: {html_path}")

if __name__ == "__main__":
    generate_dashboard()
