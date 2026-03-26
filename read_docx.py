import zipfile
import xml.etree.ElementTree as ET

def extract_text(docx_path):
    z = zipfile.ZipFile(docx_path)
    xml_content = z.read('word/document.xml')
    tree = ET.fromstring(xml_content)
    namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    text = '\n'.join([node.text for node in tree.iterfind('.//w:t', namespace) if node.text])
    with open('d:\\Antigravity\\Alphanumero\\public\\seo_report.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Done")

if __name__ == '__main__':
    extract_text('d:\\Antigravity\\Alphanumero\\public\\Detailed plan.docx')
