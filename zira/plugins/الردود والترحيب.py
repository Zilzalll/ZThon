import re
import datetime
from asyncio import sleep

from telethon import events
from telethon.utils import get_display_name

from . import zedub
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper import pmpermit_sql as pmpermit_sql
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..sql_helper.filter_sql import (
    add_filter,
    get_filters,
    remove_all_filters,
    remove_filter,
)
from ..sql_helper.welcome_sql import (
    add_welcome_setting,
    get_current_welcome_settings,
    rm_welcome_setting,
    update_previous_welcome,
)
from ..sql_helper.welcomesql import (
    addwelcome_setting,
    getcurrent_welcome_settings,
    rmwelcome_setting,
)
from . import BOTLOG, BOTLOG_CHATID

plugin_category = "الخدمات"
LOGS = logging.getLogger(__name__)


ZelzalWF_cmd = (
    "𓆩 [𝗦𝗼𝘂𝗿𝗰𝗲 𝗭𝗧𝗵𝗼𝗻 - اوامـر الـردود / والتـرحيب](t.me/ZThon) 𓆪\n\n"
    "**✾╎قائـمه اوامـر الـردود 🦾 :** \n\n"
    "**⎞𝟏⎝** `.رد`\n"
    "**•• ⦇الامـر + اسـم الـرد بالـرد ع كلمـة الـرد او بالـرد ع ميديـا⦈ لـ اضـافة رد بالكـروب**\n\n"
    "**⎞𝟐⎝** `.حذف رد`\n"
    "**•• ⦇الامـر + كلمـة الـرد⦈ لـ حـذف رد محـدد**\n\n"
    "**⎞𝟑⎝** `.ردودي`\n"
    "**•• لـ عـرض قائمـة بالـردود الخـاصـه بك**\n\n"
    "**⎞𝟒⎝** `.حذف الردود`\n"
    "**•• لـ حـذف جميـع الـردود الخـاصـه بـك**\n\n"
    "**✾╎قائـمه اوامر تـرحيب المجمـوعـات 🌐:** \n\n"
    "**⎞𝟓⎝** `.ترحيب`\n"
    "**•• ⦇الامـر + نـص التـرحـيـب⦈**\n\n"
    "**⎞𝟔⎝** `.حذف الترحيب`\n"
    "**•• لـ حـذف التـرحـيـب**\n\n"
    "**⎞𝟕⎝** `.الترحيبات`\n"
    "**•• لـ جـلـب تـرحـيـبـك**\n\n"
    "**✾╎قائـمه اوامر ترحـيـب الخـاص 🌐:**\n\n"
    "**⎞𝟖⎝** `.رحب`\n"
    "**•• ⦇الامـر + نـص التـرحيـب⦈**\n\n"
    "**⎞𝟗⎝** `.حذف رحب`\n"
    "**•• لـ حـذف تـرحيـب الخـاص**\n\n"
    "**⎞𝟏𝟎⎝** `.جلب رحب`\n"
    "**•• لـ جـلب تـرحيـب الخـاص **\n\n"
    "\n 𓆩 [𝙎𝙊𝙐𝙍𝘾𝞝 𝙕𝞝𝘿](t.me/ZThon) 𓆪"
)


# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern="الردود")
async def cmd(zelzallll):
    await edit_or_reply(zelzallll, ZelzalWF_cmd)

@zedub.zed_cmd(pattern="الترحيب")
async def cmd(zelzallll):
    await edit_or_reply(zelzallll, ZelzalWF_cmd)


