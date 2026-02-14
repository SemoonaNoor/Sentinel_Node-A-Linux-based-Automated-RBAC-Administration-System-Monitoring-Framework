#!/bin/bash
# SentinelNode Automated Backup & Cleanup Tool

BACKUP_DIR="/srv/dc_storage/backups"
SOURCE_DIR="/srv/dc_storage"
RETENTION_DAYS=7
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 1. Create Backup Directory if missing
sudo mkdir -p "$BACKUP_DIR"

echo "--- Starting SentinelNode Backup: $TIMESTAMP ---"

# 2. Backup HR and ENG data
for dept in hr_data eng_data; do
    if [ -d "$SOURCE_DIR/$dept" ]; then
        echo "Backing up $dept..."
        sudo tar -czf "$BACKUP_DIR/${dept}_$TIMESTAMP.tar.gz" -C "$SOURCE_DIR" "$dept"
        echo "SUCCESS: ${dept}_$TIMESTAMP.tar.gz created."
    fi
done

# 3. Cleanup: Delete backups older than 7 days
echo "Cleaning up old backups..."
sudo find "$BACKUP_DIR" -type f -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete

# 4. Log the action for the Dashboard
LOG_FILE="/var/log/sentinel_admin.log"
echo "$TIMESTAMP | BACKUP | User: SYSTEM | Dept: ALL | Path: $BACKUP_DIR" >> "$LOG_FILE"

echo "--- Backup Complete ---"

