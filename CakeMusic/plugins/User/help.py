from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardButton
)
from CakeMusic import bot  # Importing the app from CakeMusic

# Constants (Previously in Config)
AUTH_USERS = [7009601543, 7475631398]  # List of user IDs who can access the help menu
CMD_MENU = ["Plugin1", "Plugin2", "Plugin3", "Plugin4"]  # List of plugin names
CMD_INFO = {"Plugin1": "Description of Plugin1", "Plugin2": "Description of Plugin2"}  # Command descriptions

# Helper functions (Previously in btnsG and templates)
async def gen_inline_help_buttons(page_number, cmd_menu):
    buttons = []
    items_per_page = 5  # Number of items to display per page
    start = page_number * items_per_page
    end = start + items_per_page
    cmd_page = cmd_menu[start:end]

    for cmd in cmd_page:
        buttons.append([InlineKeyboardButton(cmd, callback_data=f'help_{cmd}')])

    # Add pagination buttons (if there are multiple pages)
    prev_page = InlineKeyboardButton("Previous", callback_data=f'help_prev_{page_number-1}' if page_number > 0 else 'help_prev_0')
    next_page = InlineKeyboardButton("Next", callback_data=f'help_next_{page_number+1}' if end < len(cmd_menu) else 'help_next_0')
    buttons.append([prev_page, next_page])

    total_pages = (len(cmd_menu) + items_per_page - 1) // items_per_page  # Calculate total pages
    return buttons, total_pages

async def help_template(user_mention, cmd_stats, page_stats):
    no_of_commands, no_of_plugins = cmd_stats
    current_page, total_pages = page_stats

    caption = f"""
    **HellBot Help Menu 🍀**
    _Hey {user_mention}, here are your commands:_

    Total Commands: {no_of_commands}
    Total Plugins: {no_of_plugins}
    
    _Page {current_page}/{total_pages}_

    Type `/help` to get more detailed command info.
    """

    return caption

# Inline query handler
@bot.on_inline_query(filters.regex(r"help_menu"))
async def help_inline(_, query: InlineQuery):
    # Check if the user is authorized to access the help menu
    if not query.from_user.id in AUTH_USERS:
        return

    # Count the number of plugins and commands available
    no_of_plugins = len(CMD_MENU)
    no_of_commands = len(CMD_INFO)

    # Generate the inline help buttons and determine the number of pages
    buttons, pages = await gen_inline_help_buttons(0, sorted(CMD_MENU))

    # Prepare the help caption with a dynamic response
    caption = await help_template(
        query.from_user.mention, (no_of_commands, no_of_plugins), (1, pages)
    )

    # Answer the inline query with the formatted results and inline keyboard
    await query.answer(
        results=[
            InlineQueryResultArticle(
                title="HellBot Help Menu 🍀",  # Title displayed in the inline result
                input_message_content=InputTextMessageContent(
                    caption,  # Content to send in the chat
                    disable_web_page_preview=True,
                ),
                description="Inline Query for Help Menu of HellBot",  # Description displayed in the inline query preview
                reply_markup=InlineKeyboardMarkup(buttons),  # Inline keyboard with buttons for navigation
            )
        ],
        cache_time=0,  # Set to 0 for dynamic updates, increase for caching
    )
