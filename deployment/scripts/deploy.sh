#!/bin/bash

# Odoo Deployment Script for Amazon Lightsail
# This script automates the deployment process

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/opt/odoo-dispatch"
REPO_URL="https://github.com/jainam1112/odoo-import-dispatch.git"
DOMAIN=""
EMAIL=""

# Functions
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

check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_error "This script must be run as root"
        exit 1
    fi
}

get_user_input() {
    echo "=== Odoo Deployment Configuration ==="
    echo
    
    read -p "Enter your domain name (e.g., yourdomain.com): " DOMAIN
    read -p "Enter your email address: " EMAIL
    
    if [[ -z "$DOMAIN" || -z "$EMAIL" ]]; then
        log_error "Domain and email are required"
        exit 1
    fi
    
    log_info "Domain: $DOMAIN"
    log_info "Email: $EMAIL"
}

install_dependencies() {
    log_info "Installing system dependencies..."
    
    # Update system
    apt update && apt upgrade -y
    
    # Install required packages
    apt install -y \
        curl \
        wget \
        git \
        vim \
        ufw \
        fail2ban \
        htop \
        unzip \
        software-properties-common \
        apt-transport-https \
        ca-certificates \
        gnupg \
        lsb-release
    
    log_success "System dependencies installed"
}

install_docker() {
    log_info "Installing Docker..."
    
    # Add Docker's official GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    # Add Docker repository
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Install Docker
    apt update
    apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    
    # Install Docker Compose standalone
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    
    # Add current user to docker group
    usermod -aG docker $SUDO_USER
    
    # Start Docker service
    systemctl start docker
    systemctl enable docker
    
    log_success "Docker installed successfully"
}

setup_firewall() {
    log_info "Configuring firewall..."
    
    # Reset UFW to defaults
    ufw --force reset
    
    # Default policies
    ufw default deny incoming
    ufw default allow outgoing
    
    # Allow SSH
    ufw allow ssh
    
    # Allow HTTP and HTTPS
    ufw allow 80/tcp
    ufw allow 443/tcp
    
    # Enable firewall
    ufw --force enable
    
    log_success "Firewall configured"
}

