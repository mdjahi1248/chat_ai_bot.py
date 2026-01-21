import os
import telebot
import requests

# =========================
# 🔐 LOAD FROM ENV (GitHub / Railway Secrets)
# =========================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not TELEGRAM_TOKEN or not GROQ_API_KEY:
    print("❌ TOKEN পাওয়া যায়নি. Railway / GitHub secrets check করো.")
    exit()

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# user mode store
user_mode = {}

# =========================
# 🤖 AI REPLY FUNCTION
# =========================
def ai_reply(text, mode="both"):
    if mode == "bangla":
        system_prompt = "You are a friendly AI assistant. Always reply only in Bangla."
    elif mode == "english":
        system_prompt = "You are a friendly AI assistant. Always reply only in English."
    else:
        system_prompt = "You are a friendly AI assistant. Reply naturally in Bangla or English."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        r = requests.post(url, headers=headers, json=data, timeout=60)
        res = r.json()
    except Exception as e:
        print("REQUEST ERROR:", e)
        return "⚠️ Server error, পরে আবার চেষ্টা করো।"

    if "choices" not in res:
        print("GROQ ERROR:", res)
        return "⚠️ AI কাজ করছে না, API / model check করো।"

    return res["choices"][0]["message"]["content"]


# =========================
# 📌 COMMANDS
# =========================
@bot.message_handler(commands=['start'])
def start(m):
    user_mode[m.chat.id] = "both"
    bot.reply_to(m,
        "🤖 হ্যালো! আমি আপনার AI Chat Bot.\n\n"
        "Commands:\n"
        "/bangla - শুধু বাংলা\n"
        "/english - শুধু English\n"
        "/help - সাহায্য\n\n"
        "যেকোনো কিছু লিখুন 🙂"
    )

@bot.message_handler(commands=['help'])
def help_cmd(m):
    bot.reply_to(m,
        "🆘 সাহায্য:\n\n"
        "/bangla - বাংলা mode\n"
        "/english - English mode\n"
        "/start - reset bot\n\n"
        "এরপর যেকোনো প্রশ্ন লিখুন।"
    )

@bot.message_handler(commands=['bangla'])
def bangla_mode(m):
    user_mode[m.chat.id] = "bangla"
    bot.reply_to(m, "🇧🇩 বাংলা mode ON ✅ এখন আমি শুধু বাংলায় কথা বলবো।")

@bot.message_handler(commands=['english'])
def english_mode(m):
    user_mode[m.chat.id] = "english"
    bot.reply_to(m, "🇺🇸 English mode ON ✅ Now I will reply only in English.")


# =========================
# 💬 CHAT HANDLER
# =========================
@bot.message_handler(func=lambda m: True)
def chat(m):
    try:
        bot.send_chat_action(m.chat.id, 'typing')
        mode = user_mode.get(m.chat.id, "both")
        reply = ai_reply(m.text, mode)
        bot.reply_to(m, reply)
    except Exception as e:
        print("AI ERROR:", e)
        bot.reply_to(m, "⚠️ এখন AI কাজ করছে না, একটু পরে আবার চেষ্টা করুন।")


print("🤖 Telegram AI bot running...")
bot.infinity_polling()
