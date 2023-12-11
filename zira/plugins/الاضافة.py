from telethon.tl.types import Channel, Chat, User
from telethon.tl import functions, types
from telethon.tl.functions.messages import  CheckChatInviteRequest, GetFullChatRequest
from telethon.errors import (ChannelInvalidError, ChannelPrivateError, ChannelPublicGroupNaError, InviteHashEmptyError, InviteHashExpiredError, InviteHashInvalidError)
from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantsRequest, InviteToChannelRequest
from zira import *
from zira import zedub
from zira.utils import admin_cmd
from ..core.managers import edit_delete, edit_or_reply


async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await event.reply("**⎉╎لم يتم العثور على المجموعة او القناة**")
            return None
        except ChannelPrivateError:
            await event.reply("**⎉╎لا يمكنني استخدام الامر من الكروبات او القنوات الخاصة**")
            return None
        except ChannelPublicGroupNaError:
            await event.reply("**⎉╎لم يتم العثور على المجموعة او القناة**")
            return None
        except (TypeError, ValueError) as err:
            await event.reply("**⎉╎رابط الكروب غير صحيح**")
            return None
    return chat_info


def make_mention(user):
    if user.username:
        return f"@{user.username}"
    else:
        return inline_mention(user)


def inline_mention(user):
    full_name = user_full_name(user) or "No Name"
    return f"[{full_name}](tg://user?id={user.id})"


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    full_name = ' '.join(names)
    return full_name


@zedub.zed_cmd(pattern="انضم ([\s\S]*)")
async def lol(event):
    a = event.text
    bol = a[6:]
    sweetie = "- جـارِ الانضمـام الـى الرابـط انتظـر قليـلاً . . ."
    zzz = await event.reply(sweetie, parse_mode=None, link_preview=None)
    try:
        await zedub(functions.channels.JoinChannelRequest(bol))
        await zzz.edit("**- تم الانضمـام .. بنجـاح  ✓**")
    except Exception as e:
        await zzz.edit(str(e))


@zedub.zed_cmd(pattern="غادر ([\s\S]*)")
async def lol(event):
    a = event.text
    bol = a[6:]
    sweetie = "- جـارِ المغـادرة مـن القنـاة . . ."
    zzz = await event.reply(sweetie, parse_mode=None, link_preview=None)
    try:
        await zedub(functions.channels.LeaveChannelRequest(bol))
        await zzz.edit("**- تم المغـادرة .. بنجـاح  ✓**")
    except Exception as e:
        await zzz.edit(str(e))


@zedub.zed_cmd(pattern="اضافه ([\s\S]*)")
async def _(event):
    to_add_users = event.pattern_match.group(1)
    if not event.is_channel and event.is_group:
        for user_id in to_add_users.split(" "):
            try:
                await event.client(
                    functions.messages.AddChatUserRequest(
                        chat_id=event.chat_id, user_id=user_id, fwd_limit=1000000
                    )
                )
            except Exception as e:
                return await edit_delete(event, f"`{str(e)}`", 5)
    else:
        for user_id in to_add_users.split(" "):
            try:
                await event.client(
                    functions.channels.InviteToChannelRequest(
                        channel=event.chat_id, users=[user_id]
                    )
                )
            except Exception as e:
                return await edit_delete(event, f"`{e}`", 5)

    await edit_or_reply(event, f"**{to_add_users} تم اضافته بنجاح ✓**")
