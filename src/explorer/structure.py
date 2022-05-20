import os
import click
import json
import csv
from glob import glob

from .common import sanitize_field_name, get_default_structures_dir

blueleaks_path = os.environ.get("BLE_BLUELEAKS_PATH")

def run():
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

            json_filename = os.path.join(get_default_structures_dir(), f"{site}.json")
            with open(json_filename, "w") as f:
                f.write(json.dumps(structure, indent=4))
            click.secho(f"Wrote {json_filename}", dim=True)
