from typing import Union, List, Pattern
from pyrogram import Client, filters as pyrofl
from config import *

# Bot Client
bot = Client(
    name="Bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="CakeMusic.plugins"),
)

# Userbot Client
app = Client(
    name="Userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,  # Replace with your session string
    plugins=dict(root="CakeMusic.plugins"),  # Optional, same plugins folder
)

# Command Decorator for Both
def cdx(commands: Union[str, List[str]]):
    return pyrofl.command(commands, ["/", "!", "."])

def cdz(commands: Union[str, List[str]]):
    return pyrofl.command(commands, ["", "/", "!", "."])

def rgx(pattern: Union[str, Pattern]):
    return pyrofl.regex(pattern)
