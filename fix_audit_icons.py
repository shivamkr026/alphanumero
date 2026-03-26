import os, re

filepath = 'd:\\Antigravity\\Alphanumero\\free-audit.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# The aggressive WhatsApp SVG that was injected
WA_SVG_REGEX = r'<svg\s+width="20"\s+height="20"\s+viewBox="0\s+0\s+448\s+512"\s+fill="#25D366">\s*<path[^>]*>\s*</svg>'

# Correct SVGs
IG_SVG = '<svg width="18" height="18" viewBox="0 0 448 512" fill="currentColor"><path d="M224.1 141c-63.6 0-114.9 51.3-114.9 114.9s51.3 114.9 114.9 114.9S339 319.5 339 255.9 287.7 141 224.1 141zm0 189.6c-41.1 0-74.7-33.5-74.7-74.7s33.5-74.7 74.7-74.7 74.7 33.5 74.7 74.7-33.6 74.7-74.7 74.7zm146.4-194.3c0 14.9-12 26.8-26.8 26.8-14.9 0-26.8-12-26.8-26.8s12-26.8 26.8-26.8 26.8 12 26.8 26.8zm76.1 27.2c-1.7-35.9-9.9-67.7-36.2-93.9-26.2-26.2-58-34.4-93.9-36.2-37-2.1-147.9-2.1-184.9 0-35.8 1.7-67.6 9.9-93.9 36.1s-34.4 58-36.2 93.9c-2.1 37-2.1 147.9 0 184.9 1.7 35.9 9.9 67.7 36.2 93.9s58 34.4 93.9 36.2c37 2.1 147.9 2.1 184.9 0 35.9-1.7 67.7-9.9 93.9-36.2 26.2-26.2 34.4-58 36.2-93.9 2.1-37 2.1-147.8 0-184.8zM398.8 388c-7.8 19.6-22.9 34.7-42.6 42.6-29.5 11.7-99.5 9-132.1 9s-102.7 2.6-132.1-9c-19.6-7.8-34.7-22.9-42.6-42.6-11.7-29.5-9-99.5-9-132.1s-2.6-102.7 9-132.1c7.8-19.6 22.9-34.7 42.6-42.6 29.5-11.7 99.5-9 132.1-9s102.7-2.6 132.1 9c19.6 7.8 34.7 22.9 42.6 42.6 11.7 29.5 9 99.5 9 132.1s2.7 102.7-9 132.1z"/></svg>'
FB_SVG = '<svg width="18" height="18" viewBox="0 0 320 512" fill="currentColor"><path d="M279.14 288l14.22-92.66h-88.91v-60.13c0-25.35 12.42-50.06 52.24-50.06h40.42V6.26S260.43 0 225.36 0c-73.22 0-121.08 44.38-121.08 124.72v70.62H22.89V288h81.39v224h100.17V288z"/></svg>'
MAP_SVG = '<svg width="18" height="18" viewBox="0 0 384 512" fill="currentColor"><path d="M215.7 499.2C267 435 384 279.4 384 192C384 86 298 0 192 0S0 86 0 192c0 87.4 117 243 168.3 307.2c12.3 15.3 35.1 15.3 47.4 0zM192 128a64 64 0 1 1 0 128 64 64 0 1 1 0-128z"/></svg>'
GLOBE_SVG = '<svg width="18" height="18" viewBox="0 0 512 512" fill="currentColor"><path d="M352 256c0 22.2-1.2 43.6-3.3 64H163.3c-2.2-20.4-3.3-41.8-3.3-64s1.2-43.6 3.3-64h185.4c2.2 20.4 3.3 41.8 3.3 64zm28.8-64H503.9c5.3 20.5 8.1 41.9 8.1 64s-2.8 43.5-8.1 64H380.8c2.1-20.6 3.2-42 3.2-64s-1.1-43.4-3.2-64zm112.6-32H376.7c-10-63.9-29.8-117.4-55.3-151.6c78.3 20.7 142 77.5 171.9 151.6zm-149.1 0H167.7c6.1-36.4 15.5-68.6 27-94.7c10.5-23.6 22.2-40.7 33.5-51.5C239.4 3.2 248.7 0 256 0s16.6 3.2 27.8 11.8c11.3 10.8 23 27.9 33.5 51.5c11.6 26.1 20.9 58.3 27 94.7zm-209 0H18.6C48.6 85.9 112.2 29.1 190.6 8.4C165.1 42.6 145.3 96.1 135.3 160zM8.1 192H131.2c-2.1 20.6-3.2 42-3.2 64s1.1 43.4 3.2 64H8.1C2.8 299.5 0 278.1 0 256s2.8-43.5 8.1-64zM194.7 446.6c-11.6-26.1-20.9-58.3-27-94.6H376.7c-6.1 36.4-15.5 68.6-27 94.6c-10.5 23.6-22.2 40.7-33.5 51.5C305.1 508.8 295.8 512 288 512s-17.1-3.2-28.3-11.8c-11.3-10.8-23-27.9-33.5-51.5zM135.3 352c10 63.9 29.8 117.4 55.3 151.6C112.2 482.9 48.6 426.1 18.6 352H135.3zm358.1 0c-30 74.1-93.6 130.9-171.9 151.6c25.5-34.2 45.2-87.7 55.3-151.6H493.4z"/></svg>'

