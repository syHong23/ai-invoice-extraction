"""
VLM + OCR Document Extraction Package
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from .ocr_handler import OCRHandler
from .data_extractor import DataExtractor

__all__ = [
    'OCRHandler', 
    'DataExtractor'
]