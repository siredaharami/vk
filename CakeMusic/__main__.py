import aiohttp, aiofiles, asyncio, base64, logging
import os, platform, random, re, socket
import sys, time, textwrap
from CakeMusic import app as bot
from CakeMusic.plugins.Play import app, call
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
    if "cookies.txt" not in os.listdir():
        LOGGER.info("⚠️ 'cookies.txt' - Not Found❗")
        sys.exit()
    if "downloads" not in os.listdir():
        os.mkdir("downloads")
    for file in os.listdir():
        if file.endswith(".session"):
            os.remove(file)
    for file in os.listdir():
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
        LOGGER.info("'MONGO_DB_URL' - Not Found !!")
        sys.exit()
 #   try:
     #   await mongo_async_cli.admin.command('ping')
#    except Exception:
   #     LOGGER.info("❌ 'MONGO_DB_URL' - Not Valid !!")
    #    sys.exit()
    LOGGER.info("✅ Required Variables Are Collected.")
    await asyncio.sleep(1)
    LOGGER.info("🌀 Starting All Clients ...")
    try:
        await bot.start()
    except Exception as e:
        LOGGER.info(f"🚫 Bot Error: {e}")
        sys.exit()
    if LOG_GROUP_ID != 0:
        try:
            await bot.send_message(LOG_GROUP_ID, "**🤖 Bot Started.**")
        except Exception:
            pass
    LOGGER.info("✅ Bot Started.")
    try:
        await app.start()
    except Exception as e:
        LOGGER.info(f"🚫 Assistant Error: {e}")
        sys.exit()
    try:
        await app.join_chat("HEROKUBIN_01")
        await app.join_chat("HEROKUBIN_01")
    except Exception:
        pass
    if LOG_GROUP_ID != 0:
        try:
            await app.send_message(LOG_GROUP_ID, "**🦋 Assistant Started.**")
        except Exception:
            pass
    LOGGER.info("✅ Assistant Started.")
    try:
        await call.start()
    except Exception as e:
        LOGGER.info(f"🚫 PyTgCalls Error: {e}")
        sys.exit()
    LOGGER.info("✅ PyTgCalls Started.")
    await asyncio.sleep(1)
    LOGGER.info("✅ Sucessfully Hosted Your Bot !!")
    LOGGER.info("✅ Now Do Visit: @AdityaServer !!")
    await idle()




if __name__ == "__main__":
    loop.run_until_complete(main())