setup_fail2ban() {
    log_info "Configuring Fail2ban..."
    
    cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log

[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log

[nginx-limit-req]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 10
EOF
    
    systemctl restart fail2ban
    systemctl enable fail2ban
    
    log_success "Fail2ban configured"
}

create_project_directory() {
    log_info "Creating project directory..."
    
    mkdir -p $PROJECT_DIR
    cd $PROJECT_DIR
    
    # Create directory structure
    mkdir -p {nginx/{ssl,logs},odoo/{addons,config,data},postgres/data,backups,scripts}
    
    log_success "Project directory created"
}

clone_repository() {
    log_info "Cloning repository..."
    
    # Clone the repository
    git clone $REPO_URL temp_repo
    
    # Copy dispatch management module
    cp -r temp_repo/dispatch_management $PROJECT_DIR/odoo/addons/
    
    # Copy deployment files
    cp temp_repo/deployment/* $PROJECT_DIR/
    cp temp_repo/deployment/nginx/* $PROJECT_DIR/nginx/
    
    # Cleanup
    rm -rf temp_repo
    
    log_success "Repository cloned"
}

configure_environment() {
    log_info "Configuring environment..."
    
    # Generate random passwords
    DB_PASSWORD=$(openssl rand -base64 32)
    ADMIN_PASSWORD=$(openssl rand -base64 32)
    SECRET_KEY=$(openssl rand -base64 64)
    
    # Create .env file
    cat > $PROJECT_DIR/.env << EOF
# Database Configuration
DB_NAME=dispatch_production
DB_USER=odoo
DB_PASSWORD=$DB_PASSWORD
DB_HOST=db

# Odoo Configuration
ODOO_ADMIN_PASSWORD=$ADMIN_PASSWORD
ODOO_DB_FILTER=dispatch_production

# Deployment Configuration
DOMAIN=$DOMAIN
EMAIL=$EMAIL

# Security
SECRET_KEY=$SECRET_KEY

# Backup Configuration
BACKUP_SCHEDULE=0 2 * * *
BACKUP_RETENTION_DAYS=30
EOF
    
    # Set proper permissions
    chmod 600 $PROJECT_DIR/.env
    
    log_success "Environment configured"
    log_warning "Database password: $DB_PASSWORD"
    log_warning "Admin password: $ADMIN_PASSWORD"
    log_warning "Please save these passwords securely!"
}

install_ssl() {
    log_info "Installing SSL certificate..."
    
    # Install Certbot
    snap install core; snap refresh core
    snap install --classic certbot
    ln -sf /snap/bin/certbot /usr/bin/certbot
    
    # Get SSL certificate
    certbot certonly --standalone \
        --email $EMAIL \
        --agree-tos \
        --no-eff-email \
        -d $DOMAIN
    
    # Copy certificates to nginx directory
    cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem $PROJECT_DIR/nginx/ssl/
    cp /etc/letsencrypt/live/$DOMAIN/privkey.pem $PROJECT_DIR/nginx/ssl/
    
    # Set up automatic renewal
    echo "0 12 * * * /usr/bin/certbot renew --quiet" | crontab -
    
    log_success "SSL certificate installed"
}

update_nginx_config() {
    log_info "Updating Nginx configuration..."
    
    # Update domain in nginx config
    sed -i "s/your-domain.com/$DOMAIN/g" $PROJECT_DIR/nginx/nginx.conf
    
    log_success "Nginx configuration updated"
}

deploy_application() {
    log_info "Deploying application..."
    
    cd $PROJECT_DIR
    
    # Start services
    docker-compose up -d
    
    # Wait for services to start
    sleep 30
    
    log_success "Application deployed successfully"
}

create_backup_script() {
    log_info "Creating backup script..."
    
    cat > $PROJECT_DIR/scripts/backup.sh << 'EOF'
#!/bin/bash

PROJECT_DIR="/opt/odoo-dispatch"
BACKUP_DIR="$PROJECT_DIR/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
docker exec odoo-dispatch_db_1 pg_dump -U odoo dispatch_production | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Backup filestore
tar -czf $BACKUP_DIR/filestore_backup_$DATE.tar.gz -C $PROJECT_DIR/odoo/data filestore

# Remove old backups (keep last 30 days)
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
EOF
    
    chmod +x $PROJECT_DIR/scripts/backup.sh
    
    # Add to crontab
    echo "0 2 * * * $PROJECT_DIR/scripts/backup.sh >> /var/log/odoo-backup.log 2>&1" | crontab -
    
    log_success "Backup script created"
}

display_completion_info() {
    echo
    echo "========================================"
    log_success "DEPLOYMENT COMPLETED SUCCESSFULLY!"
    echo "========================================"
    echo
    echo "🌐 Your Odoo instance is now available at:"
    echo "   https://$DOMAIN"
    echo
    echo "🔐 Database credentials:"
    echo "   Database: dispatch_production"
    echo "   Username: odoo"
    echo "   Password: (check .env file)"
    echo
    echo "🔧 Admin credentials:"
    echo "   Master Password: (check .env file)"
    echo
    echo "📂 Project directory: $PROJECT_DIR"
    echo "📋 Log files: $PROJECT_DIR/nginx/logs/"
    echo
    echo "🛠️ Useful commands:"
    echo "   View logs: docker-compose logs -f"
    echo "   Restart: docker-compose restart"
    echo "   Update: docker-compose pull && docker-compose up -d"
    echo "   Backup: $PROJECT_DIR/scripts/backup.sh"
    echo
    echo "🔐 SSL certificate will auto-renew"
    echo "💾 Daily backups are configured"
    echo
    log_warning "Please save the passwords from the .env file!"
}

# Main execution
main() {
    echo "=== Odoo Dispatch Management Deployment ==="
    echo
    
    check_root
    get_user_input
    
    log_info "Starting deployment process..."
    
    install_dependencies
    install_docker
    setup_firewall
    setup_fail2ban
    create_project_directory
    clone_repository
    configure_environment
    update_nginx_config
    install_ssl
    deploy_application
    create_backup_script
    
    display_completion_info
}

# Run main function
main "$@"
