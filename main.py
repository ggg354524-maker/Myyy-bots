import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from flask import Flask
from threading import Thread

web = Flask('')
@web.route('/')
def home(): return "Online"
def run(): web.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

keep_alive()

API_ID = 36483598
API_HASH = '188e25271d55c4939783589fefacde78'
STRING_SESSION = "AQIssg4AeNvWllOnyYO7N9ODBA0R7ci8g0qL942dHIXZy1TulXszq7LCjJcEgGiN4pxc41CWh3Houg19X681xaCjcLJKLqAhn57p4DnCy5_N2i0YZmAGiySV9HUTIfVdT6sW2PjRdagz9Om8T6q5MopGq4KxEgksIlvfMFl7Svdbu0SzjyV9FrUysd0-1DOSExHUxff8ah72fMYg0K6XwSq5p_R6AHcfyc00IjfXtxEE5KMG-mjfFMHD3tCvpV1JWKuHy7F6lnS0MIXXuYYvomk04cGQtRQ60w-7ooq18FTNy-JFb3zwsZaTdjRhjk9hGPPDIfbV-_qo9XAHhEUIefezvLfjuwAAAAH2umIhAA"

app = Client("my_account", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

input_lines = [
    "وش تسوي ادعس عليك يابن المصخره ي هطف ي ديوث", "كس ام عرضك وش تسوي يعني تبيني انيك ف كس عرضك ي ابن الضعيفتين", "ادعس عليك ي مصخره ي ابن المصخره ي جديد ي كس اختك", "كس اختك اصمل وش تسوي ي مصخره وش تسوي ي ديوث", "وش بك ي ابن القحبتين ب تصمل معي اليوم ي ديوث تفهم ؟ 😭✌🏽",
    "كسس عرضك ب تصمل معي صدقني ي ابن المصخره 🦄", "وش تسوي ي ضعيف يابن القحبه ي كسسس عرضك اصمل ل انيك ف اختك", "كسسس اختك اصمل وش تسوي ي ابن القحبتين", "وش بك ي ابن المصخره ي كسس عرضك وش تسوي ي ابن الضعيفه", "وش تسوي ادعس عليك ي ابن الضعيفتين ي ابن المصخرتين اصمل وش تسوي",
    "ي ابن القحبتين ي ديوث وش تسوي ي كسسس امك اصمل", "اشق كس امك ي ابن القحبتين اصمل وش تسوي ي ضعيف ي مصخره", "كس امك وش تسوي وش بك س كسس اختك ي ضعيف", "يابن القحبتين اصمل وش تسوي وش بك ي ديوث وش تسوي قل", "كس اختك ي ديوث اصمل وش تسوي وش بك ي ابن المصخره",
    "وش بك وش تسوي اشق كس امك اصمل وش تسوي 🌪️☘️", "يابن القحبه كس عرضك وش تسوي ي ضعيف يابن الشرموطتين ي مصخره ي كسس عرضك"
]

is_running = False

async def get_speed():
    try:
        async for msg in app.get_chat_history("me", limit=1):
            return float(msg.text)
    except: return 2.0 

@app.on_message(filters.me & filters.text)
async def controller(client, message):
    global is_running
    if message.text == "ادعس عليك ي مصخره":
        if is_running: return
        is_running = True
        big_list = []
        while len(big_list) < 16000:
            temp = input_lines.copy()
            random.shuffle(temp)
            big_list.extend(temp)
        big_list = big_list[:16000]
        for line in big_list:
            if not is_running: break
            try:
                await client.send_chat_action(message.chat.id, ChatAction.TYPING)
                await asyncio.sleep(0.1)
                await client.send_message(message.chat.id, line)
                await asyncio.sleep(await get_speed())
            except: await asyncio.sleep(5)
    elif message.text == "هههه وش بك ؟":
        is_running = False

app.run()
