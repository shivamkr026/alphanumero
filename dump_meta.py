import os, re

files = ['index.html', 'about.html', 'clients.html', 'contact.html', 'free-audit.html', 'privacy.html', 'services.html', 'terms.html']
for fn in files:
    try:
        with open('d:\\Antigravity\\Alphanumero\\' + fn, 'r', encoding='utf-8') as f:
            c = f.read()
            t = re.search(r'<title>(.*?)</title>', c, re.I|re.S)
            m = re.search(r'<meta name="description" content="(.*?)"', c, re.I|re.S)
            title = t.group(1) if t else 'MISSING'
            desc = m.group(1) if m else 'MISSING'
            print(f"{fn}\n  Title: {title.strip()}\n  Desc: {desc.strip()}\n")
    except Exception as e:
        print(f"Error reading {fn}: {e}")
