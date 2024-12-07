from pyrogram import Client, filters
from config import OWNER_ID
from CakeMusic import *



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
  

add_command_help(
    "sudos",
    [
        [
            "addsudo <reply/username/userid>",
            "Add any user as Sudo (Use This At your own risk maybe sudo users can control ur account).",
        ],
        ["rmsudo <reply/username/userid>", "Remove Sudo access."],
        ["sudolist", "Displays the Sudo List."],
    ],
)
