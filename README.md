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


## Author’s Message  

This project was created with one mission — to protect people.  
In a world where digital spaces have become playgrounds for both fun and danger, I wanted to build something that helps others stay safe while doing what they love. I know that there are so many kids and young gamers out there who just want to play, explore, and have fun — without realizing how many bad actors exist online waiting to take advantage of their trust.  

I built this project for them — for every child, teen, and adult who deserves to enjoy the internet without fear of being tricked or having their personal information stolen. This is my way of giving something back to the community, free of charge, so that anyone, anywhere, can guard their digital identity and learn how to protect themselves.  

This isn’t about money or recognition. It’s about doing the right thing.  
It’s about standing up for the people who don’t yet know how to defend themselves.  
If this tool helps even one person stay safe, then it has fulfilled its purpose.  

— *Created with care, compassion, and conviction — for the people.*  



