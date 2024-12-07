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
  

HelpMenu("convert").add(
    "stog", #Bugged: to-be-fixed
    "<reply>",
    "Converts animated sticker to gif.",
    None,
    "Only animated sticker and video sticker can be converted to gif.",
).add(
    "stoi",
    "<reply>",
    "Converts sticker to image.",
    None,
    "Only static stickers can be converted to image.",
).add(
    "itos",
    "<reply>",
    "Converts image to sticker.",
    None,
    "Only images can be converted to sticker.",
).add(
    "ftoi",
    "<reply>",
    "Converts file to image.",
    None,
    "Only image files can be converted to image.",
).add(
    "itof",
    "<reply>",
    "Converts image to file.",
    None,
    "Only images can be converted to file.",
).add(
    "tovoice",
    "<reply>",
    "Converts media to voice.",
    None,
    "Only video/audio can be converted to voice.",
).add(
    "tomp3",
    "<reply>",
    "Converts media to mp3.",
    None,
    "Only video/audio can be converted to mp3.",
).info(
    "Converts media to other formats."
).done()
