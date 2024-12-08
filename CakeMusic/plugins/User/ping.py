from pyrogram import Client, filters
from config import OWNER_ID
from CakeMusic import *
from CakeMusic.plugins.User.help2 import *


@app.on_message(
    filters.command(["ping"], ".") & (filters.me | filters.user(OWNER_ID))
)
@plugin(
    name="admin",
    description="""
    **Admin Plugin**
    - **Command**: /admin
    - **Description**: This plugin gives admin-like controls, such as banning users or setting permissions.
    - **Usage**: Type /admin to access admin commands.
    """
)
async def ping(client, message):
    # Stylish text
    reply_text = "⚡ **Ping Pong!**\n💠 Bot is Online and Working Perfectly!"
    
    # Image file path (Ensure this image exists in your bot's directory)
    image_path = "https://files.catbox.moe/xwygzj.jpg"  # Replace with the path to your image file

    # Sending the message with the image
    await message.reply_photo(photo=image_path, caption=reply_text)
  

