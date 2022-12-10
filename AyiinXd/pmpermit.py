import asyncio

from fipper import Client, filters
from fipper.enums import ChatType
from fipper.types import *

from pyAyiin import Ayiin, CMD_HELP, DEVS
from pyAyiin.dB.pmpermit_db import approve_user, disapprove_user, is_approved
from pyAyiin.pyrogram import eor
from pyAyiin.decorator import Ayiin, listen

from . import *


MSG_PERMIT = (
    """
╔═════════════════════╗
│  𖣘 𝚂𝙴𝙻𝙰𝙼𝙰𝚃 𝙳𝙰𝚃𝙰𝙽𝙶 𝚃𝙾𝙳 𖣘ㅤ  ㅤ
╚═════════════════════╝
 ⍟ 𝙹𝙰𝙽𝙶𝙰𝙽 𝚂𝙿𝙰𝙼 𝙲𝙷𝙰𝚃 𝙼𝙰𝙹𝙸𝙺𝙰𝙽 𝙶𝚄𝙰 𝙺𝙴𝙽𝚃𝙾𝙳
 ⍟ 𝙶𝚄𝙰 𝙰𝙺𝙰𝙽 𝙾𝚃𝙾𝙼𝙰𝚃𝙸𝚂 𝙱𝙻𝙾𝙺𝙸𝚁 𝙺𝙰𝙻𝙾 𝙻𝚄 𝚂𝙿𝙰𝙼
 ⍟ 𝙹𝙰𝙳𝙸 𝚃𝚄𝙽𝙶𝙶𝚄 𝚂𝙰𝙼𝙿𝙰𝙸 𝙼𝙰𝙹𝙸𝙺𝙰𝙽 𝙶𝚄𝙰 𝙽𝙴𝚁𝙸𝙼𝙰 𝙿𝙴𝚂𝙰𝙽 𝙻𝚄
╔═════════════════════╗
│ㅤㅤ𖣘 𝙿𝙴𝚂𝙰𝙽 𝙾𝚃𝙾𝙼𝙰𝚃𝙸𝚂 𖣘ㅤㅤ
│ㅤㅤ   𖣘 𝙰𝚈𝙸𝙸𝙽 - 𝚄𝙱𝙾𝚃 𖣘ㅤㅤ
╚═════════════════════╝
"""
)

flood = {}
OLD_MSG = {}


@listen(
    filters.private
    & filters.incoming
    & ~filters.service
    & ~filters.me
    & ~filters.bot
    & ~filters.via_bot
)
async def pmpermit_func(client: Client, message: Message):
    user_ = message.from_user
    if user_.is_bot:
        return
    if user_.is_self:
        return
    if user_.is_contact:
        return
    if user_.is_verified:
        return
    if user_.is_scam:
        await message.reply_text("`Scammer Aren't Welcome To My Masters PM!`")
        await client.block_user(user_.id)
        return
    if user_.is_support:
        return
    if is_approved(user_.id):
        return
    if user_.id in DEVS:
        if not is_approved(user_.id):
            approve_user(user_.id)
            return await message.reply("Menerima Pesan Developer")
        else:
            pass
    async for m in client.get_chat_history(user_.id, limit=6):
        if m.reply_markup:
            await m.delete()
    if str(user_.id) in flood:
        flood[str(user_.id)] += 1
    else:
        flood[str(user_.id)] = 1
    if flood[str(user_.id)] > 5:
        await message.reply_text("SPAM DETECTED, BLOCKED USER AUTOMATICALLY!")
        if str(user_.id) in OLD_MSG:
            OLD_MSG.pop(str(user_.id))
        return await client.block_user(user_.id)
    msg_dlt = await client.send_message(
        user_.id,
        MSG_PERMIT,
        reply_to_message_id=yins.ReplyCheck(message),
    )
    if str(user_.id) in OLD_MSG:
        try:
            await OLD_MSG[str(user_.id)].delete()
        except BaseException:
            pass
    OLD_MSG[str(user_.id)] = msg_dlt


@Ayiin(["ok", "a"])
async def pm_approve(client: Client, message: Message):
    if message.reply_to_message:
        reply = message.reply_to_message
        replied_user = reply.from_user
        if replied_user.is_self:
            await message.edit("Anda tidak dapat menyetujui diri sendiri.")
            return
        aname = replied_user.id
        str(replied_user.first_name)
        uid = replied_user.id
        if is_approved(uid):
            return await eor(message, "Pengguna Ini Sudah Ada Di Database")
        approve_user(uid)
        xnxx = await eor(message, "Pesan Anda Diterima Tod")
        if str(uid) in OLD_MSG:
            await OLD_MSG[str(uid)].delete()
        await asyncio.sleep(3)
        await xnxx.delete()
    else:
        aname = message.chat
        if not aname.type == ChatType.PRIVATE:
            await message.edit(
                "Saat ini Anda tidak sedang dalam PM dan Anda belum membalas pesan seseorang."
            )
            return
        aname.first_name
        uid = aname.id
        if is_approved(uid):
            return await eor(message, "Pengguna Ini Sudah Ada Di Database")
        approve_user(uid)
        xnxx = await eor(message, "Pesan Anda Telah Diterima Tod")
        if str(uid) in OLD_MSG:
            await OLD_MSG[str(uid)].delete()
        await asyncio.sleep(3)
        await xnxx.delete()


@Ayiin(["tolak", "da"])
async def pm_disapprove(client: Client, message: Message):
    if message.reply_to_message:
        reply = message.reply_to_message
        replied_user = reply.from_user
        if replied_user.is_self:
            await message.edit("Anda tidak dapat menyetujui diri sendiri.")
            return
        aname = replied_user.id
        str(replied_user.first_name)
        uid = replied_user.id
        if not is_approved(uid):
            return await eor(message, "Pengguna Ini Tidak Ada Di Database")
        disapprove_user(uid)
        xnxx = await eor(message, "Pesan Anda Ditolak Tod")
        await asyncio.sleep(3)
        await xnxx.delete()
    else:
        aname = message.chat
        if not aname.type == ChatType.PRIVATE:
            await message.edit(
                "Saat ini Anda tidak sedang dalam PM dan Anda belum membalas pesan seseorang."
            )
            return
        aname.first_name
        uid = aname.id
        if not is_approved(uid):
            return await eor(message, "Pengguna Ini Tidak Ada Di Database")
        disapprove_user(uid)
        xnxx = await eor(message, "Pesan Anda Ditolak Tod")
        await asyncio.sleep(3)
        await xnxx.delete()


@Ayiin(["block"])
async def block_user_func(client: Client, message: Message):
    if not message.reply_to_message:
        return await eor(message, "Reply to a user's message to block.")
    user_id = message.reply_to_message.from_user.id
    await eor(message, "Successfully blocked the user")
    await client.block_user(user_id)


@Ayiin(["unblock"])
async def unblock_user_func(client: Client, message: Message):
    if not message.reply_to_message:
        return await eor(message, "Reply to a user's message to unblock.")
    user_id = message.reply_to_message.from_user.id
    await client.unblock_user(user_id)
    await eor(message, "Successfully Unblocked the user")


CMD_HELP.update(
    {"pmpermit": (
        "pmpermit",
        {
            "ok": "Menerima Pesan PmPermit",
            "tolak": "Menolak Pesan PmPermit",
            "block": "Blokir Cucu Dajjal Yg Rusuh.",
            "unblocl": "Lepas Blokiran Cucu Dajjal.", 
        }
    )
    }
)