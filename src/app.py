import json
import sqlite3
import os
import sys
import shutil
from pathlib import Path
from flask import Flask, jsonify, render_template, abort, send_file, request

from common import default_structures_path, builtin_structures_path

blueleaks_path = os.environ.get("BLE_BLUELEAKS_PATH")
dbs_path = os.environ.get("BLE_DATABASES_PATH")
structures_path = os.environ.get("BLE_STRUCTURES_PATH")

app = Flask(__name__, static_folder="frontend/dist/assets", static_url_path="/assets")

# Keep track of structures in memory
structures = {}

# Cache SQL statements and their results where it's easy
sql_cache = {}


def get_structure(site):
    if site not in structures:
        with open(os.path.join(structures_path, f"{site}.json")) as f:
            structures[site] = json.load(f)

    return structures[site]


def humansize(nbytes):
    suffixes = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.0
        i += 1
    f = ("%.2f" % nbytes).rstrip("0").rstrip(".")
    return "%s %s" % (f, suffixes[i])


def get_database_filename(site):
    return os.path.join(dbs_path, f"{site}.sqlite3")


def get_all_sites():
    all_sites = []
    for filename in os.listdir(default_structures_path):
        if filename.endswith(".json"):
            all_sites.append(filename[:-5])
    all_sites.sort()
    return all_sites


def get_implemented_sites():
    implemented_sites = []
    for filename in os.listdir(structures_path):
        if filename.endswith(".json"):
            implemented_sites.append(filename[:-5])
    implemented_sites.sort()
    return implemented_sites


def get_implemented_sites_with_names():
    implemented_sites = get_implemented_sites()
    implemented_sites_with_names = []
    for site in implemented_sites:
        structure = get_structure(site)
        implemented_sites_with_names.append({"site": site, "name": structure["name"]})
    return implemented_sites_with_names


def sql_execute(site, c, sql):
    print(f"{site}.sqlite: {sql}")
    sys.stdout.flush()
    return c.execute(sql)


def sql_count(site, table):
    if ("count", site, table) in sql_cache:
        return sql_cache[("count", site, table)]

    conn = sqlite3.connect(get_database_filename(site))
    c = conn.cursor()

    sql_execute(site, c, f"SELECT COUNT(*) FROM '{table}'")
    row = c.fetchone()

    conn.close()

    sql_cache[("count", site, table)] = row[0]
    return sql_cache[("count", site, table)]


def sql_count_search(site, table, cols, search_term):
    if ("count_search", site, table) in sql_cache:
        return sql_cache[("count_search", site, table)]

    conn = sqlite3.connect(get_database_filename(site))
    c = conn.cursor()

    where_clause = build_where_clause(cols, search_term)

    sql_execute(site, c, f"SELECT COUNT(*) FROM '{table}' WHERE {where_clause}")
    row = c.fetchone()

    conn.close()

    sql_cache[("count_search", site, table)] = row[0]
    return sql_cache[("count_search", site, table)]


def sql_headers(site, table):
    conn = sqlite3.connect(get_database_filename(site))
    c = conn.cursor()

    headers = []
    for row in sql_execute(site, c, f"PRAGMA table_info('{table}');"):
        headers.append(row[1])

    conn.close()

    return headers


def sql_select_rows(site, table, limit, offset, sort_col, sort_dir):
    conn = sqlite3.connect(get_database_filename(site))
    c = conn.cursor()

    if sort_col and sort_dir:
        print(f"{sort_col} {sort_dir}")
        if sort_col == "Chronologically":
            headers = sql_headers(site, table)
            sql = f"SELECT * FROM '{table}' ORDER BY CAST('{headers[0]}' AS INTEGER) {sort_dir} LIMIT {limit} OFFSET {offset}"
        else:
            sql = f"SELECT * FROM '{table}' ORDER BY {sort_col} {sort_dir} LIMIT {limit} OFFSET {offset}"
    else:
        sql = f"SELECT * FROM '{table}' LIMIT {limit} OFFSET {offset}"
    rows = []
    for row in sql_execute(site, c, sql):
        rows.append(list(row))

    conn.close()
    return rows


def build_where_clause(cols, search_term):
    return " OR ".join([f"{col} LIKE '%{search_term}%'" for col in cols])


def sql_search_table(site, table, cols, search_term, limit, offset, sort_col, sort_dir):
    conn = sqlite3.connect(get_database_filename(site))
    c = conn.cursor()

    where_clause = build_where_clause(cols, search_term)

    if sort_col and sort_dir:
        print(f"{sort_col} {sort_dir}")
        if sort_col == "Chronologically":
            headers = sql_headers(site, table)
            sql = f"SELECT * FROM '{table}' WHERE {where_clause} ORDER BY CAST({headers[0]} AS INTEGER) {sort_dir} LIMIT {limit} OFFSET {offset}"
        else:
            sql = f"SELECT * FROM '{table}' WHERE {where_clause} ORDER BY {sort_col} {sort_dir} LIMIT {limit} OFFSET {offset}"
    else:
        sql = f"SELECT * FROM '{table}' WHERE {where_clause} LIMIT {limit} OFFSET {offset}"
    rows = []

    for row in sql_execute(site, c, sql):
        rows.append(list(row))

    conn.close()
    return rows


