import os
import random
import fitz

INPUT_FOLDER = "input_files"
SAMPLE_SIZE = 10
IMAGE_AREA_THRESHOLD = 0.7
TEXT_CHAR_THRESHOLD = 30

def is_page_image_dominated(page, threshold):
    rect = page.rect
    page_area = rect.width * rect.height
    data = page.get_text("dict")
    for b in data["blocks"]:
        if b["type"] == 1:
            x0, y0, x1, y1 = b["bbox"]
            if (x1 - x0) * (y1 - y0) / page_area >= threshold:
                return True
    return False

def page_has_text(page, char_threshold):
    txt = page.get_text()
    return len(txt.strip()) > char_threshold

def evaluate_pdf(path):
    doc = fitz.open(path)
    n = doc.page_count
    if n <= SAMPLE_SIZE:
        pages = list(range(n))
    else:
        start, end = n // 4, n * 3 // 4
        pages = random.sample(range(start, end), SAMPLE_SIZE)
    image_pages = 0
    text_pages = 0
    for pno in pages:
        page = doc[pno]
        if is_page_image_dominated(page, IMAGE_AREA_THRESHOLD):
            image_pages += 1
        if page_has_text(page, TEXT_CHAR_THRESHOLD):
            text_pages += 1
    marker = ""
    if image_pages <= SAMPLE_SIZE // 2:
        verdict = "text‑based"
    else:
        if text_pages < 2:
            verdict = "image‑only"
            marker = "*"
        else:
            verdict = "image‑with‑text"
    print(f"{marker}{os.path.basename(path)[:20]}: {verdict} "
          f"({image_pages}/{len(pages)} image‑dominated, "
          f"{text_pages}/{len(pages)} with text)")

def main():
    for fn in os.listdir(INPUT_FOLDER):
        if fn.lower().endswith(".pdf"):
            evaluate_pdf(os.path.join(INPUT_FOLDER, fn))

if __name__ == "__main__":
    main()

