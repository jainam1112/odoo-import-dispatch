#!/bin/bash

# Quick deployment script for testing
# Use this for rapid deployment without SSL

set -e

PROJECT_DIR="/opt/odoo-dispatch"

log_info() {
    echo -e "\033[0;34m[INFO]\033[0m $1"
}

log_success() {
    echo -e "\033[0;32m[SUCCESS]\033[0m $1"
}

log_error() {
    echo -e "\033[0;31m[ERROR]\033[0m $1"
}

# Check if running as root
if [[ $EUID -ne 0 ]]; then
    log_error "This script must be run as root"
    exit 1
fi

log_info "Starting quick deployment..."

# Update system
log_info "Updating system..."
apt update && apt upgrade -y

# Install Docker
log_info "Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
rm get-docker.sh

# Install Docker Compose
log_info "Installing Docker Compose..."
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Create project directory
log_info "Setting up project..."
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# Create simple docker-compose for testing
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=dispatch_production
      - POSTGRES_USER=odoo
      - POSTGRES_PASSWORD=odoo123
      - PGDATA=/var/lib/postgresql/data/pgdata
    volumes:
      - postgres_data:/var/lib/postgresql/data/pgdata
    restart: unless-stopped

  odoo:
    image: odoo:17
    depends_on:
      - db
    ports:
      - "8069:8069"
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=odoo123
    volumes:
      - odoo_data:/var/lib/odoo
      - ./addons:/mnt/extra-addons
    restart: unless-stopped

volumes:
  postgres_data:
  odoo_data:
EOF

# Create addons directory and copy dispatch management
log_info "Setting up addons..."
mkdir -p addons
# You'll need to copy your dispatch_management module here

# Start services
log_info "Starting services..."
docker-compose up -d

log_success "Quick deployment completed!"
echo
echo "🌐 Access Odoo at: http://$(curl -s ifconfig.me):8069"
echo "📂 Project directory: $PROJECT_DIR"
echo "🔐 Database: dispatch_production / odoo / odoo123"
echo
echo "To copy your dispatch management module:"
echo "scp -r ./dispatch_management root@your-server-ip:$PROJECT_DIR/addons/"
echo "docker-compose restart odoo"
