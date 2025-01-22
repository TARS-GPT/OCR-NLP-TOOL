Below is a sample **README.md** file for your **OCR + NLP project**. You can adapt this text as needed, adding more details specific to your setup or additional dependencies. 

---

# OCR + NLP Project Using FUNSD and Hugging Face

This repository demonstrates how to:
1. **Extract text** from scanned documents using **Tesseract OCR**.
2. **Correct** the extracted text using a **pre-trained language model** (Hugging Face).
3. **Evaluate** the before-and-after results on the **FUNSD** dataset using **Word Error Rate (WER)** and **Character Error Rate (CER)**.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Folder Structure](#folder-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Notes on FUNSD](#notes-on-funsd)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Project Overview

Optical Character Recognition (OCR) often produces **noisy or imperfect** text, especially with challenging scans. This project aims to improve the **accuracy** of OCR results by applying a **pre-trained language model** for post-processing corrections. The FUNSD (Form Understanding in Noisy Scanned Documents) dataset is used here to benchmark improvements, but you can adapt it for other datasets or your own scanned documents.

---

## Features

1. **Bounding Box OCR**:  
   - Each word/region in a scanned form is cropped and passed to Tesseract.

2. **Pre-trained Model Correction**:  
   - A **Hugging Face** pipeline (e.g., a T5-based model) is used in a zero-shot setting to correct spelling and grammar.

3. **Evaluation**:  
   - Compares baseline OCR output to corrected text using **WER** and **CER**.  

4. **Modular Code**:  
   - Easy to replace the correction model or add new steps (e.g., fine-tuning, synthetic data).

---

## Folder Structure

```plaintext
OCR_NLP_FUNSD/
│
├── data/
│   └── FUNSD/
│       ├── images/
│       │   ├── 000001.jpg
│       │   ├── 000002.jpg
│       │   └── ...
│       └── annotations/
│           ├── 000001.json
│           ├── 000002.json
│           └── ...
│
├── scripts/
│   ├── funsd.py          # Loads FUNSD annotations, bounding boxes
│   ├── ocr.py            # OCR logic using Tesseract
│   ├── corrector.py      # Loads Hugging Face pipeline for text correction
│   ├── evaluate.py       # WER/CER evaluation
│   └── __init__.py       # (optional) makes scripts a Python package
│
├── main.py               # Orchestrates the entire pipeline
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation (this file)
```

---

## Requirements

1. **Python 3.7+**  
2. [**Tesseract**](https://github.com/UB-Mannheim/tesseract/wiki) (standalone OCR engine)  
   - Must be installed and added to your `PATH` (on Windows) or accessible via `pytesseract.pytesseract.tesseract_cmd`.
3. **Python Packages**:  
   - [pytesseract](https://pypi.org/project/pytesseract/)  
   - [Pillow](https://pypi.org/project/Pillow/)  
   - [transformers](https://pypi.org/project/transformers/)  
   - [jiwer](https://pypi.org/project/jiwer/)  
   - [accelerate](https://pypi.org/project/accelerate/)  
   - [sentencepiece](https://pypi.org/project/sentencepiece/)  
   - (See `requirements.txt` for the full list.)

---

## Installation

1. **Clone the repository** (or download the ZIP):
   ```bash
   git clone https://github.com/<YourUsername>/OCR-NLP-FUNSD.git
   cd OCR-NLP-FUNSD
   ```
2. **(Optional) Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Install Tesseract** (if not already installed):
   - Windows: [UB-Mannheim builds](https://github.com/UB-Mannheim/tesseract/wiki).  
   - Mac: `brew install tesseract`  
   - Linux (Debian/Ubuntu): `sudo apt-get install tesseract-ocr`

5. **Configure** Tesseract in your `PATH` or specify its location in code:
   ```python
   import pytesseract
   pytesseract.pytesseract.tesseract_cmd = r"C:\Path\To\tesseract.exe"
   ```

---

## Usage

1. **Place the FUNSD dataset** in `data/FUNSD/`, ensuring:
   ```plaintext
   data/
     FUNSD/
       images/
       annotations/
   ```
2. **Run the main script**:
   ```bash
   python main.py
   ```
   - The pipeline will:
     1. Load each `*.jpg` in `images/`.
     2. Parse the matching JSON file in `annotations/`.
     3. For each bounding box, crop and run Tesseract.
     4. Evaluate baseline WER/CER.
     5. Load a Hugging Face correction model.
     6. Correct each OCR snippet and evaluate again.

3. **Check the console output** for:
   - **Number of bounding boxes** processed.  
   - **Baseline vs. Corrected** WER/CER.  
   - Improvements in accuracy.

---

## Notes on FUNSD

- **FUNSD** is a dataset for Form Understanding in Noisy Scanned Documents, containing ~199 scanned forms.  
- Each `.json` file has bounding box coordinates plus the transcribed text.  
- This project **matches** bounding boxes exactly, so no complex alignment is needed.  
- If the dataset images are in `.png` format, change your code in `scripts/ocr.py` from `"*.jpg"` to `"*.png"`.

---

## Troubleshooting

1. **No bounding boxes found**:
   - Check that your images are named `000001.jpg`, `000002.jpg`, etc., and the annotation JSONs match the same names (`000001.json`, `000002.json`).  
   - Ensure the file extensions (`.jpg` vs `.png`) match your code.

2. **TesseractNotFoundError**:
   - Install Tesseract and add it to your `PATH`. On Windows, ensure you check “Add Tesseract to system path” during installation or manually add the `C:\Program Files\Tesseract-OCR\` folder to `PATH`.

3. **Hugging Face 401 Unauthorized**:
   - Make sure the model you’re using is public.  
   - If it’s private, configure your auth token or pick a public grammar/correction model.

4. **Poor Correction Results**:
   - Zero-shot correction works best on relatively standard text. For domain-specific jargon or large paragraphs, consider:
     - **fine-tuning** a model  
     - using domain-specific dictionaries or language models.

5. **Large GPU Usage**:
   - If you’re using a large model, you might need to set `device=-1` for CPU usage or ensure you have a GPU available.

---

## License

This project is distributed under the MIT License. The **FUNSD** dataset is provided by its respective authors—check the dataset’s own **license** or terms of use before commercial usage or redistribution.

---

**Happy OCR + NLP!** Feel free to open issues or pull requests on GitHub if you have questions or improvements. If you build something cool with this pipeline, let us know!
