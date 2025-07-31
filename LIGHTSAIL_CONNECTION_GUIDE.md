# Step-by-Step Lightsail Deployment

## Connection Methods

### Method 1: Browser SSH (Easiest)
1. In Lightsail console, click your instance
2. Click "Connect using SSH" 
3. Browser terminal will open

### Method 2: SSH Client
```bash
# Replace YOUR_STATIC_IP with your actual IP
ssh ubuntu@YOUR_STATIC_IP

# If using key file:
ssh -i /path/to/your-key.pem ubuntu@YOUR_STATIC_IP
```

### Method 3: PuTTY (Windows)
1. Download your SSH key from Lightsail
2. Convert .pem to .ppk using PuTTYgen
3. Connect using PuTTY with:
   - Host: YOUR_STATIC_IP
   - Username: ubuntu
   - Private key: your .ppk file

## Next Steps After Connection

Once connected, run these commands:

```bash
# Switch to root user
sudo su -

# Update system
apt update && apt upgrade -y

# Download deployment files
wget https://github.com/jainam1112/odoo-import-dispatch/archive/master.zip
unzip master.zip
cd odoo-import-dispatch-master/deployment

# Make scripts executable
chmod +x scripts/*.sh

# Run deployment
./scripts/deploy.sh
```

## Manual File Upload Method

If you prefer to upload files manually:

```bash
# From your local machine (PowerShell/CMD):
scp -r d:\sagar\deployment ubuntu@YOUR_STATIC_IP:/tmp/

# Then on the server:
sudo su -
cd /tmp/deployment
chmod +x scripts/*.sh
./scripts/deploy.sh
```
