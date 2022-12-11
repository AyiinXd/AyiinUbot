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

import dotenv
import heroku3
import os
import sys

from fipper import Client
from fipper.enums import ParseMode
from fipper.types import *
from git import Repo
from git.exc import GitCommandError

from config import *

from pyAyiin import CMD_HELP, HOSTED_ON, ayiin_ver
from pyAyiin.assistant import callback
from random import choice

from . import *
from .inline import help_string



# Callback Inline Help
@callback(pattern="plugins-tab", client_only=True)
async def plugins_page(_, cb: CallbackQuery):
    btn = yins.HelpXd(0, CMD_HELP, "xd")
    await cb.edit_message_text(
        text=help_string(),
        reply_markup=InlineKeyboardMarkup(btn)
    )


@callback(pattern="xd-next\\((.+?)\\)", client_only=True)
async def give_next_page(_, cb: CallbackQuery):
    current_page_number = int(cb.matches[0].group(1))
    btn = yins.HelpXd(current_page_number + 1, CMD_HELP, "xd")
    await cb.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btn))


@callback(pattern="xd-prev\\((.+?)\\)", client_only=True)
async def give_old_page(_, cb: CallbackQuery):
    current_page_number = int(cb.matches[0].group(1))
    btn = yins.HelpXd(current_page_number - 1, CMD_HELP, "xd")
    await cb.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btn))


@callback(pattern="back-to-plugins-(.*)", client_only=True)
async def get_back(_, cb: CallbackQuery):
    page_number = int(cb.matches[0].group(1))
    btn = yins.HelpXd(page_number, CMD_HELP, "xd")
    await cb.edit_message_text(text=help_string(), reply_markup=InlineKeyboardMarkup(btn))


@callback(pattern="pluginlist-(.*)", client_only=True)
async def give_plugin_cmds(_, cb: CallbackQuery):
    plugin_name, page_number = cb.matches[0].group(1).split("|", 1)
    plugs = await yins.PluginXd(CMD_HELP, plugin_name)
    cmd_string = f"<b>PLUGIN:</b> {plugin_name.capitalize()}\n<b>HNDLR:</b> <code>{choice(hndlr)}</code>\n\n" + "".join(plugs)
    await cb.edit_message_text(
        cmd_string,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Back",
                        callback_data=f"back-to-plugins-{page_number}",
                    )
                ]
            ]
        ),
    )


@callback(pattern='update_now', client_only=True)
async def update_callback(_, cb: CallbackQuery):
    repo = Repo()
    ac_br = repo.active_branch
    ups_rem = repo.remote("upstream")
    if HOSTED_ON == "Heroku":
        heroku = heroku3.from_key(Var.HEROKU_API)
        heroku_app = None
        heroku_applications = heroku.apps()
        if not Var.HEROKU_APP_NAME:
            await cb.answer(
                "<•> Please set up the HEROKU_APP_NAME variable to be able to update userbot.",
                show_alert=True,
            )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == Var.HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await cb.answer(
                f"<i>Invalid Heroku credentials for updating userbot dyno.</i>",
                show_alert=True,
            )
            repo.__del__()
            return
        try:
            await cb.edit_message_text(
            "<b>[HEROKU]:</b> <i>Update Deploy AyiinUbot Sedang Dalam Proses...</i>"
            )
        except:
            pass
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + Var.HEROKU_API + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            await cb.edit_message_text(
            "<i>AyiinUbot Berhasil Diupdate! Userbot bisa di Gunakan Lagi.</i>"
            )
            remote.push(refspec=f"HEAD:refs/heads/{ac_br}", force=True)
        except GitCommandError as error:
            await cb.edit_message_text(f"`Here is the error log:\n{error}`")
            repo.__del__()
            return
        except:
            pass
        try:
            await cb.edit_message_text(
            "<i>AyiinUbot Berhasil Diupdate! Userbot bisa di Gunakan Lagi.</i>"
            )
        except:
            pass
    else:
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await yins.install_requirements()
        try:
            await cb.edit_message_text(
            "<i>AyiinUbot Berhasil Diupdate! Userbot bisa di Gunakan Lagi.</i>",
            )
        except:
            pass
        args = [sys.executable, "-m", "pyAyiin"]
        os.execle(sys.executable, *args, os.environ)
        return


