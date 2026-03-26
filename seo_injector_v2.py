import os, re

HTML_FILES = ['index.html', 'about.html', 'clients.html', 'contact.html', 'free-audit.html', 'privacy.html', 'services.html', 'terms.html']
BASE_URL = "https://alphanumerouno.in"

LOCAL_BUSINESS_SCHEMA = """
<!-- LocalBusiness Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Numero Uno Marketing Pvt. Ltd.",
  "image": "https://alphanumerouno.in/public/logo.png",
  "@id": "https://alphanumerouno.in/",
  "url": "https://alphanumerouno.in/",
  "telephone": "+919632091371",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "No.63, Katha No.6, Agara, Thataguni",
    "addressLocality": "Bangalore",
    "postalCode": "560082",
    "addressCountry": "IN"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 12.836,
    "longitude": 77.521
  },
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    "opens": "09:00",
    "closes": "18:00"
  },
  "sameAs": ["https://www.linkedin.com/company/numero-uno-marketing-india/"]
}
</script>
"""

for filename in HTML_FILES:
    filepath = os.path.join('d:\\Antigravity\\Alphanumero', filepath) if not os.path.exists(filename) else filename
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Extract Title and Description safely
    t_match = re.search(r'<title>(.*?)</title>', content, re.I | re.S)
    m_match = re.search(r'<meta name="description"\s+content="(.*?)"', content, re.I | re.S)
    
    title = t_match.group(1).strip() if t_match else "Numero Uno Marketing"
    desc = m_match.group(1).strip() if m_match else "Digital Marketing Agency in Bangalore"
    
    # Clean possible newlines from title and desc
    title = title.replace('\\n', ' ').replace('\\r', ' ').strip()
    desc = desc.replace('\\n', ' ').replace('\\r', ' ').strip()
    
    # 2. Fix Canonical Link
    canonical_url = f"{BASE_URL}/" if filename == 'index.html' else f"{BASE_URL}/{filename}"
    canonical_tag_regex = r'<link\s+rel="canonical"\s+href="[^"]*"\s*/?>'
    
    if re.search(canonical_tag_regex, content, re.I):
        # Remove old canonical to append a clean new one later
        content = re.sub(canonical_tag_regex, '', content, flags=re.I)
        
    og_tags = f'''
  <!-- SEO & Social Tags -->
  <link rel="canonical" href="{canonical_url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
'''
    
    # Remove existing SEO block if script is run multiple times
    content = re.sub(r'<!-- SEO & Social Tags -->.*?<meta name="twitter:description"[^>]*>', '', content, flags=re.I|re.S)

    # Insert tags before </head>
    content = re.sub(r'</head>', og_tags + '</head>', content, flags=re.I)
        
    # 3. Inject LocalBusiness Schema (only on index.html)
    if filename == 'index.html':
        content = re.sub(r'<!-- LocalBusiness Schema -->.*?</script>', '', content, flags=re.I|re.S)
        content = re.sub(r'</head>', LOCAL_BUSINESS_SCHEMA + '</head>', content, flags=re.I)
        
    # 4. Add Alt tags to images missing it
    def fix_img_alt(match):
        img_tag = match.group(0)
        if 'alt=' not in img_tag.lower():
            # insert alt immediately after <img
            return img_tag[:4] + ' alt="Numero Uno Marketing"' + img_tag[4:]
        elif 'alt=""' in img_tag.lower():
            return re.sub(r'alt=""', 'alt="Numero Uno Marketing Visual"', img_tag, flags=re.I)
        return img_tag
    
    content = re.sub(r'<img\s+[^>]*>', fix_img_alt, content, flags=re.I)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("SEO tags injected successfully (V2).")
