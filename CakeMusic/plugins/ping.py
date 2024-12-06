import time
import psutil
import platform
from pyrogram import filters
from CakeMusic.__main__. import app
from config import OWNER_ID

# Record the bot's start time
BOT_START_TIME = time.time()

def get_readable_time(seconds: int) -> str:
    """Convert seconds to a readable time format (Days, Hours, Minutes, Seconds)."""
    count = seconds
    days = count // (24 * 3600)
    count %= 24 * 3600
    hours = count // 3600
    count %= 3600
    minutes = count // 60
    count %= 60
    return f"{days}d {hours}h {minutes}m {count}s"

@app.on_message(
    filters.command(["ping"], ".") & (filters.me | filters.user(OWNER_ID))
)
async def ping_command(client, message):
    # Measure response time
    start_time = time.time()
    reply = await message.reply_text("ᴘɪɴɢ ᴘᴏɴɢ ᴘɪɴɢ...")
    end_time = time.time()
    ping_time = (end_time - start_time) * 1000

    # Calculate uptime
    uptime = get_readable_time(int(time.time() - BOT_START_TIME))

    # System stats
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    system_info = platform.system() + " " + platform.release()

    # Advanced response
    response_text = (
        f"🏓 ᴘᴏɴɢ\n\n"
        f"📡 ʀᴇꜱᴘᴏɴꜱᴇ ᴛɪᴍᴇ `{ping_time:.2f} ms`\n"
        f"⏱ ᴜᴘᴛɪᴍᴇ `{uptime}`\n"
        f"🖥 ꜱʏꜱᴛᴇᴍ ɪɴꜰᴏ `{system_info}`\n"
        f"⚙️ ᴄᴘᴜ ᴜꜱᴀɢᴇ `{cpu_usage}%`\n"
        f"💾 ᴍᴇᴍᴏʀʏ ᴜꜱᴀɢᴇ `{memory_usage}%`"
    )
    await reply.edit_text(response_text)
    
