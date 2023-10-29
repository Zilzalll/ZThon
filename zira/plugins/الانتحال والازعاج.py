import html

from telethon.tl import functions
from telethon.tl.functions.users import GetFullUserRequest

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import gvarstatus
from ..sql_helper.echo_sql import (
    addecho,
    get_all_echos,
    get_echos,
    is_echo,
    remove_all_echos,
    remove_echo,
    remove_echos,
)
from . import ALIVE_NAME, BOTLOG, BOTLOG_CHATID, zedub, edit_delete, get_user_from_event

plugin_category = "العروض"
ANTHAL = gvarstatus("ANTHAL") or "(اعادة الحساب|اعادة|اعاده)"


@zedub.zed_cmd(pattern="انتحال(?:\s|$)([\s\S]*)")
async def _(event):
    replied_user, error_i_a = await get_user_from_event(event)
    if replied_user is None:
        return
    user_id = replied_user.id
    profile_pic = await event.client.download_profile_photo(user_id, Config.TEMP_DIR)
    first_name = html.escape(replied_user.first_name)
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.last_name
    if last_name is not None:
        last_name = html.escape(last_name)
        last_name = last_name.replace("\u2060", "")
    if last_name is None:
        last_name = "⁪⁬⁮⁮⁮⁮ ‌‌‌‌"
    replied_user = (await event.client(GetFullUserRequest(replied_user.id))).full_user
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = replied_user.about
    await event.client(functions.account.UpdateProfileRequest(first_name=first_name))
    await event.client(functions.account.UpdateProfileRequest(last_name=last_name))
    await event.client(functions.account.UpdateProfileRequest(about=user_bio))
    try:
        pfile = await event.client.upload_file(profile_pic)
    except Exception as e:
        return await edit_delete(event, f"**اووبس خطـأ بالانتحـال:**\n__{e}__")
    await event.client(functions.photos.UploadProfilePhotoRequest(pfile))
    await edit_delete(event, "**⎉╎تـم انتحـال الشخـص .. بنجـاح ༗**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#الانتحـــال\n ⪼ تم انتحـال حسـاب الشخـص ↫ [{first_name}](tg://user?id={user_id }) بنجاح ✅",
        )


@zedub.zed_cmd(pattern=f"{ANTHAL}$")
async def revert(event):
    firstname = gvarstatus("FIRST_NAME") or ALIVE_NAME
    lastname = gvarstatus("LAST_NAME") or ""
    bio = gvarstatus("DEFAULT_BIO") or "{وَتَوَكَّلْ عَلَى اللَّهِ ۚ وَكَفَىٰ بِاللَّهِ وَكِيلًا}"
    await event.client(
        functions.photos.DeletePhotosRequest(
            await event.client.get_profile_photos("me", limit=1)
        )
    )
    await event.client(functions.account.UpdateProfileRequest(about=bio))
    await event.client(functions.account.UpdateProfileRequest(first_name=firstname))
    await event.client(functions.account.UpdateProfileRequest(last_name=lastname))
    await edit_delete(event, "**⎉╎تمت اعادة الحساب لوضعـه الاصلـي \n⎉╎والغـاء الانتحـال .. بنجـاح ✅**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#الغـاء_الانتحـال\n**⪼ تم الغـاء الانتحـال .. بنجـاح ✅**\n**⪼ تم إعـاده معلـوماتك الى وضعـها الاصـلي**",
        )

# ================================================================================================ #
# =========================================الازعاج================================================= #
# ================================================================================================ #

@zedub.zed_cmd(pattern="(تقليد|ازعاج)$")
async def echo(event):
    if event.reply_to_msg_id is None:
        return await edit_or_reply(event, "**- بالـرد على الشخص الذي تريد ازعاجـه**")
    zedubevent = await edit_or_reply(event, "**- يتم تفعيل هذا الامر انتظر قليلا ..**")
    user, rank = await get_user_from_event(event, zedubevent, nogroup=True)
    if not user:
        return
    reply_msg = await event.get_reply_message()
    chat_id = event.chat_id
    user_id = reply_msg.sender_id
    if event.is_private:
        chat_name = user.first_name
        chat_type = "Personal"
    else:
        chat_name = event.chat.title
        chat_type = "Group"
    user_name = user.first_name
    user_username = user.username
    if is_echo(chat_id, user_id):
        return await edit_or_reply(event, "**⎉╎تم تفعيل الازعاج على الشخص .. بنجاح✓**")
    try:
        addecho(chat_id, user_id, chat_name, user_name, user_username, chat_type)
    except Exception as e:
        await edit_delete(zedubevent, f"**⎉╎خطـأ :**\n`{str(e)}`")
    else:
        await edit_or_reply(
            zedubevent,
            "**- تم تفعيل امر التقليد على هذا الشخص\nسيتم تقليد جميع رسائله هنا**",
        )

