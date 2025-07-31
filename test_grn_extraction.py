import fitz  # PyMuPDF
import re
import base64

def test_grn_extraction():
    """Test GRN extraction functionality"""
    pdf_path = r"c:\Users\jaina\Downloads\INV2025G01154_DHYEY ENTERPRISE_Delivery Order G.PDF"
    
    try:
        # Read PDF file as base64 (simulate file upload)
        with open(pdf_path, 'rb') as f:
            pdf_binary = f.read()
            pdf_base64 = base64.b64encode(pdf_binary)
        
        # Extract from base64 (simulate Odoo processing)
        pdf_bytes = base64.b64decode(pdf_base64)
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        first_page = doc[0].get_text()
        
        print("🔍 TESTING GRN EXTRACTION FUNCTIONALITY")
        print("=" * 50)
        
        data = {}
        
        # Extract E-Way Bill No. from D.O.No.
        do_patterns = [
            r'D\.O\.No\.?\s*:?\s*([A-Z0-9]+)',
            r'DO\s*No\.?\s*:?\s*([A-Z0-9]+)',
            r'Delivery\s*Order\s*No\.?\s*:?\s*([A-Z0-9]+)',
            r'D\.O\.No\.?\s*:?\s*\n\s*([A-Z0-9]+)',  # Handle newlines
            r'E-Way\s*Bill\s*No\.?\s*:?\s*([A-Z0-9]+)',
            r'Eway\s*Bill\s*:?\s*([A-Z0-9]+)',
        ]
        
        print("📋 Looking for E-Way Bill patterns:")
        for i, pattern in enumerate(do_patterns):
            match = re.search(pattern, first_page, re.IGNORECASE)
            print(f"  Pattern {i+1}: {pattern}")
            if match:
                data['eway_bill_no'] = match.group(1).strip()
                print(f"  ✅ MATCH: {data['eway_bill_no']}")
                break
            else:
                print("  ❌ No match")
        
        # Extract Logistics Partner Information
        warehouse_patterns = [
            r'To,?\s*([A-Z\s]+WAREHOUSE[A-Z\s-]*)',
            r'To,?\s*([A-Z\s]+LOGISTICS[A-Z\s-]*)',
            r'To,?\s*([A-Z\s]+TRANSPORT[A-Z\s-]*)',
            r'To,?\s*([A-Z][A-Z\s-]+)(?=\n)',
            r'Logistics\s*Partner[:\s]*([A-Z\s-]+)',
            r'Transport\s*Company[:\s]*([A-Z\s-]+)',
        ]
        
        print("\n📋 Looking for Logistics Partner patterns:")
        for i, pattern in enumerate(warehouse_patterns):
            match = re.search(pattern, first_page, re.IGNORECASE)
            print(f"  Pattern {i+1}: {pattern}")
            if match:
                logistics_name = match.group(1).strip()
                logistics_name = re.sub(r'\s+', ' ', logistics_name)
                if len(logistics_name) > 5:
                    data['logistics_partner'] = logistics_name
                    print(f"  ✅ MATCH: {data['logistics_partner']}")
                    break
            print("  ❌ No match")
        
        # Extract Logistics Address
        if 'logistics_partner' in data:
            print(f"\n📋 Looking for address after: {data['logistics_partner']}")
            partner_index = first_page.find(data['logistics_partner'])
            if partner_index != -1:
                remaining_text = first_page[partner_index + len(data['logistics_partner']):]
                address_lines = []
                lines = remaining_text.split('\n')
                for line in lines[:4]:
                    line = line.strip()
                    if line and not line.startswith('Tel') and not line.startswith('D.O') and not line.startswith('Dear'):
                        address_lines.append(line)
                        print(f"  Address line: {line}")
                    elif line.startswith('Tel') or line.startswith('D.O') or line.startswith('Dear'):
                        print(f"  Stopping at: {line}")
                        break
                if address_lines:
                    data['logistics_address'] = '\n'.join(address_lines)
                    print(f"  ✅ Complete address: {data['logistics_address']}")
        
        print("\n📋 FINAL EXTRACTION RESULTS:")
        print("-" * 40)
        for key, value in data.items():
            print(f"{key}: {value}")
        
        if not data:
            print("❌ No data extracted. Check patterns or PDF content.")
        
        return data
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {}

if __name__ == "__main__":
    test_grn_extraction()
