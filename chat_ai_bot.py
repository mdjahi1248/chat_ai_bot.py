import telebot
import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def ai_reply(text):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful multilingual AI. Reply naturally in Bangla, English, Hindi, or Nepali."},
            {"role": "user", "content": text}
        ],
        "max_tokens": 500
    }

    r = requests.post(url, headers=headers, json=data)
    res = r.json()
    return res["choices"][0]["message"]["content"]

@bot.message_handler(func=lambda m: True)
def chat(m):
    try:
        reply = ai_reply(m.text)
        bot.reply_to(m, reply)
    except:
        bot.reply_to(m, "⚠️ AI এখন কাজ করছে না")

print("Bot running...")
bot.infinity_polling()
