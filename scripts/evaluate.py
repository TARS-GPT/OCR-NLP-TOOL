# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 02:21:43 2025

@author: rajan
"""

from jiwer import wer, cer

def evaluate_ocr(recognized_texts, ground_truth_texts):
    """
    Returns average WER and CER across the list of recognized_texts vs. ground_truth_texts.
    Each item is a short string (e.g., bounding box text).
    """
    total_wer = 0.0
    total_cer = 0.0
    n = len(ground_truth_texts)

    for r_text, g_text in zip(recognized_texts, ground_truth_texts):
        total_wer += wer(g_text, r_text)
        total_cer += cer(g_text, r_text)

    return total_wer / n, total_cer / n
