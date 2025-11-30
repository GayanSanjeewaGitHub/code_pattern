# Installation and Setup Guide

## Step 1: Install Tesseract OCR

### Download Tesseract
1. Go to: https://github.com/UB-Mannheim/tesseract/wiki
2. Download Windows installer: `tesseract-ocr-w64-setup-5.3.3.20231005.exe`
3. Run installer
4. **Important**: Remember installation path (default: `C:\Program Files\Tesseract-OCR\`)

### Verify Installation
```powershell
# Check if tesseract is accessible
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
```

## Step 2: Install Python Dependencies

```powershell
# Navigate to desk folder
cd d:\DailyGITHUB_DistinGuished_Engineer\2025 Nov\code_pattern\desk

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Run the Extractor

### Option A: Capture New Screenshot
```powershell
python screenshot_extractor.py
```
- 3-second countdown
- Switch to PrimeCare window
- Screenshot captured automatically
- Data extracted and saved

### Option B: Extract from Existing Image
```powershell
python extract_from_file.py path\to\screenshot.png
```

### Option C: Batch Process Multiple Screenshots
```powershell
# Place all screenshots in screenshots/ folder
python extract_from_file.py
```

## Step 4: View Results

### Check Output
```powershell
# View extracted CSV
cd extracted_data
notepad primecare_extract_*.csv

# View screenshots
cd ..\screenshots
explorer .
```

## Quick Test

```powershell
# Test installation
python -c "from screenshot_extractor import PrimeCareExtractor; print('✅ Installation successful!')"
```

## Troubleshooting

### Issue: "tesseract is not installed"
**Solution**: 
```powershell
# Verify tesseract path
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --version

# If different path, update in code:
# tesseract_path=r"YOUR_PATH\tesseract.exe"
```

### Issue: "No module named 'pytesseract'"
**Solution**:
```powershell
pip install --upgrade pytesseract pillow opencv-python
```

### Issue: "No data extracted"
**Solutions**:
1. Check screenshot quality in `screenshots/` folder
2. Ensure PrimeCare table is visible
3. Try capturing specific region
4. Verify Tesseract is working: `tesseract --version`

## Examples

### Example 1: Full Screen Capture
```python
from screenshot_extractor import PrimeCareExtractor

extractor = PrimeCareExtractor()
df = extractor.run_full_extraction()
print(df)
```

### Example 2: Specific Region
```python
from screenshot_extractor import PrimeCareExtractor

extractor = PrimeCareExtractor()
# Capture only table area: (x, y, width, height)
df = extractor.run_full_extraction(region=(100, 200, 1200, 600))
```

### Example 3: Custom Processing
```python
from screenshot_extractor import PrimeCareExtractor
from PIL import Image

extractor = PrimeCareExtractor()

# Take screenshot
img = extractor.capture_screen()

# Extract using preferred method
data = extractor.extract_table_data(img)  # or extract_with_template_matching(img)

# Display
extractor.display_results(data)

# Save
extractor.save_to_csv(data)
```

## File Structure After Setup

```
desk/
├── screenshot_extractor.py       # Main script
├── extract_from_file.py          # Extract from existing images
├── requirements.txt              # Dependencies
├── SETUP.md                      # This file
├── README.md                     # Documentation
├── screenshots/                  # Auto-created: Captured screenshots
│   └── primecare_20251127_*.png
└── extracted_data/               # Auto-created: Extracted CSV files
    └── primecare_extract_*.csv
```

## Next Steps

1. ✅ Install Tesseract
2. ✅ Install Python dependencies
3. ✅ Run test capture
4. ✅ Review extracted data
5. 🚀 Integrate into your workflow!
