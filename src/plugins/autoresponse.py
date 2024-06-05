from typing import Dict, Any

from pyrogram import filters, Client
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from loguru import logger

from ..database.base import AsyncBase


class AutoRespond:

    def __init__(self, app: Client, db: AsyncBase) -> None:
        self.app = app
        self.db = db
        self.__set_up()

    async def toggle_autoresponse(self, _, message: Message) -> None:
        current_state: bool = await self.db.fetch_one('enabled')
        new_state = 'disabled' if current_state else 'enabled'
        logger.success('Autoresponse switched to: {}', new_state)
        await self.db.update_one('enabled', not current_state)
        await message.reply_text(f'Autoresponse is {new_state}!')

    async def get_reply_text(self, _, message: Message) -> None:
        reply_text: str | None = await self.db.fetch_one('reply_text')
        if not reply_text:
            await message.reply_text(
                'Reply text is empty.\n'
                'Set it up by <em>/setuptext</em> command!'
            )
        else:
            await message.reply_text(reply_text)

    async def set_reply_text(self, _, message: Message) -> None:
        text = message.text.split(' ', 1)
        if len(text) == 2 and text[1].strip():
            new_reply_text = text[1].strip()
            await self.db.update_one('reply_text', new_reply_text)
            await message.reply_text('Reply text is successfully set up!')
        else:
            await message.reply_text(
                'Please provide a valid reply text after the command.'
            )

    async def auto_response_handler(self, _, message: Message) -> None:
        data: Dict[str, Any] = await self.db.fetch_all()
        state: bool = data.get('enabled')
        reply_text: str | None = data.get('reply_text')
        if state:
            if reply_text:
                await message.reply_text(
                    reply_text,
                    disable_notification=True
                )

    def __set_up(self) -> None:
        handlers = [
            MessageHandler(
                self.toggle_autoresponse,
                filters.command('on') & filters.me
            ),
            MessageHandler(
                self.get_reply_text,
                filters.command('show') & filters.me
            ),
            MessageHandler(
                self.set_reply_text,
                filters.command('set') & filters.me
            ),
            MessageHandler(
                self.auto_response_handler,
                filters.text & filters.private
            )
        ]
        for handler in handlers:
            self.app.add_handler(handler)
