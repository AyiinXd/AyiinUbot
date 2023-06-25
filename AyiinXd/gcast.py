# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-UserBot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-UserBot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de
#
# Recode By : @AyiinXd
#
# Ayiin - Ubot
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/AyiinUbot >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/AyiinUbot/blob/main/LICENSE/>.
#
# FROM AyiinUbot <https://github.com/AyiinXd/AyiinUbot>
# t.me/AyiinChat & t.me/AyiinSupport
#
# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

import asyncio

from fipper import Client, enums
from fipper.errors import FloodWait
from fipper.types import Message

from pyAyiin import Ayiin, CMD_HELP, DEVS, GCAST_BLACKLIST
from pyAyiin.dB.blacklistgcast import add_blacklist_gcast, blacklisted, is_blacklist_gcast, remove_blacklist_gcast


from . import yins


@Ayiin(["fgcast", "fw_cast"], langs=True)
async def gcast_cmd(client: Client, message: Message, _):
    '''
    ========================×========================
            Copyright (C) 2023-present AyiinXd
    ========================×========================
    '''
    BL = await blacklisted()
    if message.reply_to_message:
        AyiinXD = await message.reply(_["p"])
    else:
        return await message.edit_text(_["reply"])
    x = message.reply_to_message.id
    y = message.chat.id
    done = 0
    error = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in [
                enums.ChatType.GROUP,
                enums.ChatType.SUPERGROUP]:
            chat = dialog.chat.id
            if chat not in GCAST_BLACKLIST and chat not in BL:
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
    await AyiinXD.edit_text(_["gcast_1"].format(done, error))


@Ayiin(["gcast", "broadcast"], langs=True)
async def gcast_cmd(client: Client, message: Message, _):
    '''
    ========================×========================
            Copyright (C) 2023-present AyiinXd
    ========================×========================
    '''
    BL = await blacklisted()
    if message.reply_to_message:
        AyiinXD = await message.reply(_['p'])
    else:
        return await message.edit_text(_['reply'])
    x = message.reply_to_message.id
    y = message.chat.id
    done = 0
    error = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in [
                enums.ChatType.GROUP,
                enums.ChatType.SUPERGROUP]:
            chat = dialog.chat.id
            if chat not in GCAST_BLACKLIST and chat not in BL:
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
    await AyiinXD.edit_text(_['gcast_2'].format(done, error))


@Ayiin(["gucast"], langs=True)
async def gucast_cmd(client: Client, message: Message, _):
    '''
    ========================×========================
            Copyright (C) 2023-present AyiinXd
    ========================×========================
    '''
    if message.reply_to_message:
        XD = await message.reply(_['p'])
    else:
        return await message.edit_text(_['reply'])
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
    await XD.edit_text(_['gcast_3'].format(done, error))



@Ayiin(['addblacklist', 'addbl'], langs=True)
async def add_bl(client: Client, message: Message, _):
    '''
    ========================×========================
            Copyright (C) 2023-present AyiinXd
    ========================×========================
    '''
    chat_id = message.chat.id
    cmd = yins.get_cmd(message)
    if cmd:
        try:
            chat_ids = await client.get_chat(cmd)
            is_done = await is_blacklist_gcast(chat_ids.id)
            if not is_done:
                await add_blacklist_gcast(chat_ids.id)
                return await message.reply(_['gcast_4'].format(chat_ids.id))
            else:
                return await message.reply(_['gcast_5'].format(chat_ids.id))
        except Exception as e:
            return await message.reply(_['err'].format(e))
    else:
        is_done = await is_blacklist_gcast(chat_id)
        if not is_done:
            await add_blacklist_gcast(chat_id)
            return await message.reply(_['gcast_4'].format(chat_id))
        else:
            return await message.reply(_['gcast_5'].format(chat_id))


@Ayiin(['delblacklist', 'delbl'], langs=True)
async def del_bl(client: Client, message: Message, _):
    '''
    ========================×========================
            Copyright (C) 2023-present AyiinXd
    ========================×========================
    '''
    chat_id = message.chat.id
    cmd = yins.get_cmd(message)
    if cmd:
        try:
            chat_ids = await client.get_chat(cmd)
            is_done = await is_blacklist_gcast(chat_ids.id)
            if is_done:
                await remove_blacklist_gcast(chat_ids.id)
                return await message.reply(_['gcast_6'].format(chat_ids.id))
            else:
                return await message.reply(_['gcast_7'].format(chat_ids.id))
        except Exception as e:
            return await message.reply(_['err'].format(e))
    else:
        is_done = await is_blacklist_gcast(chat_id)
        if is_done:
            await remove_blacklist_gcast(chat_id)
            return await message.reply(_['gcast_6'].format(chat_id))
        else:
            return await message.reply(_['gcast_7'].format(chat_id))


@Ayiin(['blacklist', 'blchat'], langs=True)
async def list_bl(client: Client, message: Message, _):
    '''
    ========================×========================
            Copyright (C) 2023-present AyiinXd
    ========================×========================
    '''
    chats = await blacklisted()
    chat_id = f'{chats}'
    list = (
        chat_id.replace("[", "")
        .replace("]", "")
        .replace(",", "\n⇒ ")
    )
    count = len(chats)
    if count == 0:
        return await message.reply(_['gcast_8'])
    return await message.reply(_['gcast_9'].format(count, list))


CMD_HELP.update(
    {"gcast": (
        "gcast",
        {
            "fgcast [reply]": "Forward Broadcast messages in group chats.",
            "gcast [reply]": "Broadcast messages in group chats.",
            "gucast [reply]": "Broadcast messages in user.",
            "addbl": "Menambahkan ID Blacklist Gcast gunakan di group atau berikan username/id group",
            "delbl": "Menghapus ID Blacklist Gcast gunakan di group atau berikan username/id group",
            "blchat": "Melihat daftar ID Blacklist Gcast",
        }
    )
    }
)
