import re
from pyrogram import *
from pyrogram.types import *
from CakeMusic import *
from CakeMusic.version import __version__
from CakeMusic.sukh.buttons import *
from CakeMusic.sukh.inline import *
from CakeMusic.sukh.wrapper import *

from pyrogram.errors import UsernameNotFound, BotResponseTimeout, PeerIdInvalid, RPCError
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

async def inline_help_menu(app, query):
    try:
        # Wrap the code that causes the error in try-except block
        bot_results = await app.get_inline_bot_results(query)
        # Handle successful bot results here
        return bot_results
    except UsernameNotFound as e:
        # Handle case when username is not found
        logging.error(f"Username not found: {e}")
        return "Sorry, the username you are looking for is not available."
    except BotResponseTimeout as e:
        # Handle bot response timeout
        logging.error(f"Bot response timed out: {e}")
        return "The bot took too long to respond, please try again later."
    except PeerIdInvalid as e:
        # Handle invalid peer ID
        logging.error(f"Invalid peer ID: {e}")
        return "The peer ID provided is invalid."
    except RPCError as e:
        # Handle any other RPC errors
        logging.error(f"RPC error occurred: {e}")
        return "An error occurred while communicating with the Telegram servers. Please try again."
    except Exception as e:
        # Catch any other unexpected exceptions
        logging.error(f"Unexpected error: {e}")
        return "An unexpected error occurred. Please try again."

# Now you can call the inline_help_menu function
# Example usage
# bot_results = await inline_help_menu(app, query)

@app.on_message(filters.command("help2"))
async def inline_help_menu(client, message):
    image = None
    try:
        if image:
            bot_results = await app.get_inline_bot_results(
                f"@{bot.me.username}", "help_menu_logo"
            )
        else:
            # Removed timeout argument as it's not supported
            query = "help_menu_text"  # Ensure this query is valid and correctly defined
            bot_results = await app.get_inline_bot_results(query)
            bot_results = await app.get_inline_bot_results(
                f"@{bot.me.username}", "help_menu_text"
            )
        await app.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=bot_results.query_id,
            result_id=bot_results.results[0].id,
        )
    except Exception as e:
        print(f"Error: {e}")
        bot_results = await app.get_inline_bot_results(
            f"@{bot.me.username}", "help_menu_text"
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
    except Exception as e:
        print(f"Failed to delete message: {e}")
        pass


@bot.on_callback_query(filters.regex(r"help_(.*?)"))
@cb_wrapper
async def help_button(client, query):
    plug_match = re.match(r"help_plugin(.+?)", query.data)
    prev_match = re.match(r"help_prev(.+?)", query.data)
    next_match = re.match(r"help_next(.+?)", query.data)
    back_match = re.match(r"help_back", query.data)
    top_text = f"""
**💫 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ʜᴇʟᴘ ᴍᴇɴᴜ ᴏᴘ.
sʜᴜᴋʟᴀ ᴜsᴇʀʙᴏᴛ  » {__version__} ✨
 
❤️ᴄʟɪᴄᴋ ᴏɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ᴛᴏ
ɢᴇᴛ ᴜsᴇʀʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs ❤️.
 
🌹ᴘᴏᴡᴇʀᴇᴅ ʙʏ ♡  [ ᴜᴘᴅᴀᴛᴇ ](https://t.me/SHIVANSH474) 🌹**
"""
    
    if plug_match:
        plugin = plug_match.group(1)
        text = (
            "****💫 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ʜᴇʟᴘ ᴍᴇɴᴜ ᴏғ \n💕 ᴘʟᴜɢɪɴ ✨ ** {}\n".format(
                plugs[plugin].__NAME__
            )
            + plugs[plugin].__MENU__
        )
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="↪️ Back", callback_data="help_back"
                    )
                ],
            ]
        )

        await bot.edit_inline_text(
            query.inline_message_id,
            text=text,
            reply_markup=key,
            disable_web_page_preview=True
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
            reply_markup=InlineKeyboardMarkup(
                paginate_plugins(0, plugs, "help")
            ),
            disable_web_page_preview=True,
        )
