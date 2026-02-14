#!/bin/bash

# Check if the user provided a name and department
if [ $# -lt 2 ]; then
    echo "Usage: sudo ./sentinel_admin.sh [username] [department]"
    exit 1
fi

USER=$1
DEPT=$2

# 1. Dynamically Create Group and User
sudo groupadd $DEPT 2>/dev/null  # Ignore error if group exists
sudo useradd -m -s /bin/bash $USER 2>/dev/null
echo "$USER:password123" | sudo chpasswd

# Add to group
sudo usermod -aG $DEPT $USER

# 2. Sync with Samba (Module 4)
# This allows the user to log in from Windows
echo -e "password123\npassword123" | sudo smbpasswd -a -s $USER

# 3. Setup the Secure Storage (Module 2)
DIR="/srv/dc_storage/${DEPT}_data"
sudo mkdir -p $DIR
sudo chown :$DEPT $DIR
sudo chmod 770 $DIR

# 4. Log the action for our Python Dashboard to read (Module 3)
LOG_FILE="/var/log/sentinel_admin.log"
sudo touch $LOG_FILE
sudo chmod 666 $LOG_FILE
echo "$(date '+%Y-%m-%d %H:%M:%S') | CREATE | User: $USER | Dept: $DEPT | Path: $DIR" >> $LOG_FILE

echo "------------------------------------------------"
echo "SUCCESS: $USER added to $DEPT"
echo "ACCESS: Secure folder created at $DIR"
echo "SAMBA: User synced for Network Access"
echo "------------------------------------------------"
