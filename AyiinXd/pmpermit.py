# Ayiin - Ubot
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/AyiinUbot >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/AyiinUbot/blob/main/LICENSE/>.
#
# FROM AyiinUbot <https://github.com/AyiinXd/AyiinUbot>
# t.me/AyiinChat & t.me/AyiinSupport


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

from fipper import Client, filters
from fipper.types import *

from pyAyiin import Ayiin, CMD_HELP, DEVS, tgbot
from pyAyiin.dB.pmpermit_db import approve_user, is_approved
from pyAyiin.pyrogram import eor
from pyAyiin.decorator import Ayiin, listen

from config import *

from . import *


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
        await message.reply_text("Scammer Tidak Diterima di PM Tuan Saya!")
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
    pm_limit = int(Var.PERMIT_LIMIT)
    limits = pm_limit + 1
    async for m in client.get_chat_history(user_.id, limit=limits):
        if m.reply_markup:
            await m.delete()
    if str(user_.id) in flood:
        flood[str(user_.id)] += 1
    else:
        flood[str(user_.id)] = 1
    if flood[str(user_.id)] > pm_limit:
        await message.reply_text("SPAM TERDETEKSI, MEMBLOKIR OTOMATIS!")
        if str(user_.id) in OLD_MSG:
            OLD_MSG.pop(str(user_.id))
        return await client.block_user(user_.id)
    try:
        tgbot.me = await tgbot.get_me()
        results = await client.get_inline_bot_results(tgbot.me.username, f"pmpermit_{user_.id}")
        msg_dlt = await message.reply_inline_bot_result(
            results.query_id,
            results.results[0].id,
            reply_to_message_id=message.id,
        )
    except BaseException as e:
        return await message.reply(f"<b>ERROR:</b> <code>{e}</code>")
    if str(user_.id) in OLD_MSG:
        try:
            await OLD_MSG[str(user_.id)].delete()
        except BaseException:
            pass
    OLD_MSG[str(user_.id)] = msg_dlt


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
            "block": "Blokir Cucu Dajjal Yg Rusuh.",
            "unblocl": "Lepas Blokiran Cucu Dajjal.", 
        }
    )
    }
)
