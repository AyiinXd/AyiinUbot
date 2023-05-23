# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

import platform
import re
import socket
import uuid
import psutil

from asyncio import gather
from os import remove
from time import sleep

from fipper import Client
from fipper.enums import ChatType
from fipper.types import Message

from pyAyiin import Ayiin, CMD_HELP
from pyAyiin.pyrogram import eor

from . import *


@Ayiin(["cinfo", "chatinfo", "ginfo"])
async def chatinfo_handler(client: Client, message: Message):
    Ayiin = await eor(message, "<i>Processing...</i>")
    try:
        if len(message.command) > 1:
            chat_u = message.command[1]
            chat = await client.get_chat(chat_u)
        else:
            if message.chat.type == ChatType.PRIVATE:
                return await message.edit(
                    f"Gunakan perintah ini di dalam grup atau gunakan <code>^chatinfo [group username atau id]</code>"
                )
            else:
                chatid = message.chat.id
                chat = await client.get_chat(chatid)
        h = f"{chat.type}"
        if h.startswith("ChatType"):
            y = h.replace("ChatType.", "")
            type = y.capitalize()
        else:
            type = "Private"
        username = f"@{chat.username}" if chat.username else "-"
        description = f"{chat.description}" if chat.description else "-"
        dc_id = f"{chat.dc_id}" if chat.dc_id else "-"
        out_str = f"""
<b>❯❯ CHAT INFORMATION ❮❮</b>

🆔 <b>Chat ID:</b> <code>{chat.id}</code>
👥 <b>Title:</b> {chat.title}
👥 <b>Username:</b> {username}
📩 <b>Type:</b> <code>{type}</code>
🏛️ <b>DC ID:</b> <code>{dc_id}</code>
🗣️ <b>Is Scam:</b> <code>{chat.is_scam}</code>
🎭 <b>Is Fake:</b> <code>{chat.is_fake}</code>
✅ <b>Verified:</b> <code>{chat.is_verified}</code>
🚫 <b>Restricted:</b> <code>{chat.is_restricted}</code>
🔰 <b>Protected:</b> <code>{chat.has_protected_content}</code>
🚻 <b>Total members:</b> <code>{chat.members_count}</code>
📝 <b>Description:</b>
<code>{description}</code>
"""
        photo_id = chat.photo.big_file_id if chat.photo else None
        if photo_id:
            photo = await client.download_media(photo_id)
            await gather(
                Ayiin.delete(),
                client.send_photo(
                    message.chat.id,
                    photo,
                    caption=out_str,
                    reply_to_message_id=yins.ReplyCheck(message),
                ),
            )
            remove(photo)
        else:
            await Ayiin.edit(out_str, disable_web_page_preview=True)
    except Exception as e:
        return await Ayiin.edit(f"<b>INFO:</b> <code>{e}</code>")


@Ayiin(["limit", "lmt"])
async def spamban(client: Client, m: Message):
    '''
    ========================×========================
            Copyright (C) 2023-present AyiinXd
    ========================×========================
    '''
    msg = await eor(m, "<i>Process...</i>")
    boti = "@SpamBot"
    await client.unblock_user(boti)
    await client.send_message(boti, "/start")
    sleep(1)
    async for xx in client.search_messages(boti, limit=1):
        if xx:
            await msg.edit_text(f"❯❯ Status Limit ❮❮\n\n{xx.text}")


@Ayiin(["sys", "system"])
async def system_stats(client, message):
    splatform = platform.system()
    platform_release = platform.release()
    platform_version = platform.version()
    architecture = platform.machine()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(socket.gethostname())
    mac_address = ":".join(re.findall("..", "%012x" % uuid.getnode()))
    processor = platform.processor()
    ram = yins.humanbytes(round(psutil.virtual_memory().total))
    cpu_freq = psutil.cpu_freq().current
    if cpu_freq >= 1000:
        cpu_freq = f"{round(cpu_freq / 1000, 2)}GHz"
    else:
        cpu_freq = f"{round(cpu_freq, 2)}MHz"
    du = psutil.disk_usage(client.workdir)
    psutil.disk_io_counters()
    disk = f"{yins.humanbytes(du.used)} / {yins.humanbytes(du.total)} " f"({du.percent}%)"
    cpu_len = len(psutil.Process().cpu_affinity())
    neat_msg = f"""❯❯ <b>System Info</b> ❮❮
    
<b>PlatForm :</b> <code>{splatform}</code>
<b>PlatForm - Release :</b> <code>{platform_release}</code>
<b>PlatFork - Version :</b> <code>{platform_version}</code>
<b>Architecture :</b> <code>{architecture}</code>
<b>Hostname :</b> <code>{hostname}</code>
<b>IP :</b> <code>{ip_address}</code>
<b>Mac :</b> <code>{mac_address}</code>
<b>Processor :</b> <code>{processor}</code>
<b>Ram :</b> <code>{ram}</code>
<b>CPU :</b> <code>{cpu_len}</code>
<b>CPU FREQ :</b> <code>{cpu_freq}</code>
<b>DISK :</b> <code>{disk}</code>
    """
    await message.reply(neat_msg)


CMD_HELP.update(
    {"tools": (
        "tools",
        {
            "cinfo": "Dapatkan info group dengan deskripsi lengkap.",
            "info": "Dapatkan info pengguna telegram dengan deskripsi lengkap.",
            "id": "Dapatkan Id Pengguna",
            "limit": "Check Limit telegram dari @SpamBot.",
            "sys": "Gunakan Ini Untuk Mengecek System Ubot Anda",
        }
        )
    }
)
