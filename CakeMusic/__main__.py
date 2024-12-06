import aiohttp, aiofiles, asyncio, base64, logging
import os, platform, random, re, socket
import sys, time, textwrap
from CakeMusic import app as bot  # Bot Client
from CakeMusic.plugins.Play import app, call  # Assistant Client
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
from pytgcalls import PyTgCalls, filters as pytgfl
from pyrogram import idle, __version__ as pyro_version
from pytgcalls.__version__ import __version__ as pytgcalls_version

from ntgcalls import TelegramServerError
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import (
    ChatAdminRequired,
    FloodWait,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pytgcalls.exceptions import NoActiveGroupCall
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls.types import ChatUpdate, Update, GroupCallConfig
from pytgcalls.types import Call, MediaStream, AudioQuality, VideoQuality

from PIL import Image, ImageDraw, ImageEnhance
from PIL import ImageFilter, ImageFont, ImageOps
from youtubesearchpython.__future__ import VideosSearch
from config import *

loop = asyncio.get_event_loop()

# Userbot Client
userbot = Client(
    name="Userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION,  # Replace with your session string
    plugins=dict(root="CakeMusic.plugins"),  # Optional, same plugins folder
)

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

async def main():
    LOGGER.info("🐬 Updating Directories ...")
    if "cache" not in os.listdir():
        os.mkdir("cache")
    if "downloads" not in os.listdir():
        os.mkdir("downloads")
    for file in os.listdir():
        if file.endswith(".session"):
            os.remove(file)
        if file.endswith(".session-journal"):
            os.remove(file)
    LOGGER.info("✅ All Directories Updated.")
    await asyncio.sleep(1)

    LOGGER.info("🌐 Checking Required Variables ...")
    if not API_ID:
        LOGGER.info("❌ 'API_ID' - Not Found ‼️")
        sys.exit()
    if not API_HASH:
        LOGGER.info("❌ 'API_HASH' - Not Found ‼️")
        sys.exit()
    if not BOT_TOKEN:
        LOGGER.info("❌ 'BOT_TOKEN' - Not Found ‼️")
        sys.exit()
    if not STRING_SESSION:
        LOGGER.info("❌ 'STRING_SESSION' - Not Found ‼️")
        sys.exit()
    if not MONGO_DB_URL:
        LOGGER.info("❌ 'MONGO_DB_URL' - Not Found ‼️")
        sys.exit()
    LOGGER.info("✅ Required Variables Are Collected.")

    await asyncio.sleep(1)
    LOGGER.info("🌀 Starting All Clients ...")
    
    # Starting Bot
    try:
        await bot.start()
        LOGGER.info("✅ Bot Started.")
        if LOG_GROUP_ID != 0:
            await bot.send_message(LOG_GROUP_ID, "**🤖 Bot Started.**")
    except Exception as e:
        LOGGER.info(f"🚫 Bot Error: {e}")
        sys.exit()

    # Starting Userbot
    try:
        await userbot.start()
        LOGGER.info("✅ Userbot Started.")
        if LOG_GROUP_ID != 0:
            await userbot.send_message(LOG_GROUP_ID, "**👤 Userbot Started.**")
    except Exception as e:
        LOGGER.info(f"🚫 Userbot Error: {e}")
        sys.exit()

    # Starting Assistant (from Play plugin)
    try:
        await app.start()
        await app.join_chat("HEROKUBIN_01")  # Replace with your group/channel
        LOGGER.info("✅ Assistant Started.")
        if LOG_GROUP_ID != 0:
            await app.send_message(LOG_GROUP_ID, "**🦋 Assistant Started.**")
    except Exception as e:
        LOGGER.info(f"🚫 Assistant Error: {e}")
        sys.exit()

    # Starting PyTgCalls
    try:
        await call.start()
        LOGGER.info("✅ PyTgCalls Started.")
    except Exception as e:
        LOGGER.info(f"🚫 PyTgCalls Error: {e}")
        sys.exit()

    LOGGER.info("✅ Successfully Hosted Your Bot!")
    await idle()

if __name__ == "__main__":
    loop.run_until_complete(main())
