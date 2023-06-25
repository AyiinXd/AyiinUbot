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

from git import Repo

from pyAyiin import Ayiin, CMD_HELP, tgbot

from . import *


@Ayiin(["update"], langs=True)
async def updater(client, msg, _):
    xx = await eor(msg, _['p'])
    m = await yins.updater()
    repo = Repo.init()
    branch = repo.active_branch
    changelog, tl_chnglog = await yins.gen_chlog(
        repo, f"HEAD..upstream/{branch}"
    )
    if m:
        try:
            tgbot.me = await tgbot.get_me()
            results = await client.get_inline_bot_results(tgbot.me.username, f"in_update")
            await msg.reply_inline_bot_result(
                results.query_id,
                results.results[0].id,
                reply_to_message_id=yins.ReplyCheck(msg),
            )
            await xx.delete()
        except BaseException as e:
            return await eod(msg, _['err'].format(e))
    else:
        await xx.edit(
            _['update'].format(branch, branch),
            disable_web_page_preview=True,
        )


CMD_HELP.update(
    {"update": (
        "update",
        {
            "update" : "Gunakan Ini Untuk Mengecek Apakah Userbot Anda Versi Terbaru."
        }
    )
    }
)
