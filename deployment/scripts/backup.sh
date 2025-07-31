#!/bin/bash

# Backup script for Odoo Dispatch Management
# Backs up database and filestore

PROJECT_DIR="/opt/odoo-dispatch"
BACKUP_DIR="$PROJECT_DIR/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Database backup
echo "Starting database backup..."
docker exec $(docker-compose ps -q db) pg_dump -U odoo dispatch_production | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Filestore backup
echo "Starting filestore backup..."
docker run --rm \
  -v $(docker volume ls -q | grep filestore):/source \
  -v $BACKUP_DIR:/backup \
  alpine tar -czf /backup/filestore_backup_$DATE.tar.gz -C /source .

# Configuration backup
echo "Backing up configuration..."
tar -czf $BACKUP_DIR/config_backup_$DATE.tar.gz -C $PROJECT_DIR .env docker-compose.yml nginx/

# Remove old backups (keep last 30 days)
find $BACKUP_DIR -name "*backup_*.gz" -mtime +30 -delete

# Log backup completion
echo "$(date): Backup completed - $DATE" >> /var/log/odoo-backup.log

echo "Backup completed successfully!"
echo "Files created:"
echo "- Database: $BACKUP_DIR/db_backup_$DATE.sql.gz"
echo "- Filestore: $BACKUP_DIR/filestore_backup_$DATE.tar.gz"
echo "- Config: $BACKUP_DIR/config_backup_$DATE.tar.gz"
