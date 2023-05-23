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

from fipper import Client
from fipper.errors import PeerIdInvalid
from fipper.types import Message

from pyAyiin import Ayiin, CMD_HELP
from pyAyiin.pyrogram import eod, eor

from . import *


@Ayiin(['id', 'get_id'])
async def get_id(client: Client, msg: Message):
    usr_text = ''
    xxx = await eor(msg, '**Processing...**')
    reply = msg.reply_to_message
    chats = msg.chat.id
    cmd = yins.get_cmd(msg)
    if reply:
        if reply.from_user:
            mention = reply.from_user.mention
            ids = reply.from_user.id
            usr_text += f'**User:** {mention}\n'
            usr_text += f'**ID:** {ids}\n\n'
        else:
            mention = reply.forward_from.mention
            ids = reply.forward_from.id
            usr_text += f'**User:** {mention}\n'
            usr_text += f'**ID:** {ids}\n\n'
        usr_text += f'**Get ID By {client.me.username}'
        await xxx.edit(usr_text)
    elif cmd:
        try:
            user = await client.get_users(cmd)
        except PeerIdInvalid:
            await eod(xxx, 'Maaf saya tidak bisa menemukan pengguna...')
        mention = user.mention
        ids = user.id
        usr_text += f'**User:** {mention}\n'
        usr_text += f'**ID:** {ids}\n\n'
        usr_text += f'**Get ID By {client.me.username}'
        await xxx.edit(usr_text)
    else:
        await xxx.edit(f'**ID:** {chats}')


CMD_HELP.update(
    {'get_id': (
        'get_id',
        {
            'id <reply/id>' : 'Berikan id atau balas ke pesan pengguna untuk mendapatkan id.\n\nKetik .id untuk mendapatkan id chat saat ini.'
        }
    )
    }
)
