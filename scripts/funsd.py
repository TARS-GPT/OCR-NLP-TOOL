# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 02:18:47 2025

@author: rajan
"""

import json
import os

def load_funsd_annotation(json_path):
    """
    Returns a list of (bbox, text) for each labeled region in the FUNSD annotation.
    bbox = (left, top, right, bottom).
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = []
    for block in data["form"]:
        box = block["box"]  # [left, top, right, bottom]
        text = block["text"].strip()
        if text:
            bbox_tuple = (box[0], box[1], box[2], box[3])
            results.append((bbox_tuple, text))
    return results
