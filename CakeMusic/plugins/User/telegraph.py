import os
from pyrogram import filters
from CakeMusic import *
import requests


def upload_file(file_path):
    url = "https://catbox.moe/user/api.php"
    data = {"reqtype": "fileupload", "json": "true"}
    files = {"fileToUpload": open(file_path, "rb")}
    response = requests.post(url, data=data, files=files)

    if response.status_code == 200:
        return True, response.text.strip()
    else:
        return False, f"ᴇʀʀᴏʀ: {response.status_code} - {response.text}"


@app.on_message(filters.command(["tgm"]))
async def get_link_group(client, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Pʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇᴅɪᴀ ғɪʟᴇ ᴛᴏ ᴜᴘʟᴏᴀᴅ ᴏɴ ᴛᴇʟᴇɢʀᴀᴘʜ."
        )

    media = message.reply_to_message
    file_size = 0
    if media.photo:
        file_size = media.photo.file_size
    elif media.video:
        file_size = media.video.file_size
    elif media.document:
        file_size = media.document.file_size

    # Check if file size exceeds 500MB
    if file_size > 500 * 1024 * 1024:
        return await message.reply_text("Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ғɪʟᴇ ᴜɴᴅᴇʀ 500MB.")

    try:
        text = await message.reply("❍ ʜᴏʟᴅ ᴏɴ ʙᴀʙʏ....♡")

        async def progress(current, total):
            try:
                await text.edit_text(f"📥 Dᴏᴡɴʟᴏᴀᴅɪɴɢ... {current * 100 / total:.1f}%")
            except Exception:
                pass

        try:
            # Download the file locally
            local_path = await media.download(progress=progress)
            await text.edit_text("📤 Uᴘʟᴏᴀᴅɪɴɢ ᴛᴏ ᴄᴀᴛʙᴏx...")

            # Upload the file and get the link
            success, upload_path = upload_file(local_path)

            if success:
                await text.edit_text(f"🌐 | ʏᴏᴜʀ ʟɪɴᴋ: {upload_path}")
            else:
                await text.edit_text(
                    f"❌ Aɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴜᴘʟᴏᴀᴅɪɴɢ ʏᴏᴜʀ ғɪʟᴇ:\n{upload_path}"
                )

            # Remove the local file after uploading
            try:
                os.remove(local_path)
            except Exception:
                pass

        except Exception as e:
            await text.edit_text(f"❌ Fɪʟᴇ ᴜᴘʟᴏᴀᴅ ғᴀɪʟᴇᴅ\n\n<i>Rᴇᴀsᴏɴ: {e}</i>")
            try:
                os.remove(local_path)
            except Exception:
                pass
            return
    except Exception:
        pass
