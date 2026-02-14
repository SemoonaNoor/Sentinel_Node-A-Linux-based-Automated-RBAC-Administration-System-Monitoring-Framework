# Sentinel Node: System Architecture

This document outlines the technical design and logic flow of the Sentinel Node framework.

## 1. Logic Flow (RBAC Model)
Sentinel Node uses a "Group-First" security model. When a user is onboarded, the system follows this logic:

1. **Identity Creation**: System creates a standard Linux user.
2. **Departmental Grouping**: System ensures a Linux group exists for the department (e.g., `hr`, `eng`).
3. **Directory Hardening**: A directory is created at `/srv/dc_storage/`. 
   - Ownership is set to `root:[department]`.
   - Permissions are set to `770` (Owner: Read/Write/Exec, Group: Read/Write/Exec, Others: **None**).
4. **Samba Synchronization**: The user is added to the Samba database to allow remote network access.

## 2. Component Diagram
```mermaid
graph TD
    A[Admin Terminal] -->|Executes| B(sentinel_admin.sh)
    B -->|Modifies| C[Linux /etc/passwd & /etc/group]
    B -->|Configures| D[Filesystem Permissions]
    B -->|Updates| E[Samba TDB Database]
    
    F[Sentinel Dashboard] -->|Reads| G[/var/log/sentinel_admin.log]
    F -->|Polls| H[System Kernel via psutil]
    
    I[Backup Engine] -->|Compresses| J[/srv/dc_storage/]
    I -->|Maintenance| K[7-Day Retention Cleanup]
