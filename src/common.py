import os

builtin_structures_path = "/var/blueleaks-explorer/structures-builtin"

default_structures_path = "/var/blueleaks-explorer/structures-default"
os.makedirs(default_structures_path, exist_ok=True)


def sanitize_field_name(table):
    valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    new_table = ""
    for c in table:
        if c == "-" or c == " " or c == "/" or c == ":":
            new_table += "_"
        elif c in valid_chars:
            new_table += c
    return new_table
