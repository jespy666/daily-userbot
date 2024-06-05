from pyrogram.client import Client
from src.app import create_app
from src.plugins.autoresponse import AutoRespond
from src.database.mongo import AsyncMongoManager

from loguru import logger

from config import DBConfig


if __name__ == '__main__':
    try:
        logger.success("Starting the application...")
        app: Client = create_app()
        logger.info("Pyrogram client created")
        db_config = DBConfig()
        db = AsyncMongoManager(db_config, 'common')
        logger.info("Database connection initialized")
        AutoRespond(app, db)
        logger.info("added plugin 'Autoresponse'")
        app.run()
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        logger.critical("Pyrogram client stopped")