@zedub.zed_cmd(incoming=True)
async def filter_incoming_handler(event):
    name = event.raw_text
    filters = get_filters(event.chat_id)
    if not filters:
        return
    a_user = await event.get_sender()
    chat = await event.get_chat()
    me = await event.client.get_me()
    title = get_display_name(await event.get_chat()) or "هـذه الدردشــه"
    participants = await event.client.get_participants(chat)
    count = len(participants)
    mention = f"[{a_user.first_name}](tg://user?id={a_user.id})"
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    first = a_user.first_name
    last = a_user.last_name
    fullname = f"{first} {last}" if last else first
    username = f"@{a_user.username}" if a_user.username else mention
    userid = a_user.id
    my_first = me.first_name
    my_last = me.last_name
    my_fullname = f"{my_first} {my_last}" if my_last else my_first
    my_username = f"@{me.username}" if me.username else my_mention
    for trigger in filters:
        pattern = f"( |^|[^\\w]){re.escape(trigger.keyword)}( |$|[^\\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            file_media = None
            filter_msg = None
            if trigger.f_mesg_id:
                msg_o = await event.client.get_messages(
                    entity=BOTLOG_CHATID, ids=int(trigger.f_mesg_id)
                )
                file_media = msg_o.media
                filter_msg = msg_o.message
                link_preview = True
            elif trigger.reply:
                filter_msg = trigger.reply
                link_preview = False
            await event.reply(
                filter_msg.format(
                    mention=mention,
                    title=title,
                    count=count,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                    my_first=my_first,
                    my_last=my_last,
                    my_fullname=my_fullname,
                    my_username=my_username,
                    my_mention=my_mention,
                ),
                file=file_media,
                link_preview=link_preview,
            )


@zedub.zed_cmd(
    pattern="رد (.*)",
    command=("رد", plugin_category),
    info={
        "header": "To save filter for the given keyword.",
        "اضـافـات الــرد": {
            "{mention}": "اضافه منشن",
            "{title}": "اضافة اسم كـروب الـرد",
            "{count}": "اضافة عدد اعضاء الكروب",
            "{first}": "اضافة الاسم الاول",
            "{last}": "اضافة الاسم الاخر",
            "{fullname}": "اضافة الاسم الكامل",
            "{userid}": "اضافة ايدي الشخص",
            "{username}": "اضافة معرف الشخص",
            "{my_first}": "اضافة اسمك الاول",
            "{my_fullname}": "اضافة اسمك الكامل",
            "{my_last}": "اضافة اسمك الاخر",
            "{my_mention}": "اضافة تاك حسابك",
            "{my_username}": "اضافة معرفك",
        },
        "الاسـتخـدام": "{tr}رد + كلمـه بالـرد ع نـص الـرد",
    },
)
async def add_new_filter(event):
    "To save the filter"
    keyword = event.pattern_match.group(1)
    string = event.text.partition(keyword)[2]
    msg = await event.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#الــردود\
            \n**⪼ ايـدي الدردشـه :**  {event.chat_id}\
            \n**⪼ الــرد :**  {keyword}\
            \n**⪼ تم حفظ الرسـالة كـرد على المستخدمين في المجموعـة المحـددة ...**",
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=event.chat_id,
                silent=True,
            )
            msg_id = msg_o.id
        else:
            await edit_or_reply(
                event,
                "**❈╎يتطلب رد ميديـا تعيين كـروب السجـل اولاً ..**\n**❈╎لاضافـة كـروب السجـل**\n**❈╎اتبـع الشـرح ⇚** https://t.me/zzzvrr/13",
            )
            return
    elif msg and msg.text and not string:
        string = msg.text
    elif not string:
        return await edit_or_reply(event, "**- يجب استخدام الامر بشكل صحيح**")
    success = "**- ❝ الـرد ↫** {} **تـم {} بـ نجـاح 🎆☑️"
    if add_filter(str(event.chat_id), keyword, string, msg_id) is True:
        return await edit_or_reply(event, success.format(keyword, "اضافتـه"))
    remove_filter(str(event.chat_id), keyword)
    if add_filter(str(event.chat_id), keyword, string, msg_id) is True:
        return await edit_or_reply(event, success.format(keyword, "تحديثـه"))
    await edit_or_reply(event, f"**- اووبـس .. لقـد حـدث خطأ اثنـاء إعـداد الـرد** {keyword}")


