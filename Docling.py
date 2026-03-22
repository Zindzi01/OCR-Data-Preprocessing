"""
Docling PDF Text Extraction 

"""
from docling.document_converter import DocumentConverter
from pathlib import Path

# -------------------------
# Paths
# -------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
INPUT_PDF_DIR = PROJECT_ROOT / "input_pdfs"
OUTPUT_MD_DIR = PROJECT_ROOT / "output_md"
OUTPUT_MD_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------
# Initialize Docling
# -------------------------
converter = DocumentConverter()

# -------------------------
# Process PDFs
# -------------------------
for pdf_path in INPUT_PDF_DIR.glob("*.pdf"):
    print(f"Processing: {pdf_path.name}")

    # Convert PDF
    result = converter.convert(str(pdf_path))
    document = result.document

    # Export Markdown
    markdown = document.export_to_markdown()
    md_file = OUTPUT_MD_DIR / f"{pdf_path.stem}.md"
    md_file.write_text(markdown, encoding="utf-8")

    print(f" Markdown saved: {md_file.name}")

print("\n All PDFs processed successfully!")
