from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputTextMessageContent
from CakeMusic import *

# The bot will respond to commands from the userbot
@bot.on_message(filters.command("help") & filters.private)
async def help_command(client, message):
    # Define the inline keyboard with buttons
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Voicechat", callback_data="voicechat")],
            [InlineKeyboardButton("YouTube", callback_data="youtube")],
            [InlineKeyboardButton("Prev", callback_data="prev"), InlineKeyboardButton("Close", callback_data="close"), InlineKeyboardButton("Next", callback_data="next")],
        ]
    )

    # Send a message with the inline keyboard as a response to /help from the userbot
    await message.reply(
        "**👻 Help Menu:**\n"
        "📜 Loaded 52 plugins with a total of 218 commands.\n"
        "📄 Page: 6/6",
        reply_markup=keyboard
    )

# Callback query handler for button presses
@bot.on_callback_query()
async def on_callback_query(client, callback_query):
    data = callback_query.data

    if data == "voicechat":
        await callback_query.answer("Voicechat selected.")
    elif data == "youtube":
        await callback_query.answer("YouTube selected.")
    elif data == "prev":
        await callback_query.answer("Previous page not implemented.")
    elif data == "close":
        await callback_query.message.delete()
    elif data == "next":
        await callback_query.answer("Next page not implemented.")
    else:
        await callback_query.answer("Unknown action.")
        

from pyrogram import Client, filters


# Userbot /help command
@app.on_message(filters.command("help") & filters.private)
async def help_command(client, message):
    # The userbot triggers the /help command to the bot
    bot = client.get_chat_member("@PBXMUSICUSER_BOT")  # Get the bot via its username (use @YourBotUsername)
    
    # Send the /help command to the bot
    await bot.send_message(
        "@PBXMUSICUSER_BOT",  # Send /help command to bot
        "/help"  # Trigger the /help command from the userbot to the bot client
)
    
