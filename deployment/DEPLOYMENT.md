# Deployment Package for Amazon Lightsail

This folder contains all the necessary files to deploy your Odoo Dispatch Management system to Amazon Lightsail.

## 📁 File Structure

```
deployment/
├── README.md                    # Deployment instructions
├── docker-compose.yml          # Docker services configuration
├── .env.example                 # Environment variables template
├── nginx/
│   └── nginx.conf              # Nginx reverse proxy configuration
├── odoo/
│   └── config/
│       └── odoo.conf           # Odoo configuration file
└── scripts/
    ├── deploy.sh               # Full production deployment script
    ├── quick-deploy.sh         # Quick deployment for testing
    ├── backup.sh               # Backup script
    └── update.sh               # Update script
```

## 🚀 Quick Deployment

1. **Upload to your server:**
   ```bash
   scp -r deployment/ ubuntu@your-server-ip:/tmp/
   ```

2. **Run deployment:**
   ```bash
   ssh ubuntu@your-server-ip
   sudo su -
   cd /tmp/deployment
   chmod +x scripts/quick-deploy.sh
   ./scripts/quick-deploy.sh
   ```

3. **Copy your module:**
   ```bash
   scp -r dispatch_management ubuntu@your-server-ip:/opt/odoo-dispatch/addons/
   ```

## 🏭 Production Deployment

For production with SSL, domain, and security:

```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

## 📚 Documentation

See `README.md` for complete deployment instructions.

## 🔧 Customization

- Edit `.env.example` and rename to `.env`
- Modify `docker-compose.yml` for your requirements
- Update `nginx/nginx.conf` with your domain
- Adjust `odoo/config/odoo.conf` for performance tuning
