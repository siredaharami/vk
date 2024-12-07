from CakeMusic import app  # Import the app client from your CakeMusic module
from pyrogram import filters
from pyrogram.types import Message

@app.on_message(filters.command("ping"))
async def ping(bot: app, msg: Message):
    """
    Ping command: Respond with 'Pong!' when the /ping command is issued.
    """
    await msg.reply("Pong!")
