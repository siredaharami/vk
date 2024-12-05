from pyrogram import Client, filters as pyrofl
from config import *



app = Client(
    name="Bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

def cdx(commands: Union[str, List[str]]):
    return pyrofl.command(commands, ["/", "!", "."])


def cdz(commands: Union[str, List[str]]):
    return pyrofl.command(commands, ["", "/", "!", "."])


def rgx(pattern: Union[str, Pattern]):
    return pyrofl.regex(pattern)
    
