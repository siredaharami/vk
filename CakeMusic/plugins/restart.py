import asyncio
from pyrogram import Client, filters as pyrofl
from config import MONGO_DB_URL, OWNER_ID
from CakeMusic.misc import SUDOERS
from pyrogram.types import Message
from CakeMusic import bot

@bot.on_message(cdx(["restart"]) & SUDOERS)
async def restart(client: Client, message: Message):
    reply = await message.reply_text("ʀᴇꜱᴛᴀʀᴛɪɴɢ...")
    await message.delete()
    await reply.edit_text("ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʀᴇꜱᴛᴀʀᴛᴇᴅ ʙᴀᴅᴜꜱᴇʀʙᴏᴛ...\n\n💞 ᴡᴀɪᴛ 1-2 ᴍɪɴᴜᴛᴇꜱ\nʟᴏᴀᴅ ᴘʟᴜɢɪɴꜱ...</b>")
    os.system(f"kill -9 {os.getpid()} && python3 -m YukkiMusic")

#sudo
