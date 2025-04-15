
# jesync_mikrowisp_Lqos_csv.py
import requests
import csv
import random
import time
import subprocess
import json
import os
from collections import OrderedDict

# === GLOBAL SETTINGS ===
BANDWIDTH_MIN_RATE = 10
BANDWIDTH_MAX_RATE = 50
DEFAULT_SCAN_INTERVAL = 600
ID_LENGTH = 8
ALLOWED_PLANS = ["Basic", "Premium", "Fiber100"]  # Only include clients with these Mikrowisp plans

# === MIKROWISP CONFIG ===
MIKROWISP_API_TOKEN = "Smx2SVdkbUZIdjlCUlkxdFo1cUNMQT09"  # Replace with real token
BASE_URL = "https://demo.mikrosystem.net/api/v1"

# === FILE PATHS ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE_PATH = os.path.join(SCRIPT_DIR, "ShapedDevices.csv")

# === Utility Functions ===
def generate_id(length=ID_LENGTH):
    return ''.join(random.choices('0123456789', k=length))

def safe_int(value, fallback):
    try:
        return int(value)
    except (ValueError, TypeError):
        return fallback

def post_request(endpoint, payload):
    try:
        response = requests.post(f"{BASE_URL}/{endpoint}", json=payload, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"[ERROR] Request to {endpoint} failed: {e}")
    return {}

def load_existing_csv():
    existing = OrderedDict()
    if os.path.exists(CSV_FILE_PATH):
        with open(CSV_FILE_PATH, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing[row["Device Name"]] = row
    return existing

# === Build Shaped Devices from Mikrowisp ===
def build_shaped_devices(existing_entries):
    shaped = OrderedDict(existing_entries)

    # Step 1: Get all clients
    clients_data = post_request("GetClients", {"token": MIKROWISP_API_TOKEN})
    clients = clients_data.get("clientes", [])

    existing_ips = {entry.get("IPv4"): name for name, entry in shaped.items()}

    for client in clients:
        client_id = client.get("id")
        if not client_id:
            continue

        # Step 2: Get client details
        details = post_request("GetClientsDetails", {
            "token": MIKROWISP_API_TOKEN,
            "idcliente": client_id
        })

        detail = details.get("cliente")
        if not detail:
            continue

        ipv4 = detail.get("ip", "").strip()
        ipv6 = detail.get("ipv6", "").strip()
        username = detail.get("usuario", f"client{client_id}")
        plan_name = detail.get("servicio", "Default")

        # Skip if already exists
        if username in shaped:
            continue

        # Skip if plan not allowed
        if plan_name not in ALLOWED_PLANS:
            print(f"[SKIP] Plan {plan_name} is not in ALLOWED_PLANS")
            continue

        download_max = safe_int(detail.get("velocidad_bajada"), BANDWIDTH_MAX_RATE)
        upload_max = safe_int(detail.get("velocidad_subida"), BANDWIDTH_MAX_RATE)
        download_min = safe_int(detail.get("velocidad_bajada_min"), BANDWIDTH_MIN_RATE)
        upload_min = safe_int(detail.get("velocidad_subida_min"), BANDWIDTH_MIN_RATE)

        if not ipv4 or ipv4 in existing_ips:
            print(f"[SKIP] IP conflict or missing: {ipv4}")
            continue

        shaped[username] = {
            "Circuit ID": generate_id(),
            "Circuit Name": f"{username}-{client_id}",
            "Device ID": generate_id(),
            "Device Name": username,
            "Parent Node": f"PPP-{plan_name}",
            "MAC": detail.get("mac", ""),
            "IPv4": ipv4,
            "IPv6": ipv6,
            "Download Min Mbps": download_min,
            "Upload Min Mbps": upload_min,
            "Download Max Mbps": download_max,
            "Upload Max Mbps": upload_max,
            "Comment": "ppp"
        }
        existing_ips[ipv4] = username

    return shaped

# === Write to CSV ===
def write_shaped_devices_csv(data):
    fieldnames = ["Circuit ID", "Circuit Name", "Device ID", "Device Name", "Parent Node",
                  "MAC", "IPv4", "IPv6", "Download Min Mbps", "Upload Min Mbps",
                  "Download Max Mbps", "Upload Max Mbps", "Comment"]
    with open(CSV_FILE_PATH, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data.values():
            writer.writerow(row)

# === Trigger LibreQoS Update ===
def trigger_libreqos_reload():
    try:
        subprocess.run(["sudo", "/opt/libreqos/src/LibreQoS.py", "--updateonly"], check=True)
        print("[INFO] LibreQoS updated successfully.")
    except Exception as e:
        print(f"[ERROR] LibreQoS update failed: {e}")

# === Main Loop ===
def main_loop():
    while True:
        print("[INFO] Syncing Mikrowisp to ShapedDevices.csv...")
        existing_entries = load_existing_csv()
        shaped = build_shaped_devices(existing_entries)
        write_shaped_devices_csv(shaped)
        trigger_libreqos_reload()
        print(f"[INFO] Sleeping for {DEFAULT_SCAN_INTERVAL} seconds...")
        time.sleep(DEFAULT_SCAN_INTERVAL)

if __name__ == "__main__":
    main_loop()
