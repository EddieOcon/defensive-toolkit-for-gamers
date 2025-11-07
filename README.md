# Defensive Toolkit for Gamers

A small, open-source toolkit to help gamers protect local credentials and spot phishing attempts on their machine/network.
This repository contains two safe, non-destructive components:

- `safevault/` — a local encrypted vault engine for secrets (passwords, tokens). Uses modern KDF + AEAD primitives.
- `guardian/` — a honeypot/logger for suspicious domains/paths; writes structured JSON logs for analysis.

> NOTE: This project is defensive-only. It is not a phishing tool, does not exfiltrate credentials, and is intended to help users detect or block suspicious login pages and secure local secrets.

## Quickstart (demo)

1. Clone the repo:
```bash
git clone https://github.com/<your-user>/defensive-toolkit-for-gamers.git
cd defensive-toolkit-for-gamers
