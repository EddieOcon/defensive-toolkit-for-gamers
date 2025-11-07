from safevault.core import *
from guardian.honeypot import *

if __name__ == "__main__":
    print("🛡️ Defensive Toolkit Demo Running...")
    # create vault
    print("Creating secure vault...")
    # simulate event
    log_event("example.com", "/login", {"User-Agent": "demo"})
    print("✅ Logs saved to guardian/logs.jsonl")
