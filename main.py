import telebot
import time
import random
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "Bot is Running!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

TOKEN = '8691167970:AAHjcP9A0WFBpDtbau0lQGvw77nogd43A_M'
bot = telebot.TeleBot(TOKEN)

base_words = ["وين", "كيف", "يا ولد", "اصمل", "وش تسوي", "وش فيك", "طيب", "كمل", "يا مسكين"]
EASY_CHALLENGES = [" ".join(random.sample(base_words, len(base_words))) for _ in range(10000)]

phil_base = [
    "نحن مجرد ركام من الذكريات ننتظر حتمية الفناء في صمت",
    "الحياة دائرة مفرغة من العبث نكرر فيها خيبات من سبقونا",
    "الزمن يسرق منا ما تبقى من دهشة حتى نتلاشى كالهباء",
    "كل اجتماع هو مشروع عزاء مؤجل ننتظر فيه دورنا تلو الآخر",
    "نحن غرباء في عالم لا يبالي محاصرون بين العدم والعدم"
]
PHIL_CHALLENGES = [random.choice(phil_base) for _ in range(10000)]

user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ارحب، اكتب (فس) أو (سهل)")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.strip()
    name = message.from_user.first_name 

    if text == "فس":
        target_text = random.choice(PHIL_CHALLENGES)
        user_data[chat_id] = {'text': target_text, 'start': time.time()}
        bot.send_message(chat_id, target_text)
        return
    
    if text == "سهل":
        target_text = random.choice(EASY_CHALLENGES)
        user_data[chat_id] = {'text': target_text, 'start': time.time()}
        bot.send_message(chat_id, target_text)
        return

    if chat_id in user_data:
        if text == user_data[chat_id]['text']:
            duration = round(time.time() - user_data[chat_id]['start'], 2)
            result_msg = f"بطل يا {name}#\nسرعتك هيا {duration} ثانية"
            bot.reply_to(message, result_msg)
            del user_data[chat_id]

if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True)
