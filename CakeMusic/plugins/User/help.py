import re
import asyncio
from math import ceil
from traceback import format_exc
from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    InlineQueryResultPhoto, InlineQueryResultArticle, InputTextMessageContent
)
from CakeMusic.version import *
from CakeMusic.misc import SUDOERS
from CakeMusic import app, bot

# Helper Classes and Functions
class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text

def paginate_plugins(page_n, plugin_dict, prefix, chat=None):
    plugins = sorted(
        [
            EqInlineKeyboardButton(
                x.__NAME__,
                callback_data=f"{prefix}_plugin({chat},{x.__NAME__.lower()})" if chat else f"{prefix}_plugin({x.__NAME__.lower()})"
            )
            for x in plugin_dict.values()
        ]
    )
    pairs = list(zip(plugins[::3], plugins[1::3], plugins[2::3]))
    i = 0
    for m in pairs:
        for _ in m:
            i += 1
    if len(plugins) - i == 1:
        pairs.append((plugins[-1],))
    elif len(plugins) - i == 2:
        pairs.append((plugins[-2], plugins[-1]))

    COLUMN_SIZE = 3
    max_num_pages = ceil(len(pairs) / COLUMN_SIZE)
    modulo_page = page_n % max_num_pages

    if len(pairs) > COLUMN_SIZE:
        pairs = pairs[
            modulo_page * COLUMN_SIZE : COLUMN_SIZE * (modulo_page + 1)
        ] + [
            (
                EqInlineKeyboardButton("❮", callback_data=f"{prefix}_prev({modulo_page})"),
                EqInlineKeyboardButton(" Oᴡɴᴇʀ ", url=f"tg://openmessage?user_id={app.me.id}"),
                EqInlineKeyboardButton("❯", callback_data=f"{prefix}_next({modulo_page})")
            )
        ]

    return pairs

# Help Menu Functions
async def help_menu_logo():
    thumb_image = "https://files.catbox.moe/r58nec.jpg"
    button = paginate_plugins(0, plugs, "help")
    return [
        InlineQueryResultPhoto(
            photo_url=thumb_image,
            title="💫 ʜᴇʟᴘ ᴍᴇɴᴜ ✨",
            thumb_url=thumb_image,
            description="🥀 Open Help Menu Of SHUKLAUSERBOT ✨...",
            caption=f"""
**💫 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ʜᴇʟᴘ ᴍᴇɴᴜ ᴏᴘ.
sʜᴜᴋʟᴀ ᴜsᴇʀʙᴏᴛ  » {__version__} ✨**

❤️ᴄʟɪᴄᴋ ᴏɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ᴛᴏ ɢᴇᴛ ᴜsᴇʀʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs ❤️

🌹ᴘᴏᴡᴇʀᴇᴅ ʙʏ ♡ [ᴜᴘᴅᴀᴛᴇ](https://t.me/SHIVANSH474) 🌹
            """,
            reply_markup=InlineKeyboardMarkup(button),
        )
    ]

async def help_menu_text():
    button = paginate_plugins(0, plugs, "help")
    return [
        InlineQueryResultArticle(
            title="💫 ʜᴇʟᴘ ᴍᴇɴᴜ ✨",
            input_message_content=InputTextMessageContent(
                f"""
**💫 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ʜᴇʟᴘ ᴍᴇɴᴜ ᴏᴘ.
sʜᴜᴋʟᴀ ᴜsᴇʀʙᴏᴛ  » {__version__} ✨**

❤️ᴄʟɪᴄᴋ ᴏɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ᴛᴏ ɢᴇᴛ ᴜsᴇʀʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs ❤️

🌹ᴘᴏᴡᴇʀᴇᴅ ʙʏ ♡ [ᴜᴘᴅᴀᴛᴇ](https://t.me/SHIVANSH474) 🌹
                """,
                disable_web_page_preview=True,
            ),
            reply_markup=InlineKeyboardMarkup(button),
        )
    ]

# Inline Query Handler
@app.on_inline_query()
async def inline_query_handler(bot, query):
    text = query.query
    try:
        if text.startswith("help_menu_logo"):
            answer = await help_menu_logo()
        elif text.startswith("help_menu_text"):
            answer = await help_menu_text()
        else:
            answer = []
        await bot.answer_inline_query(query.id, results=answer, cache_time=10)
    except Exception as e:
        print(f"Error in inline query: {e}")

# Command to Open Help Menu
@app.on_message(filters.command("help") & filters.user(SUDOERS))
async def inline_help_menu(client, message):
    try:
        bot_results = await app.get_inline_bot_results(f"@{bot.me.username}", "help_menu_logo")
        await app.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=bot_results.query_id,
            result_id=bot_results.results[0].id,
        )
        await message.delete()
    except Exception as e:
        print(f"Error in help menu: {e}")

# Callback Query Handler
@bot.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query):
    try:
        plug_match = re.match(r"help_plugin(.+?)", query.data)
        prev_match = re.match(r"help_prev(.+?)", query.data)
        next_match = re.match(r"help_next(.+?)", query.data)
        back_match = re.match(r"help_back", query.data)

        top_text = f"""
**🥀 Welcome To Help Menu Of Daxx Userbot » {__version__} ✨...

Click On Below 🌺 Buttons To Get Userbot Commands.

🌷Powered By : [DAXX Server](https://t.me/DAXXSUPPORT).**
"""

        if plug_match:
            plugin = plug_match.group(1)
            text = f"**🥀 Plugin:** {plugs[plugin].__NAME__}\n" + plugs[plugin].__MENU__
            key = InlineKeyboardMarkup([[InlineKeyboardButton("↪️ Back", callback_data="help_back")]])
            await bot.edit_inline_text(query.inline_message_id, text=text, reply_markup=key)

        elif prev_match:
            curr_page = int(prev_match.group(1))
            await bot.edit_inline_text(
                query.inline_message_id,
                text=top_text,
                reply_markup=InlineKeyboardMarkup(paginate_plugins(curr_page - 1, plugs, "help")),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            await bot.edit_inline_text(
                query.inline_message_id,
                text=top_text,
                reply_markup=InlineKeyboardMarkup(paginate_plugins(next_page + 1, plugs, "help")),
            )

        elif back_match:
            await bot.edit_inline_text(
                query.inline_message_id,
                text=top_text,
                reply_markup=InlineKeyboardMarkup(paginate_plugins(0, plugs, "help")),
            )
    except Exception as e:
        print(f"Error in callback query: {e}")
