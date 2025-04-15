# Jesync Mikrowisp to LibreQoS Integration

This Python script integrates Mikrowisp API with LibreQoS by syncing active users and bandwidth limits into `ShapedDevices.csv`.

## 🚀 Features
- Token-based Mikrowisp API v1.1 authentication
- Auto-generates LibreQoS-compatible CSV
- Syncs new users only, skipping duplicates
- Auto-reloads LibreQoS each cycle
- Configurable bandwidth defaults and plans

## 📦 Requirements
```bash
pip install requests
```

## 📥 Installation

### Clone or Download
```bash
cd /opt/libreqos/src/
git clone https://github.com/YOUR_USERNAME/jesync-mikrowisp-libreqos.git
```

### Create Required Folder
```bash
sudo mkdir -p /opt/libreqos/src/jesync_dashboard
sudo chown -R $USER:$USER /opt/libreqos/src/jesync_dashboard
```

### Move Script
```bash
cp jesync_mikrowisp_Lqos_csv.py /opt/libreqos/src/jesync_dashboard/
```

### Configure Script
Edit top variables like `MIKROWISP_API_TOKEN`, `ALLOWED_PLANS`, and `SCAN_INTERVAL`.

## 🧪 Manual Run
```bash
python3 /opt/libreqos/src/jesync_dashboard/jesync_mikrowisp_Lqos_csv.py
```

## 🔁 Auto Start

### Cron
```bash
crontab -e
```
Add:
```bash
*/10 * * * * /usr/bin/python3 /opt/libreqos/src/jesync_dashboard/jesync_mikrowisp_Lqos_csv.py >> /var/log/jesync_mikrowisp.log 2>&1
```

### Systemd
```bash
sudo nano /etc/systemd/system/jesync_mikrowisp.service
```

Paste:
```ini
[Unit]
Description=Jesync Mikrowisp Sync to LibreQoS
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/libreqos/src/jesync_dashboard/jesync_mikrowisp_Lqos_csv.py
Restart=always
RestartSec=10
User=root

[Install]
WantedBy=multi-user.target
```

Then run:
```bash
sudo systemctl daemon-reexec
sudo systemctl enable jesync_mikrowisp
sudo systemctl start jesync_mikrowisp
```

## 💣 Uninstall

### Remove systemd service:
```bash
sudo systemctl stop jesync_mikrowisp
sudo systemctl disable jesync_mikrowisp
sudo rm /etc/systemd/system/jesync_mikrowisp.service
sudo systemctl daemon-reexec
```

### Remove files:
```bash
sudo rm /opt/libreqos/src/jesync_dashboard/jesync_mikrowisp_Lqos_csv.py
sudo rm /opt/libreqos/src/jesync_dashboard/ShapedDevices.csv
sudo rm -rf /opt/libreqos/src/jesync_dashboard/
```

### Remove cron (if used):
```bash
crontab -e
# Delete any line referencing jesync_mikrowisp
```

---

Maintained by [Jesync | JNHL IT Solutions](https://jesync.com)
