"""
PrimeCare Screen Capture and Data Extractor
===========================================
Captures screenshot of PrimeCare pharmacy system and extracts Status and Drug Name fields.

Requirements:
- Tesseract OCR installed on Windows
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Default path: C:\\Program Files\\Tesseract-OCR\\tesseract.exe

Usage:
    python screenshot_extractor.py
"""

import pyautogui
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
import pandas as pd
from datetime import datetime
import os
import re
from pathlib import Path


class PrimeCareExtractor:
    """Extract patient prescription data from PrimeCare screenshots."""
    
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
            filename = self.screenshots_dir / f"primecare_{timestamp}.png"
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
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
        
        # Convert back to PIL
        processed = Image.fromarray(denoised)
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(processed)
        processed = enhancer.enhance(2.0)
        
        return processed
    
    def extract_table_data(self, image):
        """
        Extract Status and Drug Name from PrimeCare table using OCR.
        
        Args:
            image: PIL Image object
            
        Returns:
            List of dictionaries containing Status and Drug Name
        """
        print("🔍 Extracting data from image...")
        
        # Preprocess image
        processed_img = self.preprocess_image(image)
        
        # Perform OCR
        ocr_data = pytesseract.image_to_data(processed_img, output_type=pytesseract.Output.DICT)
        
        # Extract text with coordinates
        data = []
        for i, text in enumerate(ocr_data['text']):
            if text.strip():
                data.append({
                    'text': text.strip(),
                    'left': ocr_data['left'][i],
                    'top': ocr_data['top'][i],
                    'width': ocr_data['width'][i],
                    'height': ocr_data['height'][i],
                    'conf': ocr_data['conf'][i]
                })
        
        return self._parse_table_structure(data)
    
    def _parse_table_structure(self, ocr_data):
        """
        Parse OCR data to extract Status and Drug Name in table format.
        
        Args:
            ocr_data: List of dictionaries with OCR results
            
        Returns:
            List of dictionaries with Status and Drug Name
        """
        print("📊 Parsing table structure...")
        
        # Group text by rows (similar Y coordinates)
        rows = {}
        tolerance = 15  # Pixel tolerance for same row
        
        for item in ocr_data:
            if item['conf'] < 30:  # Skip low confidence text
                continue
                
            y_pos = item['top']
            
            # Find existing row or create new one
            found_row = False
            for row_y in rows.keys():
                if abs(y_pos - row_y) < tolerance:
                    rows[row_y].append(item)
                    found_row = True
                    break
            
            if not found_row:
                rows[y_pos] = [item]
        
        # Sort items in each row by X position
        for row_y in rows:
            rows[row_y] = sorted(rows[row_y], key=lambda x: x['left'])
        
        # Extract Status and Drug Name
        extracted_data = []
        
        for row_y in sorted(rows.keys()):
            row_items = rows[row_y]
            
            if len(row_items) < 2:  # Skip rows with too few items
                continue
            
            # Detect column boundaries by analyzing X positions
            # Typically: Status column is leftmost, Drug Name follows
            
            # Find if row contains "TAKE" keyword (indicates status/instruction)
            has_instruction = any('TAKE' in item['text'].upper() for item in row_items)
            
            # Find if row contains drug keywords
            drug_keywords = ['OXYCODONE', 'LORAZEPAM', 'MORPHINE', 'TABLET', 'MG', 'HCL', 
                           'CODONE', 'AZEPAM', 'CAPSULE', 'ML']
            has_drug = any(any(kw in item['text'].upper() for kw in drug_keywords) 
                          for item in row_items)
            
            if not (has_instruction or has_drug):
                continue
            
            # Split row into columns based on X position gaps
            columns = []
            current_column = [row_items[0]]
            gap_threshold = 50  # Pixel gap to determine new column
            
            for i in range(1, len(row_items)):
                prev_item = row_items[i-1]
                curr_item = row_items[i]
                
                # Calculate gap between words
                gap = curr_item['left'] - (prev_item['left'] + prev_item['width'])
                
                if gap > gap_threshold:
                    # Start new column
                    columns.append(current_column)
                    current_column = [curr_item]
                else:
                    current_column.append(curr_item)
            
            columns.append(current_column)
            
            # Extract Order Key, Status, Drug Name, and Quantity from columns
            order_key = None
            status = None
            drug_name = None
            quantity = None
            
            # Process each column
            for col_idx, column in enumerate(columns):
                col_text = ' '.join([item['text'] for item in column]).strip()
                
                # Order Key column (F1, F2, F3, P4, etc.) - typically first column with letter+number
                if re.match(r'^[A-Z]\d+$', col_text) or re.match(r'^[A-Z][a-z]?\d+$', col_text):
                    if not order_key:
                        order_key = col_text
                
                # Status column contains "TAKE" instructions
                if 'TAKE' in col_text.upper() or any(word in col_text.upper() 
                    for word in ['BY MOUTH', 'TIMES', 'DAY', 'HOURS', 'DAILY']):
                    if not status:  # Only set once
                        status = col_text
                
                # Drug Name column contains medication names
                if any(kw in col_text.upper() for kw in drug_keywords):
                    if not drug_name:  # Only set once
                        drug_name = col_text
                
                # Quantity column - look for number followed by TAB/TABLET/ML
                if re.search(r'\d+\s*(TAB|TABLET|ML|CAPSULE)', col_text.upper()):
                    match = re.search(r'(\d+)\s*(TAB|TABLET|ML|CAPSULE)', col_text.upper())
                    if match and not quantity:
                        quantity = match.group(1)
            
            # If no clear order key found, look in full row
            if not order_key:
                for item in row_items:
                    if re.match(r'^[A-Z]\d+$', item['text']) or re.match(r'^[A-Z][a-z]?\d+$', item['text']):
                        order_key = item['text']
                        break
            
            # If no clear status instruction found, try to extract from full row
            if not status and has_instruction:
                # Look for instruction phrases in full row
                instruction_parts = []
                for item in row_items:
                    text = item['text'].upper()
                    if any(word in text for word in ['TAKE', 'TABLET', 'BY', 'MOUTH', 
                                                      'EVERY', 'TIMES', 'DAY', 'HOURS', 'DAILY']):
                        instruction_parts.append(item['text'])
                if instruction_parts:
                    status = ' '.join(instruction_parts)
            
            # If no clear drug name found, extract drug-related terms
            if not drug_name and has_drug:
                drug_parts = []
                for item in row_items:
                    text = item['text'].upper()
                    if any(kw in text for kw in drug_keywords) or any(char.isdigit() for char in text):
                        drug_parts.append(item['text'])
                if drug_parts:
                    drug_name = ' '.join(drug_parts)
            
            # If no quantity found, look for standalone numbers that might be quantity
            if not quantity:
                for item in row_items:
                    text = item['text'].strip()
                    if text.isdigit() and int(text) < 1000:  # Reasonable quantity range
                        quantity = text
                        break
            
            if status or drug_name or order_key:
                extracted_data.append({
                    'Order Key': order_key if order_key else 'N/A',
                    'Status': status if status else 'N/A',
                    'Drug Name': drug_name if drug_name else 'N/A',
                    'Quantity': quantity if quantity else 'N/A',
                    'Row': len(extracted_data) + 1
                })
        
        return extracted_data
    
    def extract_with_template_matching(self, image):
        """
        Alternative extraction method using specific patterns for PrimeCare table.
        
        Args:
            image: PIL Image object
            
        Returns:
            List of dictionaries containing Status and Drug Name
        """
        print("🎯 Extracting using pattern matching...")
        
        # Get full OCR text
        text = pytesseract.image_to_string(image)
        
        # Split into lines
        lines = text.split('\n')
        
        extracted_data = []
        
        # Pattern for PrimeCare rows
        for line in lines:
            if not line.strip() or len(line.strip()) < 10:
                continue
            
            # Check if line contains "TAKE" instruction pattern
            has_instruction = 'TAKE' in line.upper()
            
            # Check if line contains drug keywords
            drug_keywords = ['OXYCODONE', 'LORAZEPAM', 'MORPHINE', 'TABLET', 'MG', 'HCL',
                           'CODONE', 'AZEPAM', 'CAPSULE', 'ML', 'SULF']
            has_drug = any(kw in line.upper() for kw in drug_keywords)
            
            if not (has_instruction or has_drug):
                continue
            
            order_key = None
            status = None
            drug_name = None
            quantity = None
            
            # Extract Order Key (F1, F2, P3, etc.)
            parts = line.split()
            for part in parts[:5]:  # Check first 5 words for order key
                if re.match(r'^[A-Z]\d+$', part) or re.match(r'^[A-Z][a-z]?\d+$', part):
                    order_key = part
                    break
            
            # Extract instruction/status (text containing "TAKE")
            if has_instruction:
                # Find "TAKE" and extract surrounding instruction text
                parts = line.split()
                take_idx = -1
                
                for i, part in enumerate(parts):
                    if 'TAKE' in part.upper():
                        take_idx = i
                        break
                
                if take_idx >= 0:
                    # Extract instruction phrase (typically before drug name)
                    instruction_end = take_idx + 15  # Get up to 15 words after TAKE
                    instruction_parts = parts[take_idx:instruction_end]
                    
                    # Stop at drug name keywords
                    final_instruction = []
                    for part in instruction_parts:
                        if any(kw in part.upper() for kw in drug_keywords):
                            break
                        final_instruction.append(part)
                    
                    status = ' '.join(final_instruction)
            
            # Extract drug name
            if has_drug:
                parts = line.split()
                drug_parts = []
                collecting = False
                
                for i, part in enumerate(parts):
                    # Start collecting when we hit a drug keyword
                    if any(kw in part.upper() for kw in drug_keywords):
                        collecting = True
                    
                    # Collect drug-related words (names, dosages, forms)
                    if collecting:
                        # Stop if we hit instruction keywords
                        if any(word in part.upper() for word in ['TAKE', 'BY', 'MOUTH', 'EVERY', 'FOR']):
                            break
                        drug_parts.append(part)
                        
                        # Stop after reasonable drug name length
                        if len(drug_parts) > 8:
                            break
                
                if drug_parts:
                    drug_name = ' '.join(drug_parts)
            
            # Extract Quantity
            if drug_name or status:
                # Look for quantity pattern: number followed by TAB/TABLET/ML
                qty_match = re.search(r'(\d+)\s*(TAB|TABLET|ML|CAPSULE)', line.upper())
                if qty_match:
                    quantity = qty_match.group(1)
                else:
                    # Look for standalone reasonable numbers
                    numbers = re.findall(r'\b(\d{1,3})\b', line)
                    if numbers:
                        # Filter out large numbers (likely dates/IDs)
                        reasonable_qtys = [n for n in numbers if int(n) < 500]
                        if reasonable_qtys:
                            quantity = reasonable_qtys[0]
            
            if status or drug_name or order_key:
                extracted_data.append({
                    'Order Key': order_key if order_key else 'N/A',
                    'Status': status if status else 'N/A',
                    'Drug Name': drug_name if drug_name else 'N/A',
                    'Quantity': quantity if quantity else 'N/A'
                })
        
        return extracted_data
    
    def save_to_csv(self, data, filename=None):
        """
        Save extracted data to CSV file.
        
        Args:
            data: List of dictionaries
            filename: Output filename (auto-generated if None)
        """
        if not data:
            print("⚠️  No data to save")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = self.output_dir / f"primecare_extract_{timestamp}.csv"
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"💾 Data saved to: {filename}")
        print(f"\n📋 Extracted {len(data)} records")
        
        return df
    
    def display_results(self, data):
        """
        Display extracted data in console.
        
        Args:
            data: List of dictionaries
        """
        if not data:
            print("⚠️  No data extracted")
            return
        
        print("\n" + "="*60)
        print("EXTRACTED DATA")
        print("="*60)
        
        df = pd.DataFrame(data)
        print(df.to_string(index=False))
        print("="*60)
    
    def run_full_extraction(self, region=None, method='both'):
        """
        Complete workflow: Capture screenshot and extract data.
        
        Args:
            region: Screen region to capture (None for full screen)
            method: 'table', 'pattern', or 'both'
            
        Returns:
            DataFrame with extracted data
        """
        print("\n🚀 Starting PrimeCare Data Extraction")
        print("="*60)
        
        # Capture screenshot
        screenshot = self.capture_screen(region=region)
        
        # Extract data using selected method(s)
        all_data = []
        
        if method in ['table', 'both']:
            data = self.extract_table_data(screenshot)
            all_data.extend(data)
        
        if method in ['pattern', 'both']:
            data = self.extract_with_template_matching(screenshot)
            all_data.extend(data)
        
        # Remove duplicates
        unique_data = []
        seen = set()
        
        for item in all_data:
            key = (item.get('Order Key', 'N/A'), item['Status'], item['Drug Name'])
            if key not in seen and (item['Drug Name'] != 'N/A' or item.get('Order Key', 'N/A') != 'N/A'):
                seen.add(key)
                unique_data.append(item)
        
        # Display and save results
        self.display_results(unique_data)
        df = self.save_to_csv(unique_data)
        
        print("\n✅ Extraction complete!")
        
        return df


def main():
    """Main execution function."""
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║     PrimeCare Screen Capture & Data Extractor             ║
║     Extract Status and Drug Name from screenshots         ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Initialize extractor
    try:
        extractor = PrimeCareExtractor()
    except Exception as e:
        print(f"❌ Error initializing extractor: {e}")
        print("\n⚠️  Make sure Tesseract OCR is installed:")
        print("   Download: https://github.com/UB-Mannheim/tesseract/wiki")
        return
    
    # Option 1: Capture full screen after countdown
    print("\n⏱️  Screenshot will be taken in 3 seconds...")
    print("   Switch to PrimeCare window now!")
    
    import time
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    # Run extraction
    df = extractor.run_full_extraction(method='both')
    
    # Optional: Specify region if you know coordinates
    # region = (x, y, width, height)
    # df = extractor.run_full_extraction(region=(0, 100, 1280, 500))
    
    print("\n📁 Files saved in:")
    print(f"   Screenshots: {extractor.screenshots_dir}")
    print(f"   Extracted Data: {extractor.output_dir}")


if __name__ == "__main__":
    main()