@zedub.zed_cmd(
    pattern="ردودي$",
    command=("ردودي", plugin_category),
    info={
        "header": "To list all filters in that chat.",
        "الاسـتخـدام": "{tr}ردودي",
    },
)
async def on_snip_list(event):
    "To list all filters in that chat."
    OUT_STR = "** ❈╎لاتوجـد ردود محفوظـه في هـذه الدردشـه ༗**"
    filters = get_filters(event.chat_id)
    for filt in filters:
        if OUT_STR == "** ❈╎لاتوجـد ردود محفوظـه في هـذه الدردشـه ༗**":
            OUT_STR = "𓆩 𝗦𝗼𝘂𝗿𝗰𝗲 𝗭𝗧𝗵𝗼𝗻 - قائمـة الـردود 𓆪\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
        OUT_STR += "👉 `{}`\n".format(filt.keyword)
    await edit_or_reply(
        event,
        OUT_STR,
        caption="**⧗╎الـردود المضـافـه في هـذه الدردشـه هـي :**",
        file_name="filters.text",
    )


@zedub.zed_cmd(
    pattern="حذف رد ([\s\S]*)",
    command=("حذف رد", plugin_category),
    info={
        "header": "To delete that filter . so if user send that keyword bot will not reply",
        "الاسـتخـدام": "{tr}حذف رد + كلمة الرد",
    },
)
async def remove_a_filter(event):
    "Stops the specified keyword."
    filt = event.pattern_match.group(1)
    if not remove_filter(event.chat_id, filt):
        await event.edit("**- ❝ الـرد ↫** {} **غيـر موجـود ⁉️**".format(filt))
    else:
        await event.edit("**- ❝ الـرد ↫** {} **تم حذفه بنجاح ☑️**".format(filt))


@zedub.zed_cmd(
    pattern="حذف الردود$",
    command=("حذف الردود", plugin_category),
    info={
        "header": "To delete all filters in that group.",
        "الاسـتخـدام": "{tr}حذف الردود",
    },
)
async def on_all_snip_delete(event):
    "To delete all filters in that group."
    filters = get_filters(event.chat_id)
    if filters:
        remove_all_filters(event.chat_id)
        await edit_or_reply(event, "**⪼ تم حذف جـميع الــردود المضـافـهہ هنـا .. بنجـاح☑️**")
    else:
        await edit_or_reply(event, "**⪼ لا توجـد ردود مضـافـهہ في هـذه المجموعـة**")

# ================================================================================================ #
# =========================================الترحيب================================================= #
# ================================================================================================ #

@zedub.on(events.ChatAction)
async def _(event):
    cws = get_current_welcome_settings(event.chat_id)
    if gvarstatus("TIME_STOP") is not None: #Code by T.me/zzzzl1l
        zedstop = gvarstatus("TIME_STOP")
        now = datetime.datetime.now().time()
        if datetime.time(f"{zedstop}", 0) <= now < datetime.time(6, 0):
            return
    if (
        cws
        and (event.user_joined or event.user_added)
        and not (await event.get_user()).bot
    ):
        if gvarstatus("clean_welcome") is None:
            try:
                await event.client.delete_messages(event.chat_id, cws.previous_welcome)
            except Exception as e:
                LOGS.warn(str(e))
        a_user = await event.get_user()
        chat = await event.get_chat()
        me = await event.client.get_me()
        title = get_display_name(await event.get_chat()) or "لـ هـذه الدردشـة"
        participants = await event.client.get_participants(chat)
        count = len(participants)
        mention = "<a href='tg://user?id={}'>{}</a>".format(
            a_user.id, a_user.first_name
        )
        my_mention = "<a href='tg://user?id={}'>{}</a>".format(me.id, me.first_name)
        first = a_user.first_name
        last = a_user.last_name
        fullname = f"{first} {last}" if last else first
        username = f"@{a_user.username}" if a_user.username else mention
        userid = a_user.id
        my_first = me.first_name
        my_last = me.last_name
        my_fullname = f"{my_first} {my_last}" if my_last else my_first
        my_username = f"@{me.username}" if me.username else my_mention
        file_media = None
        current_saved_welcome_message = None
        if cws:
            if cws.f_mesg_id:
                msg_o = await event.client.get_messages(
                    entity=BOTLOG_CHATID, ids=int(cws.f_mesg_id)
                )
                file_media = msg_o.media
                current_saved_welcome_message = msg_o.message
                link_preview = True
            elif cws.reply:
                current_saved_welcome_message = cws.reply
                link_preview = False
        current_message = await event.reply(
            current_saved_welcome_message.format(
                mention=mention,
                title=title,
                count=count,
                first=first,
                last=last,
                fullname=fullname,
                username=username,
                userid=userid,
                my_first=my_first,
                my_last=my_last,
                my_fullname=my_fullname,
                my_username=my_username,
                my_mention=my_mention,
            ),
            file=file_media,
            parse_mode="html",
            link_preview=link_preview,
        )
        update_previous_welcome(event.chat_id, current_message.id)