# Target block replacers
def replace_ig_icon(match):
    m = match.group(0)
    return re.sub(WA_SVG_REGEX, IG_SVG, m, flags=re.I)

def replace_fb_icon(match):
    m = match.group(0)
    return re.sub(WA_SVG_REGEX, FB_SVG, m, flags=re.I)

def replace_google_icon(match):
    m = match.group(0)
    return re.sub(WA_SVG_REGEX, MAP_SVG, m, flags=re.I)

def replace_web_icon(match):
    m = match.group(0)
    return re.sub(WA_SVG_REGEX, GLOBE_SVG, m, flags=re.I)

# Update form field labels
content = re.sub(r'<label class="flbl">.*?Instagram handle</label>', replace_ig_icon, content, flags=re.I|re.S)
content = re.sub(r'<label class="flbl">.*?Facebook page</label>', replace_fb_icon, content, flags=re.I|re.S)
content = re.sub(r'<label class="flbl">.*?Google Business / Maps listing</label>', replace_google_icon, content, flags=re.I|re.S)
content = re.sub(r'<label class="flbl">.*?Website URL</label>', replace_web_icon, content, flags=re.I|re.S)

# Update the diagram bubbles (Google: 8 reviews, IG: 342 followers, No WhatsApp stays as WhatsApp but color can be set to gray or text inherited)
def fix_bubble(match):
    text = match.group(0)
    if 'IG:' in text: return re.sub(WA_SVG_REGEX, IG_SVG, text, flags=re.I)
    if 'Google:' in text: return re.sub(WA_SVG_REGEX, MAP_SVG, text, flags=re.I)
    return text

content = re.sub(r'<div class="dia-bl.*?>.*?</div>', fix_bubble, content, flags=re.I|re.S)

# Also clean up the WhatsApp bubble text "No WhatsApp" so that the WhatsApp SVG inherits color to make it look red/gray instead of green if it was styled
content = re.sub(r'(<div class="dia-bl dia-red">)\s*' + WA_SVG_REGEX, r'\1<svg width="14" height="14" viewBox="0 0 448 512" fill="currentColor"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-5.5-2.8-23.2-8.5-44.2-27.1-16.4-14.6-27.4-32.7-30.6-38.1-3.2-5.4-.3-8.3 2.4-11.1 2.4-2.5 5.5-6.5 8.3-9.7 2.8-3.3 3.7-5.5 5.5-9.3.1-3.7-.8-6.9-1.9-9.7-1.1-2.8-9.8-23.6-13.4-32.4-3.5-8.6-7.1-7.4-9.8-7.5-2.5-.1-5.4-.1-8.3-.1s-7.5 1.1-11.5 5.5c-4 4.4-15.4 15.1-15.4 36.8s15.8 42.8 18 45.7c2.2 2.8 31.1 47.4 75.3 66.5 10.5 4.5 18.8 7.3 25.2 9.3 10.6 3.4 20.2 2.9 27.8 1.7 8.5-1.3 26.2-10.7 30-21.1 3.7-10.3 3.7-19.2 2.5-21.1-1.1-1.9-4.2-2.8-9.7-5.5z"/></svg>', content, flags=re.I|re.S)

# Wait, `free-audit.html` is the only one affected!
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Icons restored safely on free-audit.html.")
