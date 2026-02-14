import os
import time
import psutil
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from datetime import datetime

# Initialize Console
console = Console()

def get_system_stats():
    """Fetches CPU, RAM, and Disk metrics."""
    # interval=0.1 prevents the 0.0% bug on the first run
    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    
    stats = Table(show_header=False, box=None, expand=True)
    stats.add_column(style="cyan")
    stats.add_column(style="magenta", justify="right")
    
    stats.add_row("CPU Usage:", f"[bold]{cpu}%[/bold]")
    stats.add_row("RAM Usage:", f"[bold]{ram}%[/bold]")
    stats.add_row("Disk Usage:", f"[bold]{disk}%[/bold]")
    
    return Panel(stats, title="[b]System Metrics[/b]", border_style="blue")

def get_service_status():
    """Monitors essential server services."""
    # Note: Using 'smbd' for Samba and 'apache2' for Web
    services = ["apache2", "smbd", "ssh"]
    table = Table(show_header=True, header_style="bold green", expand=True, box=None)
    table.add_column("Service")
    table.add_column("Status", justify="right")

    for s in services:
        # systemctl is-active returns 0 if the service is running
        status = os.system(f"systemctl is-active --quiet {s}")
        state = "[bold green]ONLINE[/bold green]" if status == 0 else "[bold red]OFFLINE[/bold red]"
        table.add_row(s, state)
    
    return Panel(table, title="[b]Active Services[/b]", border_style="green")

def get_admin_logs():
    """Reads the custom audit log created by your shell script."""
    log_path = "/var/log/sentinel_admin.log"
    table = Table(show_header=True, header_style="bold yellow", expand=True, box=None)
    table.add_column("Timestamp", width=20, style="dim")
    table.add_column("Action", justify="center")
    table.add_column("User", style="bright_white")
    table.add_column("Dept", style="bright_yellow")

    if os.path.exists(log_path):
        try:
            with open(log_path, "r") as f:
                lines = f.readlines()[-6:]  # Show last 6 actions
                for line in lines:
                    # Expected format: Date | CREATE | User: name | Dept: name
                    parts = line.strip().split(" | ")
                    if len(parts) >= 4:
                        ts = parts[0]
                        act = parts[1]
                        usr = parts[2].split(": ")[1] if ": " in parts[2] else parts[2]
                        dep = parts[3].split(": ")[1] if ": " in parts[3] else parts[3]
                        table.add_row(ts, act, usr, dep.upper())
        except Exception:
            table.add_row("-", "LOG ERROR", "-", "-")
    else:
        table.add_row("N/A", "No logs found", "-", "-")

    return Panel(table, title="[b]Admin Audit Trail[/b]", border_style="yellow")

def make_layout():
    """Defines the TUI layout structure."""
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main", size=10),
        Layout(name="footer", size=10)
    )
    layout["main"].split_row(
        Layout(name="stats"),
        Layout(name="services")
    )
    return layout

# --- MAIN LOOP ---
layout = make_layout()

try:
    with Live(layout, refresh_per_second=2, screen=True):
        while True:
            # Update Header with Time
            cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            layout["header"].update(
                Panel(f"[bold white]SENTINEL NODE ADMIN SUITE[/bold white] | System Time: {cur_time}", style="on blue")
            )
            
            # Update Body Content
            layout["stats"].update(get_system_stats())
            layout["services"].update(get_service_status())
            layout["footer"].update(get_admin_logs())
            
            time.sleep(0.5)
except KeyboardInterrupt:
    console.print("\n[bold red]Dashboard Stopped.[/bold red]")

