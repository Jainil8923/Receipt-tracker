from PIL import Image
import pytesseract
from transformers import pipeline
import re

def extract_text_from_image(image_path: str) -> str:
    image = Image.open(image_path).convert("RGB")
    return pytesseract.image_to_string(image)
def identify_organization_from_text(text: str) -> str:
    text_lower = text.lower()

    if "dmart" in text_lower or "avenue supermarkets" in text_lower:
        return "DMart"
    elif "domino" in text_lower or "pizza" in text_lower:
        return "Domino's"
    elif "zomato" in text_lower or "zmt" in text_lower:
        return "Zomato"
    else:
        return "Unknown"

def parse_dmart_text(text: str):
    result = {"date": None, "total": None, "items": []}

    date_match = re.search(r"(?:Invoice Date|ORDER DATE):\s*(\d{2}/\d{2}/\d{2,4})", text)
    if date_match:
        result["date"] = date_match.group(1)

    total_match = re.search(r"([\d,]+\.\d{2})\s+to be collected", text)
    if total_match:
        result["total"] = total_match.group(1)

    item_lines = []
    for line in text.split("\n"):
        if re.search(r"\b\d+\s+\d+\.\d{2}", line):
            item_lines.append(line.strip())

    for line in item_lines:
        parts = re.findall(r"([a-zA-Z\s\-]+)\s+(\d+\.\d{2})", line)
        if parts:
            name, price = parts[-1]
            result["items"].append({"name": name.strip(), "price": price})

    return result

def extract_dmart_info(ocr_text: str) -> dict:
    print(ocr_text)
    date_pattern = r"Date\s*[:\-]?\s*(\d{2}-\d{2}-\d{4})"
    total_pattern = r"Total\s*[:\-]?\s*([\d,]+\.\d{2})"
    items_pattern = r"(\d+\.\d{2})\s*([\w\s]+)\s*(\d+\.\d{2})"
    
    date = re.search(date_pattern, ocr_text)
    total = re.search(total_pattern, ocr_text)
    items = re.findall(items_pattern, ocr_text)

    return {
        "date": date.group(1) if date else None,
        "total": total.group(1) if total else None,
        "items": [{"name": item[1], "price": item[2]} for item in items]
    }

def extract_dominos_info(ocr_text: str) -> dict:
    date_pattern = r"Order Date\s*[:\-]?\s*(\d{2}-\d{2}-\d{4})"
    total_pattern = r"Total\s*[:\-]?\s*([\d,]+\.\d{2})"
    items_pattern = r"(\d+\.\d{2})\s*([\w\s]+)\s*(\d+\.\d{2})"
    
    date = re.search(date_pattern, ocr_text)
    total = re.search(total_pattern, ocr_text)
    items = re.findall(items_pattern, ocr_text)

    return {
        "date": date.group(1) if date else None,
        "total": total.group(1) if total else None,
        "items": [{"name": item[1], "price": item[2]} for item in items]
    }

def extract_zomato_info(ocr_text: str) -> dict:
    date_pattern = r"Date\s*[:\-]?\s*(\d{2}-\d{2}-\d{4})"
    total_pattern = r"Total\s*[:\-]?\s*([\d,]+\.\d{2})"
    items_pattern = r"(\d+\.\d{2})\s*([\w\s]+)\s*(\d+\.\d{2})"
    
    date = re.search(date_pattern, ocr_text)
    total = re.search(total_pattern, ocr_text)
    items = re.findall(items_pattern, ocr_text)

    return {
        "date": date.group(1) if date else None,
        "total": total.group(1) if total else None,
        "items": [{"name": item[1], "price": item[2]} for item in items]
    }

def process_receipt(image_path: str) -> dict:
    ocr_text = extract_text_from_image(image_path)
    organization = identify_organization_from_text(ocr_text)
    if organization.lower() == "dmart":
        return parse_dmart_text(ocr_text)
    elif organization.lower() == "domino's":
        return extract_dominos_info(ocr_text)
    elif organization.lower() == "zomato":
        return extract_zomato_info(ocr_text)
    else:
        return {"error": "Organization not supported"}
