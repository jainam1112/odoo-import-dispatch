#!/usr/bin/env python3
"""
Test Email Functionality for Dispatch Management

This script will help test the email notification system
"""

import base64

def create_test_grn_content():
    """Create a simple test GRN content"""
    content = """
TEST GOODS RECEIPT NOTE
======================

D.O.No.: TEST123456
Date: 29-07-2025

To,
TEST LOGISTICS WAREHOUSE
Test Address Line 1
Test City - 400001

Dear Team,

This is a test GRN for email notification testing.

Product: Test Widget
Quantity: 10 units
Order No: TEST001

Best regards,
Test Team
"""
    return base64.b64encode(content.encode()).decode()

if __name__ == "__main__":
    print("Test GRN Content (Base64):")
    print(create_test_grn_content())
    print("\nTo test emails:")
    print("1. Create dispatch order")
    print("2. Upload above content as GRN")
    print("3. Check Settings > Technical > Email > Emails")