@callback(pattern='changelog', client_only=True)
async def changelog_callback(client, cb: CallbackQuery):
    msg = cb.message
    changelog, tl_chnglog = await yins.gen_chlog(
        repo, f"HEAD..upstream/{branch}"
    )
    if changelog:
        if len(changelog) > 4096:
            await cb.edit_message_text("<b>Changelog terlalu besar, dikirim sebagai file.</b>")
            file = open("output.txt", "w+")
            file.write(changelog)
            file.close()
            await client.send_document(
                msg.chat.id,
                "output.txt",
                caption=f"**Klik Tombol** `Update` **Untuk Mengupdate Userbot.**",
                reply_to_message_id=yins.ReplyCheck(msg),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="•• Update ••",
                                callback_data=f"update_now",
                            )
                        ]
                    ]
                ),
            )
            os.remove("output.txt")
        await cb.edit_message_text(
            changelog,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="•• Update ••",
                            callback_data=f"update_now",
                        )
                    ]
                ]
            ),
        )


@callback(pattern="terima_(.*)", client_only=True)
async def get_back(client: Client, cb: CallbackQuery):
    user_ids = int(cb.matches[0].group(1))
    await yins.approve_pmpermit(cb, user_ids, OLD_MSG)


@callback(pattern="tolak_(.*)", client_only=True)
async def get_back(client: Client, cb: CallbackQuery):
    user_ids = int(cb.matches[0].group(1))
    await yins.disapprove_pmpermit(cb, user_ids)


# Callback Create Ubot
@callback("session_1", client_only=True)
async def added_to_group_msg(bot, cq):
    vars = 'STRING_1'
    if Var.STRING_1 is not None:
        await cq.answer(
            "String Session Ini Sudah Terisi Bego...",
            show_alert=True,
        )
    try:
        string_session = await yins.generate_premium(
            bot,
            Var.LOG_CHAT,
            f"AyiinUbot {ayiin_ver}",
            cq.message,
        )
        if HOSTED_ON == "Heroku":
            if Var.HEROKU_API is None or Var.HEROKU_APP_NAME is None:
                logs.info(
                    "Pastikan HEROKU_API dan HEROKU_APP_NAME anda dikonfigurasi dengan benar di config vars heroku"
                )
            Heroku = heroku3.from_key(Var.HEROKU_API)
            happ = Heroku.app(Var.HEROKU_APP_NAME)
            heroku_config = happ.config()
            if vars not in heroku_config:
                heroku_config[vars] = string_session
                logs.info(f"Berhasil Menambahkan Vars {vars}")
                return True
            else:
                pass
        else:
            path = dotenv.find_dotenv(".env")
            if not path:
                logs.info(".env file not found.")
            if not dotenv.get_key(path, vars):
                dotenv.set_key(path, vars, string_session)
                logs.info(f"Berhasil Menambahkan {vars}")
                os.execvp(sys.executable, [sys.executable, "-m", "pyAyiin"])
            else:
                pass
    except Exception as e:
        return await cq.message.reply("[ERROR]\n{}\nSilahkan Teruskan Pesan Ini Ke @AyiinChat".format(str(e)))
    await cq.message.delete()


# Callback Create Ubot
@callback("session_2", client_only=True)
async def added_to_group_msg(bot, cq):
    vars = 'STRING_2'
    if Var.STRING_2 is not None:
        await cq.answer(
            "String Session Ini Sudah Terisi Bego...",
            show_alert=True,
        )
    try:
        string_session = await yins.generate_premium(
            bot,
            Var.LOG_CHAT,
            f"AyiinUbot {ayiin_ver}",
            cq.message,
        )
        if HOSTED_ON == "Heroku":
            if Var.HEROKU_API is None or Var.HEROKU_APP_NAME is None:
                logs.info(
                    "Pastikan HEROKU_API dan HEROKU_APP_NAME anda dikonfigurasi dengan benar di config vars heroku"
                )
            Heroku = heroku3.from_key(Var.HEROKU_API)
            happ = Heroku.app(Var.HEROKU_APP_NAME)
            heroku_config = happ.config()
            if vars not in heroku_config:
                heroku_config[vars] = string_session
                logs.info(f"Berhasil Menambahkan Vars {vars}")
                return True
            else:
                pass
        else:
            path = dotenv.find_dotenv(".env")
            if not path:
                logs.info(".env file not found.")
            if not dotenv.get_key(path, vars):
                dotenv.set_key(path, vars, string_session)
                logs.info(f"Berhasil Menambahkan {vars}")
                os.execvp(sys.executable, [sys.executable, "-m", "pyAyiin"])
            else:
                pass
    except Exception as e:
        return await cq.message.reply("[ERROR]\n{}\nSilahkan Teruskan Pesan Ini Ke @AyiinChat".format(str(e)))
    await cq.message.delete()


