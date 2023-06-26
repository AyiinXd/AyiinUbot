# Ayiin - Ubot
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/AyiinUbot >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/AyiinUbot/blob/main/LICENSE/>.
#
# FROM AyiinUbot <https://github.com/AyiinXd/AyiinUbot>
# t.me/AyiinChats & t.me/AyiinChannel


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

import asyncio

from fipper import Client, filters
from fipper.enums import ChatType
from fipper.types import *

from pyAyiin import Ayiin, CMD_HELP, DEVS, tgbot
from pyAyiin.dB.pmpermit import (
    approve_pmpermit, 
    disapprove_pmpermit, 
    is_pmpermit_approved,
)
from pyAyiin.pyrogram import eor
from pyAyiin.decorator import Ayiin, listen

from . import *

from config import *


@listen(
    (
        filters.private
        & filters.incoming
        & ~filters.service
        & ~filters.me
        & ~filters.bot
        & ~filters.via_bot
    ),
    langs=True
)
async def pmpermit_func(client: Client, message: Message, _):
    user_ = message.from_user
    me_id = client.me.id
    pmper = Var.PMPERMIT
    if pmper == False:
        return True
    if user_.is_bot:
        return
    if user_.is_self:
        return
    if user_.is_contact:
        return
    if user_.is_verified:
        return
    if user_.is_scam:
        await message.reply_text(_['permit_1'])
        await client.block_user(user_.id)
        return
    if user_.is_support:
        return
    if await is_pmpermit_approved(me_id, user_.id):
        return
    if user_.id in DEVS:
        if not await is_pmpermit_approved(me_id, user_.id):
            await approve_pmpermit(me_id, user_.id)
            return await message.reply(_['permit_2'].format(user_.mention, user_.mention))
        else:
            pass
    pm_limit = int(Var.PERMIT_LIMIT)
    limits = pm_limit + 1
    async for m in client.get_chat_history(user_.id, limit=limits):
        if m.reply_markup:
            await m.delete()
    if str(user_.id) in flood:
        flood[str(user_.id)] += 1
    else:
        flood[str(user_.id)] = 1
    if flood[str(user_.id)] > limits:
        await message.reply_text(_['permit_3'])
        if str(user_.id) in OLD_MSG:
            OLD_MSG.pop(str(user_.id))
            flood.update({user_.id: 0})
        return await client.block_user(user_.id)
    try:
        tgbot.me = await tgbot.get_me()
        results = await client.get_inline_bot_results(tgbot.me.username, f"pmpermit_{me_id}_{user_.id}")
        msg_dlt = await message.reply_inline_bot_result(
            results.query_id,
            results.results[0].id,
            reply_to_message_id=message.id,
        )
    except BaseException:
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


@Ayiin(["ok", "a"], langs=True)
async def pm_approve(client: Client, message: Message, _):
    ids = client.me.id
    if message.reply_to_message:
        reply = message.reply_to_message
        replied_user = reply.from_user
        if replied_user.is_self:
            await message.edit(_['permit_4'])
            return
        aname = replied_user.id
        str(replied_user.first_name)
        uid = replied_user.id
        if await is_pmpermit_approved(ids, uid):
            return await eor(message, _['permit_5'])
        await approve_pmpermit(ids, uid)
        xnxx = await eor(message, _['permit_6'])
        if str(uid) in OLD_MSG and str(uid) in flood:
            await OLD_MSG[str(uid)].delete()
            flood[str(uid)] = 0
        await asyncio.sleep(3)
        await xnxx.delete()
    else:
        aname = message.chat
        if not aname.type == ChatType.PRIVATE:
            await message.edit(
                _['permit_7']
            )
            return
        aname.first_name
        uid = aname.id
        if await is_pmpermit_approved(ids, uid):
            return await eor(message, _['permit_5'])
        await approve_pmpermit(ids, uid)
        xnxx = await eor(message, _['permit_6'])
        try:
            if str(uid) in OLD_MSG and str(uid) in flood:
                await OLD_MSG[str(uid)].delete()
                flood[str(uid)] = 0
        except BaseException:
            pass
        await asyncio.sleep(3)
        await xnxx.delete()


@Ayiin(["tolak", "da"], langs=True)
async def pm_disapprove(client: Client, message: Message, _):
    ids = client.me.id
    if message.reply_to_message:
        reply = message.reply_to_message
        replied_user = reply.from_user
        if replied_user.is_self:
            await message.edit(_['permit_4'])
            return
        aname = replied_user.id
        str(replied_user.first_name)
        uid = replied_user.id
        if not await is_pmpermit_approved(ids, uid):
            return await eor(message, _['permit_8'])
        await disapprove_pmpermit(ids, uid)
        xnxx = await eor(message, _['permit_9'])
        await asyncio.sleep(3)
        await xnxx.delete()
    else:
        aname = message.chat
        if not aname.type == ChatType.PRIVATE:
            await message.edit(
                _['permit_7']
            )
            return
        aname.first_name
        uid = aname.id
        if not await is_pmpermit_approved(ids, uid):
            return await eor(message, _['permit_8'])
        await disapprove_pmpermit(ids, uid)
        xnxx = await eor(message, _['permit_9'])
        await asyncio.sleep(3)
        await xnxx.delete()


@Ayiin(["block"], langs=True)
async def block_user_func(client: Client, message: Message, _):
    if not message.reply_to_message:
        return await eor(message, _['reply'])
    user_id = message.reply_to_message.from_user.id
    # Blocking user after editing the message so that other person can get the
    # update.
    await eor(message, _['permit_10'])
    await client.block_user(user_id)


@Ayiin(["unblock"], langs=True)
async def unblock_user_func(client: Client, message: Message, _):
    if not message.reply_to_message:
        return await eor(message, _['reply'])
    user_id = message.reply_to_message.from_user.id
    await client.unblock_user(user_id)
    await eor(message, _['permit_11'])


CMD_HELP.update(
    {"pmpermit": (
        "pmpermit",
        {
            "ok": "Menerima Pesan PmPermit",
            "tolak": "Menolak Pesan PmPermit",
            "unblock [reply]": "Lepas Blokir Pengguna",
            "block [reply]": "Memblokir Pengguna",
        }
    )
    }
)
