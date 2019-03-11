import json

import settings

_data = json.load(open(settings.CONFIG_FILE, "r"))


def get_host():
    yield from _data["HOST"]


def get_db():
    yield from _data["DB"]

if __name__ == "__main__":
    print(list(get_db()))
