# 🛡️ Defensive Toolkit for Gamers

A lightweight, open-source security toolkit designed to help **gamers** protect their local credentials and detect phishing attempts.  
This toolkit empowers users to keep their logins safe and spot suspicious activity before it causes harm.

---

## 🔍 Overview

This repository includes two defensive modules:

- **`safevault/`** — a secure, local encrypted vault for storing passwords and tokens using modern KDF + AEAD primitives.  
- **`guardian/`** — a honeypot/logger that tracks suspicious domain or network activity and writes structured JSON logs for later review.

> ⚠️ **Ethical Note:**  
> This project is strictly *defensive*. It does **not** collect or transmit data to any remote server.  
> Its sole purpose is to help users secure personal information and learn about cybersecurity safely.

---

## 🚀 Quickstart (Demo)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/EddieOcon/defensive-toolkit-for-gamers.git
cd defensive-toolkit-for-gamers

#### 2️⃣ Create a Python virtual environment & install dependencies

python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows PowerShell
pip install -r requirements.txt

#####3️⃣ Run the demo

python run_demo.py

⚙️ Requirements

cryptography>=40
pytest
python-multipart    # Optional — for advanced request parsing
flask               # Optional — for web demo

📂 Project Structure

defensive-toolkit-for-gamers/
├── guardian/
│   └── honeypot.py
├── safevault/
│   └── core.py
├── tests/
│   └── test_safevault_core.py
├── gui_app.py
├── run_demo.py
├── requirements.txt
├── LICENSE
└── README.md

###💬 Author’s Message

This project was created with one mission — **to help people stay safe**.  
Too many gamers, friends, and everyday users fall victim to phishing scams, data theft, and password leaks.  
I built this toolkit not for profit, but **for the people** — to give them something that protects what matters most: their identity, privacy, and peace of mind.  

I believe everyone deserves digital safety, no matter their background or skill level.  
If this project helps even one person avoid being harmed, then it has done its job.  

**Stay safe. Stay aware. And remember — I’m here for the people. 🎮🛡️**  

— *Eddie Ocon*



