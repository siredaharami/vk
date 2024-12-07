from pyrogram import Client, filters
from CakeMusic import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent


# Inline query handler with an inline wrapper
async def inline_wrapper(func):
    async def wrapped(client, inline_query):
        try:
            # Call the actual function
            await func(client, inline_query)
        except Exception as e:
            print(f"Error occurred in inline query: {e}")
    return wrapped

# Inline query handler to respond to inline queries with a button
@inline_wrapper
@app.on_inline_query()
async def inline_query_handler(client, inline_query):
    if inline_query.query == "help":  # When user types "help" in inline query
        # Create the button
        button = InlineKeyboardButton("Click here for help", callback_data="help")
        
        # Create the result to send back
        result = InlineQueryResultArticle(
            id="1",  # Unique ID for this result
            title="Help",
            description="Click to get help",
            input_message_content=InputTextMessageContent("Here are the help details you requested."),
            reply_markup=InlineKeyboardMarkup([[button]])  # Button in the inline result
        )
        
        # Send the inline query result
        await client.answer_inline_query(inline_query.id, [result])

# Handler for the button click (callback data is "help")
@app.on_callback_query(filters.regex("help"))
async def help_callback(client, callback_query):
    try:
        # Respond with help information when the button is clicked
        await callback_query.answer("Here are the help details you requested.")
        await callback_query.message.edit_text("Here are the help details you requested.")
    except Exception as e:
        print(f"Error occurred during callback query: {e}")

# Regular help command handler (when user types /help)
@app.on_message(filters.command("help"))
async def help_command(client, message):
    # Create an inline button for help
    button = InlineKeyboardButton("Click here for help", callback_data="help")
    
    # Send a message with the button
    await message.reply(
        "Click below for help:",
        reply_markup=InlineKeyboardMarkup([[button]])
    )