def sql_select_item(site, table, item_id, headers):
    conn = sqlite3.connect(get_database_filename(site))
    c = conn.cursor()

    item_id = item_id.replace("'", "''")

    rows = []
    sql = f"SELECT * FROM '{table}' WHERE {headers[0]}='{item_id}'"
    for row in sql_execute(site, c, sql):
        rows.append(list(row))

    conn.close()
    return rows


def sql_select_join(site, table, item_id, join_from, join_to, headers):
    conn = sqlite3.connect(get_database_filename(site))
    c = conn.cursor()

    item_id = item_id.replace("'", "''")
    dest_table = join_to.split(".")[0]

    rows = []
    sql = f"SELECT '{dest_table}'.* FROM '{dest_table}' JOIN '{table}' ON {join_to}={join_from} WHERE '{table}'.{headers[0]}='{item_id}'"
    for row in sql_execute(site, c, sql):
        rows.append(list(row))

    conn.close()
    return rows


def get_table_display_name(site, table):
    structure = get_structure(site)
    return structure["tables"][table]["display"]


def get_fields(site, table):
    structure = get_structure(site)
    return structure["tables"][table]["fields"]


def get_joins(site, table):
    structure = get_structure(site)
    return structure["tables"][table]["joins"]


def render_frontend():
    return send_file("frontend/dist/index.html")


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    # Make sure BlueLeaks data is all there
    if not os.path.isdir(blueleaks_path):
        return render_template(
            "error.html",
            error_message=f"The BlueLeaks data folder {blueleaks_path} isn't a folder",
        )
    missing_dbs = []
    missing_sites = []
    sites = os.listdir(blueleaks_path)
    for site in get_all_sites():
        if site not in sites:
            missing_sites.append(site)
        if not os.path.isfile(os.path.join(dbs_path, f"{site}.sqlite3")):
            missing_dbs.append(site)
    if len(missing_sites) > 0:
        return render_template(
            "error.html",
            error_message=f"Can't find the unzipped BlueLeaks dataset. Fix the volume that maps to {blueleaks_path} in your docker-compose.yaml.",
        )
    if len(missing_dbs) > 0:
        return render_template(
            "error.html",
            error_message="SQLite3 databases are missing. You probably haven't run the initialize.py script yet.",
        )

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


@app.route("/api/structures")
def api_structures():
    implemented_sites = get_implemented_sites_with_names()

    unimplemented_sites = []
    for site in get_all_sites():
        implemented = False
        for implemented_site in implemented_sites:
            if site == implemented_site["site"]:
                implemented = True
        if not implemented:
            unimplemented_sites.append(site)

    return jsonify(
        {
            "implemented_sites": implemented_sites,
            "unimplemented_sites": unimplemented_sites,
        }
    )


@app.route("/api/structure/create/<site>", methods=["POST"])
def api_structure_create(site):
    # Validate the site
    valid_sites = get_all_sites()
    if site not in valid_sites:
        return jsonify({"error": True, "error_message": "Invalid site"})

    # Is this site already implemented?
    if os.path.exists(os.path.join(structures_path, f"{site}.json")):
        return jsonify(
            {"error": True, "error_message": "That site is already implemented"}
        )

    # Copy the default structure
    shutil.copyfile(
        os.path.join(default_structures_path, f"{site}.json"),
        os.path.join(structures_path, f"{site}.json"),
    )
    return jsonify({"error": False})


@app.route("/api/structure/<site>", methods=["GET", "POST"])
def api_structure(site):
    global structures
    # Validate the site
    valid_sites = get_all_sites()
    if site not in valid_sites:
        print(f"invalid site: {site}")
        return jsonify({"error": True, "error_message": "Invalid site"})

    # Has it been implemented?
    if not os.path.exists(os.path.join(structures_path, f"{site}.json")):
        return jsonify(
            {"error": True, "error_message": "That site hasn't been implemented"}
        )

    if request.method == "GET":
        # Return the structure
        with open(os.path.join(structures_path, f"{site}.json")) as f:
            structure = json.load(f)
        return jsonify({"error": False, "structure": structure})
    elif request.method == "POST":
        # Save the structure
        structure = request.json
        structures[site] = structure
        with open(os.path.join(structures_path, f"{site}.json"), "w") as f:
            f.write(json.dumps(structure, indent=4))
        return jsonify({"error": False})
    else:
        abort(500)


@app.route("/api/sites")
def api_sites():
    return jsonify(get_implemented_sites_with_names())


