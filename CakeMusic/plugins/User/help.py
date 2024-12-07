from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from CakeMusic import app  # Importing `app` from YukkiMusic

plugins = [f"Plugin {i}" for i in range(1, 21)]  # Example: Simulated plugin list (20 plugins)
COMMANDS_PER_PLUGIN = 1  # 1 command per plugin
PLUGINS_PER_PAGE = 4  # Plugins per page (Reduced to 4)


# Function to generate help menu buttons
def generate_help_menu(page: int):
    start = page * PLUGINS_PER_PAGE
    end = start + PLUGINS_PER_PAGE
    current_plugins = plugins[start:end]

    # Inline buttons for plugins
    buttons = [
        [InlineKeyboardButton(f"✧ {plugin} ✧", callback_data=f"plugin:{plugin[:64]}")]
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


# Help menu command handler
@app.on_message(filters.command("help"))
async def help_menu(client, message):
    total_plugins = len(plugins)
    total_commands = total_plugins * COMMANDS_PER_PLUGIN
    current_page = 0
    max_pages = (total_plugins - 1) // PLUGINS_PER_PAGE + 1

    header = (
        f"👻 **Help Menu for:** {message.from_user.mention or 'User'}\n"
        f"📜 **Loaded {total_plugins} plugins** with a total of **{total_commands} commands.**\n"
        f"📄 **Page:** {current_page + 1}/{max_pages}"
    )

    # Generate buttons
    buttons = generate_help_menu(current_page)

    await message.reply_text(
        text=header,
        reply_markup=buttons
    )


# Navigation callback handler
@app.on_callback_query(filters.regex(r"^navigate:(\d+)"))
async def navigate_handler(client, callback_query: CallbackQuery):
    page = int(callback_query.data.split(":")[1])
    total_plugins = len(plugins)
    max_pages = (total_plugins - 1) // PLUGINS_PER_PAGE + 1

    header = (
        f"👻 **Help Menu for:** {callback_query.from_user.mention or 'User'}\n"
        f"📜 **Loaded {total_plugins} plugins** with a total of **{total_plugins * COMMANDS_PER_PLUGIN} commands.**\n"
        f"📄 **Page:** {page + 1}/{max_pages}"
    )

    await callback_query.message.edit_text(
        text=header,
        reply_markup=generate_help_menu(page)
    )


# Close button callback handler
@app.on_callback_query(filters.regex(r"^close"))
async def close_handler(client, callback_query: CallbackQuery):
    await callback_query.message.delete()


# Plugin details callback handler
@app.on_callback_query(filters.regex(r"^plugin:(.+)"))
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
