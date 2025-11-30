"""
Patient Data Extractor - JSON Output
====================================
Extracts patient prescription data from PrimeCare screenshots and outputs in JSON format.

Requirements:
- Tesseract OCR installed on Windows
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Default path: C:\\Program Files\\Tesseract-OCR\\tesseract.exe

Usage:
    python patient_data_extractor_json.py <image_path>
    python patient_data_extractor_json.py  # For screen capture
"""

import pyautogui
import pytesseract
from PIL import Image, ImageEnhance
import cv2
import numpy as np
import json
from datetime import datetime
import os
import re
from pathlib import Path
import sys


class PatientDataExtractorJSON:
    """Extract patient prescription data and output as JSON."""
    
    def __init__(self, tesseract_path=r"C:\Program Files\Tesseract-OCR\tesseract.exe"):
        """
        Initialize the extractor.
        
        Args:
            tesseract_path: Path to tesseract.exe on Windows
        """
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        self.screenshots_dir = Path("screenshots")
        self.output_dir = Path("extracted_data")
        
        # Create directories
        self.screenshots_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
    def capture_screen(self, region=None, save=True):
        """
        Capture screenshot of the entire screen or specific region.
        
        Args:
            region: Tuple (x, y, width, height) for specific region, None for full screen
            save: Whether to save the screenshot
            
        Returns:
            PIL Image object
        """
        print("📸 Capturing screenshot...")
        
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()
        
        if save:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = self.screenshots_dir / f"patient_data_{timestamp}.png"
            screenshot.save(filename)
            print(f"✅ Screenshot saved: {filename}")
            
        return screenshot
    
    def preprocess_image(self, image):
        """
        Preprocess image for better OCR accuracy.
        
        Args:
            image: PIL Image object
            
        Returns:
            Preprocessed PIL Image
        """
        # Convert PIL to OpenCV format
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Resize image if too small (upscale for better OCR)
        height, width = img_cv.shape[:2]
        if height < 1000 or width < 1000:
            scale_factor = max(1000 / height, 1000 / width)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            img_cv = cv2.resize(img_cv, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Apply bilateral filter to reduce noise while keeping edges sharp
        filtered = cv2.bilateralFilter(gray, 9, 75, 75)
        
        # Apply adaptive thresholding for better results with varying lighting
        thresh = cv2.adaptiveThreshold(filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY, 11, 2)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
        
        # Dilate to make text thicker
        kernel = np.ones((1, 1), np.uint8)
        dilated = cv2.dilate(denoised, kernel, iterations=1)
        
        # Convert back to PIL
        processed = Image.fromarray(dilated)
        
        # Enhance contrast and sharpness
        enhancer = ImageEnhance.Contrast(processed)
        processed = enhancer.enhance(2.0)
        
        enhancer = ImageEnhance.Sharpness(processed)
        processed = enhancer.enhance(2.0)
        
        return processed
    
    def extract_patient_info(self, text):
        """
        Extract patient information from OCR text.
        
        Args:
            text: Raw OCR text
            
        Returns:
            Dictionary with patient info
        """
        patient_info = {
            "name": None,
            "address": None,
            "date_of_birth": None,
            "prescriptions": None
        }
        
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_upper = line.upper()
            
            # Extract patient name (usually after "Patient:" or "Address:")
            if 'PATIENT:' in line_upper or 'ADDRESS:' in line_upper:
                # Look in current and next few lines
                for j in range(i, min(i + 3, len(lines))):
                    check_line = lines[j].strip()
                    # Name pattern: LASTNAME, FIRSTNAME or full name
                    name_match = re.search(r'([A-Z]+,\s*[A-Z]+)', check_line)
                    if name_match and not patient_info["name"]:
                        patient_info["name"] = name_match.group(1)
                        break
                    # Alternative pattern: Address line might contain name
                    if 'Address:' in check_line:
                        parts = check_line.split('Address:')
                        if len(parts) > 0 and parts[0].strip():
                            patient_info["name"] = parts[0].strip()
            
            # Extract date of birth
            if 'DATE OF BIRTH' in line_upper or 'DOB' in line_upper:
                # Look for date pattern MM/DD/YYYY or similar
                dob_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', line)
                if dob_match:
                    patient_info["date_of_birth"] = dob_match.group(1)
            
            # Extract prescriptions count
            if 'PRESCRIPTION' in line_upper and 'TOTAL' in line_upper:
                prescription_match = re.search(r'(\d+)', line)
                if prescription_match:
                    patient_info["prescriptions"] = prescription_match.group(1)
        
        return patient_info
    
    def extract_product_info(self, text):
        """
        Extract product (drug) information from OCR text.
        
        Args:
            text: Raw OCR text
            
        Returns:
            List of product information
        """
        products = []
        lines = text.split('\n')
        
        drug_keywords = ['OXYCODONE', 'LORAZEPAM', 'MORPHINE', 'TABLET', 'MG', 'HCL',
                        'CODONE', 'AZEPAM', 'CAPSULE', 'ML', 'SULF', 'DUFFY']
        
        for i, line in enumerate(lines):
            line_upper = line.upper()
            
            # Check if line contains "Product:" label
            if 'PRODUCT:' in line_upper:
                # Extract product from same line or next line
                product_text = line.replace('Product:', '').replace('PRODUCT:', '').strip()
                
                if not product_text and i + 1 < len(lines):
                    product_text = lines[i + 1].strip()
                
                if product_text:
                    products.append(product_text)
            
            # Also look for drug names in general text
            elif any(kw in line_upper for kw in drug_keywords):
                # Extract drug name with dosage
                drug_match = re.search(r'([A-Z\s]+\d+\s*MG[^.]*)', line_upper)
                if drug_match:
                    drug_name = drug_match.group(1).strip()
                    if drug_name not in products:
                        products.append(drug_name)
        
        return products if products else [None]
    
    def extract_quantity_info(self, text):
        """
        Extract quantity information from OCR text.
        
        Args:
            text: Raw OCR text
            
        Returns:
            List of quantities
        """
        quantities = []
        lines = text.split('\n')
        
        for line in lines:
            line_upper = line.upper()
            
            # Check if line contains "Quantity:" label
            if 'QUANTITY:' in line_upper:
                # Extract quantity number
                qty_match = re.search(r'(\d+)\s*(ML|TAB|TABLET|CAPSULE)?', line)
                if qty_match:
                    quantity = qty_match.group(1)
                    unit = qty_match.group(2) if qty_match.group(2) else 'units'
                    quantities.append(f"{quantity} {unit}")
            
            # Look for quantity patterns like "30 ML" or "15 TAB"
            elif re.search(r'\b(\d+)\s*(ML|TAB|TABLET|CAPSULE)\b', line_upper):
                qty_match = re.search(r'\b(\d+)\s*(ML|TAB|TABLET|CAPSULE)\b', line_upper)
                if qty_match:
                    quantity_str = f"{qty_match.group(1)} {qty_match.group(2)}"
                    if quantity_str not in quantities:
                        quantities.append(quantity_str)
        
        return quantities if quantities else [None]
    
    def extract_directions(self, text):
        """
        Extract directions/instructions from OCR text.
        
        Args:
            text: Raw OCR text
            
        Returns:
            List of directions
        """
        directions = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_upper = line.upper()
            
            # Check if line contains "Directions:" label
            if 'DIRECTIONS:' in line_upper or 'DIRECTION:' in line_upper:
                # Extract directions from same line and potentially next lines
                direction_text = re.sub(r'DIRECTIONS?:', '', line, flags=re.IGNORECASE).strip()
                
                # Collect multi-line directions
                full_direction = [direction_text] if direction_text else []
                
                # Look ahead for continuation
                for j in range(i + 1, min(i + 5, len(lines))):
                    next_line = lines[j].strip()
                    # Stop at next section or empty line
                    if not next_line or any(label in next_line.upper() 
                                           for label in ['PRODUCT:', 'QUANTITY:', 'PATIENT:', 'CONTINUANCE']):
                        break
                    full_direction.append(next_line)
                
                if full_direction:
                    directions.append(' '.join(full_direction))
            
            # Look for "TAKE" instructions
            elif 'TAKE' in line_upper:
                # Extract full instruction
                take_instruction = line.strip()
                # Continue to next line if instruction seems incomplete
                if i + 1 < len(lines) and not any(label in lines[i + 1].upper() 
                                                   for label in ['PRODUCT:', 'QUANTITY:', 'PATIENT:']):
                    take_instruction += ' ' + lines[i + 1].strip()
                
                if take_instruction not in directions:
                    directions.append(take_instruction)
        
        return directions if directions else [None]
    
    def extract_from_image(self, image):
        """
        Extract all patient data from image.
        
        Args:
            image: PIL Image object or path to image file
            
        Returns:
            Dictionary with extracted data
        """
        print("🔍 Extracting patient data from image...")
        
        # Load image if path provided
        if isinstance(image, (str, Path)):
            image = Image.open(image)
        
        # Preprocess image
        processed_img = self.preprocess_image(image)
        
        # Perform OCR with custom config for better accuracy
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(processed_img, config=custom_config)
        
        # Debug: print extracted text
        print(f"\n📄 Raw OCR Text ({len(text)} chars):")
        print("="*60)
        print(text[:500] if len(text) > 500 else text)
        print("="*60)
        
        # Extract all components
        patient_info = self.extract_patient_info(text)
        products = self.extract_product_info(text)
        quantities = self.extract_quantity_info(text)
        directions = self.extract_directions(text)
        
        # Build structured data
        extracted_data = {
            "extraction_timestamp": datetime.now().isoformat(),
            "patient": patient_info,
            "prescriptions": []
        }
        
        # Combine product, quantity, and directions
        max_items = max(len(products), len(quantities), len(directions))
        
        for i in range(max_items):
            prescription = {
                "product": products[i] if i < len(products) else None,
                "quantity": quantities[i] if i < len(quantities) else None,
                "directions": directions[i] if i < len(directions) else None
            }
            extracted_data["prescriptions"].append(prescription)
        
        return extracted_data
    
    def save_to_json(self, data, filename=None):
        """
        Save extracted data to JSON file.
        
        Args:
            data: Dictionary with extracted data
            filename: Output filename (auto-generated if None)
            
        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = self.output_dir / f"patient_data_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Data saved to: {filename}")
        return filename
    
    def display_json(self, data):
        """
        Display extracted data as formatted JSON.
        
        Args:
            data: Dictionary with extracted data
        """
        print("\n" + "="*60)
        print("EXTRACTED PATIENT DATA (JSON)")
        print("="*60)
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print("="*60)
    
    def run_full_extraction(self, image_path=None, region=None):
        """
        Complete workflow: Capture/load image and extract data.
        
        Args:
            image_path: Path to existing image (None to capture new screenshot)
            region: Screen region to capture if taking screenshot
            
        Returns:
            Dictionary with extracted data
        """
        print("\n🚀 Starting Patient Data Extraction")
        print("="*60)
        
        # Load or capture image
        if image_path:
            print(f"📂 Loading image: {image_path}")
            image = Image.open(image_path)
        else:
            image = self.capture_screen(region=region)
        
        # Extract data
        data = self.extract_from_image(image)
        
        # Display and save results
        self.display_json(data)
        self.save_to_json(data)
        
        print("\n✅ Extraction complete!")
        
        return data


def main():
    """Main execution function."""
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║     Patient Data Extractor - JSON Output                 ║
║     Extract Patient, Product, Quantity, Directions        ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Initialize extractor
    try:
        extractor = PatientDataExtractorJSON()
    except Exception as e:
        print(f"❌ Error initializing extractor: {e}")
        print("\n⚠️  Make sure Tesseract OCR is installed:")
        print("   Download: https://github.com/UB-Mannheim/tesseract/wiki")
        return
    
    # Check for image path argument
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        if not os.path.exists(image_path):
            print(f"❌ Error: Image file not found: {image_path}")
            return
        
        print(f"\n📷 Extracting from image: {image_path}")
        data = extractor.run_full_extraction(image_path=image_path)
    else:
        # Capture new screenshot
        print("\n⏱️  Screenshot will be taken in 3 seconds...")
        print("   Switch to patient data window now!")
        
        import time
        for i in range(3, 0, -1):
            print(f"   {i}...")
            time.sleep(1)
        
        data = extractor.run_full_extraction()
    
    print("\n📁 Files saved in:")
    print(f"   Screenshots: {extractor.screenshots_dir}")
    print(f"   JSON Output: {extractor.output_dir}")
    
    # Return data for programmatic use
    return data


if __name__ == "__main__":
    main()
