import os

from os import getenv
from io import BytesIO
from dotenv import load_dotenv
from pyrogram import Client, filters

# config variables
if os.path.exists("Config.env"):
    load_dotenv("Config.env")

API_ID = int(getenv("API_ID", "25742938"))
API_HASH = getenv("API_HASH", "b35b715fe8dc0a58e8048988286fc5b6")
BOT_TOKEN = getenv("BOT_TOKEN", "7656510911:AAHx2GcEV9q_HOQ5NjysO1V2cMdAaVQpz8Y")
STRING_SESSION = getenv("STRING_SESSION", "BQGIzloAOBgXQvRpl8euAjWpsYdQBDNP2eBae110aMP-eUDCfVdETHfFtRrWxPl1NUXnK2oAX7MyfLL1TdbQ35PuJ8CrrbS5xXxeHN4zR6k7W09ZRkdwuF7GETxKK3gAwtaF3qZmop8xmFjMewyuLP36awmqDKtpP-je4jLif4V2Vyqa2P7zEO-MQT1m0eb0qCI6BkC8WJ5_hWJzy9uEGk_fr-dOnMtffcocMpFrAia1aw_j0z2xTglDoIyW1QlNVH1mU89V00OedRS4TSMkC6_621rhsc9HmcTQ4pGz2We56hJ-hvHjOJfoLnpaWBfybeu3BEW74P6Fxwpm90djdbmymwyZTgAAAAF-_9otAA")
MONGO_DB_URL = getenv("MONGO_DB_URL", "mongodb+srv://hnyx:wywyw2@cluster0.9dxlslv.mongodb.net/?retryWrites=true&w=majority")
OWNER_ID = int(getenv("OWNER_ID", "7009601543"))
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", "-1002356967761"))
START_IMAGE_URL = getenv("START_IMAGE_URL", "https://files.catbox.moe/6v7esb.jpg")
HANDLERS = getenv("HANDLERS", ". ! ?").strip().split()


class Symbols:
    anchor = "✰"
    arrow_left = "↞"
    arrow_right = "↠"
    back = "☜ ʙᴀᴄᴋ"
    bullet = "•"
    check_mark = "✓"
    close = "❌ 𝗖𝗟𝗢𝗦𝗘 ❌"
    cross_mark = "✗"
    diamond_1 = "◇"
    diamond_2 = "◈"
    next = "⤚ ɴᴇxᴛ"
    previous = "ᴘʀᴇᴠ ⤙"
    radio_select = "◉"
    radio_unselect = "〇"
    triangle_left = "◂"
    triangle_right = "▸"

#pbx

# Global config: do not edit
    BOT_CMD_INFO = {}
    BOT_CMD_MENU = {}
    BOT_HELP = {}
    CMD_INFO = {}
    CMD_MENU = {}
    HELP_DICT = {}
    TEMPLATES = {}

class ENV:
    """Database ENV Names"""

    airing_template = "AIRING_TEMPLATE"
    airpollution_template = "AIRPOLLUTION_TEMPLATE"
    alive_pic = "ALIVE_PIC"
    alive_template = "ALIVE_TEMPLATE"
    anilist_user_template = "ANILIST_USER_TEMPLATE"
    anime_template = "ANIME_TEMPLATE"
    btn_in_help = "BUTTONS_IN_HELP"
    character_template = "CHARACTER_TEMPLATE"
    chat_info_template = "CHAT_INFO_TEMPLATE"
    climate_api = "CLIMATE_API"
    climate_template = "CLIMATE_TEMPLATE"
    command_template = "COMMAND_TEMPLATE"
    currency_api = "CURRENCY_API"
    custom_pmpermit = "CUSTOM_PMPERMIT"
    gban_template = "GBAN_TEMPLATE"
    github_user_template = "GITHUB_USER_TEMPLATE"
    help_emoji = "HELP_EMOJI"
    help_template = "HELP_TEMPLATE"
    is_logger = "IS_LOGGER"
    lyrics_api = "LYRICS_API"
    manga_template = "MANGA_TEMPLATE"
    ocr_api = "OCR_API"
    ping_pic = "PING_PIC"
    ping_template = "PING_TEMPLATE"
    pm_logger = "PM_LOGGER"
    pm_max_spam = "PM_MAX_SPAM"
    pmpermit = "PMPERMIT"
    pmpermit_pic = "PMPERMIT_PIC"
    remove_bg_api = "REMOVE_BG_API"
    thumbnail_url = "THUMBNAIL_URL"
    statistics_template = "STATISTICS_TEMPLATE"
    sticker_packname = "STICKER_PACKNAME"
    tag_logger = "TAG_LOGGER"
    telegraph_account = "TELEGRAPH_ACCOUNT"
    time_zone = "TIME_ZONE"
    unload_plugins = "UNLOAD_PLUGINS"
    unsplash_api = "UNSPLASH_API"
    usage_template = "USAGE_TEMPLATE"
    user_info_template = "USER_INFO_TEMPLATE"

# users config: do not edit
    AUTH_USERS = filters.user()

all_env: list[str] = [
    value for key, value in ENV.__dict__.items() if not key.startswith("__")
]
