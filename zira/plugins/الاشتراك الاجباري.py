# Zed-Thon
# Copyright (C) 2022 Zed-Thon . All Rights Reserved
#
# This file is a part of < https://github.com/Zed-Thon/ZelZal/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/Zed-Thon/ZelZal/blob/zira/LICENSE/>.
import os
import re
import telethon
from telethon.events import CallbackQuery, InlineQuery
from telethon import Button, events, functions
from telethon.tl import functions, types
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import EditBannedRequest, GetFullChannelRequest, GetParticipantRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChatBannedRights

from . import zedub
from ..sql_helper.fsub_sql import *
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..core.managers import edit_delete, edit_or_reply
from ..core.logger import logging
from . import BOTLOG, BOTLOG_CHATID, admin_groups, get_user_from_event
# =========================================================== #
#                                                  الملـــف كتـــابـــة  - T.me/ZThon                                    #
# =========================================================== #
Warn = "تخمـط بـدون ذكـر المصـدر - راح توثقهـا فضيحـه ع نفسـك"
# =========================================================== #
#                                                       زلـــزال الهيبـــه - T.me/zzzzl1l                                  #
# =========================================================== #
#                                              تـاريـخ كتابـة الملـف - 30 اكتوبر/2022                                  #
#                                                   الملف كان مدفوع وتم تنزيله مجاني                                   #
#                                                  الدليل https://t.me/ZThon/260                                 #
# =========================================================== #

zilzal = zedub.uid
zed_dev = (2095357462, 1895219306, 925972505)
LOGS = logging.getLogger(__name__)
zelzaal = False
MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
ANTI_DDDD_ZEDTHON_MODE = ChatBannedRights(
    until_date=None, view_messages=None, send_messages=True, send_media=True, send_stickers=True, send_gifs=True
)

async def is_admin(event, user):
    try:
        sed = await event.client.get_permissions(event.chat_id, user)
        if sed.is_admin:
            is_mod = True
        else:
            is_mod = False
    except:
        is_mod = False
    return is_mod


async def check_him(channel, user):
    try:
        result = await bot(
            functions.channels.GetParticipantRequest(channel, user)
        )
        return True
    except telethon.errors.rpcerrorlist.UserNotParticipantError:
        return False


