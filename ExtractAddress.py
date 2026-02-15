from pdfminer.pdfpage import PDFPage
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LAParams
imporot re

file_path = "input.pdf"

def count_pdf_pages(file_path):
    with open(file_path, 'rb') as f:
        page_count = sum(1 for _ in PDFPage.get_pages(f))
    return page_count

def remove_internal_repetition(text):
    if not text: return text
    n = len(text)
    if n % 2 == 0:
        mid = n // 2
        if text[:mid] == text[mid:]:
            return text[:mid]
    return text

def get_title_block_list(file_path, page_numbers):
    params = LAParams(char_margin=10.0, line_margin=0.1)
    title_block_data = []
    for page_layout in extract_pages(file_path, page_numbers=page_numbers, laparams=params):
        page_height = page_layout.height
        bottom_threshold = page_height * 0.2 
        # sort by vertex
        elements = sorted(page_layout, key=lambda e: (e.x0, -e.y1))
        seen_texts = set()
        for element in elements:
            if isinstance(element, LTTextContainer):
                if element.y0 > bottom_threshold:
                    continue
                raw_text = element.get_text()
                clean_text = remove_internal_repetition(raw_text)
                if clean_text and clean_text not in seen_texts:
                    title_block_data.append(clean_text)
                    seen_texts.add(clean_text)
    return title_block_data

def extract_address(lines):
    text = next((line for line in lines if "住居表示" in line or "住所" in line), "")
    match = re.search(r'(?:住居表示|住所)：(.*?)(?=\n)', text, re.DOTALL)
    if match:
        raw_address = match.group(1)
        clean_address = re.sub(r'〒?\d{3}-\d{4}', '', raw_address)
        clean_address = re.sub(r'[\s\u3000]+', '', clean_address)
        return clean_address
    return None

pagenum = count_pdf_pages(file_path)
data = []
for i in range(pagenum):
    data.append(get_title_block_list(file_path, [i]))

for d in data:
    print(extract_address(d))

