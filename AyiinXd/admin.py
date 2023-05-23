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
from fipper.errors import ChatAdminRequired, UserCreator
from fipper.types import ChatPermissions, ChatPrivileges, Message

from pyAyiin import Ayiin, CMD_HELP, DEVS
from pyAyiin.pyrogram import eor

from . import *


unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@Ayiin(
    ["setchatphoto", "setgpic"],
    group_only=True,
)
async def set_chat_photo(client: Client, message: Message):
    if await yins.CheckAdmin(client, message) is True:
        if message.reply_to_message:
            if message.reply_to_message.photo:
                await client.set_chat_photo(
                    message.chat.id, photo=message.reply_to_message.photo.file_id
                )
                return
        else:
            await message.edit_text("Reply to a photo to set it !")


@Ayiin(["Cban"], devs=True)
@Ayiin(["ban"])
async def member_ban(client: Client, message: Message):
    if await yins.CheckAdmin(client, message) is True:
        Ayiin = await eor(message, "<i>Processing...</i>")
        user_id, reason = await yins.extract_user_and_reason(message, sender_chat=True)
        if not user_id:
            return await Ayiin.edit("I can't find that user.")
        if user_id == client.me.id:
            return await Ayiin.edit("I can't ban myself.")
        if user_id in DEVS:
            return await Ayiin.edit("I can't ban my developer!")
        try:
            mention = (await client.get_users(user_id)).mention
        except IndexError:
            mention = (
                message.reply_to_message.sender_chat.title
                if message.reply_to_message
                else "Anon"
            )
        msg = (
            f"<b>Banned User:</b> {mention}\n"
            f"<b>Banned By:</b> {message.from_user.mention if message.from_user else 'Anon'}\n"
        )
        if message.command[0][0] == "d":
            await message.reply_to_message.delete()
        if reason:
            msg += f"<b>Reason:</b> {reason}"
        try:
            await message.chat.ban_member(user_id)
            await Ayiin.edit(msg)
        except ChatAdminRequired:
            await Ayiin.edit("<i>Maaf Anda Tidak Mempunyai Hak Admin ( Blokir Pengguna )</i>")
        except UserCreator:
            return await Ayiin.edit("<i>Begooo Dia Owner Gc Tod</i>")


@Ayiin(["Cunban"], devs=True)
@Ayiin(["unban"])
async def member_unban(client: Client, message: Message):
    if await yins.CheckAdmin(client, message) is True:
        Ayiin = await eor(message, "<i>Processing...</i>")
        reply = message.reply_to_message
        if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
            return await Ayiin.edit("You cannot unban a channel")

        if len(message.command) == 2:
            user = message.text.split(None, 1)[1]
        elif len(message.command) == 1 and reply:
            user = message.reply_to_message.from_user.id
        else:
            return await Ayiin.edit(
                "Provide a username or reply to a user's message to unban."
            )
        await message.chat.unban_member(user)
        umention = (await client.get_users(user)).mention
        await Ayiin.edit(f"Unbanned! {umention}")


@Ayiin(["Cpin", "Cunpin"], devs=True)
@Ayiin(["pin", "unpin"])
async def pin_message(client: Client, message):
    if not message.reply_to_message:
        return await eor(message, "Reply to a message to pin/unpin it.")
    r = message.reply_to_message
    if message.chat.type == enums.ChatType.PRIVATE:
        try:
            if message.command[0][0] == "u":
                await r.unpin()
                return await eor(
                    message,
                    f"<i>Unpinned This Message.</i>",
                    disable_web_page_preview=True,
                )
            await r.pin(disable_notification=True)
            await eor(
                message,
                f"<i>Pinned This Message.</i>",
                disable_web_page_preview=True,
            )
            return
        except BaseException:
            pass
    if await yins.CheckAdmin(client, message) is True:
        Ayiin = await eor(message, "<i>Processing...</i>")
        try:
            if message.command[0][0] == "u":
                await r.unpin()
                return await Ayiin.edit(
                    f"<i>Unpinned <a href={r.link}>This</a> message.</i>",
                    disable_web_page_preview=True,
                )
            await r.pin(disable_notification=True)
            await Ayiin.edit(
                f"<i>Pinned <a href={r.link}>this</a> message.</i>",
                disable_web_page_preview=True,
            )
        except ChatAdminRequired:
            return await Ayiin.edit("<i>Maaf Anda Tidak Mempunyai Hak Admin ( Tautkan Pesan )</i>")


