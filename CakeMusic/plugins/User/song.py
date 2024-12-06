import requests
import shutil
import yt_dlp
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch
from CakeMusic import app
from CakeMusic import *
# Constants
COOKIES_FILE = "cookies.txt"
SPAM_WINDOW_SECONDS = 5
SPAM_THRESHOLD = 3
user_last_message_time = {}
user_command_count = {}

@app.on_message(cdx("song"))
async def download_song(client, message):
    user_id = message.from_user.id
    current_time = message.date.timestamp()
    
    # Spam protection
    last_message_time = user_last_message_time.get(user_id, 0)
    if current_time - last_message_time < SPAM_WINDOW_SECONDS:
        user_last_message_time[user_id] = current_time
        user_command_count[user_id] = user_command_count.get(user_id, 0) + 1
        if user_command_count[user_id] > SPAM_THRESHOLD:
            warning_msg = await message.reply_text(f"{message.from_user.mention} ᴘʟᴇᴀsᴇ ᴅᴏɴ'ᴛ sᴘᴀᴍ. ᴛʀʏ ᴀɢᴀɪɴ ᴀғᴛᴇʀ 5 sᴇᴄᴏɴᴅs.")
            await asyncio.sleep(3)
            await warning_msg.delete()
            return
    else:
        user_command_count[user_id] = 1
        user_last_message_time[user_id] = current_time

    # Extract query
    query = " ".join(message.command[1:])
    if not query:
        await message.reply("🔗 ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ꜱᴏɴɢ ɴᴀᴍᴇ ᴏʀ ʟɪɴᴋ.")
        return

    # Reply with search status
    m = await message.reply("🔍ꜱᴇᴀʀᴄʜɪɴɢ...")
    ydl_opts = {
        "format": "bestaudio[ext=m4a]",
        "noplaylist": True,
        "quiet": True,
        "logtostderr": False,
        "cookiefile": COOKIES_FILE,
    }

    try:
        # Search for the song
        results = YoutubeSearch(query, max_results=1).to_dict()
        if not results:
            await m.edit("😮‍💨 ɴᴏ ʀᴇꜱᴜʟᴛꜱ ꜰᴏᴜɴᴅ. ᴄʜᴇᴄᴋ ʏᴏᴜʀ ꜱᴇᴀʀᴄʜ.")
            return

        # Extract song details
        result = results[0]
        link = f"https://youtube.com{result['url_suffix']}"
        title = result["title"]
        thumbnail_url = result["thumbnails"][0]
        duration = result["duration"]
        views = result["views"]
        channel_name = result["channel"]

        # Download thumbnail
        thumbnail_file = f"{title}.jpg"
        with open(thumbnail_file, "wb") as f:
            f.write(requests.get(thumbnail_url).content)

        # Download song
        await m.edit("💫 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...")
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info)
            ydl.download([link])

        # Parse duration in seconds
        duration_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(duration.split(":"))))

        # Upload audio
        await m.edit("😍 ᴜᴘʟᴏᴀᴅɪɴɢ...")
        await message.reply_audio(
            audio_file,
            thumb=thumbnail_file,
            title=title,
            caption=f"{title}\nRequested by ➪ {message.from_user.mention}\nViews ➪ {views}\nChannel ➪ {channel_name}",
            duration=duration_seconds,
        )

        # Cleanup
        os.remove(audio_file)
        os.remove(thumbnail_file)
        await m.delete()

    except Exception as e:
        await m.edit("🙂 ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ! ᴄᴏɴᴛᴀᴄᴛ @ll_BAD_MUNDA_ll.")
        print(f"Error: {e}")
