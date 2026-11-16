"""
Credential auditor for the two included localhost lab emulators.
The target host is deliberately fixed to 127.0.0.1.
"""
import base64
import csv
import json
import socket
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

HOST = "127.0.0.1"
TELNET_PORT = 2323
HTTP_URL = "http://127.0.0.1:8000/"
ROOT = Path(__file__).resolve().parent
CREDENTIAL_FILE = ROOT / "data" / "default_credentials.json"
REPORT_DIR = ROOT / "reports"

def load_credentials():
    with open(CREDENTIAL_FILE, encoding="utf-8") as f:
        return json.load(f)["credentials"]

def telnet_login(username, password, timeout=2):
    """Try one username/password pair against the local Telnet-style emulator."""
    try:
        with socket.create_connection((HOST, TELNET_PORT), timeout=timeout) as sock:
            sock.settimeout(timeout)
            stream = sock.makefile("rwb")
            stream.readline()          # banner
            stream.readline()          # username prompt
            stream.write((username + "\n").encode())
            stream.flush()
            stream.readline()          # password prompt
            stream.write((password + "\n").encode())
            stream.flush()
            result = stream.readline().decode("utf-8", "ignore").strip()
            return result == "LOGIN_SUCCESS"
    except OSError:
        return None

def http_login(username, password, timeout=2):
    """Try one Basic Auth pair against the local HTTP emulator."""
    token = base64.b64encode(f"{username}:{password}".encode()).decode()
    request = urllib.request.Request(HTTP_URL, headers={"Authorization": "Basic " + token})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status == 200
    except urllib.error.HTTPError as exc:
        if exc.code == 401:
            return False
        return None
    except (OSError, TimeoutError):
        return None

def audit_service(service):
    credentials = load_credentials()
    checker = telnet_login if service.lower() == "telnet" else http_login
    for item in credentials:
        result = checker(item["username"], item["password"])
        if result is None:
            return {"service": service.upper(), "status": "UNAVAILABLE",
                    "username": "", "password": "", "detail": "Local emulator is not running"}
        if result:
            return {"service": service.upper(), "status": "DEFAULT CREDENTIAL FOUND",
                    "username": item["username"], "password": item["password"],
                    "detail": "A configured common credential successfully authenticated"}
    return {"service": service.upper(), "status": "NO MATCH IN TEST LIST",
            "username": "", "password": "", "detail": "No configured credential pair matched"}

def dictionary_attack(service, username):
    """Try the configured dictionary against one username on a localhost service."""
    checker = telnet_login if service.lower() == "telnet" else http_login
    passwords = list(dict.fromkeys(x["password"] for x in load_credentials()))
    attempts = 0
    for password in passwords:
        attempts += 1
        result = checker(username, password)
        if result is None:
            return {"service": service.upper(), "status": "UNAVAILABLE",
                    "attempts": attempts, "password": ""}
        if result:
            return {"service": service.upper(), "status": "MATCH FOUND",
                    "attempts": attempts, "password": password}
    return {"service": service.upper(), "status": "NO MATCH IN DICTIONARY",
            "attempts": attempts, "password": ""}

def weak_password_check(password):
    reasons = []
    if len(password) < 8:
        reasons.append("shorter than 8 characters")
    if password.lower() in {"admin", "password", "123456", "welcome", "root", "user"}:
        reasons.append("common or default password")
    if password.isalpha() or password.isdigit():
        reasons.append("uses only letters or only digits")
    if not reasons:
        return "No basic weakness detected"
    return "Weak: " + ", ".join(reasons)

def save_report(rows):
    REPORT_DIR.mkdir(exist_ok=True)
    path = REPORT_DIR / ("audit_report_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv")
    fields = ["timestamp", "service", "status", "username", "password", "detail"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        stamp = datetime.now().isoformat(timespec="seconds")
        for row in rows:
            writer.writerow({"timestamp": stamp, **{k: row.get(k, "") for k in fields[1:]}})
    return path
