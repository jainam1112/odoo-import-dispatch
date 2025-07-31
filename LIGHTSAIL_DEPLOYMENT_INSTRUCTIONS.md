# 🚀 Amazon Lightsail Deployment Instructions

## Quick Start (30 minutes)

### Step 1: Create Lightsail Instance
1. Go to https://lightsail.aws.amazon.com/
2. Create instance:
   - **OS**: Ubuntu 22.04 LTS
   - **Plan**: $20/month (4 GB RAM) - Recommended
   - **Name**: odoo-dispatch-server
3. Create Static IP ($5/month) and attach it

### Step 2: Connect and Deploy

#### Option A: One-Command Deployment (Easiest)
```bash
# Connect to your instance via SSH, then run:
sudo su -
curl -sSL https://raw.githubusercontent.com/jainam1112/odoo-import-dispatch/master/lightsail-deploy.sh | bash
```

#### Option B: Manual Upload and Deploy
```bash
# From your local machine:
scp d:\sagar\lightsail-deploy.sh ubuntu@YOUR_STATIC_IP:/tmp/

# On your Lightsail instance:
sudo su -
chmod +x /tmp/lightsail-deploy.sh
/tmp/lightsail-deploy.sh
```

#### Option C: Upload Deployment Folder
```bash
# From your local machine:
scp -r d:\sagar\deployment ubuntu@YOUR_STATIC_IP:/tmp/

# On your Lightsail instance:
sudo su -
cd /tmp/deployment
chmod +x scripts/*.sh
./scripts/quick-deploy.sh
```

### Step 3: Access Your Odoo System
1. **Open browser**: http://YOUR_STATIC_IP:8069
2. **Create database**: dispatch_production
3. **Install modules**: Apps → Update Apps List → Install "Dispatch Management"
4. **Configure email**: Settings → Technical → Email → Outgoing Mail Servers

### Step 4: Configure Email Notifications
1. Go to Settings → Technical → Email → Outgoing Mail Servers
2. Create new server:
   - **Name**: Gmail SMTP
   - **SMTP Server**: smtp.gmail.com
   - **Port**: 587
   - **Security**: TLS (STARTTLS)
   - **Username**: your-email@gmail.com
   - **Password**: your-app-password

## Production Deployment with SSL

For production with custom domain and SSL:

```bash
# Run the full production deployment
sudo su -
cd /opt/odoo-dispatch
./scripts/deploy.sh
# Enter your domain when prompted
```

## Management Commands

Once deployed:

```bash
# View logs
cd /opt/odoo-dispatch
docker-compose logs -f

# Restart services
docker-compose restart

# Create backup
./scripts/backup.sh

# Update application
git pull origin master
docker-compose restart
```

## Troubleshooting

### Can't access Odoo?
```bash
# Check if services are running
docker-compose ps

# Check firewall
sudo ufw status

# Check logs
docker-compose logs odoo
```

### Database connection errors?
```bash
# Restart database
docker-compose restart db

# Check database logs
docker-compose logs db
```

## Cost Summary
- **Instance (4GB)**: $20/month
- **Static IP**: $5/month
- **Total**: $25/month

## What You Get
✅ Complete Odoo 17 system
✅ Dispatch Management module
✅ Email notifications
✅ Daily automated backups
✅ Firewall protection
✅ Docker containerization
✅ Easy management scripts

**Your dispatch management system will be ready in 30 minutes!** 🎉
