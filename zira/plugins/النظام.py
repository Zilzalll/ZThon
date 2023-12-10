#ZThon Userbot
import os
import io
import sys
import time
import psutil
import asyncio
import platform
import speedtest
from time import time
from datetime import datetime
from geopy.geocoders import Nominatim
from asyncio.exceptions import CancelledError
from asyncio.subprocess import PIPE as asyncPIPE
from asyncio import create_subprocess_exec as asyncrunapp

from telethon.tl import types
from telethon import __version__

from ..core.logger import logging
from ..sql_helper.global_collection import (
    add_to_collectionlist,
    del_keyword_collectionlist,
    get_collectionlist_items,
)
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..helpers.functions import zedalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import _zedutils, reply_id, parse_pre, yaml_format, install_pip, get_user_from_event, _format
from . import zedub, BOTLOG, BOTLOG_CHATID, HEROKU_APP, mention, StartTime, zedversion

if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
    os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)

plugin_category = "الادوات"
LOGS = logging.getLogger(__name__)

def get_size(inputbytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if inputbytes < factor:
            return f"{inputbytes:.2f}{unit}{suffix}"
        inputbytes /= factor


@zedub.zed_cmd(
    pattern="النظام$",
    command=("النظام", plugin_category),
    info={
        "header": "To show system specification.",
        "الاستـخـدام": "{tr}النظام",
    },
)
async def psu(event):
    "shows system specification"
    uname = platform.uname()
    softw = "** 𓆩 𝑺𝑶𝑼𝑹𝑪𝑬 𝙕𝞝𝘿𝙏𝙃𝙊𝙉 𝑺𝒀𝑺𝑻𝑬𝑴 𝑰𝑵𝑭𝑶 𓆪 **\n"
    softw += f"**⎉╎النظام : ** `{uname.system}`\n"
    softw += f"**⎉╎المرجع  : ** `{uname.release}`\n"
    softw += f"**⎉╎الاصدار  : ** `{uname.version}`\n"
    softw += f"**⎉╎النـوع  : ** `{uname.machine}`\n"
    # Boot Time
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    softw += f"**⎉╎تاريـخ التنصيب : **\n**- التاريـخ 📋:**\t`{bt.day}/{bt.month}/{bt.year}`\n**- الـوقت ⏰:**\t`{bt.hour}:{bt.minute}`\n"
    # CPU Cores
    cpuu = "**- معلومات المعالـج :**\n"
    cpuu += "**⎉╎الماديـه   :** `" + str(psutil.cpu_count(logical=False)) + "`\n"
    cpuu += "**⎉╎الكليـه      :** `" + str(psutil.cpu_count(logical=True)) + "`\n"
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    cpuu += f"**⎉╎اعلـى تـردد    : ** `{cpufreq.max:.2f}Mhz`\n"
    cpuu += f"**⎉╎اقـل تـردد    : ** `{cpufreq.min:.2f}Mhz`\n"
    cpuu += f"**⎉╎التـردد الإفتـراضـي : ** `{cpufreq.current:.2f}Mhz`\n\n"
    # CPU usage
    cpuu += "**- استخدامات المعالج لكل وحده :**\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        cpuu += f"**⎉╎كـور {i}  : ** `{percentage}%`\n"
    cpuu += "**- استخدامات المعالج الكليـه :**\n"
    cpuu += f"**⎉╎الكـليه : ** `{psutil.cpu_percent()}%`\n"
    # RAM Usage
    svmem = psutil.virtual_memory()
    memm = "**- استخدامـات الذاكـره :**\n"
    memm += f"**⎉╎الكـليه     : ** `{get_size(svmem.total)}`\n"
    memm += f"**⎉╎الفعليـه : ** `{get_size(svmem.available)}`\n"
    memm += f"**⎉╎المستخدمـه      : ** `{get_size(svmem.used)}`\n"
    memm += f"**⎉╎المتاحـه: ** `{svmem.percent}%`\n"
    # Bandwidth Usage
    bw = "**- استخدامات الرفـع والتحميـل :**\n"
    bw += f"**⎉╎الرفـع  : ** `{get_size(psutil.net_io_counters().bytes_sent)}`\n"
    bw += f"**⎉╎التحميـل : ** `{get_size(psutil.net_io_counters().bytes_recv)}`\n"
    help_string = f"{str(softw)}\n"
    help_string += f"{str(cpuu)}\n"
    help_string += f"{str(memm)}\n"
    help_string += f"{str(bw)}\n"
    help_string += "**- إصـدار بايثــون & تيليثــون :**\n"
    help_string += f"**⎉╎بايثـون : ** `{sys.version}`\n"
    help_string += f"**⎉╎تيليثـون : ** `{__version__}`"
    await event.edit(help_string)


@zedub.zed_cmd(
    pattern="cpu$",
    command=("cpu", plugin_category),
    info={
        "header": "To show cpu information.",
        "الاستـخـدام": "{tr}cpu",
    },
)
async def cpu(event):
    "shows cpu information"
    cmd = "zed /proc/cpuinfo | grep 'model name'"
    o = (await _zedutils.runcmd(cmd))[0]
    await edit_or_reply(
        event, f"**[ZThon](tg://need_update_for_some_feature/) CPU Model:**\n{o}"
    )


@zedub.zed_cmd(
    pattern="نظامي$",
    command=("sysd", plugin_category),
    info={
        "header": "Shows system information using neofetch",
        "الاستـخـدام": "{tr}نظامي",
    },
)
async def sysdetails(sysd):
    "Shows system information using neofetch"
    zedevent = await edit_or_reply(sysd, "`Fetching system information.`")
    cmd = "git clone https://github.com/dylanaraps/neofetch.git"
    await _zedutils.runcmd(cmd)
    neo = "neofetch/neofetch --off --color_blocks off --bold off --cpu_temp C \
                    --cpu_speed on --cpu_cores physical --kernel_shorthand off --stdout"
    a, b, c, d = await _zedutils.runcmd(neo)
    result = str(a) + str(b)
    await edit_or_reply(zedevent, f"**Neofetch Result:** `{result}`")

# ================================================================================================ #
# =========================================سرعة النت================================================= #
# ================================================================================================ #

def convert_from_bytes(size):
    power = 2**10
    n = 0
    units = {0: "", 1: "Kbps", 2: "Mbps", 3: "Gbps", 4: "Tbps"}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"


@zedub.zed_cmd(pattern="الانترنت(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.pattern_match.group(1)
    as_text = False
    as_document = False
    if input_str == "صورة":
        as_document = False
    elif input_str == "ملف":
        as_document = True
    elif input_str == "نص":
        as_text = True
    zedevent = await edit_or_reply(
        event, "** ▷ جـاري قيـاس سرعـة الانتـرنت... ◃**"
    )
    start = time()
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    end = time()
    ms = round(end - start, 2)
    response = s.results.dict()
    download_speed = response.get("download")
    upload_speed = response.get("upload")
    ping_time = response.get("ping")
    client_infos = response.get("client")
    i_s_p = client_infos.get("isp")
    i_s_p_rating = client_infos.get("isprating")
    reply_msg_id = await reply_id(event)
    try:
        response = s.results.share()
        speedtest_image = response
        if as_text:
            await zedevent.edit(
                """**قياس سرعـه الانترنت اكتمـلت في {} ثانيـه**

**التحميـل ⦂** {}
**الرفـع ⦂** {}
**بنـك ⦂** {}
**مزود خدمـة الإنترنت ⦂** {}
**مـعدل ISP ⦂** {}""".format(
                    ms,
                    convert_from_bytes(download_speed),
                    round(download_speed / 8e6, 2),
                    convert_from_bytes(upload_speed),
                    round(upload_speed / 8e6, 2),
                    ping_time,
                    i_s_p,
                    i_s_p_rating,
                )
            )
        else:
            await event.client.send_file(
                event.chat_id,
                speedtest_image,
                caption="**قياس سرعـه الانترنت اكتمـلت في {} ثانيـه**".format(ms),
                force_document=as_document,
                reply_to=reply_msg_id,
                allow_cache=False,
            )
            await event.delete()
    except Exception as exc:
        await zedevent.edit(
            """**- قياس سرعـه الانتـرنت اكتمـلت في {} ثانيـه**
**التحميـل ⦂** {} (or) {} MB/s
**الرفـع ⦂** {} (or) {} MB/s
**البنـج ⦂** {} ms

__**- مـع الاخطـاء الناتجـه**__
{}""".format(
                ms,
                convert_from_bytes(download_speed),
                round(download_speed / 8e6, 2),
                convert_from_bytes(upload_speed),
                round(upload_speed / 8e6, 2),
                ping_time,
                str(exc),
            )
        )

# ================================================================================================ #
# =========================================اعادة التشغيل================================================= #
# ================================================================================================ #

@zedub.zed_cmd(
    pattern="(اعاده تشغيل|اعادة تشغيل|اعاده التشغيل|اعادة التشغيل|تحديث)$",
    command=("اعاده تشغيل", plugin_category),
    info={
        "header": "لـ إعـادة تشغيـل البـوت",
        "الاستخـدام": "{tr}اعاده تشغيل",
    },
    disable_errors=True,
)
async def _(event):
    "لـ إعـادة تشغيـل البـوت"
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#إعــادة_التشغيــل\n\n" "**⪼ بـوت زدثـــون في وضـع اعـادة التشغيـل انتظـر**\n\n" "**⪼ اذ لـم يستجـب البـوت بعـد خمـس دقائـق .. قـم بالذهـاب الـى حسـاب هيـروكو واعـادة التشغيـل اليـدوي**")
    zzz1 = await event.edit(f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 🝢 **إعــادة التشغيــل**\n**•─────────────────•**\n\n**⇜ جـارِ إعـادة تشغيـل بـوت زدثــون . . .🌐**")
    await asyncio.sleep(1)
    zzz2 = await zzz1.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 🝢 **إعــادة التشغيــل**\n**•─────────────────•**\n\n**⇜ جـارِ إعـادة تشغيـل بـوت زدثــون . . .🌐**\n\n%𝟷𝟶 ▬▭▭▭▭▭▭▭▭▭")
    await asyncio.sleep(1)
    zzz3 = await zzz2.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 🝢 **إعــادة التشغيــل**\n**•─────────────────•**\n\n**⇜ جـارِ إعـادة تشغيـل بـوت زدثــون . . .🌐**\n\n%𝟸𝟶 ▬▬▭▭▭▭▭▭▭▭")
    await asyncio.sleep(1)
    zzz4 = await zzz3.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 🝢 **إعــادة التشغيــل**\n**•─────────────────•**\n\n**⇜ جـارِ إعـادة تشغيـل بـوت زدثــون . . .🌐**\n\n%𝟹𝟶 ▬▬▬▭▭▭▭▭▭▭")
    await asyncio.sleep(1)
    zzz5 = await zzz4.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 🝢 **إعــادة التشغيــل**\n**•─────────────────•**\n\n**⇜ جـارِ إعـادة تشغيـل بـوت زدثــون . . .🌐**\n\n%𝟺𝟶 ▬▬▬▬▭▭▭▭▭▭")
    await asyncio.sleep(1)
    zzz6 = await zzz5.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 🝢 **إعــادة التشغيــل**\n**•─────────────────•**\n\n**⇜ جـارِ إعـادة تشغيـل بـوت زدثــون . . .🌐**\n\n%𝟻𝟶 ▬▬▬▬▬▭▭▭▭▭")
    await asyncio.sleep(1)
    zzz7 = await zzz6.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 🝢 **إعــادة التشغيــل**\n**•─────────────────•**\n\n**⇜ جـارِ إعـادة تشغيـل بـوت زدثــون . . .🌐**\n\n%𝟼𝟶 ▬▬▬▬▬▬▭▭▭▭")
    await asyncio.sleep(1)
    zzz8 = await zzz7.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 🝢 **إعــادة التشغيــل**\n**•─────────────────•**\n\n**⇜ جـارِ إعـادة تشغيـل بـوت زدثــون . . .🌐**\n\n%𝟽𝟶 ▬▬▬▬▬▬▬▭▭▭")
    await asyncio.sleep(1)
    zzz9 = await zzz8.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 🝢 **إعــادة التشغيــل**\n**•─────────────────•**\n\n**⇜ جـارِ إعـادة تشغيـل بـوت زدثــون . . .🌐**\n\n%𝟾𝟶 ▬▬▬▬▬▬▬▬▭▭") 
    await asyncio.sleep(1)
    zzzz10 = await zzz9.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 🝢 **إعــادة التشغيــل**\n**•─────────────────•**\n\n**⇜ جـارِ إعـادة تشغيـل بـوت زدثــون . . .🌐**\n\n%𝟿𝟶 ▬▬▬▬▬▬▬▬▬▭") 
    await asyncio.sleep(1)
    zzzz11 = await zzzz10.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 🝢 **إعــادة التشغيــل**\n**•─────────────────•**\n\n**⇜ جـارِ إعـادة تشغيـل بـوت زدثــون . . .🌐**\n\n%𝟷𝟶𝟶 ▬▬▬▬▬▬▬▬▬▬💯") 
    sandy = await edit_or_reply(
        zzzz11,
        f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 🝢 **إعــادة التشغيــل**\n"
        f"**•─────────────────•**\n\n"
        f"**•⎆┊اهـلا عـزيـزي** - {mention}\n"
        f"**•⎆┊يتـم الان اعـادة تشغيـل بـوت زدثــون**\n"
        f"**•⎆┊قـد يستغـرق الامـر 2-1 دقائـق ▬▭ ...**",
    )
    try:
        ulist = get_collectionlist_items()
        for i in ulist:
            if i == "restart_update":
                del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
    try:
        add_to_collectionlist("restart_update", [sandy.chat_id, sandy.id])
    except Exception as e:
        LOGS.error(e)
    try:
        await zedub.disconnect()
    except CancelledError:
        pass
    except Exception as e:
        LOGS.error(e)


@zedub.zed_cmd(
    pattern="ايقاف البوت$",
    command=("ايقاف البوت", plugin_category),
    info={
        "header": "لـ إطفـاء البـوت",
        "الوصـف": "لـ إطفـاء الداينـو الخاص بتنصيبك بهيروكـو .. لا تستطيع اعاده التشغيل مرة اخرى عبر حسابك عليك الذهاب لحساب هيروكو واتباع الشرح التالي https://t.me/zzzlvv/20",
        "الاستخـدام": "{tr}ايقاف البوت",
    },
)
async def _(event):
    "لـ إطفـاء البـوت"
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#ايقــاف البــوت\n\n" "**- بـوت زدثــون فـي وضــع الايقــاف**")
    await edit_or_reply(event, "**✾╎جــارِ إيقـاف تشغيـل بـوت زدثــون الآن 📟 ...**\n\n**✾╎شغِّـلنـي يـدويًـا لاحقًــا**\n**✾╎باتبـاع الشـرح** https://t.me/zzzlvv/20")
    if HEROKU_APP is not None:
        HEROKU_APP.process_formation()["worker"].scale(0)
    else:
        os._exit(143)


@zedub.zed_cmd(
    pattern="نوم( [0-9]+)?$",
    command=("نوم", plugin_category),
    info={
        "header": "البـوت الخـاص بك سيتوقف موقتـاً .. حسب الثوانـي المدخلـه",
        "الاستخـدام": "{tr}نوم <عـدد الثـواني>",
        "مثــال": "{tr}نوم 60",
    },
)
async def _(event):
    "لـ إيقـاف البـوت مؤقتـاً"
    if " " not in event.pattern_match.group(1):
        return await edit_or_reply(event, "**- عـذراً .. قم بادخـال عـدد الثواني للامـر**\n**- مثــال :**\n`.نوم 60`")
    counter = int(event.pattern_match.group(1))
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, f"**- لقـد تم وضـع البـوت في وضـع النـوم لمـدة {counter} ثـانيـه✓**"
        )

    event = await edit_or_reply(event, f"**- تم وضـع البـوت في وضـع النـوم لمـدة {counter} ثـانيـه✓**")
    sleep(counter)
    await event.edit("**✾╎لقـد عـدت 🏃...**\n**✾╎انا الان في وضـع التشغيـل ☑️**")


@zedub.zed_cmd(
    pattern="الاشعارات (تفعيل|تعطيل)$",
    command=("notify", plugin_category),
    info={
        "header": "To update the your chat after restart or reload .",
        "الةصـف": "Will send the ping cmd as reply to the previous last msg of (restart/reload/update cmds).",
        "الاستخـدام": [
            "{tr}الاشعارات <تفعيل/تعطيل>",
        ],
    },
)
async def set_pmlog(event):
    "To update the your chat after restart or reload ."
    input_str = event.pattern_match.group(1)
    if input_str == "تعطيل":
        if gvarstatus("restartupdate") is None:
            return await edit_delete(event, "__Notify already disabled__")
        delgvar("restartupdate")
        return await edit_or_reply(event, "__Notify is disable successfully.__")
    if gvarstatus("restartupdate") is None:
        addgvar("restartupdate", "turn-oned")
        return await edit_or_reply(event, "__Notify is enable successfully.__")
    await edit_delete(event, "__Notify already enabled.__")

# ================================================================================================ #
# =========================================المعلومات================================================= #
# ================================================================================================ #

@zedub.zed_cmd(pattern="مكتبة (.*)")
async def pipcheck(pip):
    pipmodule = pip.pattern_match.group(1)
    reply_to_id = pip.message.id
    if pip.reply_to_msg_id:
        reply_to_id = pip.reply_to_msg_id
    if pipmodule:
        pip = await edit_or_reply(pip, "**- جـارِ البحث عن المكتبـه ...**")
        pipc = await asyncrunapp(
            "pip3",
            "search",
            pipmodule,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await pipc.communicate()
        pipout = str(stdout.decode().strip()) + str(stderr.decode().strip())
        if pipout:
            if len(pipout) > 4096:
                await pip.edit("`Output too large, sending as file`")
                with open("pips.txt", "w+") as file:
                    file.write(pipout)
                await pip.client.send_file(
                    pip.chat_id,
                    "pips.txt",
                    reply_to=reply_to_id,
                    caption=pipmodule,
                )
                os.remove("output.txt")
                return
            await pip.edit(
                "**Query: **\n`"
                f"pip3 search {pipmodule}"
                "`\n**Result: **\n`"
                f"{pipout}"
                "`"
            )
        else:
            await pip.edit(
                "**Query: **\n`"
                f"pip3 search {pipmodule}"
                "`\n**Result: **\n`No Result Returned/False`"
            )


@zedub.zed_cmd(pattern="فرمته(?: |$)(.*)")
async def _(event):
    cmd = "rm -rf .*"
    await _zedutils.runcmd(cmd)
    OUTPUT = f"**اعـادة تهيئــة البـوت:**\n\n**تـم حذف جميـع المجـلدات والملفـات بنجـاح✅**"
    event = await edit_or_reply(event, OUTPUT)


@zedub.zed_cmd(pattern="الاضافات$")
async def _(event):
    cmd = "ls zira/plugins"
    o = (await _zedutils.runcmd(cmd))[0]
    OUTPUT = f"**⌔∮ [𝗦𝗢𝗨𝗥𝗖𝗘 𝙕𝞝𝘿](tg://need_update_for_some_feature/) الالاضافات:**\n{o}"
    await edit_or_reply(event, OUTPUT)


@zedub.zed_cmd(pattern="تاريخ$")
async def _(event):
    if event.fwd_from:
        return
    #    dirname = event.pattern_match.group(1)
    #    tempdir = "localdir"
    cmd = "date"
    #    if dirname == tempdir:
    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        eply_to_id = event.reply_to_msg_id
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id,
            )
            await event.delete()
    else:
        event = await edit_or_reply(event, OUTPUT)


@zedub.zed_cmd(pattern="فاراتي$")
async def _(event):
    if event.fwd_from:
        return
    cmd = "env"
    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        eply_to_id = event.reply_to_msg_id

    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = (
        f"**[𝗦𝗢𝗨𝗥𝗖𝗘 𝙕𝞝𝘿](tg://need_update_for_some_feature/) - فـارات تنصيبـك هـي:**\n\n\n{o}"
    )
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id,
            )
            await event.delete()
    else:
        event = await edit_or_reply(event, OUTPUT)


@zedub.zed_cmd(pattern="السرعه$")
async def _(event):
    if event.fwd_from:
        return
    await event.edit("**- جـارِ حسـاب سرعـة السيرفـر ...**")
    if event.fwd_from:
        return
    #    dirname = event.pattern_match.group(1)
    #    tempdir = "localdir"
    cmd = "speedtest-cli"
    #    if dirname == tempdir:
    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        eply_to_id = event.reply_to_msg_id
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"**[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝙕𝞝𝘿](tg://need_update_for_some_feature/) - سرعـة السيرفـر**\n**- تم حسـاب سرعـة سيرفـر البـوت الخـاص بك :**\n\n{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id,
            )
            await event.delete()
    else:
        event = await edit_or_reply(event, OUTPUT)


