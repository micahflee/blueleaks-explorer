import json
import sqlite3
import os
from flask import Flask, jsonify, render_template, abort

app = Flask(__name__)

# This gets set below in run()
blueleaks_path = None

# Load structure
with open("./structure.json") as f:
    structure = json.load(f)


def get_database_filename(site):
    return os.path.join("databases", f"{site}.sqlite3")


def sql_count(site, table):
    conn = sqlite3.connect(get_database_filename(site))
    c = conn.cursor()

    c.execute(f"SELECT COUNT(*) FROM {table}")
    row = c.fetchone()

    conn.close()

    return row[0]


def sql_headers(site, table):
    conn = sqlite3.connect(get_database_filename(site))
    c = conn.cursor()

    headers = []
    for row in c.execute(f"PRAGMA table_info({table});"):
        headers.append(row[1])

    conn.close()

    return headers


def sql_select(site, table):
    conn = sqlite3.connect(get_database_filename(site))
    c = conn.cursor()

    rows = []
    for row in c.execute(f"SELECT * FROM {table}"):
        rows.append(list(row))

    conn.close()
    return rows


def render_frontend():
    return render_template("frontend.html")


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return render_frontend()


@app.route("/structure.json")
def structure_json():
    return jsonify(structure)


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


@app.route("/api/<site>/<table>/rows")
def api_rows(site, table):
    if site not in structure:
        abort(500)
    if table not in structure[site]["tables"]:
        abort(500)

    headers = sql_headers(site, table)

    if "important_fields" in structure[site]["tables"][table]:
        important_fields = structure[site]["tables"][table]["important_fields"]
    else:
        important_fields = headers

    if "field_types" in structure[site]["tables"][table]:
        field_types = structure[site]["tables"][table]["field_types"]
    else:
        field_types = {}

    return jsonify(
        {
            "site_name": structure[site]["name"],
            "headers": headers,
            "rows": sql_select(site, table),
            "count": sql_count(site, table),
            "important_fields": important_fields,
            "field_types": field_types,
        }
    )


def run(new_blueleaks_path):
    global blueleaks_path
    blueleaks_path = new_blueleaks_path
    app.run("127.0.0.1", "8080")
