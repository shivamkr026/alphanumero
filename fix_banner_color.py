import os, re

HTML_FILES = ['index.html', 'about.html', 'clients.html', 'contact.html', 'free-audit.html', 'privacy.html', 'services.html', 'terms.html']

for filename in HTML_FILES:
    filepath = os.path.join('d:\\Antigravity\\Alphanumero', filename)
    if not os.path.exists(filepath): continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Safely inject the variable if it's not actually DEFINED
    if '--yellow:' not in content and '--yellow:#FFD600' not in content:
        content = re.sub(r'(--lime2:#8EB69B;)', r'\1--yellow:#FFD600;', content, count=1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print('Banner variable --yellow fixed successfully.')
