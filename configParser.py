import json

import settings

_data = json.load(open(settings.CONFIG_FILE, "r"))


def get_host():
    for host in _data["HOST"]:
        yield host


def get_db():
    for db in _data["DB"]:
        yield db


if __name__ == "__main__":
    print(list(get_db()))
