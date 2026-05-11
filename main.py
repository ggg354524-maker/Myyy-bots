import random
import sys
import asyncio
import time
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError

api_id = 36483598
api_hash = '188e25271d55c4939783589fefacde78'

words_list = [
    "كس امك", "يابن الشرموطه", "يابن الضعيفتين", 
    "يابن الشرموطتين", "يابن القحبتين", "ي ابن الديوث", 
    "كس اختك", "ادعس امك", "ياكس امك", 
    "ي ابن الضعيفه", "ادوس مامتك", "كس عيلتك",
    "ي ابن العاهرتين", "ي ابن المصخرتين", "يا هطف", "ي مصخره", "مضحكه"
]

special_words = ["اسسسرع", "اجري معاي", "لا تشرددد", "اسررررع", "هيا اكتب معاي"]
emojis = ["🦋✌🏽😭", "☘️"]

client = TelegramClient('saloum', api_id, api_hash)
is_running = False

@client.on(events.NewMessage(outgoing=True))
async def handler(event):
    global is_running
    
    if event.is_private and event.to_id.user_id == (await client.get_me()).id:
        if event.raw_text == "خلاص":
            is_running = False
            await event.edit("⚠️ STOPPED")
            return

        if event.raw_text.startswith("اصمل "):
            parts = event.raw_text.split(" ")
            enemy_name = parts[1] if len(parts) > 1 else "هطف"
            speed = float(parts[2]) if len(parts) > 2 else 2.0
            is_running = True
            await event.edit(f"🚀 RUNNING\nTarget: {enemy_name}\nSpeed: {speed}")
            
            target_chat = None
            async for dialog in client.iter_dialogs():
                if dialog.is_group:
                    target_chat = dialog.id
                    break
            
            if not target_chat:
                await event.edit("❌ NO GROUP")
                is_running = False
                return

            last_special_time = time.time()
            last_enemy_time = time.time()
            last_sent_line = ""

            while is_running:
                current_time = time.time()

                if current_time - last_enemy_time >= 15:
                    try:
                        await client.send_message(target_chat, f"ي {enemy_name} {random.choice(words_list)} 🦋")
                        last_enemy_time = current_time
                    except: pass

                if current_time - last_special_time >= 10:
                    random.shuffle(special_words)
                    try:
                        await client.send_message(target_chat, f"{' '.join(special_words)} {random.choice(emojis)}")
                        last_special_time = current_time
                    except: pass

                while True:
                    selected = random.sample(words_list, 3)
                    new_line = " ".join(selected)
                    if new_line != last_sent_line:
                        last_sent_line = new_line
                        break

                try:
                    async with client.action(target_chat, 'typing'):
                        await asyncio.sleep(speed * 0.6)
                        await client.send_message(target_chat, new_line)
                    await asyncio.sleep(speed * 0.4)
                except FloodWaitError as e:
                    await asyncio.sleep(e.seconds)
                except:
                    await asyncio.sleep(speed)

client.start()
client.run_until_disconnected()
