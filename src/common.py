import os

builtin_structures_path = "/var/blueleaks-explorer/builtin-structures"

default_structures_path = "/var/blueleaks-explorer/default-structures"
os.path.makedirs(default_structures_path, exist_ok=True)


def sanitize_field_name(table):
    valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    new_table = ""
    for c in table:
        if c == "-" or c == " " or c == "/" or c == ":":
            new_table += "_"
        elif c in valid_chars:
            new_table += c
    return new_table
