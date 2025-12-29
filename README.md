# Telegram Link & Broadcast Bot

A fully customizable Telegram bot to manage links and broadcast messages to your users.  
Built with **Python** and **python-telegram-bot v21.6**. Fully Heroku-deployable.

---

## Features

- `/start` command with stylish welcome message and channel join button  
- `/setlinks` command (Owner only) – manage links  
- `/broadcast` command (Owner only) – broadcast message to all users  
- Automatically saves users who start the bot (`users.json`)  
- Links are saved in `links.json`  
- Fully customizable using **environment variables**  

---

## Files in Repository

- `bot.py` – Main bot code  
- `requirements.txt` – Dependencies  
- `Procfile` – Heroku worker process  
- `app.json` – Heroku app config  
- `links.json` – Stores bot links  
- `users.json` – Stores user IDs  
- `README.md` – This file  

---

## Setup & Deployment on Heroku

### 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
