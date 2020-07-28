import json
import sqlite3
import os
from pathlib import Path
from flask import Flask, jsonify, render_template, abort, send_file, request

app = Flask(__name__)

# This gets set below in run()
blueleaks_path = None

# Load structure
structure = {}


def humansize(nbytes):
    suffixes = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.0
        i += 1
    f = ("%.2f" % nbytes).rstrip("0").rstrip(".")
    return "%s %s" % (f, suffixes[i])


def get_database_filename(site):
    return os.path.join("databases", f"{site}.sqlite3")


def sql_count(site, table):
    conn = sqlite3.connect(get_database_filename(site))
    c = conn.cursor()

    c.execute(f"SELECT COUNT(*) FROM '{table}'")
    row = c.fetchone()

    conn.close()

    return row[0]


def sql_headers(site, table):
    conn = sqlite3.connect(get_database_filename(site))
    c = conn.cursor()

    headers = []
    for row in c.execute(f"PRAGMA table_info('{table}');"):
        headers.append(row[1])

    conn.close()

    return headers


def sql_select_rows(site, table, limit, offset):
    conn = sqlite3.connect(get_database_filename(site))
    c = conn.cursor()

    rows = []
    for row in c.execute(f"SELECT * FROM {table} LIMIT {limit} OFFSET {offset}"):
        rows.append(list(row))

    conn.close()
    return rows


def sql_select_item(site, table, item_id, headers):
    conn = sqlite3.connect(get_database_filename(site))
    c = conn.cursor()

    item_id = item_id.replace("'", "''")

    rows = []
    for row in c.execute(f"SELECT * FROM '{table}' WHERE '{headers[0]}'='{item_id}'"):
        rows.append(list(row))

    conn.close()
    return rows


def sql_select_join(site, table, item_id, join_from, join_to, headers):
    conn = sqlite3.connect(get_database_filename(site))
    c = conn.cursor()

    item_id = item_id.replace("'", "''")
    dest_table = join_to.split(".")[0]

    sql = f"SELECT '{dest_table}'.* FROM '{dest_table}' JOIN '{table}' ON {join_to}={join_from} WHERE '{table}'.'{headers[0]}'='{item_id}'"

    rows = []
    for row in c.execute(sql):
        rows.append(list(row))

    conn.close()
    return rows


def get_table_display_name(site, table):
    if "display" in structure[site]["tables"][table]:
        return structure[site]["tables"][table]["display"]
    else:
        return table


def get_important_fields(site, table, headers):
    if "important_fields" in structure[site]["tables"][table]:
        return structure[site]["tables"][table]["important_fields"]
    else:
        return headers


def get_field_types(site, table):
    if "field_types" in structure[site]["tables"][table]:
        return structure[site]["tables"][table]["field_types"]
    else:
        return {}


def render_frontend():
    return render_template("frontend.html")


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    # Download a data file
    if path.startswith("blueleaks-data"):
        listing_path = path[len("blueleaks-data") :]
        if listing_path == "":
            listing_path = "/"
        filename = os.path.join(blueleaks_path, listing_path.lstrip("/"))
        if os.path.exists(filename):
            if os.path.isdir(filename):
                # Render directory listing
                dirs = []
                files = []

                if listing_path != "/":
                    dirs.append(
                        {
                            "name": "..",
                            "link": os.path.join(
                                "/blueleaks-data",
                                os.path.dirname(listing_path).lstrip("/"),
                            ),
                        }
                    )

                for name in os.listdir(filename):
                    if os.path.isdir(os.path.join(filename, name)):
                        dirs.append(
                            {
                                "name": name,
                                "link": os.path.join(
                                    "/blueleaks-data", listing_path.lstrip("/"), name
                                ),
                            }
                        )
                    else:
                        size_bytes = Path(os.path.join(filename, name)).stat().st_size
                        files.append(
                            {
                                "name": name,
                                "link": os.path.join(
                                    "/blueleaks-data", listing_path.lstrip("/"), name
                                ),
                                "size": humansize(size_bytes),
                            }
                        )

                return render_template(
                    "directory_listing.html",
                    listing_path=listing_path,
                    dirs=dirs,
                    files=files,
                )
            else:
                return send_file(filename)
        else:
            abort(404)
    else:
        # Everything else, render the frontend
        return render_frontend()


