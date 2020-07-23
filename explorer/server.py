import json
from flask import Flask

app = Flask(__name__)

# This gets set below in run()
blueleaks_path = None

# Load structure
with open("./structure.json") as f:
    structure = json.load(f)


@app.route("/")
def hello_world():
    return "Hello, World!"


def run(new_blueleaks_path):
    global blueleaks_path
    blueleaks_path = new_blueleaks_path
    app.run("127.0.0.1", "8080")
