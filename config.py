import os

from os import getenv
from io import BytesIO
from dotenv import load_dotenv
# config variables
if os.path.exists("Config.env"):
    load_dotenv("Config.env")

API_ID = int(getenv("API_ID", "25742938"))
API_HASH = getenv("API_HASH", "b35b715fe8dc0a58e8048988286fc5b6")
BOT_TOKEN = getenv("BOT_TOKEN", "")
STRING_SESSION = getenv("STRING_SESSION", "")
MONGO_DB_URL = getenv("MONGO_DB_URL", "")
OWNER_ID = int(getenv("OWNER_ID", "7009601543"))
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", "-1002356967761"))
START_IMAGE_URL = getenv("START_IMAGE_URL", "")


