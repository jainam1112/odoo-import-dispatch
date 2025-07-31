#!/usr/bin/env python3
"""
Simple Local SMTP Server for Testing Email Functionality
This server will print all emails to console instead of sending them
"""

import asyncio
import sys
from aiosmtpd import controller
from email import message_from_bytes

class EmailHandler:
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        print(f"\n📧 Email TO: {address}")
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        print("\n" + "="*60)
        print("📨 NEW EMAIL RECEIVED")
        print("="*60)
        
        print(f"From: {envelope.mail_from}")
        print(f"To: {', '.join(envelope.rcpt_tos)}")
        
        try:
            # Parse the email content
            msg = message_from_bytes(envelope.content)
            print(f"Subject: {msg.get('Subject', 'No Subject')}")
            print(f"Date: {msg.get('Date', 'No Date')}")
            print("\n--- EMAIL BODY ---")
            
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        print(part.get_payload(decode=True).decode())
                        break
                    elif part.get_content_type() == "text/html":
                        print("HTML Email Content:")
                        print(part.get_payload(decode=True).decode())
                        break
            else:
                print(msg.get_payload())
                
        except Exception as e:
            print(f"Error parsing email: {e}")
            print("Raw content:")
            print(envelope.content.decode('utf-8', errors='ignore'))
        
        print("="*60)
        print("✅ Email logged successfully!")
        print("="*60 + "\n")
        
        return '250 Message accepted for delivery'

def start_smtp_server():
    """Start the local SMTP server"""
    handler = EmailHandler()
    controller_instance = controller.Controller(handler, hostname='localhost', port=1025)
    
    print("🚀 Starting Local SMTP Server...")
    print("📍 Server: localhost:1025")
    print("📧 All emails will be displayed in this console")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        controller_instance.start()
        print("✅ SMTP Server started successfully!")
        print("🔗 Configure Odoo with: localhost:1025 (no authentication)")
        
        # Keep the server running
        try:
            asyncio.get_event_loop().run_forever()
        except KeyboardInterrupt:
            pass
            
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("💡 Trying alternative method...")
        return False
    finally:
        controller_instance.stop()
        print("\n🛑 SMTP Server stopped")
    
    return True

if __name__ == "__main__":
    try:
        start_smtp_server()
    except ImportError:
        print("❌ aiosmtpd not available. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "aiosmtpd"])
        print("✅ Installation complete. Restarting server...")
        start_smtp_server()
    except Exception as e:
        print(f"❌ Could not start SMTP server: {e}")
        print("💡 Please install aiosmtpd: pip install aiosmtpd")
