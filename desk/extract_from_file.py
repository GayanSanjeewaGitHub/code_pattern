"""
Quick Example: Extract from Existing Screenshot
==============================================
Use this if you already have a screenshot and want to extract data from it.
"""

from screenshot_extractor import PrimeCareExtractor
from PIL import Image
from pathlib import Path


def extract_from_file(image_path):
    """
    Extract Status and Drug Name from an existing screenshot file.
    
    Args:
        image_path: Path to screenshot image file
    """
    print(f"\n📂 Loading image: {image_path}")
    
    # Initialize extractor
    extractor = PrimeCareExtractor()
    
    # Load image
    image = Image.open(image_path)
    
    # Extract data using both methods
    print("\n🔍 Method 1: Table Structure Parsing")
    data1 = extractor.extract_table_data(image)
    extractor.display_results(data1)
    
    print("\n🔍 Method 2: Pattern Matching")
    data2 = extractor.extract_with_template_matching(image)
    extractor.display_results(data2)
    
    # Combine and remove duplicates
    all_data = data1 + data2
    unique_data = []
    seen = set()
    
    for item in all_data:
        key = (item['Status'], item['Drug Name'])
        if key not in seen and item['Drug Name'] != 'N/A':
            seen.add(key)
            unique_data.append(item)
    
    # Save to CSV
    if unique_data:
        df = extractor.save_to_csv(unique_data)
        print("\n✅ Extraction complete!")
        return df
    else:
        print("\n⚠️  No data extracted. Check image quality or OCR settings.")
        return None


def batch_extract_from_folder(folder_path="screenshots"):
    """
    Extract data from all screenshots in a folder.
    
    Args:
        folder_path: Path to folder containing screenshots
    """
    extractor = PrimeCareExtractor()
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"❌ Folder not found: {folder_path}")
        return
    
    # Get all image files
    image_files = list(folder.glob("*.png")) + list(folder.glob("*.jpg"))
    
    if not image_files:
        print(f"⚠️  No images found in {folder_path}")
        return
    
    print(f"\n📁 Found {len(image_files)} images")
    
    all_results = []
    
    for img_file in image_files:
        print(f"\n{'='*60}")
        print(f"Processing: {img_file.name}")
        print(f"{'='*60}")
        
        try:
            image = Image.open(img_file)
            data = extractor.extract_table_data(image)
            
            if data:
                # Add source filename
                for item in data:
                    item['Source'] = img_file.name
                
                all_results.extend(data)
                print(f"✅ Extracted {len(data)} records")
            else:
                print(f"⚠️  No data extracted from {img_file.name}")
                
        except Exception as e:
            print(f"❌ Error processing {img_file.name}: {e}")
    
    # Save combined results
    if all_results:
        output_file = extractor.output_dir / "batch_extract_combined.csv"
        df = extractor.save_to_csv(all_results, filename=output_file)
        print(f"\n✅ Batch extraction complete! Total records: {len(all_results)}")
        return df
    else:
        print("\n⚠️  No data extracted from any images")
        return None


if __name__ == "__main__":
    import sys
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║  PrimeCare Extract from Existing Screenshot              ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Example 1: Extract from specific file
    if len(sys.argv) > 1:
        # Use file path from command line argument
        image_path = sys.argv[1]
        extract_from_file(image_path)
    
    # Example 2: Batch process all screenshots
    elif Path("screenshots").exists() and list(Path("screenshots").glob("*.png")):
        print("\n📂 Found screenshots folder. Processing all images...")
        batch_extract_from_folder("screenshots")
    
    # Example 3: Use sample if available
    else:
        print("\nUsage:")
        print("  python extract_from_file.py <image_path>")
        print("\nOr place images in 'screenshots/' folder for batch processing")
        print("\nExample:")
        print("  python extract_from_file.py primecare_screenshot.png")
