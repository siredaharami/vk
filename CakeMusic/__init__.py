from pytgcalls.types import ChatUpdate, Update, GroupCallConfig
from typing import Union, List, Pattern
from pytgcalls import PyTgCalls, filters as pytgfl
from pytgcalls.types import Call, MediaStream, AudioQuality, VideoQuality
from pyrogram import Client, filters as pyrofl
from config import *  # Ensure this file contains all required variables: API_ID, API_HASH, BOT_TOKEN, STRING_SESSION


# Bot client configuration
bot = Client(
    name="Bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="CakeMusic.plugins")  # Ensure the plugins folder is structured correctly
)

# Assistant client configuration
app = Client(
    name="Assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION,  # Ensure STRING_SESSION is valid and properly generated
    plugins=dict(root="CakeMusic.plugins")  # Plugins shared with bot
)


# Command filters for bot and app
def cdx(commands: Union[str, List[str]]):
    """Filter commands starting with /, !, or ."""
    return pyrofl.command(commands, prefixes=["/", "!", "."])


def cdz(commands: Union[str, List[str]]):
    """Filter commands starting with no prefix or /, !, ."""
    return pyrofl.command(commands, prefixes=["", "/", "!", "."])


def rgx(pattern: Union[str, Pattern]):
    """Filter messages matching a regex pattern."""
    return pyrofl.regex(pattern)

bot_owner_only = pyrofl.user(OWNER_ID)


call = PyTgCalls(app)
call_config = GroupCallConfig(auto_start=False)

mongo_async_cli = _mongo_async_(MONGO_DB_URL)
mongodb = mongo_async_cli.adityaxdb

# store start time
__start_time__ = time.time()


# Start both clients
if __name__ == "__main__":
    bot.start()  # Ensure Bot is starting correctly
    app.start()  # Ensure Assistant is starting correctly
    print("Both clients are running!")
