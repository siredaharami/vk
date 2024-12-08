import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from CakeMusic import *
from CakeMusic.version import __version__
from CakeMusic.sukh.buttons import *
from CakeMusic.sukh.inline import *
from CakeMusic.sukh.wrapper import *


# Command handler for help2
@app.on_message(filters.command("help2"))
async def inline_help_menu(client, message):
    image = None
    try:
        if image:
            bot_results = await app.get_inline_bot_results(
                f"@{app.me.username}", "help_menu_logo"
            )
        else:
            bot_results = await app.get_inline_bot_results(
                f"@{app.me.username}", "help_menu_text"
            )
        await app.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=bot_results.query_id,
            result_id=bot_results.results[0].id,
        )
    except Exception as e:
        print(f"Error fetching bot results: {e}")
        bot_results = await app.get_inline_bot_results(
            f"@{app.me.username}", "help_menu_text"
        )
        await app.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=bot_results.query_id,
            result_id=bot_results.results[0].id,
        )

    try:
        await message.delete()
    except Exception as e:
        print(f"Error deleting message: {e}")


# Callback handler for inline buttons
@bot.on_callback_query(filters.regex(r"help_(.*?)"))
@cb_wrapper
async def help_button(client, query):
    plug_match = re.match(r"help_plugin(.+?)", query.data)
    prev_match = re.match(r"help_prev(.+?)", query.data)
    next_match = re.match(r"help_next(.+?)", query.data)
    back_match = re.match(r"help_back", query.data)
    
    top_text = f"""
**💫 Welcome to Help Menu op.
Shukla UserBot  » {__version__} ✨
 
❤️Click on below buttons to get userbot commands ❤️.

Powered by [Updates](https://t.me/SHIVANSH474) 🌹
"""
    
    if plug_match:
        plugin = plug_match.group(1)
        text = f"**💫 Welcome to Help Menu of Plugin: {plugs[plugin].__NAME__}**\n{plugs[plugin].__MENU__}"
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="↪️ Back", callback_data="help_back"
                    )
                ],
            ]
        )

        await app.edit_inline_text(
            query.inline_message_id,
            text=text,
            reply_markup=key,
            disable_web_page_preview=True
        )
    
    elif prev_match:
        curr_page = int(prev_match.group(1))
        await app.edit_inline_text(
            query.inline_message_id,
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_plugins(curr_page - 1, plugs, "help")
            ),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match.group(1))
        await app.edit_inline_text(
            query.inline_message_id,
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_plugins(next_page + 1, plugs, "help")
            ),
            disable_web_page_preview=True,
        )

    elif back_match:
        await app.edit_inline_text(
            query.inline_message_id,
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_plugins(0, plugs, "help")
            ),
            disable_web_page_preview=True,
        )


# Run the bot
app.run()
