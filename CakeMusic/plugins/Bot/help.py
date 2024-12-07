from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent


# Command Handler for /help (this is for the userbot command)
@bot.on_message(filters.command("help") & filters.private)
async def help_command(client, message):
    # Inline buttons for the help menu
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Voicechat", callback_data="voicechat"),
                InlineKeyboardButton("YouTube", callback_data="youtube"),
            ],
            [
                InlineKeyboardButton("Prev", callback_data="prev"),
                InlineKeyboardButton("Close", callback_data="close"),
                InlineKeyboardButton("Next", callback_data="next"),
            ],
        ]
    )

    # Sending the Help message with inline keyboard
    await message.reply(
        "**👻 Help Menu:**\n"
        "📜 Loaded 52 plugins with a total of 218 commands.\n"
        "📄 Page: 6/6",
        reply_markup=keyboard
    )

# Inline Query Handler for when the user interacts with the bot
@bot.on_inline_query()
async def inline_query_handler(client, query):
    # Here we create an inline result to show when the user interacts with the bot inline.
    results = [
        InlineQueryResultArticle(
            title="Help Menu",
            input_message_content=InputTextMessageContent(
                "**👻 Help Menu:**\n"
                "📜 Loaded 52 plugins with a total of 218 commands.\n"
                "📄 Page: 6/6"
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Voicechat", callback_data="voicechat"),
                        InlineKeyboardButton("YouTube", callback_data="youtube"),
                    ],
                    [
                        InlineKeyboardButton("Prev", callback_data="prev"),
                        InlineKeyboardButton("Close", callback_data="close"),
                        InlineKeyboardButton("Next", callback_data="next"),
                    ],
                ]
            )
        )
    ]

    # Send the inline query results
    await query.answer(results)

# Callback Query Handler for button clicks
@bot.on_callback_query()
async def callback_query_handler(client, callback_query):
    data = callback_query.data

    if data == "voicechat":
        await callback_query.answer("Voicechat button clicked!", show_alert=True)
    elif data == "youtube":
        await callback_query.answer("YouTube button clicked!", show_alert=True)
    elif data == "prev":
        await callback_query.answer("Previous page not implemented!")
    elif data == "close":
        await callback_query.message.delete()
    elif data == "next":
        await callback_query.answer("Next page not implemented!")
    else:
        await callback_query.answer("Unknown action!")
        
