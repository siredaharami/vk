import logging
import time
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
import config
SUDOERS = filters.user()

logging.getLogger("pyrogram").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)
boot = time.time()
mongodb = MongoCli(config.MONGO_URL)
db = mongodb.Anonymous
mongo = MongoClient(config.MONGO_URL)
mongodb = mongo.VIP
OWNER = config.OWNER_ID
_boot_ = time.time()
def sudo():
    global SUDOERS
    OWNER = config.OWNER_ID
    if config.MONGO_URL is None:
        SUDOERS.add(OWNER)
    else:
        sudoersdb = mongodb.sudoers
        sudoers = sudoersdb.find_one({"sudo": "sudo"})
        sudoers = [] if not sudoers else sudoers["sudoers"]
        SUDOERS.add(OWNER)
        if OWNER not in sudoers:
            sudoers.append(OWNER)
            sudoersdb.update_one(
                {"sudo": "sudo"},
                {"$set": {"sudoers": sudoers}},
                upsert=True,
            )
        if sudoers:
            for x in sudoers:
                SUDOERS.add(x)
    print(f"Sudoers Loaded.")
