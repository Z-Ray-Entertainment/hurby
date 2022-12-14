import os

import requests

from utils import const, json_loader, logger

_TMP_FILE = "external-ban-list.json"
_TMP_FILE_ABSOLUTE = const.CONST.DIR_TMP_ABSOLUTE + "/" + _TMP_FILE


def get_twitch_bot_names(url) -> dict:
    if _tmp_file_exist():
        return _load_tmp_file()
    else:
        r = requests.get(url)
        if 200 <= r.status_code < 300:
            external_json = requests.get(url).json()
            bots = {
                "names": [],
                "ids": []
            }
            for user in external_json:
                if user["reason"] == "bot_account":
                    bots["names"].append(user["twitch_name"])
                    bots["ids"].append(user["twitch_id"])
            save_tmp_file(bots)
            return bots
        else:
            logger.log(logger.WARN, "Can't access external banlist, will not update blacklist:\n" + r.text)
        return None


def _tmp_file_exist():
    try:
        f = open(_TMP_FILE_ABSOLUTE)
        return True
    except IOError:
        return False


def save_tmp_file(bots: dict):
    json_loader.save_json(_TMP_FILE_ABSOLUTE, bots)


def _load_tmp_file() -> dict:
    return json_loader.load_json(_TMP_FILE_ABSOLUTE)


def delete_tmp_file():
    os.remove(_TMP_FILE_ABSOLUTE)
