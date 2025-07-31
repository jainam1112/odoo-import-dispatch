#!/bin/bash

# Update script for Odoo Dispatch Management
# Updates the application and restarts services

PROJECT_DIR="/opt/odoo-dispatch"
REPO_URL="https://github.com/jainam1112/odoo-import-dispatch.git"

cd $PROJECT_DIR

echo "=== Odoo Update Process ==="

# Backup before update
echo "Creating backup before update..."
./scripts/backup.sh

# Pull latest changes
echo "Pulling latest changes..."
git clone $REPO_URL temp_update
cp -r temp_update/dispatch_management ./odoo/addons/
rm -rf temp_update

# Update Docker images
echo "Updating Docker images..."
docker-compose pull

# Restart services
echo "Restarting services..."
docker-compose down
docker-compose up -d

# Wait for services to start
sleep 30

# Update Odoo modules
echo "Updating Odoo modules..."
docker-compose exec odoo odoo -d dispatch_production -u dispatch_management --stop-after-init

# Restart Odoo
docker-compose restart odoo

echo "Update completed successfully!"
echo "Services are running at: http://$(curl -s ifconfig.me):8069"
