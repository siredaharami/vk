from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from CakeMusic import *

# Simulated plugin list and commands count
plugins = [f"Plugin {i}" for i in range(1, 219)]  # 218 plugins example
COMMANDS_PER_PLUGIN = 1  # For simplicity, assume 1 command per plugin
PLUGINS_PER_PAGE = 52  # Max plugins per page


# Function to generate help menu buttons
def generate_help_menu(page: int):
    start = page * PLUGINS_PER_PAGE
    end = start + PLUGINS_PER_PAGE
    current_plugins = plugins[start:end]

    buttons = [
        [InlineKeyboardButton(f"✧ {plugin} ✧", callback_data=f"plugin:{plugin}")]
        for plugin in current_plugins
    ]

    # Navigation buttons
    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton("⬅ PREV", callback_data=f"navigate:{page - 1}"))
    navigation_buttons.append(InlineKeyboardButton("❌ CLOSE", callback_data="close"))
    if end < len(plugins):
        navigation_buttons.append(InlineKeyboardButton("NEXT ➡", callback_data=f"navigate:{page + 1}"))

    if navigation_buttons:
        buttons.append(navigation_buttons)

    return InlineKeyboardMarkup(buttons)


@app.on_message(filters.command("help"))
async def help_menu(client, message):
    total_plugins = len(plugins)
    total_commands = total_plugins * COMMANDS_PER_PLUGIN
    current_page = 0
    max_pages = (total_plugins - 1) // PLUGINS_PER_PAGE + 1

    header = (
        f"👻 **Help Menu for:** {message.from_user.mention}\n"
        f"📜 **Loaded {total_plugins} plugins** with a total of **{total_commands} commands.**\n"
        f"📄 **Page:** {current_page + 1}/{max_pages}"
    )

    await message.reply(
        header,
        reply_markup=generate_help_menu(current_page)
    )


@bot.on_callback_query(filters.regex(r"^navigate:(\d+)"))
async def navigate_handler(client, callback_query: CallbackQuery):
    page = int(callback_query.data.split(":")[1])
    total_plugins = len(plugins)
    max_pages = (total_plugins - 1) // PLUGINS_PER_PAGE + 1

    header = (
        f"👻 **Help Menu for:** {callback_query.from_user.mention}\n"
        f"📜 **Loaded {total_plugins} plugins** with a total of **{total_plugins * COMMANDS_PER_PLUGIN} commands.**\n"
        f"📄 **Page:** {page + 1}/{max_pages}"
    )

    await callback_query.message.edit_text(
        header,
        reply_markup=generate_help_menu(page)
    )


@bot.on_callback_query(filters.regex(r"^close"))
async def close_handler(client, callback_query: CallbackQuery):
    await callback_query.message.delete()


@bot.on_callback_query(filters.regex(r"^plugin:(.+)"))
async def plugin_details_handler(client, callback_query: CallbackQuery):
    plugin_name = callback_query.data.split(":")[1]
    await callback_query.message.edit_text(
        f"**Plugin Name:** {plugin_name}\n"
        f"**Description:** This plugin does amazing things!\n"
        f"**Commands Available:** 1\n",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="navigate:0")]
        ])
    )
