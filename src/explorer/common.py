import os


def get_databases_dir():
    if os.environ.get("BLE_DATABASES_DIR"):
        return os.environ.get("BLE_DATABASES_DIR")
    else:
        return "../databases"


def get_structures_dir():
    if os.environ.get("BLE_STRUCTURES_DIR"):
        return os.environ.get("BLE_STRUCTURES_DIR")
    else:
        return "../structures"


def get_default_structures_dir():
    if os.environ.get("BLE_DEFAULT_STRUCTURES_DIR"):
        return os.environ.get("BLE_DEFAULT_STRUCTURES_DIR")
    else:
        return "../structures-default"


def sanitize_field_name(table):
    valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    new_table = ""
    for c in table:
        if c == "-" or c == " " or c == "/" or c == ":":
            new_table += "_"
        elif c in valid_chars:
            new_table += c
    return new_table
