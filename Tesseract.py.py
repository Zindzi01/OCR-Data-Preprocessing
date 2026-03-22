from pdf2image import convert_from_path
import pytesseract
import json
import os
import cv2
import numpy as np
from PIL import Image

# ==================================================
# CONFIGURATION
# ==================================================

#  Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Input / Output folders
INPUT_DIR = "Folder_Testpdfs"
OUTPUT_BASE_DIR = "output2_Folder_Testpdfs2"

OUTPUT_MD_DIR = os.path.join(OUTPUT_BASE_DIR, "md")
OUTPUT_JSON_DIR = os.path.join(OUTPUT_BASE_DIR, "json")

# Create output folders if they don't exist
os.makedirs(OUTPUT_MD_DIR, exist_ok=True)
os.makedirs(OUTPUT_JSON_DIR, exist_ok=True)

# ==================================================
# OCR SETTINGS (FOR FORMS)
# ==================================================
# ✔ Allows punctuation (.,)
# ✔ Blocks form line noise only
# ✔ PSM 4 works best for structured forms

OCR_CONFIG = "--oem 3 --psm 4 -c tessedit_char_blacklist=|—-"

# ==================================================
# IMAGE PREPROCESSING
# ==================================================
def preprocess(image):
    """
    Improve contrast and reduce noise for OCR.
    Keeps punctuation intact.
    """
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

    # Mild thresholding (do NOT over-process)
    img = cv2.threshold(
        img, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    return Image.fromarray(img)

# ==================================================
# PROCESS ALL PDFs IN INPUT FOLDER
# ==================================================
for filename in os.listdir(INPUT_DIR):
    if not filename.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(INPUT_DIR, filename)
    base_name = os.path.splitext(filename)[0]

    print(f" Processing: {filename}")

    images = convert_from_path(pdf_path, dpi=300)

    pages = []

    for i, image in enumerate(images):
        processed_image = preprocess(image)

        text = pytesseract.image_to_string(
            processed_image,
            config=OCR_CONFIG
        )

        # Clean empty lines
        text = "\n".join(
            line.strip()
            for line in text.splitlines()
            if line.strip()
        )

        pages.append({
            "page": i + 1,
            "text": text
        })

    # ==================================================
    # SAVE MARKDOWN OUTPUT
    # ==================================================
    md_path = os.path.join(OUTPUT_MD_DIR, f"{base_name}.md")
    with open(md_path, "w", encoding="utf-8") as md_file:
        md_file.write(f"# OCR Output — {filename}\n\n")
        for page in pages:
            md_file.write(f"## Page {page['page']}\n\n")
            md_file.write(page["text"] + "\n\n")

    # ==================================================
    # SAVE JSON OUTPUT
    # ==================================================
    json_path = os.path.join(OUTPUT_JSON_DIR, f"{base_name}.json")
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(
            {
                "source_file": filename,
                "total_pages": len(pages),
                "pages": pages
            },
            json_file,
            indent=2,
            ensure_ascii=False
        )

    print(f" Finished: {filename}")

print(" All PDFs processed successfully")
