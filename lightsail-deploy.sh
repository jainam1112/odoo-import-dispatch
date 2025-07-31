#!/bin/bash

# Quick Lightsail Deployment Script for Odoo Dispatch Management
# Run this script on your Lightsail Ubuntu instance

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -ne 0 ]]; then
    log_error "Please run as root: sudo su - then run this script"
    exit 1
fi

echo "========================================"
echo "🚀 Odoo Dispatch Management Deployment"
echo "========================================"
echo

log_info "Starting deployment process..."

# Update system
log_info "Updating system packages..."
apt update && apt upgrade -y

# Install basic tools
log_info "Installing basic tools..."
apt install -y curl wget git vim htop unzip

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
PROJECT_DIR="/opt/odoo-dispatch"
log_info "Creating project directory: $PROJECT_DIR"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# Download your repository
log_info "Downloading Odoo Dispatch Management repository..."
wget https://github.com/jainam1112/odoo-import-dispatch/archive/master.zip
unzip master.zip
mv odoo-import-dispatch-master/* .
rm -rf odoo-import-dispatch-master master.zip

# Set up directory structure
log_info "Setting up directory structure..."
mkdir -p {nginx/ssl,nginx/logs,odoo/data,postgres/data,backups}

# Copy dispatch management module
log_info "Setting up Odoo modules..."
mkdir -p odoo/addons
# Note: The dispatch_management module should be in your repo
# If it's in a different location, adjust the path below
if [ -d "dispatch_management" ]; then
    cp -r dispatch_management odoo/addons/
    log_success "Dispatch management module copied"
else
    log_warning "Dispatch management module not found in expected location"
fi

# Create environment file
log_info "Creating environment configuration..."
cat > .env << EOF
# Database Configuration
DB_NAME=dispatch_production
DB_USER=odoo
DB_PASSWORD=$(openssl rand -base64 32)
DB_HOST=db

# Odoo Configuration
ODOO_ADMIN_PASSWORD=$(openssl rand -base64 32)
ODOO_DB_FILTER=dispatch_production

# Backup Configuration
BACKUP_SCHEDULE=0 2 * * *
BACKUP_RETENTION_DAYS=30
EOF

# Create simplified docker-compose for quick start
log_info "Creating Docker Compose configuration..."
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - PGDATA=/var/lib/postgresql/data/pgdata
    volumes:
      - postgres_data:/var/lib/postgresql/data/pgdata
    restart: unless-stopped
    networks:
      - odoo-network

  odoo:
    image: odoo:17
    depends_on:
      - db
    environment:
      - HOST=${DB_HOST}
      - USER=${DB_USER}
      - PASSWORD=${DB_PASSWORD}
    volumes:
      - odoo_data:/var/lib/odoo
      - ./odoo/addons:/mnt/extra-addons
    ports:
      - "8069:8069"
    restart: unless-stopped
    networks:
      - odoo-network
    command: >
      odoo
      --database=${DB_NAME}
      --db_host=${DB_HOST}
      --db_user=${DB_USER}
      --db_password=${DB_PASSWORD}
      --addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons
      --workers=2
      --limit-memory-hard=1073741824
      --limit-memory-soft=805306368

volumes:
  postgres_data:
  odoo_data:

networks:
  odoo-network:
    driver: bridge
EOF

# Set proper permissions
chown -R root:root $PROJECT_DIR
chmod 600 .env

# Configure firewall
log_info "Configuring firewall..."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 8069/tcp
ufw --force enable

# Start services
log_info "Starting Odoo services..."
docker-compose up -d

# Wait for services to start
log_info "Waiting for services to initialize..."
sleep 30

# Create backup script
log_info "Creating backup script..."
mkdir -p scripts
cat > scripts/backup.sh << 'EOF'
#!/bin/bash
PROJECT_DIR="/opt/odoo-dispatch"
BACKUP_DIR="$PROJECT_DIR/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Database backup
docker exec $(docker-compose ps -q db) pg_dump -U odoo dispatch_production | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Remove old backups (keep last 30 days)
find $BACKUP_DIR -name "*backup_*.gz" -mtime +30 -delete

echo "$(date): Backup completed - $DATE" >> /var/log/odoo-backup.log
EOF

chmod +x scripts/backup.sh

# Set up daily backup cron job
echo "0 2 * * * /opt/odoo-dispatch/scripts/backup.sh" | crontab -

# Get public IP
PUBLIC_IP=$(curl -s ifconfig.me)

# Display completion information
echo
echo "========================================"
log_success "DEPLOYMENT COMPLETED SUCCESSFULLY!"
echo "========================================"
echo
echo "🌐 Access your Odoo instance at:"
echo "   http://$PUBLIC_IP:8069"
echo
echo "🔐 Database Configuration:"
DB_PASSWORD=$(grep DB_PASSWORD .env | cut -d'=' -f2)
ADMIN_PASSWORD=$(grep ODOO_ADMIN_PASSWORD .env | cut -d'=' -f2)
echo "   Database: dispatch_production"
echo "   Username: odoo"
echo "   Password: $DB_PASSWORD"
echo
echo "🔧 Master Password: $ADMIN_PASSWORD"
echo
echo "📂 Project Directory: $PROJECT_DIR"
echo "💾 Backups: $PROJECT_DIR/backups (daily at 2 AM)"
echo
echo "🛠️ Management Commands:"
echo "   View logs: cd $PROJECT_DIR && docker-compose logs -f"
echo "   Restart: docker-compose restart"
echo "   Stop: docker-compose down"
echo "   Start: docker-compose up -d"
echo "   Backup: ./scripts/backup.sh"
echo
log_warning "IMPORTANT: Save the passwords above!"
log_warning "Configure your domain DNS to point to: $PUBLIC_IP"
echo
echo "Next steps:"
echo "1. Open http://$PUBLIC_IP:8069 in your browser"
echo "2. Create database 'dispatch_production'"
echo "3. Install the 'dispatch_management' module"
echo "4. Configure email settings for notifications"
echo
log_success "Happy dispatching! 🚚📦"
