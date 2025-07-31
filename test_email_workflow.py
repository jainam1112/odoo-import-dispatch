#!/usr/bin/env python3
"""
Test script to trigger email notifications in the dispatch management system
"""

import xmlrpc.client
import base64

# Odoo connection details
url = 'http://localhost:8069'
db = 'odoo17'  # Replace with your database name
username = 'admin'  # Replace with your username
password = 'admin'  # Replace with your password

def connect_to_odoo():
    """Connect to Odoo and get user ID"""
    try:
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        if uid:
            print(f"✅ Connected to Odoo successfully! User ID: {uid}")
            models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
            return models, uid
        else:
            print("❌ Authentication failed!")
            return None, None
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None, None

def create_sample_grn_file():
    """Create a sample GRN file content"""
    grn_content = """
GOODS RECEIPT NOTE
===================

D.O.No.: EWB123456789
Date: 2024-01-15

To,
LOGISTICS WAREHOUSE SERVICES PVT LTD
123 Industrial Area, Sector 15
Gurgaon, Haryana - 122001

Product: Sample Product
Quantity: 100 Units
E-Way Bill No: EWB123456789

Delivery Location: Mumbai Office
Customer: ABC Corporation

Logistics Partner: LOGISTICS WAREHOUSE SERVICES
"""
    return base64.b64encode(grn_content.encode()).decode()

def test_email_workflow(models, uid):
    """Test the complete email workflow"""
    try:
        print("\n🧪 Testing Email Workflow...")
        
        # 1. Create a dispatch order
        print("1️⃣ Creating dispatch order...")
        dispatch_data = {
            'name': 'TEST-DISPATCH-001',
            'order_no': 'SO-2024-001',
            'partner_id': 1,  # Assuming partner with ID 1 exists
            'product_name': 'Test Product',
            'quantity': 10,
            'state': 'draft'
        }
        
        dispatch_id = models.execute_kw(db, uid, password, 'dispatch.order', 'create', [dispatch_data])
        print(f"✅ Dispatch order created with ID: {dispatch_id}")
        
        # 2. Upload GRN to trigger first email
        print("2️⃣ Uploading GRN to trigger email notification...")
        grn_data = create_sample_grn_file()
        
        models.execute_kw(db, uid, password, 'dispatch.order', 'write', [[dispatch_id], {
            'grn_attachment': grn_data,
            'grn_filename': 'sample_grn.txt'
        }])
        print("✅ GRN uploaded - this should trigger 'GRN Uploaded' email")
        
        # 3. Upload stamped GRN to trigger second email
        print("3️⃣ Uploading stamped GRN to trigger delivery confirmation email...")
        stamped_grn_data = create_sample_grn_file()
        
        models.execute_kw(db, uid, password, 'dispatch.order', 'write', [[dispatch_id], {
            'stamped_grn_attachment': stamped_grn_data,
            'stamped_grn_filename': 'stamped_grn.txt'
        }])
        print("✅ Stamped GRN uploaded - this should trigger 'Delivery Confirmation' email")
        
        # 4. Manually trigger delivery confirmation
        print("4️⃣ Manually confirming delivery...")
        models.execute_kw(db, uid, password, 'dispatch.order', 'action_confirm_delivery_manual', [[dispatch_id]])
        print("✅ Delivery manually confirmed")
        
        # 5. Check final status
        dispatch_record = models.execute_kw(db, uid, password, 'dispatch.order', 'read', [[dispatch_id]], {'fields': ['name', 'state', 'eway_bill_no', 'logistics_partner']})
        print(f"\n📊 Final Status:")
        print(f"   Name: {dispatch_record[0]['name']}")
        print(f"   State: {dispatch_record[0]['state']}")
        print(f"   E-Way Bill: {dispatch_record[0]['eway_bill_no']}")
        print(f"   Logistics Partner: {dispatch_record[0]['logistics_partner']}")
        
        return dispatch_id
        
    except Exception as e:
        print(f"❌ Error during workflow test: {e}")
        return None

def test_direct_email_methods(models, uid, dispatch_id):
    """Test email methods directly"""
    try:
        print("\n📧 Testing direct email methods...")
        
        # Test GRN uploaded notification
        print("1️⃣ Testing GRN uploaded notification...")
        result1 = models.execute_kw(db, uid, password, 'dispatch.order', 'action_send_grn_uploaded_notification', [[dispatch_id]])
        print(f"   Result: {result1}")
        
        # Test delivery confirmation request
        print("2️⃣ Testing delivery confirmation request...")
        result2 = models.execute_kw(db, uid, password, 'dispatch.order', 'action_send_delivery_confirmation_request', [[dispatch_id]])
        print(f"   Result: {result2}")
        
    except Exception as e:
        print(f"❌ Error testing direct email methods: {e}")

def main():
    print("🚀 Starting Email Workflow Test")
    print("=" * 50)
    
    # Connect to Odoo
    models, uid = connect_to_odoo()
    if not models or not uid:
        return
    
    # Test the workflow
    dispatch_id = test_email_workflow(models, uid)
    
    if dispatch_id:
        # Test direct email methods
        test_direct_email_methods(models, uid, dispatch_id)
    
    print("\n" + "=" * 50)
    print("✅ Test completed! Check your SMTP server console for emails.")
    print("📧 You should see 2 emails in the terminal:")
    print("   1. GRN Uploaded notification")
    print("   2. Delivery Confirmation request")

if __name__ == "__main__":
    main()
