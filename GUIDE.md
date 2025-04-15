# 📘 Jesync Mikrowisp Integration – Control & Integration Guide

This guide provides full instructions for running, managing, and integrating the `jesync_mikrowisp_Lqos_csv.py` script into your LibreQoS environment.

---

## ✅ Basic Execution

### Run the script manually:

```bash
python3 /opt/libreqos/src/jesync_dashboard/jesync_mikrowisp_Lqos_csv.py
```

> This will:
> - Sync active Mikrowisp clients
> - Update or append new users to `ShapedDevices.csv`
> - Trigger `/opt/libreqos/src/LibreQoS.py --updateonly`

---

## ⚙️ Systemd Control

If you used `install.sh`, the script is already running as a systemd service.

### Check service status:

```bash
sudo systemctl status jesync_mikrowisp
```

### Restart the sync manually:

```bash
sudo systemctl restart jesync_mikrowisp
```

### Stop the service:

```bash
sudo systemctl stop jesync_mikrowisp
```

### Enable on boot:

```bash
sudo systemctl enable jesync_mikrowisp
```

---

## 🔧 Integration with LibreQoS

- LibreQoS reads `ShapedDevices.csv` from `/opt/libreqos/src/jesync_dashboard/`
- The script automatically runs this after each sync:

```bash
sudo /opt/libreqos/src/LibreQoS.py --updateonly
```

- This updates bandwidth rules for each user based on:
  - IP address
  - Upload/Download Max and Min
  - Parent Node (derived from plan name)

---

## 🛠️ How to Edit API Token or Plans

To update settings like your Mikrowisp token or allowed plans:

```bash
nano /opt/libreqos/src/jesync_dashboard/jesync_mikrowisp_Lqos_csv.py
```

Edit these lines near the top:

```python
MIKROWISP_API_TOKEN = "REPLACE_THIS"
ALLOWED_PLANS = ["Basic", "Premium", "Fiber100"]
```

---

## 🧪 How to Test

You can use the Mikrowisp demo environment:
- 🌐 [https://demo.mikrosystem.net/admin](https://demo.mikrosystem.net/admin)
- 👤 Username: `admin`
- 🔐 Password: `admin`

Replace the token and API URL in the script to point to their API demo.

---

## 💣 How to Disable or Uninstall

To remove this integration:

```bash
sudo systemctl stop jesync_mikrowisp
sudo systemctl disable jesync_mikrowisp
sudo rm /etc/systemd/system/jesync_mikrowisp.service
sudo rm /opt/libreqos/src/jesync_dashboard/jesync_mikrowisp_Lqos_csv.py
sudo rm /opt/libreqos/src/jesync_dashboard/ShapedDevices.csv
```

---

Need help? Contact [Jesync | JNHL IT Solutions](https://jesync.com)
