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

import logging

from typing import Optional

from fipper import Client
from fipper.raw.functions.channels import GetFullChannel
from fipper.raw.functions.messages import GetFullChat
from fipper.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from fipper.types import Message

from config import *
from git import Repo
from pyAyiin import PyrogramXd
from pyAyiin.Clients import *
from pyAyiin.config import Var
from pyAyiin.pyrogram import eod, eor


flood = {}
OLD_MSG = {}
repo = Repo()
branch = repo.active_branch
yins = PyrogramXd()
var = Var()
hndlr = [
    f"{var.HNDLR[0]}",
    f"{var.HNDLR[1]}",
    f"{var.HNDLR[2]}",
    f"{var.HNDLR[3]}",
    f"{var.HNDLR[4]}",
    f"{var.HNDLR[5]}",
]
logs = logging.getLogger(__name__)

file = './cache/'
cache = "cache/{}.png"
cache_thumb = "cache/thumb{}.png"
font = "assets/font.ttf"
font2 = "assets/font2.ttf"
