import os, re

files = ['index.html', 'about.html', 'clients.html', 'contact.html', 'free-audit.html', 'privacy.html', 'services.html', 'terms.html']
out = open('d:\\Antigravity\\Alphanumero\\meta_output.txt', 'w', encoding='utf-8')
for fn in files:
    try:
        c = open('d:\\Antigravity\\Alphanumero\\'+fn, encoding='utf-8').read()
        t = re.search(r'<title>(.*?)</title>', c, re.I|re.S)
        m = re.search(r'<meta name="description" content="(.*?)"', c, re.I|re.S)
        title = t.group(1).strip() if t else 'MISSING'
        desc = m.group(1).strip() if m else 'MISSING'
        out.write(f"{fn}\n  Title: {title}\n  Desc: {desc}\n\n")
    except Exception as e:
        out.write(f"Error {fn}: {e}\n")
out.close()
print('Done')
