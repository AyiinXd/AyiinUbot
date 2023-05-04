# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-UserBot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-UserBot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio

from fipper import Client, enums
from fipper.errors import FloodWait
from fipper.types import Message

from pyAyiin import Ayiin, CMD_HELP, DEVS, GCAST_BLACKLIST
from pyAyiin.pyrogram import eor

from . import yins



@Ayiin(["fgcast", "fw_cast"])
async def gcast_cmd(client: Client, message: Message):
    if message.reply_to_message:
        AyiinXD = await message.reply("<code>Started global broadcast...</code>")
    else:
        return await message.edit_text("<b>Berikan Sebuah Pesan atau Reply</b>")
    x = message.reply_to_message.id
    y = message.chat.id
    done = 0
    error = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in [
                enums.ChatType.GROUP,
                enums.ChatType.SUPERGROUP]:
            chat = dialog.chat.id
            if chat not in GCAST_BLACKLIST:
                try:
                    await client.forward_messages(chat, y, x)
                    done += 1
                except FloodWait as e:
                    f_t = int(e.value)
                    if f_t > 200:
                        continue
                    await asyncio.sleep(f_t)
                    await client.forward_messages(chat, y, x)
                    done += 1
                except Exception:
                    error += 1
                    await asyncio.sleep(0.3)
    await AyiinXD.edit_text(
        f"<b>Berhasil Menyebarkan Gosip Terusan...\n\nBerhasil Ke</b> <code>{done}</code> <b>Grup\nGagal Ke</b> <code>{error}</code> <b>Grup</b>"
    )


@Ayiin(["gcast", "broadcast"])
async def gcast_cmd(client: Client, message: Message):
    if message.reply_to_message:
        AyiinXD = await eor(message, "<code>Started global broadcast...</code>")
    else:
        return await message.edit_text("<b>Balas Ke Pesan Untuk Menyebarkan Gosipan Anda</b>")
    x = message.reply_to_message.id
    y = message.chat.id
    done = 0
    error = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in [
                enums.ChatType.GROUP,
                enums.ChatType.SUPERGROUP]:
            chat = dialog.chat.id
            if chat not in GCAST_BLACKLIST:
                try:
                    await client.copy_message(chat, y, x)
                    await asyncio.sleep(0.1)
                    done += 1
                except FloodWait as e:
                    f_t = int(e.value)
                    if f_t > 200:
                        continue
                    await asyncio.sleep(f_t)
                    await client.copy_message(chat, y, x)
                    done += 1
                except BaseException:
                    error += 1
    await AyiinXD.edit_text(
        f"<b>Status Penyebaran Gosip...\n\nBerhasil Ke</b> <code>{done}</code> <b>Grup\nGagal Ke</b> <code>{error}</code> <b>Grup</b>"
    )


@Ayiin(["gucast"])
async def gucast_cmd(client: Client, message: Message):
    if message.reply_to_message or yins.get_cmd(message):
        XD = await eor(message, "<code>Started global broadcast...</code>")
    else:
        return await message.edit_text("<b>Berikan Sebuah Pesan atau Reply</b>")
    done = 0
    error = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE and not dialog.chat.is_verified:
            if message.reply_to_message:
                msg = message.reply_to_message
            elif yins.get_cmd:
                msg = yins.get_cmd(message)
            chat = dialog.chat.id
            if chat not in DEVS:
                try:
                    if message.reply_to_message:
                        await msg.copy(chat)
                    elif yins.get_cmd:
                        await client.send_message(chat, msg)
                    done += 1
                    await asyncio.sleep(0.3)
                except Exception:
                    error += 1
                    await asyncio.sleep(0.3)
    await XD.edit_text(
        f"<b>Berhasil Mengirim Pesan Ke</b> <code>{done}</code> <b>chat, Gagal Mengirim Pesan Ke</b> <code>{error}</code> <b>chat</b>"
    )


CMD_HELP.update(
    {"gcast": (
        "gcast",
        {
            "fgcast <reply>": "Forward Broadcast messages in group chats.",
            "gcast <reply>": "Broadcast messages in group chats.",
            "gucast <reply>": "Broadcast messages in user.",
        }
    )
    }
)
