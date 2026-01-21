import telebot
import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def ai_reply(text):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a friendly multilingual AI. Reply naturally in Bangla, English, Hindi, or Nepali."},
            {"role": "user", "content": text}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    r = requests.post(url, headers=headers, json=data, timeout=60)
    res = r.json()

    if "choices" not in res:
        print("GROQ ERROR:", res)
        return "⚠️ AI এখন কাজ করছে না"

    return res["choices"][0]["message"]["content"]

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🤖 হ্যালো! আমি GM AI Bot.\nযেকোনো কিছু লিখুন 🙂")

@bot.message_handler(func=lambda m: True)
def chat(m):
    try:
        bot.send_chat_action(m.chat.id, 'typing')
        reply = ai_reply(m.text)
        bot.reply_to(m, reply)
    except Exception as e:
        print("ERROR:", e)
        bot.reply_to(m, "⚠️ AI error, পরে আবার চেষ্টা করো")

print("🤖 Bot running...")
bot.infinity_polling()