@app.route("/structure.json")
def structure_json():
    return jsonify(structure)


@app.route("/api/structures")
def api_structures():
    with open("./default_structure.json") as f:
        default_structure = json.load(f)

    all_sites = [site for site in default_structure]

    implemented_sites = []
    for filename in os.listdir("./structures"):
        if filename.endswith(".json"):
            site = filename[:-5]
            with open(os.path.join("./structures", filename)) as f:
                site_structure = json.load(f)
            implemented_sites.append({"site": site, "name": site_structure["name"]})

    return jsonify({"all_sites": all_sites, "implemented_sites": implemented_sites})


@app.route("/api/sites")
def api_sites():
    sites = []
    for site in structure:
        sites.append({"folder": site, "name": structure[site]["name"]})
    return jsonify(sites)


@app.route("/api/<site>/tables")
def api_tables(site):
    if site not in structure:
        abort(500)

    tables = []
    for table in structure[site]["tables"]:
        # Get table display name
        if "display" in structure[site]["tables"][table]:
            display_name = structure[site]["tables"][table]["display"]
        else:
            display_name = table

        tables.append(
            {
                "name": table,
                "display_name": display_name,
                "count": sql_count(site, table),
            }
        )
    return jsonify({"site_name": structure[site]["name"], "tables": tables})


@app.route("/api/<site>/<table>")
def api_rows(site, table):

    if site not in structure:
        abort(500)
    if table not in structure[site]["tables"]:
        abort(500)

    limit = request.args.get("count")
    offset = request.args.get("offset")
    table_display_name = get_table_display_name(site, table)
    headers = sql_headers(site, table)
    important_fields = get_important_fields(site, table, headers)
    field_types = get_field_types(site, table)

    return jsonify(
        {
            "site_name": structure[site]["name"],
            "table_name": table_display_name,
            "headers": headers,
            "rows": sql_select_rows(site, table, limit, offset),
            "count": sql_count(site, table),
            "important_fields": important_fields,
            "field_types": field_types,
        }
    )


@app.route("/api/<site>/<table>/<item_id>")
def api_item(site, table, item_id):
    if site not in structure:
        abort(500)
    if table not in structure[site]["tables"]:
        abort(500)

    table_display_name = get_table_display_name(site, table)
    headers = sql_headers(site, table)
    important_fields = get_important_fields(site, table, headers)
    field_types = get_field_types(site, table)

    return jsonify(
        {
            "site_name": structure[site]["name"],
            "table_name": table_display_name,
            "headers": headers,
            "rows": sql_select_item(site, table, item_id, headers),
            "important_fields": important_fields,
            "field_types": field_types,
        }
    )


@app.route("/api/<site>/<table>/join/<header>/<item_id>")
def api_join(site, table, header, item_id):
    if site not in structure:
        abort(500)
    if table not in structure[site]["tables"]:
        abort(500)
    if header not in structure[site]["tables"][table]["field_types"]:
        abort(500)
    if header not in structure[site]["tables"][table]["joins"]:
        abort(500)
    if structure[site]["tables"][table]["field_types"][header] != "join":
        abort(500)

    headers = sql_headers(site, table)
    join_from = structure[site]["tables"][table]["joins"][header]["from"]
    join_to = structure[site]["tables"][table]["joins"][header]["to"]
    rows = sql_select_join(site, table, item_id, join_from, join_to, headers)

    join_table = join_to.split(".")[0]
    join_headers = sql_headers(site, join_table)
    join_important_fields = get_important_fields(site, join_table, join_headers)
    join_field_types = get_field_types(site, join_table)

    return jsonify(
        {
            "join_table": join_table,
            "join_headers": join_headers,
            "join_rows": rows,
            "join_count": len(rows),
            "join_important_fields": join_important_fields,
            "join_field_types": join_field_types,
        }
    )


def run(new_blueleaks_path):
    global blueleaks_path, structure

    blueleaks_path = new_blueleaks_path

    with open("./structure.json") as f:
        structure = json.load(f)

    app.run("127.0.0.1", "8080")