@callback("session_3", client_only=True)
async def added_to_group_msg(bot, cq):
    vars = 'STRING_3'
    if Var.STRING_3 is not None:
        await cq.answer(
            "String Session Ini Sudah Terisi Bego...",
            show_alert=True,
        )
    try:
        string_session = await yins.generate_premium(
            bot,
            Var.LOG_CHAT,
            f"AyiinUbot {ayiin_ver}",
            cq.message,
        )
        if HOSTED_ON == "Heroku":
            if Var.HEROKU_API is None or Var.HEROKU_APP_NAME is None:
                logs.info(
                    "Pastikan HEROKU_API dan HEROKU_APP_NAME anda dikonfigurasi dengan benar di config vars heroku"
                )
            Heroku = heroku3.from_key(Var.HEROKU_API)
            happ = Heroku.app(Var.HEROKU_APP_NAME)
            heroku_config = happ.config()
            if vars not in heroku_config:
                heroku_config[vars] = string_session
                logs.info(f"Berhasil Menambahkan Vars {vars}")
                return True
            else:
                pass
        else:
            path = dotenv.find_dotenv(".env")
            if not path:
                logs.info(".env file not found.")
            if not dotenv.get_key(path, vars):
                dotenv.set_key(path, vars, string_session)
                logs.info(f"Berhasil Menambahkan {vars}")
                os.execvp(sys.executable, [sys.executable, "-m", "pyAyiin"])
            else:
                pass
    except Exception as e:
        return await cq.message.reply("[ERROR]\n{}\nSilahkan Teruskan Pesan Ini Ke @AyiinChat".format(str(e)))
    await cq.message.delete()


@callback("session_4", client_only=True)
async def added_to_group_msg(bot, cq):
    vars = 'STRING_4'
    if Var.STRING_4 is not None:
        await cq.answer(
            "String Session Ini Sudah Terisi Bego...",
            show_alert=True,
        )
    try:
        string_session = await yins.generate_premium(
            bot,
            Var.LOG_CHAT,
            f"AyiinUbot {ayiin_ver}",
            cq.message,
        )
        if HOSTED_ON == "Heroku":
            if Var.HEROKU_API is None or Var.HEROKU_APP_NAME is None:
                logs.info(
                    "Pastikan HEROKU_API dan HEROKU_APP_NAME anda dikonfigurasi dengan benar di config vars heroku"
                )
            Heroku = heroku3.from_key(Var.HEROKU_API)
            happ = Heroku.app(Var.HEROKU_APP_NAME)
            heroku_config = happ.config()
            if vars not in heroku_config:
                heroku_config[vars] = string_session
                logs.info(f"Berhasil Menambahkan Vars {vars}")
                return True
            else:
                pass
        else:
            path = dotenv.find_dotenv(".env")
            if not path:
                logs.info(".env file not found.")
            if not dotenv.get_key(path, vars):
                dotenv.set_key(path, vars, string_session)
                logs.info(f"Berhasil Menambahkan {vars}")
                os.execvp(sys.executable, [sys.executable, "-m", "pyAyiin"])
            else:
                pass
    except Exception as e:
        return await cq.message.reply("[ERROR]\n{}\nSilahkan Teruskan Pesan Ini Ke @AyiinChat".format(str(e)))
    await cq.message.delete()


@callback("session_5", client_only=True)
async def added_to_group_msg(bot, cq):
    vars = 'STRING_5'
    if Var.STRING_5 is not None:
        await cq.answer(
            "String Session Ini Sudah Terisi Bego...",
            show_alert=True,
        )
    try:
        string_session = await yins.generate_premium(
            bot,
            Var.LOG_CHAT,
            f"AyiinUbot {ayiin_ver}",
            cq.message,
        )
        if HOSTED_ON == "Heroku":
            if Var.HEROKU_API is None or Var.HEROKU_APP_NAME is None:
                logs.info(
                    "Pastikan HEROKU_API dan HEROKU_APP_NAME anda dikonfigurasi dengan benar di config vars heroku"
                )
            Heroku = heroku3.from_key(Var.HEROKU_API)
            happ = Heroku.app(Var.HEROKU_APP_NAME)
            heroku_config = happ.config()
            if vars not in heroku_config:
                heroku_config[vars] = string_session
                logs.info(f"Berhasil Menambahkan Vars {vars}")
                return True
            else:
                pass
        else:
            path = dotenv.find_dotenv(".env")
            if not path:
                logs.info(".env file not found.")
            if not dotenv.get_key(path, vars):
                dotenv.set_key(path, vars, string_session)
                logs.info(f"Berhasil Menambahkan {vars}")
                os.execvp(sys.executable, [sys.executable, "-m", "pyAyiin"])
            else:
                pass
    except Exception as e:
        return await cq.message.reply("[ERROR]\n{}\nSilahkan Teruskan Pesan Ini Ke @AyiinChat".format(str(e)))
    await cq.message.delete()


@callback(pattern='close', client_only=True)
async def close_cb(_, cb):
    try:
        await cb.message.delete()
    except BaseException:
        await cb.answer(
            'Gagal menghapus Pesan...',
            show_alert=True,
        )
