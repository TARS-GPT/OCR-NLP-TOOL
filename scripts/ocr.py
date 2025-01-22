# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 02:19:43 2025

@author: rajan
"""

import os
import glob
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from scripts.funsd import load_funsd_annotation

def ocr_bbox(image_path, bbox):
    """
    Crop a bounding box from the image and run Tesseract on the crop.
    bbox = (left, top, right, bottom)
    """
    img = Image.open(image_path)
    cropped = img.crop(bbox)
    config = "--psm 7"
    recognized_text = pytesseract.image_to_string(cropped, config=config)
    return recognized_text.strip()

def run_ocr_on_funsd(funsd_root):
    """
    Iterate over all images in FUNSD. For each bounding box, run OCR and
    collect (recognized_text, ground_truth_text).
    """
    recognized_texts = []
    ground_truth_texts = []

    image_folder = os.path.join(funsd_root, "images")
    annotation_folder = os.path.join(funsd_root, "annotations")

    image_paths = sorted(glob.glob(os.path.join(image_folder, "*.png")))
    for img_path in image_paths:
        base_name = os.path.splitext(os.path.basename(img_path))[0]  # e.g. "000001"
        json_path = os.path.join(annotation_folder, base_name + ".json")

        # Load bounding boxes + text from FUNSD
        annotations = load_funsd_annotation(json_path)
        for bbox, gt_text in annotations:
            ocr_text = ocr_bbox(img_path, bbox)
            recognized_texts.append(ocr_text)
            ground_truth_texts.append(gt_text)
    
    return recognized_texts, ground_truth_texts
