import io
import sys
import pytesseract
from PIL import Image

# --- CONFIGURATION FOR WINDOWS ---
# If you installed Tesseract in the default location, this is the path:
# (Uncomment the line below if you are on Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text(image_bytes: bytes) -> str:
    """
    Converts image bytes to text using Tesseract OCR.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to greyscale to improve accuracy
        image = image.convert('L') 
        
        # Extract text
        text = pytesseract.image_to_string(image)
        
        # Debugging: Print to terminal to see if it's working
        print(f"DEBUG: Extracted {len(text)} characters.")
        
        return text.strip()
        
    except pytesseract.TesseractNotFoundError:
        # This error is specific to the missing .exe
        raise Exception("Tesseract is not installed or the path is wrong. Please install Tesseract-OCR.")
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""