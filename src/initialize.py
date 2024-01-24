import os
import json
import csv
import sqlite3
import click

from common import (
    sanitize_field_name,
    get_default_structures_path,
    get_blueleaks_path,
    get_dbs_path,
)


def exec_sql(c, sql):
    try:
        c.execute(sql)
    except sqlite3.OperationalError as e:
        click.echo("")
        click.secho(sql, dim=True)
        raise e


def progress(site, table=None, row_count=None, finished=False):
    # Clear previous output
    click.echo("\r" + " " * 80, nl=False)

    # Print progress
    s = click.style(f"\r{site}", bold=True)
    if finished:
        s += " finished"
    elif table:
        s += " | " + f"{table}.csv"
        if row_count:
            s += " | " + click.style(f"{row_count:,} rows", dim=True)
    click.echo(s, nl=False)


def load_file(path):
    with open(path) as f:
        structure = json.load(f)
        site = structure["name"]

        # Start the database
        database_filename = os.path.join(get_dbs_path(), f"{site}.sqlite3")
        if os.path.exists(database_filename):
            click.secho(f"{database_filename} already exists so skipping", dim=True)
            return
        conn = sqlite3.connect(database_filename)
        c = conn.cursor()

        # For each table
        for table in structure["tables"]:
            progress(site, table)

            if site.startswith("usa"):
                csv_filename = os.path.join(get_blueleaks_path(), "usao", site, f"{table}.csv")
            else:
                csv_filename = os.path.join(get_blueleaks_path(), site, f"{table}.csv")

            with open(csv_filename) as csv_file:
                reader = csv.DictReader(csv_file)

                fields = [sanitize_field_name(field) for field in reader.fieldnames]
                for i in range(len(fields)):
                    if fields[i] == None:
                        fields[i] = ""
                fields = ",".join([f"'{field}'" for field in fields])

                sql = f"CREATE TABLE '{table}' ({fields})"
                exec_sql(c, sql)
                conn.commit()

                row_count = 0

                # Import rows
                for row in reader:
                    values = []
                    for field in row:
                        if row[field] == None:
                            values.append("")
                        else:
                            values.append(
                                row[field].replace("\\\\", "/").replace("'", "''")
                            )
                    for i in range(len(values)):
                        if values[i] == None:
                            values[i] = ""
                    values = ",".join([f"'{value}'" for value in values])

                    sql = f"INSERT INTO '{table}' VALUES ({values})"
                    # click.secho(sql, dim=True)
                    exec_sql(c, sql)

                    row_count += 1
                    if row_count % 1000 == 0:
                        progress(site, table, row_count)
                        conn.commit()

                conn.commit()

            progress(site, finished=True)

        conn.close()
        click.echo()


def is_struct_json(filename):
    return filename.find(".json") > -1


def import_data():
    for filename in os.listdir(get_default_structures_path()):
        if is_struct_json(filename):
            load_file(
                os.path.join(get_default_structures_path(), filename),
            )


if __name__ == "__main__":
    click.echo(click.style("BlueLeaks Explorer", fg="yellow"))
    import_data()
