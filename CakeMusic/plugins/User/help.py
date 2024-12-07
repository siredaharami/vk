from pyrogram import Client, filters

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from CakeMusic import *


# Inline query handler to respond to inline queries with a button
@bot.on_inline_query()
async def inline_query_handler(client, inline_query):
    if inline_query.query == "help":  # When user types "help" in inline query
        button = InlineKeyboardButton("Click here for help", callback_data="help")
        result = InlineQueryResultArticle(
            id="1",
            title="Help",
            description="Click to get help",
            input_message_content=InputTextMessageContent("Here are the help details you requested."),
            reply_markup=InlineKeyboardMarkup([[button]])
        )
        await client.answer_inline_query(inline_query.id, [result])

# Handler for the button click (callback data is "help")
@bot.on_callback_query(filters.regex("help"))
async def help_callback(client, callback_query):
    try:
        await callback_query.answer("Here are the help details you requested.")
        await callback_query.message.edit_text("Here are the help details you requested.")
    except Exception as e:
        print(f"Error during callback query: {e}")

# Regular help command handler
@bot.on_message(filters.command("help"))
async def help_command(client, message):
    # Create an inline button for help
    button = InlineKeyboardButton("Click here for help", callback_data="help")
    
    # Send a message with the button
    await message.reply(
        "Click below for help:",
        reply_markup=InlineKeyboardMarkup([[button]])
    )
    
