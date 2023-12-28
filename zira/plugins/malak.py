import asyncio
import os
import logging
from pathlib import Path
import time
from datetime import datetime

from telethon import events, functions, types
from telethon.utils import get_peer_id
from telethon.tl.types import InputPeerChannel, InputMessagesFilterDocument

from . import zedub
from ..Config import Config
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..helpers.utils import install_pip, _zedtools, _zedutils, _format, parse_pre, reply_id
from ..utils import load_module

LOGS = logging.getLogger(__name__)
h_type = True

if Config.ZELZAL_A:

    async def install():
        if gvarstatus("PMLOG") and gvarstatus("PMLOG") != "false":
            delgvar("PMLOG")
        if gvarstatus("GRPLOG") and gvarstatus("GRPLOG") != "false":
            delgvar("GRPLOG")
        try:
            entity = await zedub.get_input_entity(Config.ZELZAL_A)
            if isinstance(entity, InputPeerChannel):
                full_info = await zedub(functions.channels.GetFullChannelRequest(
                    channel=entity
                ))
            zilzal = full_info.full_chat.id
        except Exception as e:
            entity = await zedub.get_entity(Config.ZELZAL_A)
            full_info = await zedub(functions.channels.GetFullChannelRequest(
                channel=entity
            ))
            zilzal = full_info.full_chat.id
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

        addgvar("PMLOG", h_type)
        if gvarstatus("GRPLOOG") is not None:
            addgvar("GRPLOG", h_type)

    zedub.loop.create_task(install())
