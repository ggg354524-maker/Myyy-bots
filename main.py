import random, asyncio, time
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "I am alive"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

api_id = 36483598
api_hash = '188e25271d55c4939783589fefacde78'

base_words = ["يابن", "الضعيفتين", "الضعيفه", "ادعس", "امك", "كس", "عرضك", "هيا", "اصمل", "القحبتين", "الهطف", "لا", "تشرد", "ي مضحكه", "الشرموطه", "الديوث", "اختك", "ي ابن الهطف", "ي ابن الديوث"]
emoji_sets = ["🥺✌🏼", "😵‍💫☘️", "🌪️💤"]

client = TelegramClient(StringSession(), api_id, api_hash)
active_tasks = {}

@client.on(events.NewMessage(outgoing=True))
async def handler(event):
    global active_tasks
    text = event.raw_text
    
    if text.startswith("جلد"):
        parts = text.split()
        if len(parts) < 2: return
        
        target = parts[1]
        active_tasks[target] = True
        last_emoji_time = time.time()
        last_msg = ""
        
        while active_tasks.get(target):
            try:
                while True:
                    shuffled = random.sample(base_words, 7)
                    msg = " ".join(shuffled)
                    if msg != last_msg: break
                
                current_time = time.time()
                if current_time - last_emoji_time >= 10:
                    msg += f" {random.choice(emoji_sets)}"
                    last_emoji_time = current_time
                
                await client.send_message(target, msg)
                last_msg = msg
                await asyncio.sleep(0.6)
            except:
                break

    elif text.startswith("خلاص"):
        parts = text.split()
        if len(parts) > 1:
            target = parts[1]
            active_tasks[target] = False

if __name__ == "__main__":
    keep_alive()
    client.start() 
    client.run_until_disconnected()
