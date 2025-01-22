# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 02:21:07 2025

@author: rajan
"""

from transformers import pipeline

def load_correction_model(model_name="pszemraj/flan-t5-base-correction", device=-1):
    """
    Create and return a text-to-text generation pipeline for correction.
    device = -1 means CPU; use device=0 for GPU (if available).
    """
    corrector = pipeline(
        "text2text-generation",
        model=model_name,
        device=device
    )
    return corrector

def correct_text_with_huggingface(text, corrector_pipeline):
    """
    Use the loaded Hugging Face pipeline to correct an input text.
    """
    # Some models accept prompts like "Correct this text: ..." 
    prompt = "Correct this text: " + text
    outputs = corrector_pipeline(prompt, max_length=128, num_beams=1, do_sample=False)
    corrected_text = outputs[0]["generated_text"]
    return corrected_text
