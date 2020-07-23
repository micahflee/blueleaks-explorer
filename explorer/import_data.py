import os
import click
import json
import csv
import sqlite3


def exec_sql(c, sql):
    try:
        c.execute(sql)
    except sqlite3.OperationalError as e:
        click.secho(sql, dim=True)
        raise e


def sanitize_field_name(table):
    valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    new_table = ""
    for c in table:
        if c == "-" or c == " ":
            new_table += "_"
        elif c in valid_chars:
            new_table += c
    return new_table


def run(blueleaks_path):
    root_dir = "./"

    structure_filename = os.path.join(root_dir, "structure.json")
    dbs_dirname = os.path.join(root_dir, "databases")

    with open(structure_filename) as f:
        structure = json.load(f)

    # For each site
    for site in structure:
        click.secho(f"{structure[site]['name']} ({site})", bold=True)

        # Start the database
        database_filename = os.path.join(dbs_dirname, f"{site}.sqlite3")
        if os.path.exists(database_filename):
            click.echo(f"{database_filename} already exists so deleting it")
            os.remove(database_filename)

        conn = sqlite3.connect(database_filename)
        c = conn.cursor()

        # For each table
        for table in structure[site]["tables"]:
            click.echo(f"Importing table {table}.csv")

            csv_filename = os.path.join(blueleaks_path, site, f"{table}.csv")
            with open(csv_filename) as csv_file:
                reader = csv.DictReader(csv_file)

                fields = ", ".join(
                    [sanitize_field_name(field) for field in reader.fieldnames]
                )
                sql = f"CREATE TABLE {table} ({fields})"
                exec_sql(c, sql)
                conn.commit()

                row_count = 0

                # Import rows
                for row in reader:
                    values = (
                        str(tuple([row[field] for field in row]))
                        .replace(
                            "\\\\", ""
                        )  # Just remove "\\", to clean some of the data...
                        .replace("\\'", "''")
                    )
                    sql = f"INSERT INTO {table} VALUES {values}"
                    exec_sql(c, sql)

                    row_count += 1
                    if row_count % 1000 == 0:
                        click.secho(f"Loaded {row_count} rows", dim=True)
                        conn.commit()

            click.secho(f"Loaded {row_count} rows", dim=True)
