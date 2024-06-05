import os

from pyrogram.client import Client
from pyrogram.enums import ParseMode

from dotenv import load_dotenv

from config import BotConfig


def create_app() -> Client:
    load_dotenv()
    config = BotConfig(
        os.getenv('API_ID'),
        os.getenv('API_HASH'),
        os.getenv('APP_NAME')
    )
    return Client(
        config.app_name,
        config.api_id,
        config.api_hash,
        parse_mode=ParseMode.HTML
    )
