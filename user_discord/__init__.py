#Using template from https://github.com/Minori101/Amino.fix/blob/main/aminofix/__init__.py :D THANKS

__title__ = 'user_discord'
__author__ = 'nxSlayer'
__license__ = 'MIT'
__copyright__ = 'Copyright 2023 nxSlayer'

from .socket import SocketDiscord
from .user_discord import ClientDiscord
from .utils import objects
from .utils import payloads
from .utils import Thread

from requests import get
from json import loads

__newest__ = loads(get("https://pypi.org/pypi/user-discord/json").text)["info"]["version"]

if '2.0.6' != __newest__:
    print(f"(user-discord) There is a new version, please update for better results")