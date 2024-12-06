from typing import Union, List, Pattern
from pyrogram import Client, filters as pyrofl
from config import *



# Assistant Client
bot = Client(
    name="Assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=str(STRING_SESSION),
    plugins=dict(root="CakeMusic.plugins"),
)

def cdx(commands: Union[str, List[str]]):
    return pyrofl.command(commands, ["/", "!", "."])


def cdz(commands: Union[str, List[str]]):
    return pyrofl.command(commands, ["", "/", "!", "."])


def rgx(pattern: Union[str, Pattern]):
    return pyrofl.regex(pattern)
    
