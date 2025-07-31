#!/usr/bin/env python3
"""
Simple email test using Odoo shell
Run this from Odoo shell: python odoo-bin shell -d your_database
"""

def test_email_notification():
    """Test email notification function"""
    # Get the dispatch order model
    DispatchOrder = env['dispatch.order']
    
    # Get admin email from config
    admin_email = env['ir.config_parameter'].sudo().get_param('dispatch.admin_email', 'admin@example.com')
    print(f"Admin email configured: {admin_email}")
    
    # Create a test dispatch order
    test_order = DispatchOrder.create({
        'name': 'TEST-EMAIL-001',
        'order_no': 'SO-EMAIL-TEST-001',
        'product_name': 'Test Product for Email',
        'quantity': 5,
        'state': 'draft'
    })
    print(f"Created test dispatch order: {test_order.name}")
    
    # Test email notification methods
    print("\n1. Testing GRN uploaded notification...")
    result1 = test_order.action_send_grn_uploaded_notification()
    print(f"GRN notification result: {result1}")
    
    print("\n2. Testing delivery confirmation request...")
    result2 = test_order.action_send_delivery_confirmation_request()
    print(f"Delivery confirmation result: {result2}")
    
    # Check mail queue
    mail_queue = env['mail.mail'].search([('subject', 'ilike', test_order.name)])
    print(f"\n📧 Emails in queue: {len(mail_queue)}")
    for mail in mail_queue:
        print(f"   - Subject: {mail.subject}")
        print(f"   - To: {mail.email_to}")
        print(f"   - State: {mail.state}")
    
    print("\n✅ Email test completed!")
    return test_order

# Run the test
if __name__ == "__main__":
    test_order = test_email_notification()
