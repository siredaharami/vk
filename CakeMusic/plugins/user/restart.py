import os
import shutil
import asyncio
from pyrogram.types import Message
from pyrogram import filters, Client
from CakeMusic import app
from pyrogram import Client
from CakeMusic.misc import SUDOERS

@app.on_message(
    filters.command(["restart"], ".") & (filters.me | filters.user(SUDOERS))
)
async def restart(client: Client, message: Message):
    reply = await message.reply_text("ʀᴇꜱᴛᴀʀᴛɪɴɢ...")
    await message.delete()
    await reply.edit_text("ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʀᴇꜱᴛᴀʀᴛᴇᴅ ʙᴀᴅᴜꜱᴇʀʙᴏᴛ...\n\n💞 ᴡᴀɪᴛ 1-2 ᴍɪɴᴜᴛᴇꜱ\nʟᴏᴀᴅ ᴘʟᴜɢɪɴꜱ...</b>")
    os.system(f"kill -9 {os.getpid()} && python3 -m YukkiMusic")
    
