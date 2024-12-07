from pyrogram import Client, filters
from config import OWNER_ID
from CakeMusic import *
from CakeMusic.plugins.help import HelpMenu


@app.on_message(
    filters.command(["ping"], ".") & (filters.me | filters.user(OWNER_ID))
)
async def ping(client, message):
    # Stylish text
    reply_text = "⚡ **Ping Pong!**\n💠 Bot is Online and Working Perfectly!"
    
    # Image file path (Ensure this image exists in your bot's directory)
    image_path = "https://files.catbox.moe/xwygzj.jpg"  # Replace with the path to your image file

    # Sending the message with the image
    await message.reply_photo(photo=image_path, caption=reply_text)
  

HelpMenu("ping").add(
    "ping",
    "<reason>",
    "Set your status as AFK. When someone mentions' you, the bot will tell them you're currently Offline! You can also use a media by replying to it.",
    "afk good night!",
    "To unset afk you can send a message to any chat and it'll automaticslly get disabled! You can use 'afk' in your message to bypass automatic disabling of afk.",
).info("Away From Keyboard").done()