@zedub.zed_cmd(pattern="(الغاء تقليد|ايقاف التقليد|ايقاف تقليد|الغاء الازعاج|ايقاف الازعاج|ايقاف ازعاج|الغاء ازعاج)$")
async def echo(event):
    if event.reply_to_msg_id is None:
        return await edit_or_reply(event, "**- بالـرد على الشخص الذي قمت بـ ازعاجـه لايقاف الازعاج**\n**- ارسـل (.المقلدهم) لعـرض الاشخـاص الذي قمت بازعاجهم**")
    reply_msg = await event.get_reply_message()
    user_id = reply_msg.sender_id
    chat_id = event.chat_id
    if is_echo(chat_id, user_id):
        try:
            remove_echo(chat_id, user_id)
        except Exception as e:
            await edit_delete(zedubevent, f"**⎉╎خطـأ :**\n`{e}`")
        else:
            await edit_or_reply(event, "**⎉╎تم ايقاف التقليد لهذا المستخدم**")
    else:
        await edit_or_reply(event, "**- لم يتم تفعيل التقليد على هذا المستخدم اصلا**")


@zedub.zed_cmd(pattern="حذف المقلدهم( للكل)?")
async def echo(event):
    input_str = event.pattern_match.group(1)
    if input_str:
        lecho = get_all_echos()
        if len(lecho) == 0:
            return await edit_delete(
                event, "**- لم يتم تفعيل التقليد حتى لمستخدم واحد اصلا.**"
            )
        try:
            remove_all_echos()
        except Exception as e:
            await edit_delete(event, f"**⎉╎خطـأ :**\n`{str(e)}`", 10)
        else:
            await edit_or_reply(
                event, "**⎉╎تم حذف تقليد جميع المستخدمين في جميع الدردشات.**"
            )
    else:
        lecho = get_echos(event.chat_id)
        if len(lecho) == 0:
            return await edit_delete(
                event, "**- لم يتم تفعيل التقليد حتى لمستخدم واحد اصلا.**"
            )
        try:
            remove_echos(event.chat_id)
        except Exception as e:
            await edit_delete(event, f"**⎉╎خطـأ :**\n`{e}`", 10)
        else:
            await edit_or_reply(
                event, "**⎉╎تم حذف تقليد جميع المستخدمين في جميع الدردشات.**"
            )


@zedub.zed_cmd(pattern="المقلدهم( للكل)?$")
async def echo(event):
    input_str = event.pattern_match.group(1)
    private_chats = ""
    output_str = "**⎉╎قائمـة الاشخـاص المقلـدهـم:\n\n**"
    if input_str:
        lsts = get_all_echos()
        group_chats = ""
        if len(lsts) <= 0:
            return await edit_or_reply(event, "**- لم يتم تفعيل التقليد بالاصل ؟!**")
        for echos in lsts:
            if echos.chat_type == "Personal":
                if echos.user_username:
                    private_chats += (
                        f"⪼ [{echos.user_name}](https://t.me/{echos.user_username})\n"
                    )
                else:
                    private_chats += (
                        f"⪼ [{echos.user_name}](tg://user?id={echos.user_id})\n"
                    )
            elif echos.user_username:
                group_chats += f"⪼ [{echos.user_name}](https://t.me/{echos.user_username}) في دردشة {echos.chat_name} الايدي `{echos.chat_id}`\n"
            else:
                group_chats += f"⪼ [{echos.user_name}](tg://user?id={echos.user_id}) في دردشة {echos.chat_name} الايدي `{echos.chat_id}`\n"

        if private_chats != "":
            output_str += "**الدردشات الخاصة**\n" + private_chats + "\n\n"
        if group_chats != "":
            output_str += "**المجموعات**\n" + group_chats
    else:
        lsts = get_echos(event.chat_id)
        if len(lsts) <= 0:
            return await edit_or_reply(event, "**لم يتم تفعيل التقليد بالاصل**")

        for echos in lsts:
            if echos.user_username:
                private_chats += (
                    f"⪼ [{echos.user_name}](https://t.me/{echos.user_username})\n"
                )
            else:
                private_chats += (
                    f"⪼ [{echos.user_name}](tg://user?id={echos.user_id})\n"
                )
        output_str = "**⎉╎الاشخـاص المقلـدهـم في هذه الدردشـه :\n**" + private_chats

    await edit_or_reply(event, output_str)


@zedub.zed_cmd(incoming=True, edited=False)
async def samereply(event):
    if is_echo(event.chat_id, event.sender_id) and (
        event.message.text or event.message.sticker
    ):
        await event.reply(event.message)
