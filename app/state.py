from telethon import TelegramClient, types
import os
from app.db import DB
import config
from app import logger


class Vars:
    sessions_dir = "session_files"
    database_filename = "users.db"


class State:
    bot: TelegramClient = None
    os.makedirs(Vars.sessions_dir, exist_ok=True)
    db = DB(Vars.database_filename)
    admin: types.User = None

    @classmethod
    async def setup(cls, bot: TelegramClient):
        cls.bot = bot
        await cls.db.setup()
        try:
            cls.admin = await cls.bot.get_entity(config.ADMIN_USERNAME)
        except ValueError:
            logger.error("Admin username not found")
            await cls.bot.disconnect()
