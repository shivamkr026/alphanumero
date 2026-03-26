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

GOOGLE_ICON = '<a href="#" title="Review us on Google"><svg width="20" height="20" viewBox="0 0 24 24" fill="#DB4437"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg></a>'

for filename in HTML_FILES:
    filepath = os.path.join('d:\\Antigravity\\Alphanumero', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean old tags to avoid duplicates
    # Remove existing canonical links
    content = re.sub(r'<link\s+rel="canonical"[^>]*>', '', content, flags=re.I)
    # Remove existing og tags
    content = re.sub(r'<meta\s+(?:property|name)="(?:og|twitter):[^"]+"\s+content="[^"]*"\s*/?>', '', content, flags=re.I)
    # Remove older injected block
    content = re.sub(r'<!-- SEO & Social Tags -->', '', content, flags=re.I)
    content = re.sub(r'<!-- LocalBusiness Schema -->.*?</script>', '', content, flags=re.I|re.S)

    # 2. Extract Title and Description cleanly
    t_match = re.search(r'<title>(.*?)</title>', content, re.I | re.S)
    m_match = re.search(r'<meta name="description"\s+content="(.*?)"', content, re.I | re.S)
    
    title = t_match.group(1).strip() if t_match else "Numero Uno Marketing"
    desc = m_match.group(1).strip() if m_match else "Digital Marketing Agency in Bangalore"
    
    title = title.replace('\\n', ' ').replace('\\r', ' ').strip()
    title = title.replace('"', '&quot;')
    desc = desc.replace('\\n', ' ').replace('\\r', ' ').strip()
    desc = desc.replace('"', '&quot;')

    # 3. Create canonical and OG block
    canonical_url = f"{BASE_URL}/" if filename == 'index.html' else f"{BASE_URL}/{filename}"
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

    # Optional local business schema insertion
    if filename == 'index.html':
        og_tags += LOCAL_BUSINESS_SCHEMA + "\n"

    # Inject safely before the FIRST </head>
    # Split by </head>
    head_parts = re.split(r'</head>', content, maxsplit=1, flags=re.I)
    if len(head_parts) > 1:
        content = head_parts[0] + og_tags + "</head>" + head_parts[1]
        
    # 4. Integrate Google Business Profile icon into footer.
    # We look for the LinkedIn / Facebook social icon block and append it if not there.
    if 'Review us on Google' not in content:
        # Look for the last social link before closing div
        social_link_pattern = r'(<a href="https://www\.linkedin\.com/company/[^"]*".*?</a>)'
        if re.search(social_link_pattern, content):
            content = re.sub(social_link_pattern, r'\1\n        ' + GOOGLE_ICON, content, flags=re.I)

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("SEO tags cleaned and injected correctly.")
