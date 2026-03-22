import easyocr
from pdf2image import convert_from_path, pdfinfo_from_path
import os
import numpy as np
import cv2
import json

POPPLER_PATH = r"C:\Users\..."
INPUT_DIR = ""input_pdfs
OUTPUT_DIR = "output_Tpdfs"
CONFIDENCE_THRESHOLD = 0.5

os.makedirs(OUTPUT_DIR, exist_ok=True)

reader = easyocr.Reader(['en'], gpu=False)

pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]

for pdf_file in pdf_files:
    pdf_path = os.path.join(INPUT_DIR, pdf_file)
    base_name = pdf_file.replace(".pdf", "")
    md_path = os.path.join(OUTPUT_DIR, f"{base_name}.md")
    json_path = os.path.join(OUTPUT_DIR, f"{base_name}.json")

    print(f"\n Processing: {pdf_file}")

    info = pdfinfo_from_path(pdf_path, poppler_path=POPPLER_PATH)
    num_pages = info["Pages"]

    document_json = {
        "file": pdf_file,
        "pages": []
    }

    with open(md_path, "w", encoding="utf-8") as md_file:
        md_file.write(f"# OCR Output: {pdf_file}\n\n")

        for page_num in range(1, num_pages + 1):
            print(f"   Page {page_num}")

            images = convert_from_path(
                pdf_path,
                dpi=300,
                first_page=page_num,
                last_page=page_num,
                poppler_path=POPPLER_PATH
            )

            image = images[0]
            image_np = np.array(image)
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

            results = reader.readtext(image_np)

            page_data = {
                "page": page_num,
                "text": []
            }

            md_file.write(f"## Page {page_num}\n\n")

            for _, text, confidence in results:
                if confidence >= CONFIDENCE_THRESHOLD:
                    md_file.write(f"- {text}\n")
                    page_data["text"].append({
                        "content": text,
                        "confidence": round(confidence, 3)
                    })

            md_file.write("\n")
            document_json["pages"].append(page_data)

    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(document_json, jf, indent=2, ensure_ascii=False)

    print(f" Saved: {md_path}")
    print(f" Saved: {json_path}")

print("\n All documents processed.")
