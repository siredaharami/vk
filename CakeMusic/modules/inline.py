import asyncio
from BADMUNDA.modules.buttons import *
from BADMUNDA.modules.wrapper import *
from pyrogram.types import *


async def help_menu_logo(answer):
    image = None
    if image:
        thumb_image = image
    else:
        thumb_image = "https://telegra.ph/file/3063af27d9cc8580845e1.jpg"
    button = paginate_plugins(0, plugs, "help")
    answer.append(
        InlineQueryResultPhoto(
            photo_url=f"{thumb_image}",
            title="💫 ʜᴇʟᴘ ᴍᴇɴᴜ  ✨",
            thumb_url=f"{thumb_image}",
            description=f"🥀 Open Help Menu Of PBXUSERBOT ✨...",
            caption=f"""
            **💫 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ʜᴇʟᴘ ᴍᴇɴᴜ ᴏᴘ.
ᴘʙx ᴜsᴇʀʙᴏᴛ  » {__version__} ✨
 
❤️ᴄʟɪᴄᴋ ᴏɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ᴛᴏ
ɢᴇᴛ ᴜsᴇʀʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs ❤️
 
🌹ᴘᴏᴡᴇʀᴇᴅ ʙʏ ☆  [ ᴘʙx ᴜᴘᴅᴀᴛᴇ ](https://t.me/HEROKUBIN_01) 🌹**""",
            reply_markup=InlineKeyboardMarkup(button),
        )
    )
    return answer


async def help_menu_text(answer):
    from ... import __version__
    button = paginate_plugins(0, plugs, "help")
    answer.append(
        InlineQueryResultArticle(
            title="💫 ʜᴇʟᴘ ᴍᴇɴᴜ  ✨",
            input_message_content=InputTextMessageContent(f"""
            **💫 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ʜᴇʟᴘ ᴍᴇɴᴜ ᴏᴘ.
ᴘʙx ᴜsᴇʀʙᴏᴛ  » {__version__} ✨
 
❤️ᴄʟɪᴄᴋ ᴏɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ᴛᴏ
ɢᴇᴛ ᴜsᴇʀʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs ❤️
 
🌹ᴘᴏᴡᴇʀᴇᴅ ʙʏ ☆  [ ᴘʙx ᴜᴘᴅᴀᴛᴇ ](https://t.me/HEROKUBIN_01) 🌹**""",
            disable_web_page_preview=True
            ),
            reply_markup=InlineKeyboardMarkup(button),
        )
    )
    return answer


async def run_async_inline():
    @bot.on_inline_query()
    @inline_wrapper
    async def inline_query_handler(bot, query):
        text = query.query
        if text.startswith("help_menu_logo"):
            answer = []
            answer = await help_menu_logo(answer)
            try:
                await bot.answer_inline_query(
                    query.id, results=answer, cache_time=10
                )
            except Exception as e:
                print(str(e))
                return
        elif text.startswith("help_menu_text"):
            answer = []
            answer = await help_menu_text(answer)
            try:
                await bot.answer_inline_query(
                    query.id, results=answer, cache_time=10
                )
            except Exception as e:
                print(str(e))
                return
        else:
            return
