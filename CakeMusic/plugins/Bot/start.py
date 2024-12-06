from CakeMusic import bot
from CakeMusic import *
from CakeMusic.plugins.Bot.Play import *

import aiohttp, aiofiles, asyncio, base64, logging
import os, platform, random, re, socket
import sys, time, textwrap

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




@bot.on_message(cdx(["start"]) & pyrofl.private)
async def start_message_private(client, message):
    user_id = message.from_user.id
    mention = message.from_user.mention
    await add_served_user(user_id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:5] == "verify":
            pass
            
    else:
        caption = f"""➻ нᴇʏ</b>, {mention} ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ !

● ɪ ᴀᴍ @{bot.me.username} ᴜꜱᴇʀʙᴏᴛ..

● ᴘʏᴛʜᴏɴ ➥</b> 3.10.11
● ᴘʏʀᴏɢʀᴀᴍ ➥</b> 2.0.106
● ᴘʏ-ᴛɢᴄᴀʟʟs ➥</b> 0.9.7
❖ ᴛʜɪs ɪs ᴘᴏᴡᴇʀғᴜʟ ᴜꜱᴇʀʙᴏᴛʙғᴏʀ ʏᴏᴜʀ ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ ᴠᴄ && ʀᴀɪᴅꜱ. """
        buttons = InlineKeyboardMarkup(
            [
                [
            InlineKeyboardButton(text="❍ᴡɴᴇꝛ", url="https://t.me/II_BAD_BABY_II"),
            InlineKeyboardButton(text="ᴜᴘᴅᴧᴛᴇ", url="https://t.me/HEROKUBIN_01"),
                ],
            ]
        )
        if START_IMAGE_URL:
            try:
                return await message.reply_photo(
                    photo=START_IMAGE_URL, caption=caption, reply_markup=buttons
                )
            except Exception as e:
                LOGGER.info(f"🚫 Start Image Error: {e}")
                try:
                    return await message.reply_text(text=caption, reply_markup=buttons)
                except Exception as e:
                    LOGGER.info(f"🚫 Start Error: {e}")
                    return
        else:
            try:
                return await message.reply_text(text=caption, reply_markup=buttons)
            except Exception as e:
                LOGGER.info(f"🚫 Start Error: {e}")
                return
                
                
@bot.on_message(cdx("start") & pyrofl.private)
async def start_message_private(client, message):
    mention = message.from_user.mention
    
    caption = f"""➻ нᴇʏ</b>, {mention} ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ !

● ɪ ᴀᴍ @{bot.me.username} ᴜꜱᴇʀʙᴏᴛ..

● ᴘʏᴛʜᴏɴ ➥</b> 3.10.11
● ᴘʏʀᴏɢʀᴀᴍ ➥</b> 2.0.106
● ᴘʏ-ᴛɢᴄᴀʟʟs ➥</b> 0.9.7
❖ ᴛʜɪs ɪs ᴘᴏᴡᴇʀғᴜʟ ᴜꜱᴇʀʙᴏᴛʙғᴏʀ ʏᴏᴜʀ ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ ᴠᴄ && ʀᴀɪᴅꜱ. """
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="• ᴧᴅᴅ мᴇ ʙᴧʙʏ •",
                    url=f"https://t.me/{bot.me.username}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    text="💌 𝖧ᴇʟᴘ $ 𝖢ᴏᴍᴍᴀɴᴅs 💌",
                    callback_data="help_command_list",
                )
            ],
        ]
    )
    if START_IMAGE_URL:
        try:
            return await message.reply_photo(
                photo=START_IMAGE_URL, caption=caption, reply_markup=buttons
            )
        except Exception as e:
            LOGGER.info(f"🚫 Start Image Error: {e}")
            try:
                return await message.reply_text(text=caption, reply_markup=buttons)
            except Exception as e:
                LOGGER.info(f"🚫 Start Error: {e}")
                return
    else:
        try:
            return await message.reply_text(text=caption, reply_markup=buttons)
        except Exception as e:
            LOGGER.info(f"🚫 Start Error: {e}")
            return
                
                
                
@bot.on_callback_query(rgx("help_command_list"))
async def open_command_list_alert(client, query):
    caption = """
♡━━━━━━━━━━━━⚆ _ ⚆━━━━━━━━━━━━━♡
**✫ ᴀʟʟ ᴍᴇᴍʙᴇʀs ᴄᴀɴ ᴜsᴇ :**
  ● /play - Stream Only Audio On VC.
  ● /vplay - Stream Audio With Video.

**✫ ᴏɴʟʏ ғᴏʀ ᴄʜᴀᴛ ᴀᴅᴍɪɴs :**
  ● /pause - Pause Running Stream.
  ● /resume - Resume Paused Stream.
  ● /skip - Skip Current Stream To Next.
  ● /end - Stop Current Running Stream.

**Note:** All Commands Will Work
Only in Channels/Groups.
♡━━━━━━━━━━━━⚆ _ ⚆━━━━━━━━━━━━━♡

**✫ ᴏɴʟʏ ғᴏʀ ᴏᴡɴᴇʀ :**
   ● /ping - Oᴡɴᴇʀs Kɴᴏᴡ
   ● /stats - Oᴡɴᴇʀs Kɴᴏᴡ
   ● /gcast - Oᴡɴᴇʀs Kɴᴏᴡ

"""
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🔙 Back",
                    callback_data="back_to_home",
                )
            ],
        ]
    )
    try:
        return await query.edit_message_text(text=caption, reply_markup=buttons)
    except Exception as e:
        LOGGER.info(f"🚫 Cmd Menu Error: {e}")
        return
        
@bot.on_callback_query(rgx("back_to_home"))
async def back_to_home_menu(client, query):
    mention = query.from_user.mention
    caption = f"""➻ нᴇʏ</b>, {mention} ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ !

● ɪ ᴀᴍ @{bot.me.username} ᴜꜱᴇʀʙᴏᴛ..

● ᴘʏᴛʜᴏɴ ➥</b> 3.10.11
● ᴘʏʀᴏɢʀᴀᴍ ➥</b> 2.0.106
● ᴘʏ-ᴛɢᴄᴀʟʟs ➥</b> 0.9.7
❖ ᴛʜɪs ɪs ᴘᴏᴡᴇʀғᴜʟ ᴜꜱᴇʀʙᴏᴛʙғᴏʀ ʏᴏᴜʀ ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ ᴠᴄ && ʀᴀɪᴅꜱ. """
    
    buttons = InlineKeyboardMarkup(
            [
                [
            InlineKeyboardButton(text="❍ᴡɴᴇꝛ", url="https://t.me/II_BAD_BABY_II"),
            InlineKeyboardButton(text="ᴜᴘᴅᴧᴛᴇ", url="https://t.me/HEROKUBIN_01"),
                ],
            ]
        )
    try:
        return await query.edit_message_text(text=caption, reply_markup=buttons)
    except Exception as e:
        LOGGER.info(f"🚫 Back Menu Error: {e}")
        return


@bot.on_callback_query(rgx("force_close"))
async def delete_cb_query(client, query):
    try:
        return await query.message.delete()
    except Exception:
        return
