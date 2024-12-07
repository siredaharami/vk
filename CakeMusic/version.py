from pyrogram import idle, __version__ as pyro_version
from platform import python_version
from pytgcalls.__version__ import __version__ as pytgcalls_version
from pyrogram import __version__ as pyrogram_version


__version__ = {
    "Baduserbot": "3.0",
    "PyTgCalls": pytgcalls_version,
    "pyrogram": pyrogram_version,
    "python": python_version(),
}
