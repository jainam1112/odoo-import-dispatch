import fitz  # PyMuPDF
import re
import base64
import io

def test_delivery_order_extraction():
    """Test extraction from the provided delivery order PDF"""
    pdf_path = r"c:\Users\jaina\Downloads\INV2025G01154_DHYEY ENTERPRISE_Delivery Order G.PDF"
    
    try:
        # Open and read PDF
        doc = fitz.open(pdf_path)
        first_page = doc[0].get_text()
        
        print("🔍 TESTING DELIVERY ORDER EXTRACTION")
        print("=" * 50)
        
        data = {}
        
        # Extract E-Way Bill No. from D.O.No.
        do_patterns = [
            r'D\.O\.No\.?\s*:?\s*([A-Z0-9]+)',
            r'DO\s*No\.?\s*:?\s*([A-Z0-9]+)',
            r'Delivery\s*Order\s*No\.?\s*:?\s*([A-Z0-9]+)',
            r'D\.O\.No\.?\s*:?\s*\n\s*([A-Z0-9]+)',  # Handle newlines
        ]
        for pattern in do_patterns:
            match = re.search(pattern, first_page, re.IGNORECASE)
            if match:
                data['eway_bill_no'] = match.group(1).strip()
                print(f"✅ E-Way Bill No: {data['eway_bill_no']}")
                break
        
        # Extract Logistics Partner Information
        warehouse_patterns = [
            r'To,\s*([A-Z\s]+WAREHOUSE[A-Z\s-]*)',
            r'To,\s*([A-Z\s]+LOGISTICS[A-Z\s-]*)',
            r'To,\s*([A-Z\s]+TRANSPORT[A-Z\s-]*)',
            r'To,\s*([A-Z][A-Z\s-]+)(?=\n)',
        ]
        for pattern in warehouse_patterns:
            match = re.search(pattern, first_page, re.IGNORECASE)
            if match:
                logistics_name = match.group(1).strip()
                logistics_name = re.sub(r'\s+', ' ', logistics_name)
                if len(logistics_name) > 5:
                    data['logistics_partner'] = logistics_name
                    print(f"✅ Logistics Partner: {data['logistics_partner']}")
                    break
        
        # Extract Logistics Address
        if 'logistics_partner' in data:
            partner_index = first_page.find(data['logistics_partner'])
            if partner_index != -1:
                remaining_text = first_page[partner_index + len(data['logistics_partner']):]
                address_lines = []
                lines = remaining_text.split('\n')
                for line in lines[:4]:
                    line = line.strip()
                    if line and not line.startswith('Tel') and not line.startswith('D.O'):
                        address_lines.append(line)
                    elif line.startswith('Tel') or line.startswith('D.O'):
                        break
                if address_lines:
                    data['logistics_address'] = '\n'.join(address_lines)
                    print(f"✅ Logistics Address: {data['logistics_address']}")
        
        # Extract Delivery Location (customer address)
        customer_patterns = [
            r'M/s\.\s*([A-Z\s]+)(?:\n|\r)',
            r'To\s*M/s\.\s*([A-Z\s]+)(?:\n|\r)',
        ]
        for pattern in customer_patterns:
            match = re.search(pattern, first_page, re.IGNORECASE)
            if match:
                customer_name = match.group(1).strip()
                customer_index = first_page.find(customer_name)
                if customer_index != -1:
                    remaining_text = first_page[customer_index + len(customer_name):]
                    address_lines = []
                    lines = remaining_text.split('\n')
                    for line in lines[:3]:
                        line = line.strip()
                        if line and not line.startswith('Sno') and not line.startswith('Description'):
                            address_lines.append(line)
                        elif line.startswith('Sno') or line.startswith('Description'):
                            break
                    if address_lines:
                        data['delivery_location'] = '\n'.join(address_lines)
                        print(f"✅ Delivery Location: {data['delivery_location']}")
                break
        
        print("\n📋 EXTRACTION SUMMARY:")
        print("-" * 30)
        for key, value in data.items():
            print(f"{key}: {value}")
        
        return data
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {}

if __name__ == "__main__":
    test_delivery_order_extraction()
