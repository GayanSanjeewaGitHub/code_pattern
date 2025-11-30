# PrimeCare Screen Capture & Data Extractor

Automated screenshot capture and data extraction tool for PrimeCare pharmacy system.

## Features

✅ **Automatic Screenshot Capture** - Captures Windows screen with countdown
✅ **OCR Text Extraction** - Extracts Status and Drug Name using Tesseract
✅ **Image Preprocessing** - Enhances image quality for better accuracy
✅ **Dual Extraction Methods** - Table structure parsing + Pattern matching
✅ **CSV Export** - Saves extracted data to CSV with timestamps
✅ **Organized Output** - Separate folders for screenshots and extracted data

## Installation

### 1. Install Tesseract OCR (Required)

Download and install Tesseract for Windows:
- Download: https://github.com/UB-Mannheim/tesseract/wiki
- Direct link: https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe
- Default installation path: `C:\Program Files\Tesseract-OCR\`

**Important**: During installation, note the installation path!

### 2. Install Python Dependencies

```powershell
cd desk
pip install -r requirements.txt
```

## Usage

### Basic Usage (Full Screen)

```powershell
python screenshot_extractor.py
```

The script will:
1. Show 3-second countdown
2. Capture full screen
3. Extract Status and Drug Name
4. Save to CSV and display results

### Advanced Usage (In Your Code)

```python
from screenshot_extractor import PrimeCareExtractor

# Initialize
extractor = PrimeCareExtractor()

# Capture and extract
df = extractor.run_full_extraction()

# Capture specific region (x, y, width, height)
df = extractor.run_full_extraction(region=(100, 200, 1200, 600))

# Use specific extraction method
df = extractor.run_full_extraction(method='table')  # or 'pattern' or 'both'
```

### Custom Tesseract Path

If Tesseract is installed in a different location:

```python
extractor = PrimeCareExtractor(
    tesseract_path=r"D:\Custom\Path\tesseract.exe"
)
```

## Output Structure

```
desk/
├── screenshots/                    # Captured screenshots
│   └── primecare_20251127_143052.png
├── extracted_data/                 # Extracted CSV files
│   └── primecare_extract_20251127_143052.csv
└── screenshot_extractor.py         # Main script
```

## Extracted Data Format

CSV columns:
- **Status**: Patient prescription status (P, F, R, etc.)
- **Drug Name**: Full drug name with dosage (e.g., "OXYCODONE HCL 5 MG TABLET")
- **Row**: Row number

Example output:
```
Status,Drug Name,Row
P,OXYCODONE HCL 5 MG TABLET PO,1
P,LORAZEPAM 0.5 MG TABLET PO,2
F,OXYCODONE HCL 10 MG TABLET PO,3
```

## Methods

### PrimeCareExtractor Class

#### `capture_screen(region=None, save=True)`
Captures screenshot of entire screen or specific region.

**Parameters:**
- `region`: Tuple (x, y, width, height) or None for full screen
- `save`: Boolean to save screenshot to file

**Returns:** PIL Image object

#### `extract_table_data(image)`
Extracts data using table structure parsing.

**Parameters:**
- `image`: PIL Image object

**Returns:** List of dictionaries with Status and Drug Name

#### `extract_with_template_matching(image)`
Extracts data using pattern matching for PrimeCare specific formats.

**Parameters:**
- `image`: PIL Image object

**Returns:** List of dictionaries with Status and Drug Name

#### `run_full_extraction(region=None, method='both')`
Complete workflow: capture + extract + save.

**Parameters:**
- `region`: Screen region to capture
- `method`: 'table', 'pattern', or 'both'

**Returns:** Pandas DataFrame

## Troubleshooting

### Error: "tesseract is not installed"

**Solution**: Install Tesseract OCR from the link above and ensure it's in the correct path.

### Error: "pytesseract.pytesseract.TesseractNotFoundError"

**Solution**: Update the tesseract path:
```python
extractor = PrimeCareExtractor(
    tesseract_path=r"C:\Your\Custom\Path\tesseract.exe"
)
```

### Low Accuracy / Wrong Extraction

**Solutions:**
1. Ensure PrimeCare window is maximized and clearly visible
2. Use higher screen resolution
3. Capture specific region instead of full screen:
   ```python
   df = extractor.run_full_extraction(region=(50, 100, 1200, 500))
   ```
4. Adjust preprocessing parameters in `preprocess_image()` method

### No Data Extracted

**Solutions:**
1. Check if screenshot captured the correct window
2. Verify table is visible in screenshot
3. Try different extraction method: `method='pattern'`
4. Manually check saved screenshot in `screenshots/` folder

## How It Works

### 1. Screenshot Capture
Uses `pyautogui` to capture Windows screen with 3-second countdown.

### 2. Image Preprocessing
- Converts to grayscale
- Applies OTSU thresholding
- Denoises using OpenCV
- Enhances contrast

### 3. OCR Extraction
- Uses Tesseract OCR to extract text with coordinates
- Filters low-confidence results

### 4. Data Parsing
**Table Method**: Groups text by row coordinates, identifies columns
**Pattern Method**: Matches medical terminology and status codes

### 5. Output Generation
- Removes duplicates
- Saves to timestamped CSV
- Displays in console

## Performance Tips

1. **Use Region Capture** for faster processing:
   ```python
   df = extractor.run_full_extraction(region=(0, 100, 1280, 500))
   ```

2. **Single Method** if one works better:
   ```python
   df = extractor.run_full_extraction(method='table')
   ```

3. **Batch Processing** multiple screenshots:
   ```python
   for screenshot_file in Path("screenshots").glob("*.png"):
       image = Image.open(screenshot_file)
       data = extractor.extract_table_data(image)
       extractor.save_to_csv(data, f"output_{screenshot_file.stem}.csv")
   ```

## Requirements

- Python 3.8+
- Windows OS
- Tesseract OCR 5.0+
- Dependencies in requirements.txt

## License

MIT License - See LICENSE file

## Support

For issues or questions:
1. Check Troubleshooting section
2. Verify Tesseract installation
3. Check screenshot quality in `screenshots/` folder
4. Review extracted data in `extracted_data/` folder
