import os, re

HTML_FILES = ['index.html', 'about.html', 'clients.html', 'contact.html', 'free-audit.html', 'privacy.html', 'services.html', 'terms.html']

for filename in HTML_FILES:
    filepath = os.path.join('d:\\Antigravity\\Alphanumero', filename)
    if not os.path.exists(filepath): continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The exact regex to kill the Google icon div/a
    content = re.sub(r'\n?\s*<a href="#" title="Review us on Google">.*?</a>', '', content, flags=re.S|re.I)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print('Google review link removed from all pages.')