@Ayiin(["Cmute"], devs=True)
@Ayiin(["mute"])
async def mute(client: Client, message: Message):
    if await yins.CheckAdmin(client, message) is True:
        Ayiin = await eor(message, "<i>Processing...</i>")
        user_id, reason = await yins.extract_user_and_reason(message)
        if not user_id:
            return await Ayiin.edit("I can't find that user.")
        if user_id == client.me.id:
            return await Ayiin.edit("I can't mute myself.")
        if user_id in DEVS:
            return await Ayiin.edit("I can't mute my developer!")
        mention = (await client.get_users(user_id)).mention
        msg = (
            f"<b>Muted User:</b> {mention}\n"
            f"<b>Muted By:</b> {message.from_user.mention if message.from_user else 'Anon'}\n"
        )
        if reason:
            msg += f"<b>Reason:</b> {reason}"
        try:
            await message.chat.restrict_member(user_id, permissions=ChatPermissions())
            await Ayiin.edit(msg)
        except ChatAdminRequired:
            return await Ayiin.edit("<i>Maaf Anda Tidak Mempunyai Hak Admin </i>")
        except UserCreator:
            return await Ayiin.edit("<i>Begooo Dia Owner Gc Tod</i>")


@Ayiin(["Cunmute"], devs=True)
@Ayiin(["unmute"])
async def unmute(client: Client, message: Message):
    if await yins.CheckAdmin(client, message) is True:
        Ayiin = await eor(message, "<i>Processing...</i>")
        user_id = await yins.extract_user(message)
        if not user_id:
            return await Ayiin.edit("I can't find that user.")
        await message.chat.restrict_member(user_id, permissions=unmute_permissions)
        umention = (await client.get_users(user_id)).mention
        await Ayiin.edit(f"Unmuted! {umention}")


@Ayiin(["Ckick", "Cdkick"], devs=True)
@Ayiin(["kick", "dkick"])
async def kick_user(client: Client, message: Message):
    if await yins.CheckAdmin(client, message) is True:
        Ayiin = await eor(message, "<i>Processing...</i>")
        user_id, reason = await yins.extract_user_and_reason(message)
        if not user_id:
            return await Ayiin.edit("I can't find that user.")
        if user_id == client.me.id:
            return await Ayiin.edit("I can't kick myself.")
        if user_id == DEVS:
            return await Ayiin.edit("I can't kick my developer.")
        if user_id in (await yins.list_admins(client, message.chat.id)):
            return await Ayiin.edit("I can't kick an admin, You know the rules, so do i.")
        mention = (await client.get_users(user_id)).mention
        msg = f"""
<b>Kicked User:</b> {mention}
<b>Kicked By:</b> {message.from_user.mention if message.from_user else 'Anon'}"""
        if message.command[0][0] == "d":
            await message.reply_to_message.delete()
        if reason:
            msg += f"\n<b>Reason:</b> <code>{reason}</code>"
        try:
            await message.chat.ban_member(user_id)
            await Ayiin.edit(msg)
            await asyncio.sleep(1)
            await message.chat.unban_member(user_id)
        except ChatAdminRequired:
            return await Ayiin.edit("<i>Maaf Anda Tidak Mempunyai Hak Admin Itu</i>")
        except UserCreator:
            return await Ayiin.edit("<i>Begooo Dia Owner Gc Tod</i>")


@Ayiin(["Cpromote", "Cfullpromote"], devs=True)
@Ayiin(["promote", "fullpromote"])
async def promotte(client: Client, message: Message):
    if await yins.CheckAdmin(client, message) is True:
        user_id = await yins.extract_user(message)
        umention = (await client.get_users(user_id)).mention
        Ayiin = await eor(message, "<i>Processing...</i>")
        if not user_id:
            return await Ayiin.edit("I can't find that user.")
        if message.command[0][0] == "f":
            try:
                await message.chat.promote_member(
                    user_id,
                    privileges=ChatPrivileges(
                        can_manage_chat=True,
                        can_delete_messages=True,
                        can_manage_video_chats=True,
                        can_restrict_members=True,
                        can_change_info=True,
                        can_invite_users=True,
                        can_pin_messages=True,
                        can_promote_members=True,
                    ),
                )
                return await Ayiin.edit(f"Fully Promoted! {umention}")
            except ChatAdminRequired:
                return await Ayiin.edit("<i>Maaf Anda Tidak Mempunyai Hak Admin ( Menambahkan Admin Baru )</i>")
            except UserCreator:
                return await Ayiin.edit("<i>Begooo Dia Owner Gc Tod</i>")

        try:
            await message.chat.promote_member(
                user_id,
                privileges=ChatPrivileges(
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_restrict_members=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                    can_promote_members=False,
                ),
            )
            await Ayiin.edit(f"Promoted! {umention}")
        except ChatAdminRequired:
            return await Ayiin.edit("<i>Maaf Anda Tidak Mempunyai Hak Admin ( Menambahkan Admin Baru )</i>")
        except UserCreator:
            return await Ayiin.edit("<i>Begooo Dia Owner Gc Tod</i>")


