# BlueLeaks Explorer

Software for journalists to use to inspect all of the data in the BlueLeaks dump.

## Getting started

You need to build the default structures and then import the data, like:

```sh
./app.py structure --blueleaks-path /media/user/blueleaks/
./app.py import --blueleaks-path /media/user/blueleaks/
```

Building the default structures will create a 98mb of JSON files in the `structures/default` folder. And importing will take a long time and create 4.7gb of sqlite3 databases in your `databases` folder.

And you need to install node modules and build the js bundle:

```sh
cd frontend
npm install
./build.js
```

Then start the server:

```sh
./app.py server --blueleaks-path /media/user/blueleaks/
```

If you're actively developing, you can also monitor for changes and rebuild the frontend with:

```sh
cd frontend
npm run dev
```
