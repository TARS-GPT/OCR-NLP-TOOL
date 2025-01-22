# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 02:22:06 2025

@author: rajan
"""

import os
import sys

# Local imports
from scripts.ocr import run_ocr_on_funsd
from scripts.corrector import load_correction_model, correct_text_with_huggingface
from scripts.evaluate import evaluate_ocr

def main():
    # 1) Path to FUNSD dataset
    # E.g., "C:/Projects/OCR_NLP_FUNSD/data/FUNSD"
    funsd_root = os.path.join("data", "FUNSD")
    if not os.path.exists(funsd_root):
        print(f"FUNSD root not found at: {funsd_root}")
        sys.exit(1)

    # 2) Run OCR on FUNSD bounding boxes
    recognized, ground_truth = run_ocr_on_funsd(funsd_root)
    print(f"Total segments (bounding boxes) processed: {len(recognized)}")

    # 3) Evaluate baseline
    baseline_wer, baseline_cer = evaluate_ocr(recognized, ground_truth)
    print(f"\nBaseline OCR Results:")
    print(f"  WER: {baseline_wer:.4f}")
    print(f"  CER: {baseline_cer:.4f}")

    # 4) Load a pretrained correction model (no fine-tuning)
    print("\nLoading correction model from Hugging Face...")
    corrector_pipeline = load_correction_model(
        model_name="pszemraj/flan-t5-base-correction",
        device=-1  # Use 0 if you have a GPU
    )

    # 5) Apply text correction
    recognized_corrected = []
    for i, text in enumerate(recognized):
        if text.strip():
            corrected_text = correct_text_with_huggingface(text, corrector_pipeline)
            recognized_corrected.append(corrected_text)
        else:
            recognized_corrected.append(text)  # empty or whitespace

    # 6) Evaluate corrected text
    corrected_wer, corrected_cer = evaluate_ocr(recognized_corrected, ground_truth)
    print(f"\nCorrected OCR Results:")
    print(f"  WER: {corrected_wer:.4f}")
    print(f"  CER: {corrected_cer:.4f}")

    # 7) Compare improvement
    print("\nImprovements (Baseline -> Corrected):")
    print(f"  WER improvement: {baseline_wer - corrected_wer:.4f}")
    print(f"  CER improvement: {baseline_cer - corrected_cer:.4f}")

if __name__ == "__main__":
    main()
    