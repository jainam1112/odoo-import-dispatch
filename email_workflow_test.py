#!/usr/bin/env python3
"""
Email Workflow Test Script for Dispatch Management

This script demonstrates the new email notification workflow:
1. When GRN is uploaded → Status changes to 'Out for Delivery' → Email to Admin
2. When Stamped GRN is uploaded → Status changes to 'Delivered' → Email to Admin for customer confirmation
3. Admin manually confirms delivery → Status changes to 'Delivery Confirmed'

Usage:
- Upload a GRN file to see status change and email notification
- Upload a stamped GRN to see the next status change and email
- Use the "Confirm Delivery" button to complete the workflow
"""

import base64
import os

def create_sample_grn():
    """Create a sample GRN content for testing"""
    sample_content = """
GOODS RECEIPT NOTE
==================

D.O.No.: EWB12345678
Date: 29-07-2025

To,
ACME LOGISTICS WAREHOUSE
Plot No. 123, Industrial Area
Mumbai - 400001
Tel: 022-12345678

Dear Sir/Madam,

We have received the following goods:

Product: Widget ABC
Quantity: 100 units
Order No: ORD001

Logistics Partner: ACME LOGISTICS WAREHOUSE

Please find the attached delivery documents.

Best regards,
Warehouse Team
"""
    return base64.b64encode(sample_content.encode()).decode()

def create_sample_stamped_grn():
    """Create a sample stamped GRN content for testing"""
    sample_content = """
GOODS RECEIPT NOTE - STAMPED
=============================

D.O.No.: EWB12345678
Date: 29-07-2025
RECEIVED & VERIFIED

To,
ACME LOGISTICS WAREHOUSE
Plot No. 123, Industrial Area
Mumbai - 400001
Tel: 022-12345678

DELIVERY CONFIRMED BY CUSTOMER
STAMP: [CUSTOMER STAMP HERE]
SIGNATURE: [CUSTOMER SIGNATURE]

Product: Widget ABC
Quantity: 100 units
Order No: ORD001

Status: DELIVERED SUCCESSFULLY

Best regards,
Warehouse Team
"""
    return base64.b64encode(sample_content.encode()).decode()

if __name__ == "__main__":
    print("Email Workflow Test Data Generated")
    print("=" * 50)
    print(f"Sample GRN (Base64): {create_sample_grn()[:50]}...")
    print(f"Sample Stamped GRN (Base64): {create_sample_stamped_grn()[:50]}...")
    
    print("\nWorkflow Steps:")
    print("1. Create a new Dispatch Order")
    print("2. Upload the sample GRN → Status changes to 'Out for Delivery' → Admin gets email")
    print("3. Upload the stamped GRN → Status changes to 'Delivered' → Admin gets confirmation email")
    print("4. Click 'Confirm Delivery' → Status changes to 'Delivery Confirmed'")
    
    print("\nEmail Configuration:")
    print("- Set admin email in Settings → Dispatch Management")
    print("- Configure outgoing mail server for actual email sending")
    print("- Check mail logs in Settings → Technical → Email → Emails")
