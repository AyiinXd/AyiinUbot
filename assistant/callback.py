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

from fipper.types import *

from pyAyiin import CMD_HELP, HOSTED_ON, ayiin_ver
from pyAyiin.assistant import callback
from random import choice

from config import Var

from . import *
from .inline import help_string



# Callback Inline Help
@callback(pattern="plugins-tab")
async def plugins_page(_, cb: CallbackQuery):
    btn = yins.HelpXd(0, CMD_HELP, "xd")
    await cb.edit_message_text(
        text=help_string(),
        reply_markup=InlineKeyboardMarkup(btn)
    )


@callback(pattern="xd-next\\((.+?)\\)")
async def give_next_page(_, cb: CallbackQuery):
    current_page_number = int(cb.matches[0].group(1))
    btn = yins.HelpXd(current_page_number + 1, CMD_HELP, "xd")
    await cb.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btn))


@callback(pattern="xd-prev\\((.+?)\\)")
async def give_old_page(_, cb: CallbackQuery):
    current_page_number = int(cb.matches[0].group(1))
    btn = yins.HelpXd(current_page_number - 1, CMD_HELP, "xd")
    await cb.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btn))


@callback(pattern="back-to-plugins-(.*)")
async def get_back(_, cb: CallbackQuery):
    page_number = int(cb.matches[0].group(1))
    btn = yins.HelpXd(page_number, CMD_HELP, "xd")
    await cb.edit_message_text(text=help_string(), reply_markup=InlineKeyboardMarkup(btn))


@callback(pattern="pluginlist-(.*)")
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


# Callback Create Ubot
@callback("session_1")
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
@callback("session_2")
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


@callback("session_3")
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


@callback("session_4")
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


@callback("session_5")
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
