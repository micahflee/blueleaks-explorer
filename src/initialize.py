import os
import json
import csv
import sqlite3
import click

blueleaks_path = os.environ.get("BLE_BLUELEAKS_PATH")
dbs_path = os.environ.get("BLE_DATABASES_PATH")
default_structures_path = os.environ.get("BLE_DEFAULT_STRUCTURES_PATH")


def sanitize_field_name(table):
    valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    new_table = ""
    for c in table:
        if c == "-" or c == " " or c == "/" or c == ":":
            new_table += "_"
        elif c in valid_chars:
            new_table += c
    return new_table


def build_structure():
    # Find all folders that have tables (CSV files)
    for site in os.listdir(blueleaks_path):
        if os.path.isdir(os.path.join(blueleaks_path, site)):
            structure = {}

            # Make a list of tables
            tables = []
            try:
                for filename in os.listdir(os.path.join(blueleaks_path, site)):
                    if filename.endswith(".csv"):
                        tables.append(filename[0:-4])
            except:
                # lost+found folder throws a permission denied
                pass

            # Skip if there aren't any tables
            if len(tables) == 0:
                continue

            # Start defining the structure
            structure = {"name": site, "tables": {}}

            for table in tables:
                # Get a list of columns for this table
                csv_filename = os.path.join(blueleaks_path, site, f"{table}.csv")
                with open(csv_filename) as csv_file:
                    reader = csv.DictReader(csv_file)
                    fields = [
                        {
                            "name": sanitize_field_name(field),
                            "show": True,
                            "type": "text",
                        }
                        for field in reader.fieldnames
                    ]

                    count = 0
                    for row in reader:
                        count += 1

                if count == 0:
                    hidden = True
                else:
                    hidden = False

                structure["tables"][table] = {
                    "display": table,
                    "hidden": hidden,
                    "fields": fields,
                    "joins": [],
                }

            json_filename = os.path.join(default_structures_path, f"{site}.json")
            with open(json_filename, "w") as f:
                f.write(json.dumps(structure, indent=4))
            click.secho(f"Wrote {json_filename}", dim=True)


def exec_sql(c, sql):
    try:
        c.execute(sql)
    except sqlite3.OperationalError as e:
        click.echo("")
        click.secho(sql, dim=True)
        raise e


def progress(site, table=None, row_count=None):
    # Clear previous output
    click.echo("\r" + " " * 80, nl=False)

    # Print progress
    s = click.style(f"\r{site} ({site})", bold=True)
    if table:
        s += " | " + f"{table}.csv"
        if row_count:
            s += " | " + click.style(f"{row_count:,} rows", dim=True)
    click.echo(s, nl=False)


def load_file(path):
    with open(path) as f:
        structure = json.load(f)
        site = structure["name"]

        # Start the database
        database_filename = os.path.join(dbs_path, f"{site}.sqlite3")
        if os.path.exists(database_filename):
            click.secho(f" | {database_filename} already exists so skipping", dim=True)
            return
        conn = sqlite3.connect(database_filename)
        c = conn.cursor()

        # For each table
        for table in structure["tables"]:
            progress(site, table)

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
                        progress(site, table, row_count)
                        conn.commit()

                conn.commit()

            progress(site)

        conn.close()
        click.echo()


def is_struct_json(filename):
    return filename.find(".json") > -1


def import_data():
    for filename in os.listdir(default_structures_path):
        if is_struct_json(filename):
            load_file(
                os.path.join(default_structures_path, filename),
            )


if __name__ == "__main__":
    click.echo(click.style("BlueLeaks Explorer", fg="yellow"))
    click.echo("")
    build_structure()
    import_data()
