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
from fipper.types import Message
from time import sleep

from pyAyiin import Ayiin, CMD_HELP
from pyAyiin.pyrogram import eor


@Ayiin(["purge"])
async def purges(client: Client, msg: Message):
    xx = await eor(msg, "**Mulai Menghapus...**")
    msg_ids = []
    count_del = 0
    if msg.reply_to_message:
        for start_delete in range(
            msg.reply_to_message.id,
            msg.id
        ):
            msg_ids.append(start_delete)
            if len(msg_ids) == 100:
                await client.delete_messages(
                    chat_id=msg.chat.id, message_ids=msg_ids, revoke=True
                )
                count_del += len(msg_ids)
        if len(msg_ids) > 0:
            await client.delete_messages(
                chat_id=msg.chat.id, message_ids=msg_ids, revoke=True
            )
            count_del += len(msg_ids)

    await xx.edit(f"**Berhasil Menghapus** `{count_del}` **pesan.**")
    sleep(3)
    await msg.delete()


CMD_HELP.update(
    {"purge": (
        "purge",
        {
            "purge <reply>" : "Balas ke pesan yg ingin di hapus sekaligus."
        }
    )
    }
)
