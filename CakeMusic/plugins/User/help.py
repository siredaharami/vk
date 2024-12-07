from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent
from CakeMusic import bot  # Importing app from YukkiMusic

ASSISTANT_ID =  6331052940  # Replace with the actual Telegram ID of your assistant
plugins = [f"Plugin {i}" for i in range(1, 21)]  # Example: Simulated plugins
COMMANDS_PER_PLUGIN = 1  # 1 command per plugin
PLUGINS_PER_PAGE = 4  # Only 4 plugins per page


# Function to generate inline buttons for help menu
def generate_help_menu(page: int, is_assistant: bool):
    start = page * PLUGINS_PER_PAGE
    end = start + PLUGINS_PER_PAGE
    current_plugins = plugins[start:end]

    # Inline buttons for plugins
    buttons = [
        [InlineKeyboardButton(f"✧ {plugin} ✧", callback_data=f"plugin:{plugin[:64]}")]
        for plugin in current_plugins
    ]

    # If the user is the assistant, add an admin-only button
    if is_assistant:
        buttons.append([InlineKeyboardButton("⚙️ Admin Panel", callback_data="admin_panel")])

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


# Command handler for /help command
@bot.on_message(filters.command("help"))
async def help_command(client, message):
    total_plugins = len(plugins)
    total_commands = total_plugins * COMMANDS_PER_PLUGIN
    current_page = 0
    max_pages = (total_plugins - 1) // PLUGINS_PER_PAGE + 1

    header = (
        f"👻 Help Menu for: {message.from_user.mention or 'User'}\n"
        f"📜 Loaded {total_plugins} plugins with a total of {total_commands} commands.\n"
        f"📄 Page: {current_page + 1}/{max_pages}"
    )

    is_assistant = message.from_user.id == ASSISTANT_ID  # Check if the user is the assistant

    # Send the help message with inline keyboard
    await message.reply(
        text=header,
        reply_markup=generate_help_menu(current_page, is_assistant)
    )


# Inline query handler for the /help command
@bot.on_inline_query()
async def inline_help(client, inline_query):
    total_plugins = len(plugins)
    total_commands = total_plugins * COMMANDS_PER_PLUGIN
    current_page = 0
    max_pages = (total_plugins - 1) // PLUGINS_PER_PAGE + 1

    header = (
        f"👻 Help Menu for: {inline_query.from_user.mention or 'User'}\n"
        f"📜 Loaded {total_plugins} plugins with a total of {total_commands} commands.\n"
        f"📄 Page: {current_page + 1}/{max_pages}"
    )

    is_assistant = inline_query.from_user.id == ASSISTANT_ID  # Check if the user is the assistant

    # Create inline query result (message content and inline keyboard)
    result = InlineQueryResultArticle(
        title="Help Menu",
        description="Click to explore available plugins.",
        input_message_content=InputTextMessageContent(header),
        reply_markup=generate_help_menu(current_page, is_assistant)
    )

    # Answer inline query with the result
    await inline_query.answer([result], cache_time=0)


# Handler for navigating between pages
@bot.on_callback_query(filters.regex(r"^navigate:(\d+)"))
async def navigate_handler(client, callback_query):
    page = int(callback_query.data.split(":")[1])
    total_plugins = len(plugins)
    max_pages = (total_plugins - 1) // PLUGINS_PER_PAGE + 1

    header = (
        f"👻 Help Menu for: {callback_query.from_user.mention or 'User'}\n"
        f"📜 Loaded {total_plugins} plugins with a total of {total_plugins * COMMANDS_PER_PLUGIN} commands.\n"
        f"📄 Page: {page + 1}/{max_pages}"
    )

    is_assistant = callback_query.from_user.id == ASSISTANT_ID  # Check if the user is the assistant
    await callback_query.message.edit_text(
        text=header,
        reply_markup=generate_help_menu(page, is_assistant)
    )


# Handler for the close button
@bot.on_callback_query(filters.regex(r"^close"))
async def close_handler(client, callback_query):
    await callback_query.message.delete()


# Handler for plugin details
@bot.on_callback_query(filters.regex(r"^plugin:(.+)"))
async def plugin_details_handler(client, callback_query):
    plugin_name = callback_query.data.split(":")[1]
    await callback_query.message.edit_text(
        f"Plugin Name: {plugin_name}\n"
        f"Description: This plugin does amazing things!\n"
        f"Commands Available: 1\n",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="navigate:0")]
        ])
    )


# Handler for the admin panel button (only for assistant)
@bot.on_callback_query(filters.regex(r"^admin_panel"))
async def admin_panel_handler(client, callback_query):
    if callback_query.from_user.id == ASSISTANT_ID:
        await callback_query.message.edit_text(
            "Welcome to the Admin Panel! Here you can manage advanced settings.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="navigate:0")]
            ])
        )
    else:
        await callback_query.answer("You are not authorized to access the admin panel.", show_alert=True)