@zedub.zed_cmd(
    pattern="ترحيب(?:\s|$)([\s\S]*)",
    command=("ترحيب", plugin_category),
    info={
        "header": "To welcome new users in chat.",
        "اضـافات التـرحيب": {
            "{mention}": "اضافه منشن",
            "{title}": "اضافة اسم كروب الترحيب",
            "{count}": "اضافة عدد اعضاء الكروب",
            "{first}": "اضافة الاسم الاول",
            "{last}": "اضافة الاسم الاخر",
            "{fullname}": "اضافة الاسم الكامل",
            "{userid}": "اضافة ايدي الشخص",
            "{username}": "اضافة معرف الشخص",
            "{my_first}": "اضافة اسمك الاول",
            "{my_fullname}": "اضافة اسمك الكامل",
            "{my_last}": "اضافة اسمك الاخر",
            "{my_mention}": "اضافة تاك حسابك",
            "{my_username}": "اضافة معرفك",
        },
        "الاسـتخـدام": [
            "{tr}ترحيب + نص الترحيب",
            "{tr}ترحيب بالـرد ع رسالـه ترحيبيـه   او بالـرد ع ميديـا تحتهـا نـص",
        ],
        "مثـال": "{tr}ترحيب اططلـق دخـول {mention}, نـورت مجمـوعتنـا {title} الـخ",
    },
)
async def save_welcome(event):
    "To set welcome message in chat."
    msg = await event.get_reply_message()
    string = "".join(event.text.split(maxsplit=1)[1:])
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**⪼ رسـالة التـرحيب :**\
                \n**⪼ ايـدي الـدردشـة :** {event.chat_id}\
                \n**⪼ يتم حفـظ الرسـالة كـ ملاحظـة ترحيبيـة لـ 🔖 :** {get_display_name(await event.get_chat())}, Don't delete this message !!",
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID, messages=msg, from_peer=event.chat_id, silent=True
            )
            msg_id = msg_o.id
        else:
            return await edit_or_reply(
                event,
                "**يتطلب حفظ تـرحيب الميـديـا .. تعيين فـار كـروب السجـل ؟!...**",
            )
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "**⪼ {} التـرحيب .. بنجـاح فـي هـذه الدردشـه 𓆰.**"
    if add_welcome_setting(event.chat_id, 0, string, msg_id) is True:
        return await edit_or_reply(event, success.format("تـم حفـظ"))
    rm_welcome_setting(event.chat_id)
    if add_welcome_setting(event.chat_id, 0, string, msg_id) is True:
        return await edit_or_reply(event, success.format("تـم تحـديث"))
    await edit_or_reply("**⪼ هنالك خطأ في وضع الترحيب هنا**")


@zedub.zed_cmd(
    pattern="حذف الترحيب$",
    command=("حذف الترحيب", plugin_category),
    info={
        "header": "To turn off welcome message in group.",
        "الاسـتخـدام": "{tr}حذف الترحيب",
    },
)
async def del_welcome(event):
    "To turn off welcome message"
    if rm_welcome_setting(event.chat_id) is True:
        await edit_or_reply(event, "**⪼ تـم حـذف التـرحيب .. بنجـاح فـي هـذه الدردشـه 𓆰.**")
    else:
        await edit_or_reply(event, "**⪼ ليـس لـدي اي ترحيبـات هنـا ؟!.**")


