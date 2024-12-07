import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from CakeMusic import app, bot, plugs
from CakeMusic.version import __version__
from CakeMusic.modules.buttons import paginate_plugins
from CakeMusic.modules.wrapper import cb_wrapper



@app.on_message(filters.command("help") & filters.private)
async def inline_help_menu(client, message):
    # Define the `image` variable if needed for conditional inline menu
    image = False

    try:
        # Fetch inline bot results based on the presence of `image`
        bot_results = await app.get_inline_bot_results(
            f"@{bot.me.username}", 
            "help_menu_logo" if image else "help_menu_text"
        )
        # Send the inline bot result to the user
        await app.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=bot_results.query_id,
            result_id=bot_results.results[0].id,
        )
    except Exception as e:
        print(f"Error in inline_help_menu: {e}")
    finally:
        try:
            await message.delete()
        except Exception as e:
            print(f"Failed to delete the message: {e}")


@bot.on_callback_query(filters.regex(r"help_(.*?)"))
@cb_wrapper
async def help_button(client, query):
    data = query.data
    top_text = f"""
**💫 Welcome to the Help Menu.
PBX Userbot » {__version__} ✨

❤️ Click the buttons below to get the userbot commands ❤️.

🌹 Powered by ☆ [PBX Update](https://t.me/HEROKUBIN_01) 🌹**
"""

    # Handle different callback queries
    if match := re.match(r"help_plugin(.+?)", data):
        plugin = match.group(1)
        text = f"""
**💫 Welcome to the Help Menu of
♨️ Plugin ✨ {plugs[plugin].__NAME__}**
{plugs[plugin].__MENU__}
"""
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("↪️ Back", callback_data="help_back")]]
        )
        await bot.edit_inline_text(
            query.inline_message_id,
            text=text,
            reply_markup=reply_markup,
            disable_web_page_preview=True,
        )
    elif match := re.match(r"help_prev(.+?)", data):
        curr_page = int(match.group(1))
        await bot.edit_inline_text(
            query.inline_message_id,
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_plugins(curr_page - 1, plugs, "help")
            ),
            disable_web_page_preview=True,
        )
    elif match := re.match(r"help_next(.+?)", data):
        next_page = int(match.group(1))
        await bot.edit_inline_text(
            query.inline_message_id,
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_plugins(next_page + 1, plugs, "help")
            ),
            disable_web_page_preview=True,
        )
    elif re.match(r"help_back", data):
        await bot.edit_inline_text(
            query.inline_message_id,
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_plugins(0, plugs, "help")
            ),
            disable_web_page_preview=True,
        )
