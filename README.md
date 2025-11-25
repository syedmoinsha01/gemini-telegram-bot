# 🤖 Gemini Telegram Bot (with User Memory + Typing Indicator)

A modern, fast, and intelligent Telegram bot powered by **Google Gemini 2.5 Flash**, with advanced features like:

- 🧠 **Per-user memory** (each user gets separate chat history)
- ✍️ **Typing indicator** (bot shows “typing…” while generating response)
- ⚡ Super-fast responses using Gemini Flash free API
- 🔒 Secure environment variable usage
- 🌐 Deployable on Railway (24×7 uptime)
- 🧯 `/forget` command to reset memory
- 📦 Clean & maintainable Python code

This project is perfect for building AI chatbots, assistants, customer support bots, and more.

---

## 🚀 Features

### 🔹 1. Per-User Memory System
Each Telegram user gets their **own isolated chat history**, so the bot can respond with context.

- Automatically remembers last 20 messages
- Auto-purges old messages
- Fully isolated memory for every user
- Supports unlimited users

### 🔹 2. Gemini 2.5 Flash API (FREE tier)
Uses Google’s **Gemini 2.5 Flash** model, which is:
- Free  
- Fast  
- Low-latency  
- Ideal for bots  

### 🔹 3. Typing Indicator
Shows **typing…** before sending the response, giving a natural chat feel.

### 🔹 4. Commands
| Command     | Description |
|-------------|-------------|
| `/start`    | Start the bot |
| `/help`     | Show help |
| `/forget`   | Clear personal memory |

### 🔹 5. Easy Deployment
Works perfectly on:
- Railway (recommended)
- PythonAnywhere
- VPS (Ubuntu or others)

---

## 📁 Project Structure

gemini-telegram-bot/ │ ├── main.py ├── requirements.txt └── README.md  (this file)

---

## 🔑 Required Environment Variables

Set these on **Railway → Variables** or in a local `.env` file:

| Variable Name        | Description |
|----------------------|-------------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token from BotFather |
| `GEMINI_API_KEY`     | API key from Google AI Studio |

---

## 🛠 Installation (Local Setup)

### 1. Clone the repository
```bash
git clone https://github.com/yourname/gemini-telegram-bot.git
cd gemini-telegram-bot

2. Install dependencies

pip install -r requirements.txt

3. Create .env file

TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_TOKEN
GEMINI_API_KEY=YOUR_GEMINI_API_KEY

4. Run the bot

python main.py


---

☁️ Deploy to Railway (24×7 free hosting)

Step 1 — Push code to GitHub

Upload main.py + requirements.txt to your repo.

Step 2 — Connect to Railway

1. Go to: https://railway.app


2. Create a new project → Deploy from GitHub


3. Select this repository



Step 3 — Add Environment Variables

Go to → Project → Variables
Add:

TELEGRAM_BOT_TOKEN=xxxxx
GEMINI_API_KEY=xxxxx

Step 4 — Start Command

Railway → Service → Settings → Start Command:

python main.py

Step 5 — Redeploy

Your bot is now live 24×7 🎉


---

🧠 Memory System Explanation

The bot stores chat history like this:

user_memory[user_id] = [
  { role: "user", content: "Hello" },
  { role: "assistant", content: "Hi!" },
  ...
]

Each user has separate memory

Memory is limited to the last 20 messages

Old messages auto-delete

/forget command clears memory instantly



---

❗ Troubleshooting

❌ Bot not responding?

✔️ Check Railway logs
✔️ Make sure TELEGRAM_BOT_TOKEN is correct
✔️ No blank spaces in key values


---

❌ “Gemini API error” ?

Check:

API key active in AI Studio

No extra spaces in the key

Correct model name:

gemini-2.5-flash



---

❌ Typing not showing?

Make sure:

await update.message.chat.send_action(ChatAction.TYPING)

exists before Gemini call.


---

📄 License

MIT — free for anyone to use, modify, and distribute.


---

❤️ Credits

Built using:

Google Gemini API

python-telegram-bot

Railway hosting


Developed with ❤️ by Syed Moinuddin
