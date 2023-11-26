import re
import asyncio

from telethon import Button, events
from telethon.events import CallbackQuery
from ..core.logger import logging
from ..core import check_owner, pool
from ..helpers.utils import _format
from . import zedub

from ..Config import Config
from . import mention

LOGS = logging.getLogger(__name__)

plugin_category = "البوت"

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    @check_owner
    async def inline_handler(event):
        from .hhh import bbb, ttt
        builder = event.builder
        result = None
        query = event.text
        await zedub.get_me()
        if query.startswith("hhh") and event.query.user_id == zedub.uid:
            result = builder.article(
                title="zzz",
                text=ttt,
                buttons=bbb,
                link_preview=False,
            )
        await event.answer([result] if result else None)