@Ayiin(["Cdemote"], devs=True)
@Ayiin(["demote"])
async def demote(client: Client, message: Message):
    if await yins.CheckAdmin(client, message) is True:
        user_id = await yins.extract_user(message)
        Ayiin = await eor(message, "<i>Processing...</i>")
        if not user_id:
            return await Ayiin.edit("I can't find that user.")
        if user_id == client.me.id:
            return await Ayiin.edit("I can't demote myself.")
        try:
            await message.chat.promote_member(
                user_id,
                privileges=ChatPrivileges(
                    can_manage_chat=False,
                    can_delete_messages=False,
                    can_manage_video_chats=False,
                    can_restrict_members=False,
                    can_change_info=False,
                    can_invite_users=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                ),
            )
            umention = (await client.get_users(user_id)).mention
            await Ayiin.edit(f"Demoted! {umention}")
        except (ChatAdminRequired or UserCreator):
            return await Ayiin.edit("<i>Maaf Anda Tidak Bisa Melakukan Itu</i>")
        except UserCreator:
            return await Ayiin.edit("<i>Begooo Dia Owner Gc Tod</i>")


@Ayiin(["staff"])
async def adminlist(client: Client, message: Message):
    replyid = None
    toolong = False
    if len(message.text.split()) >= 2:
        chat = message.text.split(None, 1)[1]
        grup = await client.get_chat(chat)
    else:
        chat = message.chat.id
        grup = await client.get_chat(chat)
    if message.reply_to_message:
        replyid = message.reply_to_message.id
    creator = []
    admin = []
    badmin = []
    async for a in client.get_chat_members(
        message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
    ):
        try:
            nama = a.user.first_name + " " + a.user.last_name
        except:
            nama = a.user.first_name
        if nama is None:
            nama = "☠️ Deleted account"
        if a.status == enums.ChatMemberStatus.ADMINISTRATOR:
            if a.user.is_bot:
                badmin.append(f'[{nama}](tg://user?id={a.user.id})')
            else:
                admin.append(f'[{nama}](tg://user?id={a.user.id})')
        elif a.status == enums.ChatMemberStatus.OWNER:
            creator.append(f'[{nama}](tg://user?id={a.user.id})')
    admin.sort()
    badmin.sort()
    totaladmins = len(creator) + len(admin) + len(badmin)
    teks = "**Admins in {}**\n".format(grup.title)
    teks += "╒═══「 Creator 」\n"
    for x in creator:
        teks += "│ • {}\n".format(x)
        if len(teks) >= 4096:
            await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
            teks = ""
            toolong = True
    teks += "╞══「 {} Human Administrator 」\n".format(len(admin))
    for x in admin:
        teks += "│ • {}\n".format(x)
        if len(teks) >= 4096:
            await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
            teks = ""
            toolong = True
    teks += "╞══「 {} Bot Administrator 」\n".format(len(badmin))
    for x in badmin:
        teks += "│ • {}\n".format(x)
        if len(teks) >= 4096:
            await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
            teks = ""
            toolong = True
    teks += "╘══「 Total {} Admins 」".format(totaladmins)
    if toolong:
        await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
    else:
        await message.edit(teks)


CMD_HELP.update(
    {"admins": (
        "admins",
        {
            "ban <reply/username/userid> <alasan>": "Membanned member dari grup.",
            "unban <reply/username/userid> <alasan>": "Membuka banned member dari grup.",
            "kick <reply/username/userid>": "Mengeluarkan pengguna dari grup.",
            "promote atau fullpromote": "Mempromosikan member sebagai admin atau cofounder.",
            "demote": "Menurunkan admin sebagai member.",
            "mute <reply/username/userid>": "Membisukan member dari Grup.",
            "unmute <reply/username/userid>": "Membuka mute member dari Grup.",
            "pin <reply>": "Untuk menyematkan pesan dalam grup.",
            "unpin <reply>": "Untuk melepaskan pin pesan dalam grup.",
            "setgpic <reply ke foto>": "Untuk mengubah foto profil grup",
        }
        )
    }
)
