from pyrogram import Client, filters
import time
from CakeMusic import *

@app.on_message(filters.command("ping", prefixes=".") & filters.me)
async def ping(client, message):
    start_time = time.time()
    response = await message.reply_text("Pinging...")
    end_time = time.time()
    ping_time = (end_time - start_time) * 1000  # Convert to milliseconds
    await response.edit_text(f"🏓 Pong! `{ping_time:.2f}ms`")

