from CakeMusic import app
from pyrogram.types import InlineKeyboardButton
from traceback import format_exc
from CakeMusic.misc import SUDOERS

def sudo_users_only(mystic):
    async def wrapper(client, message):
        try:
            if (message.from_user.is_self or message.from_user.id in SUDOERS):
                return await mystic(client, message)
        except Exception as e:
            print(format_exc())
            return
    return wrapper

def inline_wrapper(func):
    async def wrapper(bot, query):
        if query.from_user.id not in SUDOERS:
            await bot.answer_inline_query(
                query.id,
                cache_time=1,
                results=[InlineQueryResultPhoto(
                    photo_url="https://files.catbox.moe/r58nec.jpg",
                    title="🥀 Shukla Userbot ✨",
                    caption=f"Deploy Your Own Shukla Userbot\nRepo: [Link](https://github.com/itzshukla/STRANGER-OPUSERBOT2.0)"
                )]
            )
        else:
            return await func(bot, query)
    return wrapper
