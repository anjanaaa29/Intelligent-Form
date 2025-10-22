import os
import pdfplumber
from PIL import Image
import logging
import easyocr
logging.getLogger("pdfminer").setLevel(logging.ERROR)

reader = easyocr.Reader(['en'], gpu=False)

def extract_text_pdf(file_path):
    text=""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            content=page.extract_text()
            if content:
                text+=content + "\n"
    return text.strip()

def extract_text_img(file_path):
    result = reader.readtext(file_path, detail=0)
    text = "\n".join(result)
    return text

def extract_form_text(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    file_path_lower=file_path.lower()
    if file_path_lower.endswith('.pdf'):
        print(f"[INFO] Extracting text from PDF: {file_path}")
        return extract_text_pdf(file_path)
    
    elif file_path_lower.endswith((".jpg",".jpeg",".png")):
        print(f"[INFO] Extracting text from image: {file_path}")
        return extract_text_img(file_path)
    else:
        return ValueError("unsupported file format. Please upload PDF,JPG or PNG.")

def extract_multiple_forms(file_list):
    all_texts={}
    for file_path in file_list:
        try:
            text=extract_form_text(file_path)
            all_texts[file_path]=text
        except Exception as e:
            print(f"[ERROR] Failed to process {file_path}:{e}")
            all_texts[file_path]=""
    return all_texts