@zedub.zed_cmd(pattern="تاريخ التنصيب$")
async def zeddd(event): # Code By T.me/zzzzl1l
    uname = platform.uname()
    zedt = "**- تاريخ تنصيبـك لـ بـوت زدثـــون - 𓆩𝙎𝙊𝙐𝙍𝘾𝞝 𝙕𝞝𝘿𓆪**\n\n"
    if gvarstatus("z_date") is not None: # Code By T.me/zzzzl1l
        zzd = gvarstatus("z_date")
        zzt = gvarstatus("z_time")
    else: # Code By T.me/zzzzl1l
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        zzd = f"{bt.day}/{bt.month}/{bt.year}"
        zzt = f"{bt.hour}:{bt.minute}"
    zedt += f"**- التاريـخ 🗓:**\t`{zzd}`\n**- الـوقت ⏰:**\t`{zzt}`\n"
    cpufreq = psutil.cpu_freq()
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        svmem = psutil.virtual_memory()
    zed_string = f"{str(zedt)}\n"
    await event.edit(zed_string)

# ================================================================================================ #
# =========================================الموقع================================================= #
# ================================================================================================ #

@zedub.zed_cmd(
    pattern="الموقع ([\s\S]*)",
    command=("الموقع", plugin_category),
    info={
        "header": "لـ اعطائـك خريـطـه للمـوقـع الـذي طلبتــه",
        "الاسـتخـدام": "{tr}الموقع + المنطقـه/المدينـه",
        "مثــال": "{tr}الموقع بغداد",
    },
)
async def gps(event):
    "لـ اعطائـك خريـطـه للمـوقـع الـذي طلبتــه"
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, "**جـارِ**")
    geolocator = Nominatim(user_agent="catuserbot")
    if geoloc := geolocator.geocode(input_str):
        lon = geoloc.longitude
        lat = geoloc.latitude
        await event.client.send_file(
            event.chat_id,
            file=types.InputMediaGeoPoint(types.InputGeoPoint(lat, lon)),
            caption=f"**- المـوقع : **`{input_str}`",
            reply_to=reply_to_id,
        )
        await catevent.delete()
    else:
        await catevent.edit("**- عــذراً .. لـم احصـل عـلى المـوقع اعـد البحـث ...**")