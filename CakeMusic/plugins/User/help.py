import asyncio
from CakeMusic import *
import re
from math import ceil
from traceback import format_exc

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultPhoto,
    InlineQueryResultArticle,
    InputTextMessageContent,
    CallbackQuery,
    Message
)

# Define constants
SUDOERS = [7009601543]  # Replace with actual sudo user IDs
BOT_USERNAME = "TEST_BOT_NEW_MUSIC_Bot"  # Replace with your bot's username
BOT_OWNER_ID = 7009601543  # Replace with your bot's owner ID
THUMB_IMAGE = "https://files.catbox.moe/r58nec.jpg"  # Thumbnail image URL
VERSION = "1.0.0"  # Userbot version

# Utility: Paginate Plugins
def paginate_plugins(page_n, plugin_dict, prefix, chat=None):
    if not chat:
        plugins = sorted(
            [
                InlineKeyboardButton(
                    x.__NAME__,
                    callback_data=f"{prefix}_plugin({x.__NAME__.lower()})",
                )
                for x in plugin_dict.values()
            ]
        )
    else:
        plugins = sorted(
            [
                InlineKeyboardButton(
                    x.__NAME__,
                    callback_data=f"{prefix}_plugin({chat},{x.__NAME__.lower()})",
                )
                for x in plugin_dict.values()
            ]
        )
    COLUMN_SIZE = 3
    max_num_pages = ceil(len(plugins) / COLUMN_SIZE)
    modulo_page = page_n % max_num_pages

    pairs = [
        plugins[i:i + COLUMN_SIZE] for i in range(0, len(plugins), COLUMN_SIZE)
    ]
    pairs = pairs[modulo_page * COLUMN_SIZE:(modulo_page + 1) * COLUMN_SIZE]

    pairs.append([
        InlineKeyboardButton("❮", callback_data=f"{prefix}_prev({modulo_page})"),
        InlineKeyboardButton("Owner", url=f"tg://openmessage?user_id={BOT_OWNER_ID}"),
        InlineKeyboardButton("❯", callback_data=f"{prefix}_next({modulo_page})"),
    ])
    return pairs

# Wrapper: Restrict Access
def sudo_users_only(func):
    async def wrapper(client: Client, message: Message):
        if message.from_user.id in SUDOERS or message.from_user.is_self:
            return await func(client, message)
        else:
            await message.reply("❎ You are not authorized to use this command.")
    return wrapper

def cb_wrapper(func):
    async def wrapper(client: Client, callback_query: CallbackQuery):
        if callback_query.from_user.id in SUDOERS or callback_query.from_user.id == BOT_OWNER_ID:
            return await func(client, callback_query)
        else:
            await callback_query.answer("❎ You are not authorized to use this action.", show_alert=True)
    return wrapper

# Inline Query Handlers
async def help_menu_logo():
    button = paginate_plugins(0, plugs, "help")
    return [
        InlineQueryResultPhoto(
            photo_url=THUMB_IMAGE,
            title="💫 Help Menu ✨",
            thumb_url=THUMB_IMAGE,
            description="🥀 Open Help Menu of YourBot ✨...",
            caption=f"**💫 Welcome to Help Menu of YourBot v{VERSION} ✨**",
            reply_markup=InlineKeyboardMarkup(button),
        )
    ]

async def help_menu_text():
    button = paginate_plugins(0, plugs, "help")
    return [
        InlineQueryResultArticle(
            title="💫 Help Menu ✨",
            input_message_content=InputTextMessageContent(
                f"**💫 Welcome to Help Menu of YourBot v{VERSION} ✨**",
                disable_web_page_preview=True,
            ),
            reply_markup=InlineKeyboardMarkup(button),
        )
    ]

# Command: Show Help Menu
@app.on_message(filters.command("help"))
@sudo_users_only
async def show_help_menu(client: Client, message: Message):
    try:
        bot_results = await app.get_inline_bot_results(f"@{BOT_USERNAME}", "help_menu_text")
        await app.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=bot_results.query_id,
            result_id=bot_results.results[0].id,
        )
        await message.delete()
    except Exception as e:
        print(f"Error in help menu: {e}")

# Callback Query: Handle Buttons
@app.on_callback_query(filters.regex(r"help_(.*?)"))
@cb_wrapper
async def handle_help_buttons(client: Client, query: CallbackQuery):
    match = re.match(r"help_(.*?)(.+?)", query.data)
    if not match:
        await query.answer("Invalid action!")
        return

    action, param = match.groups()
    top_text = f"**💫 Welcome to Help Menu of YourBot v{VERSION} ✨**"

    if action == "plugin":
        plugin = param
        text = f"**Plugin Help**: {plugin} details here."
        key = InlineKeyboardMarkup([[InlineKeyboardButton("↪️ Back", callback_data="help_back")]])
        await query.edit_message_text(text=text, reply_markup=key, disable_web_page_preview=True)
    elif action == "prev":
        curr_page = int(param)
        await query.edit_message_text(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(paginate_plugins(curr_page - 1, plugs, "help")),
        )
    elif action == "next":
        next_page = int(param)
        await query.edit_message_text(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(paginate_plugins(next_page + 1, plugs, "help")),
        )
    elif action == "back":
        await query.edit_message_text(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(paginate_plugins(0, plugs, "help")),
        )
        
