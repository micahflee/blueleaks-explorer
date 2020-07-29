import os
import click
import json
import csv
import sqlite3

from .common import sanitize_field_name, get_databases_dir, get_default_structures_dir


def exec_sql(c, sql):
    try:
        c.execute(sql)
    except sqlite3.OperationalError as e:
        click.echo("")
        click.secho(sql, dim=True)
        raise e


def progress(structure, site, table=None, row_count=None):
    # Clear previous output
    click.echo("\r" + " " * 80, nl=False)

    # Print progress
    s = click.style(f"\r{structure[site]['name']} ({site})", bold=True)
    if table:
        s += " | " + f"{table}.csv"
        if row_count:
            s += " | " + click.style(f"{row_count} rows", dim=True)
    click.echo(s, nl=False)


def progress_2(site, table=None, row_count=None):
    # Clear previous output
    click.echo("\r" + " " * 80, nl=False)

    # Print progress
    s = click.style(f"\r{site} ({site})", bold=True)
    if table:
        s += " | " + f"{table}.csv"
        if row_count:
            s += " | " + click.style(f"{row_count} rows", dim=True)
    click.echo(s, nl=False)


def load_file(dbs_dirname, blueleaks_path, path):
    print(f"load_file: {path}")
    with open(path) as f:
        structure = json.load(f)
        site = structure["name"]

        # Start the database
        database_filename = os.path.join(dbs_dirname, f"{site}.sqlite3")
        if os.path.exists(database_filename):
            click.secho(f" | {database_filename} already exists so skipping", dim=True)
            return
        conn = sqlite3.connect(database_filename)
        c = conn.cursor()

        # For each table
        for table in structure["tables"]:
            progress_2(site, table)

            csv_filename = os.path.join(blueleaks_path, site, f"{table}.csv")
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
                        progress_2(site, table, row_count)
                        conn.commit()

                conn.commit()

            progress_2(site)

        conn.close()
        click.echo()


def is_struct_json(filename):
    return filename.find(".json") > -1


def run(blueleaks_path):
    root_dir = "../"

    dbs_dirname = get_databases_dir()
    default_structures_dir = get_default_structures_dir()

    for filename in os.listdir(default_structures_dir):
        if is_struct_json(filename):
            load_file(
                dbs_dirname,
                blueleaks_path,
                os.path.join(default_structures_dir, filename),
            )
