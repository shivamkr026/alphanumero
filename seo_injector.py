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
    "dayOfWeek": [
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday"
    ],
    "opens": "09:00",
    "closes": "18:00"
  },
  "sameAs": [
    "https://www.linkedin.com/company/numero-uno-marketing-india/"
  ]
}
</script>
"""

for filename in HTML_FILES:
    filepath = os.path.join('d:\\Antigravity\\Alphanumero', filename)
    if not os.path.exists(filepath): continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Extract Title and Description
    t_match = re.search(r'<title>(.*?)</title>', content, re.I | re.S)
    m_match = re.search(r'<meta name="description" content="(.*?)"', content, re.I | re.S)
    
    title = t_match.group(1).strip() if t_match else "Numero Uno Marketing"
    desc = m_match.group(1).strip() if m_match else "Digital Marketing Agency in Bangalore"
    
    # 2. Fix Canonical Link
    canonical_url = f"{BASE_URL}/" if filename == 'index.html' else f"{BASE_URL}/{filename}"
    canonical_tag_regex = r'<link\s+rel="canonical"\s+href="[^"]*"\s*/?>'
    new_canonical = f'<link rel="canonical" href="{canonical_url}">'
    
    if re.search(canonical_tag_regex, content, re.I):
        content = re.sub(canonical_tag_regex, new_canonical, content, flags=re.I)
    else:
        # If missing, put it right after meta description
        content = re.sub(r'(<meta name="description"[^>]*>)', r'\1\n  ' + new_canonical, content, flags=re.I)
        
    # 3. Inject Open Graph and Twitter Cards (if not already there)
    if 'og:title' not in content:
        og_tags = f'''
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">'''
        # Insert right after canonical link
        content = re.sub(r'(<link rel="canonical" href="[^"]*">)', r'\1' + og_tags, content, flags=re.I)
        
    # 4. Inject LocalBusiness Schema (only on index.html)
    if filename == 'index.html' and 'LocalBusiness Schema' not in content:
        content = re.sub(r'(</head>)', f'{LOCAL_BUSINESS_SCHEMA}\n\\1', content, flags=re.I)
        
    # 5. Add Alt tags to images missing it
    # Find all <img> tags
    def fix_img_alt(match):
        img_tag = match.group(0)
        # If no alt at all, or alt="", add default alt
        if 'alt="' not in img_tag.lower():
            # insert alt immediately after <img
            return img_tag[:4] + ' alt="Numero Uno Marketing Image"' + img_tag[4:]
        elif 'alt=""' in img_tag.lower():
            return re.sub(r'alt=""', 'alt="Numero Uno Marketing Visual"', img_tag, flags=re.I)
        return img_tag
    
    content = re.sub(r'<img\s+[^>]*>', fix_img_alt, content, flags=re.I)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("SEO tags injected successfully.")
