# Amazon Lightsail Deployment Instructions

## 🚀 Quick Start (30 minutes)

### Step 1: Create Lightsail Instance

1. **Login to AWS Console**
   - Go to [AWS Lightsail Console](https://lightsail.aws.amazon.com/)
   - Click "Create instance"

2. **Configure Instance**
   - **Platform**: Linux/Unix
   - **Blueprint**: Ubuntu 22.04 LTS
   - **Instance plan**: $20/month (4 GB RAM, 2 vCPUs, 80 GB SSD)
   - **Instance name**: `odoo-dispatch-server`

3. **Create Static IP** (Optional but recommended)
   - Go to Networking → Static IPs
   - Create static IP and attach to your instance
   - Cost: $5/month

### Step 2: Connect and Deploy

1. **Connect via SSH**
   ```bash
   # From Lightsail console, click "Connect using SSH"
   # Or use your own SSH client:
   ssh ubuntu@YOUR_STATIC_IP
   ```

2. **Switch to root**
   ```bash
   sudo su -
   ```

3. **Run Quick Deploy**
   ```bash
   # Download and run the deployment script
   curl -sSL https://raw.githubusercontent.com/jainam1112/odoo-import-dispatch/main/deployment/scripts/quick-deploy.sh | bash
   ```

### Step 3: Upload Your Module

1. **Copy dispatch management module**
   ```bash
   # From your local machine:
   scp -r ./dispatch_management ubuntu@YOUR_STATIC_IP:/opt/odoo-dispatch/addons/
   
   # On the server:
   sudo chown -R root:root /opt/odoo-dispatch/addons/
   cd /opt/odoo-dispatch
   docker-compose restart odoo
   ```

### Step 4: Configure Odoo

1. **Access Odoo**
   - Open browser: `http://YOUR_STATIC_IP:8069`
   - Create database: `dispatch_production`
   - Install your `dispatch_management` module

2. **Configure SMTP** (for emails)
   - Go to Settings → Technical → Email → Outgoing Mail Servers
   - Use Gmail SMTP or Amazon SES

---

## 🏭 Production Deployment (2 hours)

### Step 1: Domain Setup

1. **Point your domain to Lightsail**
   - Add A record: `yourdomain.com` → `YOUR_STATIC_IP`
   - Add CNAME record: `www.yourdomain.com` → `yourdomain.com`

### Step 2: Full Production Deploy

1. **Upload deployment files**
   ```bash
   # Upload the entire deployment folder
   scp -r ./deployment ubuntu@YOUR_STATIC_IP:/tmp/
   ```

2. **Run production deployment**
   ```bash
   ssh ubuntu@YOUR_STATIC_IP
   sudo su -
   cd /tmp/deployment
   chmod +x scripts/deploy.sh
   ./scripts/deploy.sh
   ```

3. **Follow prompts**
   - Enter your domain name
   - Enter your email address
   - Script will handle SSL, security, and configuration

---

## 📊 Cost Breakdown

### Monthly Costs
- **Lightsail Instance (4GB)**: $20/month
- **Static IP**: $5/month
- **Domain** (optional): $10-15/year
- **Total**: ~$25/month

### One-time Setup
- Domain registration: $10-15/year
- Development time: 2-4 hours

---

## 🔧 Management Commands

### On the server:

```bash
# View logs
cd /opt/odoo-dispatch
docker-compose logs -f

# Restart services
docker-compose restart

# Update application
./scripts/update.sh

# Create backup
./scripts/backup.sh

# Monitor resources
htop
docker stats
```

---

## 🔐 Security Features

✅ **Automatic SSL** (Let's Encrypt)  
✅ **Firewall** (UFW configured)  
✅ **Fail2ban** (Brute force protection)  
✅ **Nginx rate limiting**  
✅ **Daily backups**  
✅ **Security headers**  

---

## 📱 Monitoring & Maintenance

### Daily Tasks (Automated)
- Database backups
- SSL certificate renewal
- Log rotation

### Weekly Tasks (Manual)
- Check system resources
- Review logs for errors
- Test backup restoration

### Monthly Tasks (Manual)
- Update system packages
- Review security logs
- Performance optimization

---

## 🆘 Troubleshooting

### Common Issues

1. **Can't access Odoo**
   ```bash
   # Check if services are running
   docker-compose ps
   
   # Check firewall
   sudo ufw status
   
   # Check logs
   docker-compose logs odoo
   ```

2. **Database connection errors**
   ```bash
   # Restart database
   docker-compose restart db
   
   # Check database logs
   docker-compose logs db
   ```

3. **SSL certificate issues**
   ```bash
   # Renew certificate manually
   sudo certbot renew
   
   # Check certificate status
   sudo certbot certificates
   ```

### Get Help
- Check logs: `/opt/odoo-dispatch/nginx/logs/`
- System logs: `journalctl -f`
- Contact support with error details

---

## 🚀 Ready to Deploy?

Choose your deployment method:

1. **🏃‍♂️ Quick Start**: For testing and development
2. **🏭 Production**: For live business use
3. **📈 High Availability**: For enterprise (contact for advanced setup)

**Next Step**: Create your Lightsail instance and run the deployment script!
