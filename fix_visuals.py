import os, re

HTML_FILES = ['index.html', 'about.html', 'clients.html', 'contact.html', 'free-audit.html', 'privacy.html', 'services.html', 'terms.html']

for filename in HTML_FILES:
    filepath = os.path.join('d:\\Antigravity\\Alphanumero', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix `--yellow` variable in :root across all files
    # Check if --yellow is missing in :root, and add it
    if '--yellow' not in content:
        content = re.sub(r'(--lime2:#8EB69B;)', r'\1--yellow:#FFD600;', content, count=1)
    
    # 2. Add color:#fff to .wa-float just in case to enable currentColor or pure white
    if '.wa-float{' in content and 'color:#fff' not in content:
        content = re.sub(r'(\.wa-float\{[^}]*?)(?=})', r'\1;color:#fff', content)

    # 3. Replace fill="#25D366" in all SVGs inside certain green-background anchor tags with fill="#FFFFFF"
    
    def fix_white_svg(match):
        # match.group() is the whole <a> tag containing wa-float, side-tab-wa, or smb-wa
        a_tag = match.group(0)
        return re.sub(r'fill="#25D366"', 'fill="#FFFFFF"', a_tag, flags=re.I)
        
    # Match anchor tags that have those specific classes and contain an SVG
    # Using regex to target the anchor blocks
    content = re.sub(r'<a[^>]*?class="[^"]*(wa-float|side-tab-wa|smb-wa)[^"]*"[^>]*>.*?</a>', fix_white_svg, content, flags=re.I | re.S)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Visuals fixed successfully.")
