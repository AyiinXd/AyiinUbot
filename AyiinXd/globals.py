# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-UserBot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-UserBot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

from fipper import Client, filters
from fipper.types import *

from pyAyiin import Ayiin, CMD_HELP, DEVS
from pyAyiin.pyrogram import eor
from pyAyiin.dB.gban import add_gbanned, gbanned_users, is_gbanned, remove_gbanned
from pyAyiin.decorator import listen


from . import *


@Ayiin(["Cgban"], devs=True)
@Ayiin(["gban"], langs=True)
async def gban_user(client: Client, message: Message, _):
    user_id, reason = await yins.extract_user_and_reason(message, sender_chat=True)
    Ayiin = await message.reply(_['p'])
    if not user_id:
        return await Ayiin.edit(_['err_user'])
    if user_id == client.me.id:
        return await Ayiin.edit(_['gban_1'])
    if user_id in DEVS:
        return await Ayiin.edit(_['ayiin_2'])
    if user_id:
        try:
            user = await client.get_users(user_id)
        except Exception:
            return await Ayiin.edit(_['err_user'])

    if await is_gbanned(user.id):
        return await Ayiin.edit(_['gban_2'].format(user.mention))
    f_chats = await yins.get_ub_chats(client)
    if not f_chats:
        return await Ayiin.edit(_['gban_3'])
    er = 0
    done = 0
    for gokid in f_chats:
        try:
            await client.ban_chat_member(chat_id=gokid, user_id=int(user.id))
            done += 1
        except BaseException:
            er += 1
    await add_gbanned(user.id)
    msg = _['gban_4'].format(user.mention, user.id)
    if reason:
        msg += _['admin_4'].format(reason)
    msg += _['gban_5'].format(done)
    await Ayiin.edit(msg)


@Ayiin(["Cungban"], devs=True)
@Ayiin(["ungban"], langs=True)
async def ungban_user(client: Client, message: Message, _):
    user_id, reason = await yins.extract_user_and_reason(message, sender_chat=True)
    Ayiin = await message.reply(_['p'])
    if not user_id:
        return await Ayiin.edit(_['err_user'])
    if user_id:
        try:
            user = await client.get_users(user_id)
        except Exception:
            return await Ayiin.edit(_['err_user'])

    try:
        if not await is_gbanned(user.id):
            return await Ayiin.edit(_['gban_6'])
        ung_chats = await yins.get_ub_chats(client)
        if not ung_chats:
            return await Ayiin.edit(_['gban_3'])
        er = 0
        done = 0
        for good_boi in ung_chats:
            try:
                await client.unban_chat_member(chat_id=good_boi, user_id=user.id)
                done += 1
            except BaseException:
                er += 1
        await remove_gbanned(user.id)
        msg = _['gban_7'].format(user.mention, user.id)
        if reason:
            msg += _['admin_4'].format(reason)
        msg += _['gban_5'].format(done)
        await Ayiin.edit(msg)
    except Exception as e:
        await Ayiin.edit(_['err'].format(e))
        return


@Ayiin(["listgban"], langs=True)
async def gbanlist(client: Client, message: Message, _):
    users = await gbanned_users()
    Ayiin = await eor(message, _['p'])
    if not users:
        return await Ayiin.edit(_['gban_8'])
    return await Ayiin.edit(_['gban_9'].format(users))


@listen(filters.incoming & filters.group)
async def globals_check(client: Client, message: Message):
    if not message:
        return
    if not message.from_user:
        return
    user_id = message.from_user.id
    chat_id = message.chat.id
    if not user_id:
        return
    if await is_gbanned(user_id):
        try:
            await client.ban_chat_member(chat_id, user_id)
        except BaseException:
            pass

    message.continue_propagation()


CMD_HELP.update(
    {"globals": (
        "globals",
        {
            "gban <reply/username/userid>": "Melakukan Global Banned Ke Semua Grup Dimana anda Sebagai Admin.",
            "ungban <reply/username/userid>": "Membatalkan Global Banned.",
            "listgban": "Menampilkan List Global Banned.",
        }
    )
    }
)
