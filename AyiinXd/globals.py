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
@Ayiin(["gban"])
async def gban_user(client: Client, message: Message):
    user_id, reason = await yins.extract_user_and_reason(message, sender_chat=True)
    if message.from_user.id != client.me.id:
        Ayiin = await message.reply("<i>Gbanning...</i>")
    else:
        Ayiin = await message.edit("<i>Gbanning....</i>")
    if not user_id:
        return await Ayiin.edit("Saya tidak dapat menemukan pengguna itu.")
    if user_id == client.me.id:
        return await Ayiin.edit("<i>Ngapain NgeGban diri sendiri Goblok</i> 🐽")
    if user_id in DEVS:
        return await Ayiin.edit("<i>Gagal GBAN karena dia adalah Pembuat saya</i>🗿")
    if user_id:
        try:
            user = await client.get_users(user_id)
        except Exception:
            return await Ayiin.edit("<i>Harap tentukan pengguna yang valid!</i>")

    if await is_gbanned(user.id):
        return await Ayiin.edit(
            f"<a href=tg://user?id={user.id}>Cucu Dajjal</a> <b>ini sudah ada di daftar gbanned</b>"
        )
    f_chats = await yins.get_ub_chats(client)
    if not f_chats:
        return await Ayiin.edit("<i>Anda tidak mempunyai GC yang anda admin</i> 🥺")
    er = 0
    done = 0
    for gokid in f_chats:
        try:
            await client.ban_chat_member(chat_id=gokid, user_id=int(user.id))
            done += 1
        except BaseException:
            er += 1
    await add_gbanned(user.id)
    msg = (
        r"<b>\\#GBanned_User//</b>"
        f"\n\n<b>First Name:</b> <a href=tg://user?id={user.id}>{user.first_name}</a>"
        f"\n<b>User ID:</b> <code>{user.id}</code>")
    if reason:
        msg += f"\n<b>Reason:</b> <code>{reason}</code>"
    msg += f"\n<b>Affected To:</b> <code>{done}</code> <b>Chats</b>"
    await Ayiin.edit(msg)


@Ayiin(["Cungban"], devs=True)
@Ayiin(["ungban"])
async def ungban_user(client: Client, message: Message):
    user_id, reason = await yins.extract_user_and_reason(message, sender_chat=True)
    if message.from_user.id != client.me.id:
        Ayiin = await message.reply("<i>UnGbanning...</i>")
    else:
        Ayiin = await message.edit("<i>UnGbanning....</i>")
    if not user_id:
        return await Ayiin.edit("Saya tidak dapat menemukan pengguna itu.")
    if user_id:
        try:
            user = await client.get_users(user_id)
        except Exception:
            return await Ayiin.edit("<i>Harap tentukan pengguna yang valid!</i>")

    try:
        if not await is_gbanned(user.id):
            return await Ayiin.edit("<i>User already ungban</i>")
        ung_chats = await yins.get_ub_chats(client)
        if not ung_chats:
            return await Ayiin.edit("<i>Anda tidak mempunyai GC yang anda admin</i> 🥺")
        er = 0
        done = 0
        for good_boi in ung_chats:
            try:
                await client.unban_chat_member(chat_id=good_boi, user_id=user.id)
                done += 1
            except BaseException:
                er += 1
        await remove_gbanned(user.id)
        msg = (
            r"<b>\\#UnGbanned_User//</b>"
            f"\n\n<b>First Name:</b> <a href=tg://user?id={user.id}>{user.first_name}</a>"
            f"\n<b>User ID:</b> <code>{user.id}</code>")
        if reason:
            msg += f"\n<b>Reason:</b> <code>{reason}</code>"
        msg += f"\n<b>Affected To:</b> <code>{done}</code> <b>Chats</b>"
        await Ayiin.edit(msg)
    except Exception as e:
        await Ayiin.edit(f"<b>ERROR:</b> <code>{e}</code>")
        return


@Ayiin(["listgban"])
async def gbanlist(client: Client, message: Message):
    users = await gbanned_users()
    Ayiin = await eor(message, "<i>Processing...</i>")
    if not users:
        return await Ayiin.edit("Belum ada Pengguna yang Di-Gban")
    gban_list = "<b>GBanned Users:</b>\n"
    count = 0
    for i in users:
        count += 1
        gban_list += f"<b>{count} -</b> <code>{i.sender}</code>\n"
    return await Ayiin.edit(gban_list)


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
