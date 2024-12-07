from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from CakeMusic.database.templates import help_template
from CakeMusic.plugins.btnsG import gen_inline_help_buttons
from CakeMusic import bot


@app_inline_query(filters.regex(r"help_menu"))
async def help_inline(_, query: InlineQuery):
    if query.from_user.id not in OWNER_ID:
        return
    # Generate buttons and calculate the number of pages
    buttons, pages = await gen_inline_help_buttons(0, [])
    caption = await help_template(
        query.from_user.mention, (0, 0), (1, pages)
    )
    await query.answer(
        results=[
            InlineQueryResultArticle(
                title="Pbxbot 2.0 Help Menu 👻",
                input_message_content=InputTextMessageContent(
                    message_text=caption,
                    disable_web_page_preview=True,
                ),
                description="Inline Query for Help Menu of PbxBot",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        ],
        cache_time=0,  # Disable caching for testing purposes
    )
