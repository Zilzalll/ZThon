import asyncio
import os
import logging
from pathlib import Path
import time
from datetime import datetime

from telethon import events, types
from telethon.tl.types import PeerChannel
from telethon.utils import get_peer_id
from telethon.tl.types import InputMessagesFilterDocument

from . import zedub
from ..Config import Config
from ..helpers.utils import install_pip, _zedtools, _zedutils, _format, parse_pre, reply_id
from ..utils import load_module

LOGS = logging.getLogger(__name__)

if Config.ZELZAL_A:

    async def install():
        try:
            zilzal = await zedub.get_entity(PeerChannel(Config.ZELZAL_A))
        except:
            zilzal = Config.ZELZAL_A

        documentss = await zedub.get_messages(zilzal, None, filter=InputMessagesFilterDocument)
        total = int(documentss.total)
        for module in range(total):
            plugin_to_install = documentss[module].id
            plugin_name = documentss[module].file.name
            if plugin_name.endswith(".py"):
                if os.path.exists(f"zira/plugins/{plugin_name}"):
                    return
                downloaded_file_name = await zedub.download_media(
                    await zedub.get_messages(Config.ZELZAL_A, ids=plugin_to_install),
                    "zira/plugins/",
                )
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                flag = True
                check = 0
                while flag:
                    try:
                        load_module(shortname.replace(".py", ""))
                        break
                    except ModuleNotFoundError as e:
                        install_pip(e.name)
                        check += 1
                        if check > 5:
                            break

    zedub.loop.create_task(install())
