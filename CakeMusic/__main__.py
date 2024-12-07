import config
import aiohttp, aiofiles, asyncio, base64, logging
import os, platform, random, re, socket
import sys, time, textwrap
from CakeMusic import __version__ as version
from CakeMusic import app, bot, call
from os import getenv
from io import BytesIO
from time import strftime
from functools import partial
from dotenv import load_dotenv
from datetime import datetime
from typing import Union, List, Pattern
from logging.handlers import RotatingFileHandler

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_async_

from pyrogram import Client, filters as pyrofl
from pytgcalls import PyTgCalls
from pytgcalls.types import Update, GroupCall
from pytgcalls.exceptions import GroupCallNotFoundError, NoActiveGroupCall

from pyrogram import idle, __version__ as pyro_version
from platform import python_version
from pytgcalls.__version__ import __version__ as pytgcalls_version
from pyrogram import __version__ as pyrogram_version

from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import (
    ChatAdminRequired,
    FloodWait,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from PIL import Image, ImageDraw, ImageEnhance
from PIL import ImageFilter, ImageFont, ImageOps
from youtubesearchpython.__future__ import VideosSearch
from config import *

loop = asyncio.get_event_loop()

# Setup logging
logging.basicConfig(
    format="[%(name)s]:: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    handlers=[
        RotatingFileHandler("logs.txt", maxBytes=(1024 * 1024 * 5), backupCount=10),
        logging.StreamHandler(),
    ],
)

logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)

LOGGER = logging.getLogger("SYSTEM")


async def start_clients():
    """Start both bot and assistant clients."""
    try:
        await bot.start()
        LOGGER.info("✅ Bot Started.")
    except Exception as e:
        LOGGER.error(f"🚫 Bot Error: {e}")
        sys.exit()

    try:
        await app.start()
        LOGGER.info("✅ Assistant Started.")
    except Exception as e:
        LOGGER.error(f"🚫 Assistant Error: {e}")
        sys.exit()


async def send_startup_messages(version: dict):
    if LOG_GROUP_ID != 0:
        try:
            if not hasattr(bot, 'me') or not bot.me:
                await bot.get_me()  # Ensure bot information is fetched

            await bot.send_animation(
                config.LOG_GROUP_ID,
                "https://files.catbox.moe/zvwx1y.mp4",
                caption=(
                    f"**✅ Userbot is Online!**\n\n"
                    f"**🔹 Version ➠ ** `{version['CakeMusic']}`\n"
                    f"**🔹 Pyrogram ➠ ** `{version['pyrogram']}`\n"
                    f"**🔹 Python ➠ ** `{version['python']}`\n"
                    f"**🔹 PyTgCalls ➠ ** `{version['pytgcalls']}`"
                ),
                disable_notification=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "💫 Start Me",
                                url=f"https://t.me/{bot.me.username}?start=start",
                            ),
                            InlineKeyboardButton(
                                "💖 Repo",
                                url="https://github.com/Badhacker98/PBX_2.0/fork",
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                "💬 Support", url="https://t.me/ll_THE_BAD_BOT_ll"
                            )
                        ],
                    ]
                ),
            )
            await app.send_message(LOG_GROUP_ID, "**🦋 Assistant Started.**")
        except Exception as e:
            LOGGER.warning(f"Could not send startup messages: {e}")


async def main():
    LOGGER.info("🌐 Checking Required Variables ...")
    required_env_vars = [
        "API_ID",
        "API_HASH",
        "BOT_TOKEN",
        "STRING_SESSION",
        "MONGO_DB_URL",
    ]
    for var in required_env_vars:
        if not globals().get(var):
            LOGGER.error(f"❌ '{var}' - Not Found !!")
            sys.exit()

    LOGGER.info("✅ Required Variables Collected.")
    await asyncio.sleep(1)

    LOGGER.info("🌀 Starting Clients ...")
    await start_clients()

    LOGGER.info("🌀 Sending Startup Messages ...")
    version_info = {
        "CakeMusic": version,
        "pyrogram": pyrogram_version,
        "python": python_version(),
        "pytgcalls": pytgcalls_version,
    }
    await send_startup_messages(version_info)

    LOGGER.info("🌀 Starting PyTgCalls ...")
    try:
        await call.start()
        LOGGER.info("✅ PyTgCalls Started.")
    except GroupCallNotFoundError:
        LOGGER.error("🚫 No Active Group Call Found!")
        sys.exit()
    except Exception as e:
        LOGGER.error(f"🚫 PyTgCalls Error: {e}")
        sys.exit()

    LOGGER.info("✅ Successfully Hosted Your Bot !!")
    LOGGER.info("✅ Visit @AdityaServer for Updates !!")
    await idle()


if __name__ == "__main__":
    loop.run_until_complete(main())
