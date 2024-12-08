from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineQuery
)

ASSISTANT_ID = 6331052940  # Replace with your actual assistant (owner) ID
SUDO_USERS = [6331052940]  # List of sudo users' IDs (can add more IDs)

plugins = [
    "Music Plugin",
    "Plugin 2",
    "Plugin 3",
    "Plugin 4",
    "Plugin 5",
]
COMMANDS_PER_PLUGIN = 1
PLUGINS_PER_PAGE = 4

plugin_descriptions = {
    "Music Plugin": "Provides music playback commands for the bot.",
    "Plugin 2": "This plugin handles admin tasks.",
    "Plugin 3": "A fun plugin with various entertainment features.",
    "Plugin 4": "Custom utilities for managing the bot.",
    "Plugin 5": "Additional commands to enhance functionality.",
}

plugin_commands = {
    "Music Plugin": ["/play [song name] - Play a song in the chat."],
    "Plugin 2": ["/ban [user] - Ban a user."],
    "Plugin 3": ["/joke - Get a random joke."],
    "Plugin 4": ["/info - Get bot information."],
    "Plugin 5": ["/ping - Check bot responsiveness."],
}


# Function to generate inline buttons for help menu
def generate_help_menu(page: int, is_assistant: bool):
    start = page * PLUGINS_PER_PAGE
    end = start + PLUGINS_PER_PAGE
    current_plugins = plugins[start:end]

    buttons = [
        [InlineKeyboardButton(f"✧ {plugin} ✧", callback_data=f"plugin:{plugin[:64]}")]
        for plugin in current_plugins
    ]

    if is_assistant:
        buttons.append([InlineKeyboardButton("⚙️ Admin Panel", callback_data="admin_panel")])

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
@app.on_message(filters.command("help"))
async def help_command(_, message):
    total_plugins = len(plugins)
    total_commands = total_plugins * COMMANDS_PER_PLUGIN
    current_page = 0
    max_pages = (total_plugins - 1) // PLUGINS_PER_PAGE + 1

    header = (
        f"👻 Help Menu for: {message.from_user.mention or 'User'}\n"
        f"📜 Loaded {total_plugins} plugins with a total of {total_commands} commands.\n"
        f"📄 Page: {current_page + 1}/{max_pages}"
    )

    is_assistant = message.from_user.id == ASSISTANT_ID or message.from_user.id in SUDO_USERS

    if is_assistant:
        # If the user is the assistant, send inline buttons with the list of plugins
        await message.reply(
            text=header,
            reply_markup=generate_help_menu(current_page, is_assistant)
        )
    else:
        # Regular users get a simple text response
        await message.reply(
            text=header
        )


# Inline query handler for the /help command
@bot.on_inline_query()
async def inline_help(client, inline_query: InlineQuery):
    total_plugins = len(plugins)
    total_commands = total_plugins * COMMANDS_PER_PLUGIN
    current_page = 0
    max_pages = (total_plugins - 1) // PLUGINS_PER_PAGE + 1

    header = (
        f"👻 Help Menu for: {inline_query.from_user.mention or 'User'}\n"
        f"📜 Loaded {total_plugins} plugins with a total of {total_commands} commands.\n"
        f"📄 Page: {current_page + 1}/{max_pages}"
    )

    is_assistant = inline_query.from_user.id == ASSISTANT_ID or inline_query.from_user.id in SUDO_USERS

    # Create inline query result (message content and inline keyboard)
    result = InlineQueryResultArticle(
        title="Help Menu",
        description="Click to explore available plugins.",
        input_message_content=InputTextMessageContent(header),
        reply_markup=generate_help_menu(current_page, is_assistant)
    )

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

    is_assistant = callback_query.from_user.id == ASSISTANT_ID or callback_query.from_user.id in SUDO_USERS
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
    description = plugin_descriptions.get(plugin_name, "No description available.")
    commands = plugin_commands.get(plugin_name, ["No commands available."])

    await callback_query.message.edit_text(
        f"**Plugin Name:** {plugin_name}\n"
        f"**Description:** {description}\n"
        f"**Commands Available:**\n" + "\n".join(commands),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="navigate:0")]
        ])
    )


# Handler for the admin panel button (only for assistant)
@bot.on_callback_query(filters.regex(r"^admin_panel"))
async def admin_panel_handler(client, callback_query):
    if callback_query.from_user.id == ASSISTANT_ID or callback_query.from_user.id in SUDO_USERS:
        await callback_query.message.edit_text(
            "Welcome to the Admin Panel! Here you can manage advanced settings.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="navigate:0")]
            ])
        )
    else:
        await callback_query.answer("You are not authorized to access the admin panel.", show_alert=True)
