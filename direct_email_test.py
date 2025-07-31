#!/usr/bin/env python3
"""
Direct email test using Python mail library
This will test if our local SMTP server can receive emails
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def test_smtp_server():
    """Test the local SMTP server directly"""
    try:
        print("🧪 Testing Local SMTP Server...")
        
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = 'noreply@company.com'
        msg['To'] = 'jainamdedhia@gmail.com'
        msg['Subject'] = f'Test Email from Dispatch System - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        
        body = """
        <html>
        <body>
        <h2>🧪 Test Email Notification</h2>
        <p>This is a test email to verify that the email notification system is working correctly.</p>
        
        <h3>Test Details:</h3>
        <ul>
            <li>SMTP Server: localhost:1025</li>
            <li>Time: {}</li>
            <li>Purpose: Email workflow testing</li>
        </ul>
        
        <p><strong>If you can see this email in the SMTP server console, the email system is working!</strong></p>
        
        <p>Best regards,<br/>
        Dispatch Management System</p>
        </body>
        </html>
        """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        msg.attach(MIMEText(body, 'html'))
        
        # Connect to local SMTP server
        print("📡 Connecting to localhost:1025...")
        server = smtplib.SMTP('localhost', 1025)
        
        # Send email
        print("📧 Sending test email...")
        text = msg.as_string()
        server.sendmail('noreply@company.com', 'jainamdedhia@gmail.com', text)
        server.quit()
        
        print("✅ Test email sent successfully!")
        print("📺 Check the SMTP server console for the email content.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error sending test email: {e}")
        return False

def test_dispatch_workflow_email():
    """Test the dispatch workflow email format"""
    try:
        print("\n🧪 Testing Dispatch Workflow Email Format...")
        
        # Create GRN uploaded notification email
        msg1 = MIMEMultipart()
        msg1['From'] = 'noreply@company.com'
        msg1['To'] = 'jainamdedhia@gmail.com'
        msg1['Subject'] = 'GRN Uploaded - Dispatch Order TEST-001'
        
        body1 = """
        <html>
        <body>
        <p>Dear Admin,</p>
        <p>A GRN has been uploaded for Dispatch Order <strong>TEST-001</strong>.</p>
        <p><strong>Details:</strong></p>
        <ul>
            <li>Order No: SO-TEST-001</li>
            <li>Customer: Test Customer</li>
            <li>Product: Test Product</li>
            <li>Logistics Partner: LOGISTICS WAREHOUSE SERVICES</li>
            <li>E-Way Bill No: EWB123456789</li>
        </ul>
        <p>Status has been updated to <strong>Out for Delivery</strong>.</p>
        <p>Please upload the stamped GRN to proceed with delivery confirmation.</p>
        <p>Best regards,<br/>Dispatch Management System</p>
        </body>
        </html>
        """
        
        msg1.attach(MIMEText(body1, 'html'))
        
        # Create delivery confirmation email
        msg2 = MIMEMultipart()
        msg2['From'] = 'noreply@company.com'
        msg2['To'] = 'jainamdedhia@gmail.com'
        msg2['Subject'] = 'Delivery Confirmation Required - Dispatch Order TEST-001'
        
        body2 = """
        <html>
        <body>
        <p>Dear Admin,</p>
        <p>The stamped GRN has been uploaded for Dispatch Order <strong>TEST-001</strong>.</p>
        <p><strong>Details:</strong></p>
        <ul>
            <li>Order No: SO-TEST-001</li>
            <li>Customer: Test Customer</li>
            <li>Customer Mobile: +91 9876543210</li>
            <li>Customer Email: customer@example.com</li>
            <li>Product: Test Product</li>
            <li>Delivery Location: Mumbai Office</li>
        </ul>
        <p>Status has been updated to <strong>Delivered</strong>.</p>
        <p><strong>Action Required:</strong> Please confirm delivery with the customer and manually mark the status as "Delivery Confirmed" once confirmed.</p>
        <p>Best regards,<br/>Dispatch Management System</p>
        </body>
        </html>
        """
        
        msg2.attach(MIMEText(body2, 'html'))
        
        # Send both emails
        server = smtplib.SMTP('localhost', 1025)
        
        print("📧 Sending GRN uploaded notification...")
        server.sendmail('noreply@company.com', 'jainamdedhia@gmail.com', msg1.as_string())
        
        print("📧 Sending delivery confirmation request...")
        server.sendmail('noreply@company.com', 'jainamdedhia@gmail.com', msg2.as_string())
        
        server.quit()
        
        print("✅ Both workflow emails sent successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error sending workflow emails: {e}")
        return False

def main():
    print("🚀 Email System Test Suite")
    print("=" * 50)
    
    # Test 1: Basic SMTP connectivity
    test1_result = test_smtp_server()
    
    # Test 2: Workflow email format
    test2_result = test_dispatch_workflow_email()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   Basic SMTP Test: {'✅ PASSED' if test1_result else '❌ FAILED'}")
    print(f"   Workflow Email Test: {'✅ PASSED' if test2_result else '❌ FAILED'}")
    
    if test1_result and test2_result:
        print("\n🎉 All tests passed! Your email system is working correctly.")
        print("📺 Check the SMTP server console to see the emails.")
        print("📧 You should see 3 emails total:")
        print("   1. Basic test email")
        print("   2. GRN uploaded notification")
        print("   3. Delivery confirmation request")
    else:
        print("\n⚠️ Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    main()
