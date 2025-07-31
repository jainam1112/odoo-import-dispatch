## Gmail SMTP Configuration Summary

## Local SMTP Server Configuration (Recommended for Testing)

### Server Details:
- **SMTP Server:** localhost
- **Port:** 1025
- **Security:** None (No encryption)
- **Username:** (leave empty)
- **Password:** (leave empty)
- **Server Name:** Local SMTP Server

### Configuration Details:
- **SMTP Server:** smtp.gmail.com
- **Port:** 587
- **Security:** TLS (STARTTLS)
- **Username:** jainamdedhia@gmail.com
- **Password:** utjw twut vzqd xvzt

### Local SMTP Server Setup:
1. Local SMTP server is already running on localhost:1025
2. All emails will be displayed in the terminal console
3. No authentication required
4. Perfect for testing email functionality

### Gmail App Password Setup:
1. Go to Google Account Settings
2. Security > 2-Step Verification > App passwords
3. Select "Mail" > Generate
4. Copy the 16-character password (format: xxxx xxxx xxxx xxxx)
5. Use this password in Odoo (remove spaces): utjwtwutvzqdxvzt

### Testing Steps:
1. Configure SMTP server in Odoo
2. Test connection
3. Create dispatch order
4. Upload GRN file
5. Check your Gmail inbox for notification

### Troubleshooting:
- Ensure 2-Step Verification is enabled on Gmail
- Use App Password, not regular Gmail password
- Check spam/junk folder for emails
- Verify SMTP settings are exactly as specified

### Alternative Test (Without Gmail):
If you want to test without configuring Gmail:
- Go to Settings → Technical → Email → Emails
- Check if emails are queued in the system
- You can see email content even without sending