@app.route("/api/<site>/tables")
def api_tables(site):
    if site not in get_implemented_sites():
        abort(500)

    structure = get_structure(site)

    tables = []
    for table in structure["tables"]:
        if not structure["tables"][table]["hidden"]:
            tables.append(
                {
                    "name": table,
                    "display_name": structure["tables"][table]["display"],
                    "count": sql_count(site, table),
                }
            )
    return jsonify({"site_name": structure["name"], "tables": tables})


@app.route("/api/<site>/<table>")
def api_rows(site, table):
    if site not in get_implemented_sites():
        abort(500)

    structure = get_structure(site)

    if table not in structure["tables"]:
        abort(500)

    headers = sql_headers(site, table)
    limit = request.args.get("count")
    offset = request.args.get("offset")
    sort_col = request.args.get("sortCol")
    sort_dir = request.args.get("sortDir")

    return jsonify(
        {
            "site_name": structure["name"],
            "table_name": get_table_display_name(site, table),
            "headers": headers,
            "rows": sql_select_rows(site, table, limit, offset, sort_col, sort_dir),
            "count": sql_count(site, table),
            "fields": get_fields(site, table),
            "joins": get_joins(site, table),
        }
    )


@app.route("/api/<site>/<table>/search")
def api_search(site, table):
    if site not in get_implemented_sites():
        abort(500)

    structure = get_structure(site)

    if table not in structure["tables"]:
        abort(500)

    search_term = request.args.get("search_term")

    if search_term is None:
        abort(500)

    headers = sql_headers(site, table)
    fields = get_fields(site, table)
    search_cols = [field["name"] for field in fields if field["show"]]
    limit = request.args.get("count")
    offset = request.args.get("offset")
    sort_col = request.args.get("sortCol")
    sort_dir = request.args.get("sortDir")

    return jsonify(
        {
            "site_name": structure["name"],
            "table_name": get_table_display_name(site, table),
            "headers": headers,
            "rows": sql_search_table(
                site, table, search_cols, search_term, limit, offset, sort_col, sort_dir
            ),
            "count": sql_count_search(site, table, search_cols, search_term),
            "fields": fields,
            "joins": get_joins(site, table),
        }
    )


@app.route("/api/<site>/<table>/<item_id>")
def api_item(site, table, item_id):
    if site not in get_implemented_sites():
        abort(500)

    structure = get_structure(site)

    if table not in structure["tables"]:
        abort(500)

    headers = sql_headers(site, table)
    limit = request.args.get("count")
    offset = request.args.get("offset")

    return jsonify(
        {
            "site_name": structure["name"],
            "table_name": get_table_display_name(site, table),
            "headers": headers,
            "rows": sql_select_item(site, table, item_id, headers),
            "fields": get_fields(site, table),
            "joins": get_joins(site, table),
        }
    )


@app.route("/api/<site>/<table>/join/<join_name>/<item_id>/all")
def api_join_all(site, table, join_name, item_id):
    if site not in get_implemented_sites():
        abort(500)

    structure = get_structure(site)

    if table not in structure["tables"]:
        abort(500)

    found_join = False
    for join in structure["tables"][table]["joins"]:
        if join["name"] == join_name:
            found_join = True
            break
    if not found_join:
        abort(500)

    headers = sql_headers(site, table)
    rows = sql_select_join(site, table, item_id, join["from"], join["to"], headers)
    row_count = len(rows)

    join_table = join["to"].split(".")[0]
    join_headers = sql_headers(site, join_table)
    join_fields = get_fields(site, join_table)

    return jsonify(
        {
            "join_table": join_table,
            "join_headers": join_headers,
            "join_rows": rows,
            "join_count": row_count,
            "join_fields": join_fields,
        }
    )


@app.route("/api/<site>/<table>/join/<join_name>/<item_id>")
def api_join(site, table, join_name, item_id):
    if site not in get_implemented_sites():
        abort(500)

    structure = get_structure(site)

    if table not in structure["tables"]:
        abort(500)

    found_join = False
    for join in structure["tables"][table]["joins"]:
        if join["name"] == join_name:
            found_join = True
            break
    if not found_join:
        abort(500)

    headers = sql_headers(site, table)
    rows = sql_select_join(site, table, item_id, join["from"], join["to"], headers)
    row_count = len(rows)
    if row_count > 5:
        rows = rows[0:5]

    join_table = join["to"].split(".")[0]
    join_headers = sql_headers(site, join_table)
    join_fields = get_fields(site, join_table)

    return jsonify(
        {
            "join_table": join_table,
            "join_headers": join_headers,
            "join_rows": rows,
            "join_count": row_count,
            "join_fields": join_fields,
        }
    )


# Copy the builtin structures, if there isn't already a structure there
for site in get_all_sites():
    if os.path.exists(
        os.path.join(builtin_structures_path, f"{site}.json")
    ) and not os.path.exists(os.path.join(structures_path, f"{site}.json")):
        print(f"copying built-in structure: {site}")
        shutil.copyfile(
            os.path.join(builtin_structures_path, f"{site}.json"),
            os.path.join(structures_path, f"{site}.json"),
        )
