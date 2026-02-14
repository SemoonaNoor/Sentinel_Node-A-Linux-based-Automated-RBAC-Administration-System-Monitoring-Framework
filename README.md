# Sentinel Node: Automated RBAC & System Monitoring

Sentinel Node is a comprehensive Linux administration suite designed for secure user onboarding, real-time system telemetry, and automated disaster recovery. It implements **Role-Based Access Control (RBAC)** to secure departmental data and provides a visual dashboard for administrators to monitor the "heartbeat" of the server.

## 📂 Project Structure

```text
.
├── scripts/
│   ├── sentinel_admin.sh      # User & RBAC provisioning
│   ├── sentinel_dashboard.py  # Real-time monitoring TUI
│   └── sentinel_backup.sh     # Maintenance & Backups
├── docs/
│   ├── arch.md                # System design & Mermaid diagrams
│   └── deployment.md          # Setup instructions
├── config/
│   └── samba.conf.example     # Reference configuration
├── .gitignore                 # Prevents tracking of temp files
└── README.md                  # Project entry point

🚀 Key Features

    Automated Provisioning: Creates users, groups, and secure storage with 770 permissions.

    Real-Time Dashboard: Visual TUI built with Python rich to monitor CPU, RAM, and services.

    Data Protection: Automated backups with a 7-day rolling retention policy.

    Network Integration: Seamless Samba synchronization for departmental file sharing.

🛠️ Quick Start
1. Prerequisites
code Bash

sudo apt update
sudo apt install python3-pip samba openssh-server -y
pip3 install rich psutil

2. Launch Monitoring
code Bash

python3 scripts/sentinel_dashboard.py

3. Onboard User
code Bash

sudo ./scripts/sentinel_admin.sh [username] [department]

📜 Documentation

    Detailed system logic can be found in the Architecture Doc.

    Full installation steps are in the Deployment Guide.
