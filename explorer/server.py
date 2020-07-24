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


def sql_query(site, table, query):
    conn = sqlite3.connect(get_database_filename(site))
    c = conn.cursor()

    # Get column names
    columns = []
    for row in c.execute("PRAGMA table_info(VideoCategory);"):
        columns.append(row[1])

    rows = []
    for row in c.execute(query):
        rows.append(list(row))

    conn.close()
    return columns, rows


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


def run(new_blueleaks_path):
    global blueleaks_path
    blueleaks_path = new_blueleaks_path
    app.run("127.0.0.1", "8080")