@zedub.zed_cmd(
    pattern="الترحيبات$",
    command=("الترحيبات", plugin_category),
    info={
        "header": "To check current welcome message in group.",
        "الاسـتخـدام": "{tr}الترحيبات",
    },
)
async def show_welcome(event):
    "To show current welcome message in group"
    cws = get_current_welcome_settings(event.chat_id)
    if not cws:
        return await edit_or_reply(event, "** ⪼ لاتوجد اي رسـاله ترحيب محفوظـه هنـا ؟!...**")
    if cws.f_mesg_id:
        msg_o = await event.client.get_messages(
            entity=BOTLOG_CHATID, ids=int(cws.f_mesg_id)
        )
        await edit_or_reply(
            event, "** ⪼ أرحب حاليًا بالمستخدمين الجدد بهذه الرساله الترحيبية 𓆰.🜝**"
        )
        await event.reply(msg_o.message, file=msg_o.media)
    elif cws.reply:
        await edit_or_reply(
            event, "** ⪼ أرحب حاليًا بالمستخدمين الجدد بهذه الرساله الترحيبية 𓆰.🜝**"
        )
        await event.reply(cws.reply, link_preview=False)


@zedub.zed_cmd(
    pattern="cleanwelcome (on|off)$",
    command=("cleanwelcome", plugin_category),
    info={
        "header": "To turn off or turn on of deleting previous welcome message.",
        "description": "if you want to delete previous welcome message and send new one turn on it by deafult it will be on. Turn it off if you need",
        "الاسـتخـدام": "{tr}cleanwelcome <on/off>",
    },
)
async def del_welcome(event):
    "To turn off or turn on of deleting previous welcome message."
    input_str = event.pattern_match.group(1)
    if input_str == "on":
        if gvarstatus("clean_welcome") is None:
            return await edit_delete(event, "__Already it was turned on.__")
        delgvar("clean_welcome")
        return await edit_delete(
            event,
            "__From now on previous welcome message will be deleted and new welcome message will be sent.__",
        )
    if gvarstatus("clean_welcome") is None:
        addgvar("clean_welcome", "false")
        return await edit_delete(
            event, "__From now on previous welcome message will not be deleted .__"
        )
    await edit_delete(event, "It was turned off already")

# ================================================================================================ #
# =========================================ترحيب الخاص================================================= #
# ================================================================================================ #

@zedub.on(events.ChatAction)
async def _(event):  # sourcery no-metrics
    cws = getcurrent_welcome_settings(event.chat_id)
    if (
        cws
        and (event.user_joined or event.user_added)
        and not (await event.get_user()).bot
    ):
        a_user = await event.get_user()
        chat = await event.get_chat()
        me = await event.client.get_me()
        title = get_display_name(await event.get_chat()) or "لهـذه الدردشـه"
        participants = await event.client.get_participants(chat)
        count = len(participants)
        mention = "<a href='tg://user?id={}'>{}</a>".format(
            a_user.id, a_user.first_name
        )
        my_mention = "<a href='tg://user?id={}'>{}</a>".format(me.id, me.first_name)
        first = a_user.first_name
        last = a_user.last_name
        fullname = f"{first} {last}" if last else first
        username = f"@{a_user.username}" if a_user.username else mention
        userid = a_user.id
        my_first = me.first_name
        my_last = me.last_name
        my_fullname = f"{my_first} {my_last}" if my_last else my_first
        my_username = f"@{me.username}" if me.username else my_mention
        file_media = None
        current_saved_welcome_message = None
        if cws:
            if cws.f_mesg_id:
                msg_o = await event.client.get_messages(
                    entity=BOTLOG_CHATID, ids=int(cws.f_mesg_id)
                )
                file_media = msg_o.media
                current_saved_welcome_message = msg_o.message
                link_preview = True
            elif cws.reply:
                current_saved_welcome_message = cws.reply
                link_preview = False
        if not pmpermit_sql.is_approved(userid):
            pmpermit_sql.approve(userid, "Due to private welcome")
        await sleep(1)
        current_message = await event.client.send_message(
            userid,
            current_saved_welcome_message.format(
                mention=mention,
                title=title,
                count=count,
                first=first,
                last=last,
                fullname=fullname,
                username=username,
                userid=userid,
                my_first=my_first,
                my_last=my_last,
                my_fullname=my_fullname,
                my_username=my_username,
                my_mention=my_mention,
            ),
            file=file_media,
            parse_mode="html",
            link_preview=link_preview,
        )


