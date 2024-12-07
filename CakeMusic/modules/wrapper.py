from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultPhoto, InlineQueryResultArticle, InputTextMessageContent
from traceback import format_exc

from CakeMusic.misc import SUDOERS
from CakeMusic import app, bot


# Decorator for super-user only commands
def super_user_only(func):
    async def wrapper(client, message):
        try:
            if message.from_user and message.from_user.is_self:
                return await func(client, message)
        except Exception as e:
            print(format_exc())
    return wrapper


# Decorator for sudo-users only commands
def sudo_users_only(func):
    async def wrapper(client, message):
        try:
            if (message.from_user and 
                (message.from_user.is_self or message.from_user.id in SUDOERS)):
                return await func(client, message)
        except Exception as e:
            print(format_exc())
    return wrapper


# Decorator for callback query handlers with sudo-user check
def cb_wrapper(func):
    async def wrapper(bot, cb):
        try:
            if cb.from_user.id in SUDOERS or cb.from_user.id == bot.me.id:
                return await func(bot, cb)
            else:
                await cb.answer(
                    "❎ You Are Not A Sudo User❗",
                    cache_time=0,
                    show_alert=True
                )
        except Exception as e:
            print(format_exc())
            await cb.answer(
                f"❎ Something Went Wrong, Please Check Logs❗"
            )
    return wrapper


# Decorator for inline query handlers with sudo-user check
def inline_wrapper(func):
    from ... import __version__
    async def wrapper(bot, query):
        try:
            if query.from_user.id in SUDOERS or query.from_user.id == bot.me.id:
                return await func(bot, query)
            else:
                button = [
                    [
                        InlineKeyboardButton(
                            "💥 Deploy Pbx Userbot ✨",
                            url="https://github.com/Badhacker98/Pbx_TeamBot"
                        )
                    ]
                ]
                await bot.answer_inline_query(
                    query.id,
                    cache_time=1,
                    results=[
                        InlineQueryResultPhoto(
                            photo_url="https://telegra.ph/file/3063af27d9cc8580845e1.jpg",
                            title="🥀 Pbx Userbot ✨",
                            thumb_url="https://telegra.ph/file/3063af27d9cc8580845e1.jpg",
                            description="🌷 Deploy Your Own PBXUSERBOT🌿...",
                            caption=f"<b>🥀 Welcome » To » Pbx 🌷\n✅ Userbot {__version__} ✨...</b>",
                            reply_markup=InlineKeyboardMarkup(button),
                        )
                    ],
                )
        except Exception as e:
            print(format_exc())
            await bot.answer_inline_query(
                query.id,
                cache_time=1,
                results=[
                    InlineQueryResultArticle(
                        title="Error",
                        input_message_content=InputTextMessageContent(
                            "||**🥀 Please, Deploy Your Own Pbx Userbot❗...\n\nRepo:** <i>https://github.com/Badhacker98/Pbx_TeamBot/</i>||"
                        )
                    )
                ],
            )
    return wrapper
