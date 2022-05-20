# BlueLeaks Explorer

BlueLeaks Explorer is open source software for journalists to investigate all of the data in the [BlueLeaks dataset](https://ddosecrets.com/wiki/BlueLeaks).

## How it Works

The BlueLeaks dataset contains hundreds of folders with names like `ncric` (Northern California Regional Intelligence Center), `arictexas` (Austin Regional Intelligence Center), and `memiac` (Maine Information Analysis Center). Each of these folders includes data from a different hacked law enforcement website.

These websites use Microsoft Access databases, and the data from these databases is available in hundreds of CSV files with names like `EmailBuilder.csv` (all of the bulk emails sent by the website), `Registrations.csv` (details about everyone who has an account on the website), and `SARs.csv` ("suspicious activity reports").

BlueLeaks Explorer is a tool that lets you visualize and search the data in these CSV files. Each BlueLeaks site is different--it has a different structure, with different tables that are related to each other in different ways. Exactly how a BlueLeaks site should be laid out is called its _structure_, and you can use BlueLeaks Explorer to define it.

For example, for each table you choose which fields are interesting and should be displayed, and you can hide the rest. You can define the type of each field. If a field represents a path to a document in BlueLeaks, you can make it link directly to that document. If it's a path to an image in the BlueLeaks data, you can make it display the image. If it's includes HTML, you can render the HTML. You can also define relationships between tables--you can make it so when you view a row in `DocumentCategory`, it displays all of the `Document` rows in that categy. And when you view a `Docuument` it displays the actual `DocumentCategory` that it's associated with instead of just a `DocumentCategoryID`.

## Getting Started

To run BlueLeaks Explorer on your computer, you need [Docker](https://www.docker.com/products/docker-desktop/) installed.

When you run the [BlueLeaks Explorer Docker image](https://hub.docker.com/r/micahflee/blueleaks-explorer/tags), you must mount these volumes:

* `/data/blueleaks`: Path to extracted BlueLeaks data (for example, `/Volumes/datasets/BlueLeaks-extracted`)
* `/data/databases`: Folder for sqlite3 databases
* `/data/structures`: Folder for structure JSON files
* `/data/structures-default`: Folder for default structure JSON files

Before you can run it for the first time, you must build the default structures and then import data from all of the CSV files into SQLite databases. You can do this by running `poetry run ./app.py init` in the container, like this:

```sh
# Build the default structures
docker run \
    -p 8080:8080 \
    -v /Volumes/datasets/BlueLeaks-extracted/:/data/blueleaks \
    -v $(pwd)/databases:/data/databases \
    -v $(pwd)/structures:/data/structures \
    -v $(pwd)/structures-default:/data/structures-default \
    micahflee/blueleaks-explorer \
    poetry run ./app.py init
```

Building the default structures will create a 98mb of JSON files in the `structures/default` folder. And importing will take a long time and create 4.7gb of sqlite3 databases in your `databases` folder.

And you need to install node modules and build the js bundle:

```sh
cd src/frontend
npm install
./build.js
```

Then start the server:

```sh
cd src
./app.py server --blueleaks-path /media/user/blueleaks/
```

If you're actively developing, you can also monitor for changes and rebuild the frontend with:

```sh
cd src/frontend
npm run dev
```

## Docker

To build the docker container:

```sh
docker build src -t blueleaks-explorer
```

Then to run the container mounting these volumes:

* `/data/blueleaks`: Extracted BlueLeaks data
* `/data/databases`: Directory for sqlite3 databases
* `/data/structures`: Directory for structure JSON files
* `/data/structures-default`: Directory for default structure JSON files

```sh
docker run \
    -p 8080:8080 \
    -v /media/user/blueleaks/:/data/blueleaks \
    -v $(pwd)/databases:/data/databases \
    -v $(pwd)/structures:/data/structures \
    -v $(pwd)/structures-default:/data/structures-default \
    blueleaks-explorer
```
