import os
import time
import logging

from os import getenv

# PM GUARD VARS
PM_GUARD = bool(getenv("PM_GUARD", True))
PM_GUARD_TEXT = getenv("PM_GUARD_TEXT", "**🥀 ʜᴇʏ, ɪ ᴀᴍ ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ & ꜱᴜᴘᴇʀꜰᴀꜱᴛ ʜɪɢʜ Qᴜᴀʟɪᴛʏ ᴜꜱᴇʀʙᴏᴛ ᴀꜱꜱɪꜱᴛᴀɴᴛ ᴡɪᴛʜ ᴀɴ ᴜᴘɢʀᴀᴅᴇᴅ ᴠᴇʀꜱɪᴏɴ ꜱᴇᴄᴜʀɪᴛʏ ꜱʏꜱᴛᴇᴍ.**")
PM_GUARD_LIMIT = int(getenv("PM_GUARD_LIMIT", 5))


async def help_template(
    owner: str, cmd_n_plgn: tuple[int, int], page: tuple[int, int]
) -> str:
    template = await db.get_env(ENV.help_template)
    if template:
        message = template
    else:
        message = random.choice(HELP_MENU_TEMPLATES)
    return message.format(
        owner=owner,
        commands=cmd_n_plgn[0],
        plugins=cmd_n_plgn[1],
        current=page[0],
        last=page[1],
    )
