import os, re

HTML_FILES = ['index.html', 'about.html', 'clients.html', 'contact.html', 'free-audit.html', 'privacy.html', 'services.html', 'terms.html']

tablet_media_query = """
@media(max-width:1024px){
  .footer-grid{grid-template-columns:1fr 1fr;gap:40px}
}
"""

for filename in HTML_FILES:
    filepath = os.path.join('d:\\Antigravity\\Alphanumero', filename)
    if not os.path.exists(filepath): continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Append the media query right before the closing </style> tag
    if '@media(max-width:1024px){\n  .footer-grid' not in content:
        content = re.sub(r'</style>', f'{tablet_media_query}</style>', content, flags=re.I)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Footer tablet responsiveness added globally.")
