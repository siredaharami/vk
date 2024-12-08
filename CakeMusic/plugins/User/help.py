import re
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from CakeMusic import app, bot, plugs
from CakeMusic.version import __version__
from CakeMusic.sukh.buttons import paginate_plugins
from CakeMusic.sukh.wrapper import cb_wrapper, sudo_users_only
from pyrogram.errors import RPCError, BotResponseTimeout
import logging
import time

logging.basicConfig(level=logging.DEBUG)

async def fetch_inline_results(bot_username, query, retries=2, delay=3):
    """Fetch inline bot results with retries."""
    for attempt in range(retries):
        try:
            start_time = time.time()
            bot_results = await app.get_inline_bot_results(bot_username, query)
            end_time = time.time()
            logging.info(f"Inline query processed in {end_time - start_time} seconds")
            return bot_results
        except BotResponseTimeout as e:
            logging.warning(f"Timeout on attempt {attempt + 1}/{retries}: {e}")
            await asyncio.sleep(delay)
    raise Exception("Failed to fetch inline results after retries")
    
cache = {}

async def get_cached_inline_results(query):
    """Fetch cached results or generate new ones."""
    if query in cache:
        return cache[query]
    # Generate new results and cache them
    results = await app.get_inline_bot_results(f"@{bot.me.username}", query)
    cache[query] = results
    return results
    logging.debug(f"Fetching inline results for query: {query}")

@app.on_message(filters.command("help1"))
async def inline_help_menu(client, message):
    image = None
    try:
        if image:
            bot_results = await app.get_inline_bot_results(
                f"@{bot.me.username}", "help_menu_logo"
            )
        else:
            bot_results = await app.get_inline_bot_results(
                f"@{bot.me.username}", "help_menu_text"
            )
        await app.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=bot_results.query_id,
            result_id=bot_results.results[0].id,
        )
    except Exception:
        bot_results = await app.get_inline_bot_results(
            f"@TEST_BOT_NEW_MUSIC_Bot", "help_menu_text"
        )
        await app.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=bot_results.query_id,
            result_id=bot_results.results[0].id,
        )
    except Exception as e:
        print(e)
        return

    try:
        await message.delete()
    except:
        pass
      

@bot.on_callback_query(filters.regex(r"help_(.*?)"))
@cb_wrapper
async def help_button(client, query):
    """Handle callback queries for help menu."""
    try:
        plug_match = re.match(r"help_plugin(.+?)", query.data)
        prev_match = re.match(r"help_prev(.+?)", query.data)
        next_match = re.match(r"help_next(.+?)", query.data)
        back_match = re.match(r"help_back", query.data)

        top_text = f"""
**💫 Welcome to the Help Menu Op.
Shukla UserBot  » {__version__} ✨**

❤️ Click the buttons below to explore commands. ❤️

🌹 Powered by ♡ [Update](https://t.me/SHIVANSH474) 🌹**
"""
        if plug_match:
            plugin = plug_match.group(1)
            text = (
                f"**💫 Welcome to the help menu for plugin ✨ {plugs[plugin].__NAME__}**\n"
                + plugs[plugin].__MENU__
            )
            key = InlineKeyboardMarkup(
                [[InlineKeyboardButton("↪️ Back", callback_data="help_back")]]
            )
            await bot.edit_inline_text(
                query.inline_message_id, text=text, reply_markup=key, disable_web_page_preview=True
            )
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
        elif back_match:
            await bot.edit_inline_text(
                query.inline_message_id,
                text=top_text,
                reply_markup=InlineKeyboardMarkup(paginate_plugins(0, plugs, "help")),
                disable_web_page_preview=True,
            )
    except Exception as e:
        logging.error(f"Error in `help_button`: {e}")
