from pyrogram.types import InlineQueryResultPhoto, InlineQueryResultArticle
from CakeMusic import app
from CakeMusic.version import *
from CakeMusic.sukh.buttons import paginate_plugins

async def help_menu_logo(answer):
    image = None  # Placeholder for image
    thumb_image = image or "https://files.catbox.moe/r58nec.jpg"
    button = paginate_plugins(0, plugs, "help")
    answer.append(
        InlineQueryResultPhoto(
            photo_url=thumb_image,
            title="💫 ʜᴇʟᴘ ᴍᴇɴᴜ  ✨",
            thumb_url=thumb_image,
            description="🥀 Open Help Menu Of SHUKLAUSERBOT ✨...",
            caption=f"**💫 Welcome to Help Menu of SHUKLAUSERBOT » {__version__} ✨**",
            reply_markup=InlineKeyboardMarkup(button),
        )
    )
    return answer

async def help_menu_text(answer):
    button = paginate_plugins(0, plugs, "help")
    answer.append(
        InlineQueryResultArticle(
            title="💫 ʜᴇʟᴘ ᴍᴇɴᴜ  ✨",
            input_message_content=InputTextMessageContent(f"**💫 Welcome to Help Menu of SHUKLAUSERBOT » {__version__} ✨**"),
            reply_markup=InlineKeyboardMarkup(button),
        )
    )
    return answer
