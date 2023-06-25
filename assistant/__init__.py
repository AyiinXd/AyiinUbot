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

from config import *
from git import Repo
from pyAyiin import PyrogramXd
from pyAyiin.Clients import *
from pyAyiin.config import Var


repo = Repo()
branch = repo.active_branch
yins = PyrogramXd()
var = Var()

logs = logging.getLogger(__name__)
