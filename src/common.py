import os


def get_blueleaks_path():
    return os.environ.get("BLE_BLUELEAKS_PATH", "")


def get_dbs_path():
    return os.environ.get("BLE_DATABASES_PATH", "")


def get_structures_path():
    return os.environ.get("BLE_STRUCTURES_PATH", "")


def get_builtin_structures_path():
    return os.environ.get(
        "BLE_STRUCTURES_BUILTIN_PATH", "/var/blueleaks-explorer/structures-builtin"
    )


def get_default_structures_path():
    path = os.environ.get(
        "BLE_STRUCTURES_DEFAULT_PATH", "/var/blueleaks-explorer/structures-default"
    )

    try:
        os.makedirs(path, exist_ok=True)
    except:
        pass

    return path


def sanitize_field_name(table):
    valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    new_table = ""
    for c in table:
        if c == "-" or c == " " or c == "/" or c == ":":
            new_table += "_"
        elif c in valid_chars:
            new_table += c
    return new_table
