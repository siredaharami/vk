import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from CakeMusic import app, bot, plugs
from CakeMusic.version import __version__
from CakeMusic.sukh.buttons import paginate_plugins
from CakeMusic.sukh.wrapper import cb_wrapper, sudo_users_only
import logging
logging.basicConfig(level=logging.DEBUG)

from asyncio import sleep
from pyrogram.errors import RPCError, BotResponseTimeout

@app.on_message(filters.command("help1"))
async def inline_help_menu(client, message):
    """
    Sends an inline help menu to the user based on the availability of an image or text.
    """
    image = False  # Set to True if you want to fetch "help_menu_logo" instead of "help_menu_text"
    retries = 3
    for attempt in range(retries):
        try:
            query = "help_menu_logo" if image else "help_menu_text"
            bot_results = await app.get_inline_bot_results(f"@{bot.me.username}", query)
            await app.send_inline_bot_result(
                chat_id=message.chat.id,
                query_id=bot_results.query_id,
                result_id=bot_results.results[0].id,
            )
            break  # Exit loop if successful
        except BotResponseTimeout as e:
            print(f"Attempt {attempt + 1}: Telegram timeout: {e}")
            if attempt + 1 < retries:
                await asyncio.sleep(2)  # Retry after a small delay
            else:
                await message.reply_text(
                    "⚠️ Telegram is taking too long to respond. Please try again later."
                )
        except RPCError as e:
            print(f"Attempt {attempt + 1}: RPC Error: {e}")
            await message.reply_text("⚠️ An unexpected RPC error occurred. Please try again later.")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            await message.reply_text("⚠️ An unexpected error occurred. Please try again later.")
            break
        finally:
            try:
                await message.delete()
            except Exception:
                pass



@bot.on_callback_query(filters.regex(r"help_(.*?)"))
@cb_wrapper
async def help_button(client, query):
    """
    Handles navigation within the help menu via callback queries.
    """
    try:
        # Regex matches
        plug_match = re.match(r"help_plugin(.+?)", query.data)
        prev_match = re.match(r"help_prev(.+?)", query.data)
        next_match = re.match(r"help_next(.+?)", query.data)
        back_match = re.match(r"help_back", query.data)

        # Top-level help menu text
        top_text = f"""
**💫 Welcome to the Help Menu, Operator!
Shukla Userbot » {__version__} ✨**

❤️ Click on the buttons below to explore available commands ❤️

🌹 Powered by [Updates](https://t.me/SHIVANSH474) 🌹
"""

        # Plugin-specific help menu
        if plug_match:
            plugin = plug_match.group(1)
            plugin_name = plugs[plugin].__NAME__
            plugin_menu = plugs[plugin].__MENU__
            text = f"**💫 Help Menu for Plugin:** ✨ {plugin_name}\n\n{plugin_menu}"
            key = InlineKeyboardMarkup(
                [[InlineKeyboardButton("↪️ Back", callback_data="help_back")]]
            )
            await bot.edit_inline_text(
                query.inline_message_id,
                text=text,
                reply_markup=key,
                disable_web_page_preview=True,
            )

        # Pagination: Previous page
        elif prev_match:
            curr_page = int(prev_match.group(1))
            await bot.edit_inline_text(
                query.inline_message_id,
                text=top_text,
                reply_markup=InlineKeyboardMarkup(
                    paginate_plugins(curr_page - 1, plugs, "help")
                ),
                disable_web_page_preview=True,
            )

        # Pagination: Next page
        elif next_match:
            next_page = int(next_match.group(1))
            await bot.edit_inline_text(
                query.inline_message_id,
                text=top_text,
                reply_markup=InlineKeyboardMarkup(
                    paginate_plugins(next_page + 1, plugs, "help")
                ),
                disable_web_page_preview=True,
            )

        # Back to main help menu
        elif back_match:
            await bot.edit_inline_text(
                query.inline_message_id,
                text=top_text,
                reply_markup=InlineKeyboardMarkup(
                    paginate_plugins(0, plugs, "help")
                ),
                disable_web_page_preview=True,
            )

    except Exception as e:
        print(f"Error in help_button handler: {e}")
