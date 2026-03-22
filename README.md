# PDF Text Extraction & OCR Pipeline

## Overview
This project provides multiple approaches for extracting text from PDF documents using both structured parsing and OCR techniques. It is designed for document preprocessing workflows such as Retrieval-Augmented Generation (RAG), data pipelines, and information extraction systems.

The project includes three main scripts:

- `docling.py` – Structured PDF parsing using Docling
- `tesseract.py` – OCR-based extraction using Tesseract
- `easyocr.py` – OCR-based extraction using EasyOCR

Each script processes PDFs and outputs text in Markdown and/or JSON formats.

---

## Project Structure



project_root/

│

├── input_folder/ # Input PDFs for all scripts

│

├── output_folder/ # Rename or organize outputs here

│

├── docling.py

├── tesseract.py

├── easyocr.py

└── README.md

---

## Important Setup Note

Before running the scripts, ensure:

- All input directories are renamed to: `input_folder`
- All output directories are renamed to: `output_folder`

If your scripts still reference older folder names, update them accordingly or rename your folders to match.

---

## 1. Docling Pipeline (`docling.py`)

### Description
Uses Docling's document parser to extract structured text directly from PDFs without OCR.

### Features
- Preserves document structure  
- Outputs clean Markdown  
- Fast for machine-readable PDFs  

### Input
- Folder: `input_folder/`

### Output
- Markdown files saved to your configured `output_folder/`

### Workflow
1. Load PDFs from input folder  
2. Convert using Docling  
3. Export structured text to Markdown  

---

## 2. Tesseract OCR Pipeline (`tesseract.py`)

### Description
Uses Tesseract OCR to extract text from scanned PDFs by converting pages into images.

### Features
- Image preprocessing using OpenCV  
- Optimized for structured forms  
- Outputs both Markdown and JSON  
- Page-level text extraction  

### Requirements
- Tesseract OCR installed  
- Path configured:
pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\tesseract.exe"

### Input
- Folder: `input_folder/`

### Output
- Markdown and JSON saved to your configured `output_folder/`

### Workflow
1. Convert PDF pages to images (300 DPI)  
2. Preprocess images (grayscale + thresholding)  
3. Extract text using Tesseract  
4. Clean and structure output  
5. Save as Markdown and JSON  

---

## 3. EasyOCR Pipeline (`easyocr.py`)

### Description
Uses EasyOCR for deep learning-based text extraction from PDFs.

### Features
- Confidence-based filtering  
- Outputs structured JSON with confidence scores  
- Good for complex or low-quality scans  

### Requirements
- Poppler installed (for PDF rendering)  
- Path configured:
  POPPLER_PATH = "C:\Users\..."

### Input
- Folder: `input_folder/`

### Output
- Markdown and JSON saved to your configured `output_folder/`

### Workflow
1. Detect number of pages  
2. Convert each page to image  
3. Run EasyOCR text detection  
4. Filter results by confidence threshold  
5. Save results to Markdown and JSON  

---

## Comparison of Approaches

| Method     | Best For                       | Output Type       | Speed  | Accuracy |
|------------|-------------------------------|-------------------|--------|----------|
| Docling    | Digital PDFs (text-based)     | Markdown          | Fast   | High     |
| Tesseract  | Scanned forms/documents       | Markdown + JSON   | Medium | Medium   |
| EasyOCR    | Complex or noisy images       | Markdown + JSON   | Slower | High     |

---

## Use Cases

- Document ingestion for RAG systems  
- Converting PDFs into structured datasets  
- Extracting text from scanned forms  
- Preprocessing for machine learning pipelines  

---

## Installation

Install required Python packages:
pip install docling pytesseract pdf2image easyocr opencv-python pillow numpy

### Additional System Dependencies
- Tesseract OCR (required for `tesseract.py`)  
- Poppler (required for `easyocr.py`)  

---

## How to Run

### Run Docling
python docling.py

### Run Tesseract OCR
python tesseract.py

### Run EasyOCR
python easyocr.py


---

## Notes

- Ensure `input_folder/` contains PDF files before running scripts  
- Ensure `output_folder/` exists or is correctly referenced in scripts  
- OCR performance depends heavily on image quality and preprocessing  

---

## Future Improvements

- Add text chunking for RAG pipelines  
- Integrate embeddings and vector databases  
- Add support for batch processing with metadata tagging  
- Improve layout-aware parsing  