async def rights(event):
    result = await bot(
        functions.channels.GetParticipantRequest(
            channel=event.chat_id,
            user_id=zilzal,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.ban_users
    )


@zedub.zed_cmd(pattern="(ضع اشتراك الخاص|وضع اشتراك الخاص)(?:\s|$)([\s\S]*)")
async def _(event):
    if input_str := event.pattern_match.group(2):
        try:
            p = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(event, f"`{e}`", 5)
        try:
            if p.first_name:
                await asyncio.sleep(1.5)
                delgvar("Custom_Pm_Channel")
                addgvar("Custom_Pm_Channel", f"-100{p.id}")
                return await edit_or_reply(
                    event, f"**⎉╎تم إضافة قناة الاشتراك الاجباري للخاص .. بنجـاح ☑️**\n\n**⎉╎يوزر القناة : ↶** `{input_str}`\n**⎉╎ايدي القناة : ↶** `{p.id}`\n\n**⎉╎ارسـل الان** `.تفعيل الاشتراك خاص`"
                )
        except Exception:
            try:
                if p.title:
                    await asyncio.sleep(1.5)
                    delgvar("Custom_Pm_Channel")
                    addgvar("Custom_Pm_Channel", f"-100{p.id}")
                    return await edit_or_reply(
                        event, f"**⎉╎تم إضافة قناة الاشتراك الاجباري للخاص .. بنجـاح ☑️**\n\n**⎉╎اسم القناة : ↶** `{p.title}`\n**⎉╎ايدي القناة : ↶** `{p.id}`\n\n**⎉╎ارسـل الان** `.تفعيل الاشتراك خاص`"
                    )
            except Exception as e:
                LOGS.info(str(e))
        await edit_or_reply(event, "⪼ **أدخل معـرف القناة او قم باستخدام الامر داخل القناة**")
    elif event.reply_to_msg_id:
        r_msg = await event.get_reply_message()
        if r_msg.media:
            await asyncio.sleep(1.5)
            delgvar("Custom_Pm_Channel")
            addgvar("Custom_Pm_Channel", event.chat_id)
            await edit_or_reply(
                event,
                f"**⎉╎تم إضافة قناة الاشتراك الاجباري للخاص .. بنجـاح ☑️**\n\n**⎉╎ايدي القناة : ↶** `{event.chat_id}`\n\n**⎉╎ارسـل الان** `.تفعيل الاشتراك خاص`",
            )

        else:
            await asyncio.sleep(1.5)
            delgvar("Custom_Pm_Channel")
            addgvar("Custom_Pm_Channel", event.chat_id)
            await edit_or_reply(
                event,
                f"**⎉╎تم إضافة قناة الاشتراك الاجباري للخاص .. بنجـاح ☑️**\n\n**⎉╎ايدي القناة : ↶** `{event.chat_id}`\n\n**⎉╎ارسـل الان** `.تفعيل الاشتراك خاص`",
            )

    else:
        await asyncio.sleep(1.5)
        delgvar("Custom_Pm_Channel")
        addgvar("Custom_Pm_Channel", event.chat_id)
        await edit_or_reply(event, f"**⎉╎تم إضافة قناة الاشتراك الاجباري للخاص .. بنجـاح ☑️**\n\n**⎉╎ايدي القناة : ↶** `{event.chat_id}`\n\n**⎉╎ارسـل الان** `.تفعيل الاشتراك خاص`")


@zedub.zed_cmd(pattern="(تفعيل اشتراك الخاص|تفعيل الاشتراك خاص)")
async def start_datea(event):
    global zelzaal
    if zelzaal:
        return await edit_or_reply(event, "**⎉╎الاشتراك الاجبـاري لـ الخـاص .. مفعـل مسبقـاً ☑️**")
    zelzaal = True
    await edit_or_reply(event, "**⎉╎تم تفعيـل الاشتـراك الاجبـاري خـاص .. بنجـاح ☑️**")

@zedub.zed_cmd(pattern="(تعطيل اشتراك الخاص|تعطيل الاشتراك الخاص)")
async def stop_datea(event):
    global zelzaal
    if zelzaal:
        zelzaal = False
        return await edit_or_reply(event, "**⎉╎تم تعطيـل الاشتـراك الاجبـاري خـاص .. بنجـاح ☑️**")
    await edit_or_reply(event, "**⎉╎الاشتراك الاجبـاري لـ الخـاص .. معطـل مسبقـاً ☑️**")


@zedub.zed_cmd(incoming=True, func=lambda e: e.is_private, edited=False, forword=None)
async def f(event):
    chat_id = event.chat_id
    chat = await event.get_chat()
    user = await event.get_sender()
    zelzal = (await event.get_sender()).id
    if chat.bot:
        return
    if zelzal in zed_dev:
        return
    global zelzaal
    if zelzaal:
        try:
            ch = gvarstatus("Custom_Pm_Channel")
            try:
                ch = int(ch)
            except BaseException:
                return
            rip = await check_him(ch, event.sender_id)
            if rip is False:
                c = await zedub.get_entity(ch)
                chn = c.username
                if c.username == None:
                    ra = await zedub(ExportChatInviteRequest(ch))
                    chn = ra.link
                if chn.startswith("https://"):
                    await event.reply(f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - **الاشتࢪاك الإجباࢪي**\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**مࢪحبـاً عـزيـزي 🫂** [{user.first_name}](tg://user?id={user.id}) \n⌔╎**لـ الغـاء كتمـك 🔊**\n⌔╎**يُࢪجـى الإشتـࢪاك بالقنـاة {chn} **", link_preview=False
                    )
                    return await event.delete()
                else:
                    await event.reply(f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - **الاشتࢪاك الإجباࢪي**\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**مࢪحبـاً عـزيـزي 🫂** [{user.first_name}](tg://user?id={user.id}) \n⌔╎**لـ الغـاء كتمـك 🔊**\n⌔╎**يُࢪجـى الإشتـࢪاك بالقنـاة @{chn} **", link_preview=False
                    )
                    return await event.delete()
        except BaseException:
            return

@zedub.zed_cmd(pattern="(ضع اشتراك الكروب|وضع اشتراك الكروب) ?(.*)")
async def fs(event):
    permissions = await bot.get_permissions(event.chat_id, event.sender_id)
    if not permissions.is_admin:
        return await event.reply(
            "**⌔╎عـذراً .. عـزيـزي\n**⌔╎لا املك صلاحيات المشـرف هنـا**"
        )
    if not await is_admin(event, zilzal):
        return await event.reply("**⌔╎عـذراً .. عـزيـزي\n**⌔╎لا املك صلاحيات المشـرف هنـا**")
    if event.is_private:
        await edit_or_reply(event, "**✾╎عـذراً .. هـذا الامـر خـاص بالمجمـوعـات فقـط**")
        return
    ahmed = event.pattern_match.group(1)
    if not ahmed:
        return await edit_delete(event, "**✾╎استخـدم الامـر هكـذا**\n**✾╎.اشتراك الكروب + معـرف القنـاة**")
    args = event.pattern_match.group(2)
    channel = args.replace("@", "")
    if args == "تفعيل" or args == "تشغيل":
        return await event.reply("**⌔╎عـذراً .. يرجى التحقق من معـرف القنـاة**")
    if args in ("off", "تعطيل", "ايقاف"):
        rm_fsub(event.chat_id)
        await event.reply("**✾╎تـم إيقـاف الاشتـراك الاجبـاري هنـا .. بنجـاح ✓**")
    else:
        try:
            ch_full = await bot(GetFullChannelRequest(channel=channel))
        except Exception as e:
            await event.reply(f"{e}")
            return await event.reply("**⌔╎عـذراً .. معـرف القنـاة غيـر موجـود**")
        rip = await check_him(channel, zilzal)
        if rip is False:
            return await event.reply(
                f"**⌔╎عـذراً .. عـزيـزي**\n**⌔╎لـ تمكين الاشتـراك الاجبـاري**\n**⌔╎يجب ان تكون مشرفًا في** [القنـاة](https://t.me/{args}).",
                link_preview=False,
            )
        add_fsub(event.chat_id, str(channel))
        await event.reply(f"**✾╎تم تفعيل الاشتراك الاجباري .. بنجاح ☑️**\n**✾╎قناة الاشتراك ~** @{channel}.")


@zedub.on(events.NewMessage(pattern=None))
async def f(event):
    chat_id = event.chat_id
    chat_db = is_fsub(event.chat_id)
    event.sender_id
    user = await event.get_sender()
    zed_dev = (2095357462, 1895219306, 925972505)
    zelzal = event.sender_id
    if isinstance(user, telethon.types.User) and user.bot:
        return
    if zelzal in zed_dev:
        return
    if not await is_admin(event, zilzal):
        return
    if not chat_db:
        return
    if chat_db:
        try:
            channel = chat_db.channel
            chat_id = event.chat_id
            chat_db = is_fsub(event.chat_id)
            channel = chat_db.channel
            user = await event.get_sender()
            grp = f"t.me/{channel}"
            rip = await check_him(channel, event.sender_id)
            if rip is False:
                await bot.send_message(
                    event.chat_id, f"[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - الاشتࢪاك الإجباࢪي](t.me/ZedThon)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**مࢪحبـاً عـزيـزي 🫂** [{user.first_name}](tg://user?id={user.id}) \n⌔╎**لـ الغـاء كتمـك 🔊**\n⌔╎**يُࢪجـى الإشتـࢪاك بالقنـاة @{channel} **", link_preview=False
                )
                await event.delete()
        except:
            if not await rights(event):
                await bot.send_message(
                    event.chat_id,
                    "**⌔╎عـذراً .. عـزيـزي\n**⌔╎لا املك صلاحيات المشـرف هنـا**",
                )


@zedub.zed_cmd(pattern="تعطيل اشتراك الكروب$")
async def removef(event):
    if is_fsub(event.chat_id):
        rm_fsub(event.chat_id)
        await edit_or_reply(event, "**✾╎تـم إيقـاف الاشتـراك الاجبـاري هنـا .. بنجـاح ✓**")
    else:
        return await edit_delete(event, "**✾╎عـذراً .. الاشتـراك الاجبـاري غيـر مفعـل هنـا**")
    
