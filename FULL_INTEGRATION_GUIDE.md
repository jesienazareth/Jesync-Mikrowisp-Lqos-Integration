# 🔗 Mikrowisp to LibreQoS Integration – Full Guide

This guide explains **step-by-step** how to set up and use the Jesync Mikrowisp Integration Script to automatically sync active users and bandwidth plans from your Mikrowisp system into LibreQoS using `ShapedDevices.csv`.

---

## 📌 What This Integration Does

- Connects to your Mikrowisp via their API v1.1 using a token
- Retrieves all clients and their assigned internet plans
- Extracts bandwidth limits (upload/download max & min)
- Writes each user as a row in `ShapedDevices.csv` for LibreQoS
- Automatically triggers LibreQoS to apply shaping
- Skips duplicates and avoids re-adding the same user

---

## 📁 File Output

The script generates:

```
/opt/libreqos/src/jesync_dashboard/ShapedDevices.csv
```

This file is used by LibreQoS to apply shaping rules to all users.

---

## 🧠 Global Settings (in the script)

```python
BANDWIDTH_MIN_RATE = 10  # Mbps - fallback min if not defined in Mikrowisp
BANDWIDTH_MAX_RATE = 50  # Mbps - fallback max if not defined in Mikrowisp
DEFAULT_SCAN_INTERVAL = 600  # Seconds between sync cycles (10 minutes)
ID_LENGTH = 8  # Length of generated circuit/device IDs
ALLOWED_PLANS = ["Basic", "Premium", "Fiber100"]  # Only sync these plan names
```

You can customize these at the top of the script.

---

## ⚙️ How It Works (Logic Per Cycle)

1. Reads current `ShapedDevices.csv`
2. Fetches all active users from Mikrowisp
3. For each user:
   - Skips if already shaped
   - Skips if their plan is not allowed
   - Extracts their IP, MAC, profile name
   - Calculates shaping limits
4. Appends new users to the CSV
5. Calls:
   ```
   sudo /opt/libreqos/src/LibreQoS.py --updateonly
   ```
6. Waits for `DEFAULT_SCAN_INTERVAL` seconds, then repeats

---

## 🚀 How to Set Up

### 1️⃣ Install with One Command:

```bash
bash <(curl -s https://raw.githubusercontent.com/jesienazareth/Jesync-Mikrowisp-Lqos-Integration/main/install.sh)
```

This:
- Installs Python and `requests`
- Creates `/opt/libreqos/src/jesync_dashboard`
- Downloads the script
- Sets up and starts a systemd service

---

### 2️⃣ Edit API Token and Plans

After installation:

```bash
nano /opt/libreqos/src/jesync_dashboard/jesync_mikrowisp_Lqos_csv.py
```

Set your token and plans:

```python
MIKROWISP_API_TOKEN = "REPLACE_WITH_YOUR_TOKEN"
ALLOWED_PLANS = ["Basic", "Premium", "Fiber100"]
```

---

## 🛠 Systemd Commands

To manage the service:

```bash
sudo systemctl status jesync_mikrowisp   # View status
sudo systemctl restart jesync_mikrowisp  # Restart now
sudo systemctl stop jesync_mikrowisp     # Stop manually
```

---

API Base URL: `https://demo.mikrosystem.net/api/v1`

Update the script to test with this demo token and endpoint.

---

## ❌ Uninstallation

```bash
sudo systemctl stop jesync_mikrowisp
sudo systemctl disable jesync_mikrowisp
sudo rm /etc/systemd/system/jesync_mikrowisp.service
sudo rm /opt/libreqos/src/jesync_dashboard/jesync_mikrowisp_Lqos_csv.py
sudo rm /opt/libreqos/src/jesync_dashboard/ShapedDevices.csv
sudo rm -rf /opt/libreqos/src/jesync_dashboard
```

---

## 👨‍🔧 Maintained By

Jesync | JNHL IT Solutions  
🌐 https://jesync.com  
💬 Need support? Open an issue or message us directly.

