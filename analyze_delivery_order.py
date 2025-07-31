import fitz  # PyMuPDF
import sys

def analyze_pdf(pdf_path):
    """Analyze PDF content to understand structure"""
    try:
        doc = fitz.open(pdf_path)
        print(f"📄 PDF Analysis: {pdf_path}")
        print(f"📊 Total pages: {len(doc)}")
        print("=" * 50)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            print(f"\n📋 PAGE {page_num + 1} CONTENT:")
            print("-" * 30)
            print(text)
            print("-" * 30)
            
            # Look for specific patterns
            print("\n🔍 PATTERN ANALYSIS:")
            
            # E-Way Bill patterns
            if "E-Way" in text or "eway" in text.lower() or "D.O." in text:
                print("✅ Found E-Way Bill related content")
            
            # Logistics patterns
            if any(word in text.lower() for word in ["transport", "logistics", "carrier", "delivery"]):
                print("✅ Found logistics related content")
            
            # Address patterns
            if any(word in text.lower() for word in ["address", "pin", "state", "city"]):
                print("✅ Found address related content")
                
    except Exception as e:
        print(f"❌ Error analyzing PDF: {e}")

if __name__ == "__main__":
    pdf_path = r"c:\Users\jaina\Downloads\INV2025G01154_DHYEY ENTERPRISE_Delivery Order G.PDF"
    analyze_pdf(pdf_path)
