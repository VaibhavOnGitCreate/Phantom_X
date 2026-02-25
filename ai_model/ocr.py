import os
import shutil
import pytesseract
import cv2
import numpy as np


# ============================================================
# Phantom_X Tesseract Auto Configuration
# ============================================================

def auto_configure_tesseract():
    """
    Automatically locate Tesseract executable on Windows, Linux, or macOS.
    Returns True if found, False otherwise.
    """

    # 1. Try system PATH
    path = shutil.which("tesseract")

    if path:
        pytesseract.pytesseract.tesseract_cmd = path
        return True

    # 2. Windows common install locations
    possible_paths = [

        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"E:\tesseract\tesseract.exe",

        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",

        os.path.expanduser(
            r"~\AppData\Local\Tesseract-OCR\tesseract.exe"
        )
    ]

    for p in possible_paths:

        if os.path.exists(p):
            pytesseract.pytesseract.tesseract_cmd = p
            return True

    return False


# ============================================================
# Phantom_X Image Preprocessing (CRITICAL for accuracy)
# ============================================================

def preprocess_image(image_path):
    """
    Optimizes image for OCR accuracy.
    Designed for mobile messages and email screenshots.
    """

    img = cv2.imread(image_path)

    if img is None:
        raise Exception("Image not found or invalid format")

    # convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # increase contrast
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)

    # reduce noise
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # threshold for clean text
    _, thresh = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return thresh


# ============================================================
# Phantom_X OCR Extraction
# ============================================================

def extract_text(image_path):
    """
    Extracts text from image using PyTesseract.
    Auto configures Tesseract.
    Returns clean text string.
    """

    # auto configure tesseract
    if not auto_configure_tesseract():

        raise Exception(
            "Tesseract not found. Install from:\n"
            "https://github.com/UB-Mannheim/tesseract/wiki"
        )

    # preprocess image
    processed = preprocess_image(image_path)

    # OCR extraction optimized for messages and emails
    text = pytesseract.image_to_string(
        processed,
        config="--oem 3 --psm 6"
    )

    # clean result
    text = text.strip()

    return text


# ============================================================
# Phantom_X OCR Verification
# ============================================================

def verify_tesseract():
    """
    Returns Tesseract version if installed.
    """

    if not auto_configure_tesseract():
        return None

    try:
        version = pytesseract.get_tesseract_version()
        return str(version)

    except:
        return None





# ============================================================
# Phantom_X Test Mode
# ============================================================

if __name__ == "__main__":

    test_image = r"D:\My_projects\Phantom_X\static\capture.png"

    print("Phantom_X OCR Test")

    version = verify_tesseract()

    if version:

        print("Tesseract Version:", version)

        text = extract_text(test_image)

        print("\nExtracted Text:\n")
        print(text)

    else:

        print("Tesseract not installed")