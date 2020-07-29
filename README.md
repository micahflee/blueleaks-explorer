# BlueLeaks Explorer

Software for journalists to use to inspect all of the data in the BlueLeaks dump.

## Getting started

You need to build the default structures and then import the data, like:

```sh
cd src
./app.py structure --blueleaks-path /media/user/blueleaks/
./app.py import --blueleaks-path /media/user/blueleaks/
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
