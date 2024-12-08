import re
from pyrogram import Client, filters
from CakeMusic import app, bot
from CakeMusic.sukh.inline import help_menu_logo, help_menu_text
from CakeMusic.sukh.buttons import paginate_plugins
from CakeMusic.sukh.wrapper import sudo_users_only, inline_wrapper

@app.on_message(filters.command("help"))
@sudo_users_only
async def inline_help_menu(client, message):
    try:
        bot_results = await app.get_inline_bot_results(f"@{bot.me.username}", "help_menu_text")
        await app.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=bot_results.query_id,
            result_id=bot_results.results[0].id,
        )
    except Exception as e:
        print(e)

@bot.on_callback_query(filters.regex(r"help_(.*?)"))
@inline_wrapper
async def help_button(client, query):
    plug_match = re.match(r"help_plugin(.+?)", query.data)
    prev_match = re.match(r"help_prev(.+?)", query.data)
    next_match = re.match(r"help_next(.+?)", query.data)
    
    top_text = f"**🥀 Welcome To Help Menu of Daxx Userbot » {__version__} ✨**"

    if plug_match:
        plugin = plug_match.group(1)
        text = f"**Plugin Help**: {plugin} details here"
        key = InlineKeyboardMarkup([
            [InlineKeyboardButton("↪️ Back", callback_data="help_back")]
        ])
        await bot.edit_inline_text(query.inline_message_id, text=text, reply_markup=key)
    elif prev_match:
        await bot.edit_inline_text(
            query.inline_message_id,
            text=top_text,
            reply_markup=InlineKeyboardMarkup(paginate_plugins(int(prev_match.group(1)) - 1, plugs, "help"))
        )
    elif next_match:
        await bot.edit_inline_text(
            query.inline_message_id,
            text=top_text,
            reply_markup=InlineKeyboardMarkup(paginate_plugins(int(next_match.group(1)) + 1, plugs, "help"))
        )
    elif back_match:
        await bot.edit_inline_text(
            query.inline_message_id,
            text=top_text,
            reply_markup=InlineKeyboardMarkup(paginate_plugins(0, plugs, "help"))
        )