@zedub.zed_cmd(
    pattern="رحب(?:\s|$)([\s\S]*)",
    command=("رحب", plugin_category),
    info={
        "header": "To welcome user(sends welcome message to here private messages).",
        "description": "Saves the message as a welcome note in the chat. And will send welcome message to every new user who ever joins newly in group.",
        "option": {
            "{mention}": "To mention the user",
            "{title}": "To get chat name in message",
            "{count}": "To get group members",
            "{first}": "To use user first name",
            "{last}": "To use user last name",
            "{fullname}": "To use user full name",
            "{userid}": "To use userid",
            "{username}": "To use user username",
            "{my_first}": "To use my first name",
            "{my_fullname}": "To use my full name",
            "{my_last}": "To use my last name",
            "{my_mention}": "To mention myself",
            "{my_username}": "To use my username.",
        },
        "usage": [
            "{tr}savepwel <welcome message>",
            "reply {tr}savepwel to text message or supported media with text as media caption",
        ],
        "examples": "{tr}savepwel Hi {mention}, Welcome to {title} chat",
    },
)
async def save_welcome(event):
    "To set private welcome message."
    msg = await event.get_reply_message()
    string = "".join(event.text.split(maxsplit=1)[1:])
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#ترحـيب الخاص\
                \n**- ايـدي الدردشـة :** {event.chat_id}\
                \nThe following message is saved as the welcome note for the {get_display_name(await event.get_chat())}, Dont delete this message !!",
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID, messages=msg, from_peer=event.chat_id, silent=True
            )
            msg_id = msg_o.id
        else:
            await edit_or_reply(
                event,
                "**⪼ الميديا المعطاه تم حفظها كترحيب خاص لـ BOTLOG_CHATID  ء𓆰**",
            )
            return
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "**⪼ تـرحيب الخـاص {}  بنجـاح .. في هذه الدردشـه 𓆰**"
    if addwelcome_setting(event.chat_id, 0, string, msg_id) is True:
        return await edit_or_reply(event, success.format("تم حفظـه"))
    rmwelcome_setting(event.chat_id)
    if addwelcome_setting(event.chat_id, 0, string, msg_id) is True:
        return await edit_or_reply(event, success.format("تم تحديثـه"))
    await edit_or_reply("**- خطأ .. لا يسمح بوضع ترحيب خـاص بهذه الدردشـه**")


@zedub.zed_cmd(
    pattern="حذف رحب$",
    command=("حذف رحب", plugin_category),
    info={
        "header": "To turn off private welcome message.",
        "description": "Deletes the private welcome note for the current chat.",
        "usage": "{tr}clearpwel",
    },
)
async def del_welcome(event):
    "To turn off private welcome message"
    if rmwelcome_setting(event.chat_id) is True:
        await edit_or_reply(event, "**⪼ تم حذف تـرحيب الخـاص في هذه الدردشـه 𓆰**")
    else:
        await edit_or_reply(event, "**⪼ انت لا تمتلك تـرحيب الخـاص لــ هذه الدردشـه 𓆰**")


@zedub.zed_cmd(
    pattern="قائمه رحب$",
    command=("قائمه رحب", plugin_category),
    info={
        "header": "To check current private welcome message in group.",
        "usage": "{tr}listpwel",
    },
)
async def show_welcome(event):
    "To show current private welcome message in group"
    cws = getcurrent_welcome_settings(event.chat_id)
    if not cws:
        await edit_or_reply(event, "**⪼ لا يوجد ترحـيب خاص بهـذه الدردشـه 𓆰**")
        return
    if cws.f_mesg_id:
        msg_o = await event.client.get_messages(
            entity=BOTLOG_CHATID, ids=int(cws.f_mesg_id)
        )
        await edit_or_reply(
            event, "**⪼ انا ارحب بالاعضاء الجدد في هذه الدردشه بالخاص باستخدام هذا الترحيب 𓆰**"
        )
        await event.reply(msg_o.message, file=msg_o.media)
    elif cws.reply:
        await edit_or_reply(
            event, "**⪼ انا ارحب بالاعضاء الجدد في هذه الدردشه بالخاص باستخدام هذا الترحيب 𓆰**"
        )
        await event.reply(cws.reply, link_preview=False)
