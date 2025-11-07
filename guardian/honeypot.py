# guardian/honeypot.py
import http.server
import socketserver
import json
import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from pathlib import Path

BLOCKLIST_FILE = "blocked_domains.json"
LOG_FILE = "honeypot.log"

def get_hosts_path():
    if os.name == "nt":
        return r"C:\Windows\System32\drivers\etc\hosts"
    else:
        return "/etc/hosts"

def load_blocked_domains():
    if not os.path.exists(BLOCKLIST_FILE):
        return []
    with open(BLOCKLIST_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("blocked", [])

def update_hosts(blocked_domains):
    hosts_path = get_hosts_path()
    print(f"[+] Updating hosts file: {hosts_path}")
    try:
        with open(hosts_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print("[-] Could not read hosts file:", e)
        sys.exit(1)

    lines = content.splitlines()
    existing = set()
    for line in lines:
        if line.strip().startswith("#") or not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 2:
            existing.add(parts[1].lower())

    new_lines = lines[:]
    for domain in blocked_domains:
        d = domain.lower().strip()
        if d and d not in existing:
            new_lines.append(f"127.0.0.1 {d}")

    try:
        with open(hosts_path, "w", encoding="utf-8") as f:
            f.write("\n".join(new_lines) + "\n")
        print("[+] Hosts file updated.")
    except Exception as e:
        print("[-] Could not write hosts file (run as admin/root?):", e)
        sys.exit(1)

# Simple Tkinter popup notification (runs on main thread)
def show_alert(domain):
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning(
        "Suspicious domain blocked",
        f"Blocked access to suspicious domain:\n\n{domain}\n\n"
        "This might be a phishing or scam site."
    )
    root.destroy()

def log_event(domain, path, headers):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")
    entry = {
        "time": ts,
        "domain": domain,
        "path": path,
        "headers": dict(headers),
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

class HoneypotHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        host = self.headers.get("Host", "unknown")
        log_event(host, self.path, self.headers)
        # show notification in a separate thread so we don't block HTTP
        threading.Thread(target=show_alert, args=(host,), daemon=True).start()

        # Serve a simple warning page
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        html = f"""
        <html><head><title>Warning</title></head>
        <body style="font-family: sans-serif; background-color: #111; color: #eee;">
          <h2>Suspicious domain blocked</h2>
          <p>Domain: <b>{host}</b></p>
          <p>This domain has been blocked by your local guardian script.</p>
        </body></html>
        """
        self.wfile.write(html.encode("utf-8"))

    def log_message(self, fmt, *args):
        # silence default logging to stderr
        return

def run_server(port=80):
    handler = HoneypotHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"[+] Honeypot HTTP server listening on port {port}")
        httpd.serve_forever()

def main():
    blocked = load_blocked_domains()
    if not blocked:
        print(f"[-] No blocked domains defined in {BLOCKLIST_FILE}")
        sys.exit(1)

    print("[+] Blocked domains:")
    for d in blocked:
        print("   -", d)

    update_hosts(blocked)

    # try to bind to 80; fallback to 8080 if needed
    port = 80
    try:
        run_server(port=port)
    except PermissionError:
        print("[-] No permission for port 80, trying port 8080 (adjust hosts if needed)")
        run_server(port=8080)

if __name__ == "__main__":
    main()
