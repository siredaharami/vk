from pyrogram import idle, __version__ as pyro_version
from platform import python_version
from pytgcalls.__version__ import __version__ as pytgcalls_version
from pyrogram import __version__ as pyrogram_version
import aiohttp, aiofiles, asyncio, base64, logging
from config import *


__version__ = {
    "Baduserbot": "2.5",
}

#pbx
LOGGER = logging.getLogger("SYSTEM")
async def main():
    LOGGER.info("🌐 Checking Required Variables ...")
    required_env_vars = [
        "MONGO_DB_URL",
    ]
