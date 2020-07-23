import json
import subprocess
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# This gets set below in run()
blueleaks_path = None

# Load structure
with open("./structure.json") as f:
    structure = json.load(f)


def render_frontend():
    return render_template("frontend.html")


@app.route("/")
def index():
    return render_frontend()


@app.route("/structure.json")
def structure_json():
    return jsonify(structure)


def run(new_blueleaks_path):
    global blueleaks_path
    blueleaks_path = new_blueleaks_path
    app.run("127.0.0.1", "8080")
