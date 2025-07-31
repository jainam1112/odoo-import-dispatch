"""
Manual Email Test Instructions
==============================

Since we have the local SMTP server running, let's test the email workflow manually:

1. Go to http://localhost:8069 in your browser
2. Login to Odoo
3. Navigate to Dispatch Management → Dispatch Orders
4. Create a new dispatch order with these details:
   - Order No: TEST-EMAIL-001
   - Product: Test Product
   - Quantity: 10
   - Customer: Select any customer

5. Save the dispatch order

6. Upload the test GRN file (test_grn.txt) in the "Goods Receipt Note" field
   - This should automatically change status to "Out for Delivery"
   - This should trigger the first email notification

7. Upload a stamped GRN file in the "Stamped GRN" field
   - This should automatically change status to "Delivered"  
   - This should trigger the second email notification

8. Click the "Confirm Delivery" button
   - This should change status to "Delivery Confirmed"

Expected Results:
- You should see 2 emails appear in the SMTP server console
- Email 1: "GRN Uploaded - Dispatch Order [ORDER_NAME]"
- Email 2: "Delivery Confirmation Required - Dispatch Order [ORDER_NAME]"

The SMTP server console should show something like:
📧 Email TO: jainamdedhia@gmail.com
📧 Subject: GRN Uploaded - Dispatch Order TEST-EMAIL-001
📧 Email TO: jainamdedhia@gmail.com  
📧 Subject: Delivery Confirmation Required - Dispatch Order TEST-EMAIL-001
"""

print(__doc__)
