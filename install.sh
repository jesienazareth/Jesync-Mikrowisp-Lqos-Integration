#!/bin/bash
echo "🔧 Jesync Mikrowisp → LibreQoS Integration Auto Installer"

# Step 1: Prepare folder
echo "📁 Creating directory /opt/libreqos/src/jesync_dashboard"
sudo mkdir -p /opt/libreqos/src/jesync_dashboard
cd /opt/libreqos/src/jesync_dashboard || exit 1

# Step 2: Install dependencies
echo "📦 Installing dependencies..."
sudo apt update
sudo apt install -y python3-pip git curl
pip3 install requests

# Step 3: Download the script
echo "⬇️ Downloading integration script..."
SCRIPT_URL="https://raw.githubusercontent.com/jesienazareth/Jesync-Mikrowisp-Lqos-Integration/main/jesync_mikrowisp_Lqos_csv.py"
curl -s -O "$SCRIPT_URL"

# Step 4: Create systemd service
echo "🛠️ Creating systemd service..."
SERVICE_PATH="/etc/systemd/system/jesync_mikrowisp.service"
sudo bash -c "cat > $SERVICE_PATH" <<EOF
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
EOF

# Step 5: Enable + Start service
echo "🚀 Enabling and starting jesync_mikrowisp service..."
sudo systemctl daemon-reexec
sudo systemctl enable jesync_mikrowisp
sudo systemctl start jesync_mikrowisp

# Final message
echo ""
echo "✅ Installation Complete!"
echo "📄 Script path: /opt/libreqos/src/jesync_dashboard/jesync_mikrowisp_Lqos_csv.py"
echo "⚙️  Service: jesync_mikrowisp (enabled and running)"
echo "📝 Remember to edit the script and set your Mikrowisp API token!"
echo "   nano /opt/libreqos/src/jesync_dashboard/jesync_mikrowisp_Lqos_csv.py"
