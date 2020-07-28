# BlueLeaks Explorer

Software for journalists to use to inspect all of the data in the BlueLeaks dump.

## Getting started

You need to build the default structure and then import the data, like:

```sh
./app.py structure --blueleaks-path /media/user/blueleaks/
./app.py import --blueleaks-path /media/user/blueleaks/
```

Creating the structure will create a 103mb `default-structure.json` file. And importing will take a long time and create 4.7gb of sqlite3 databases in your `databases` folder.

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
