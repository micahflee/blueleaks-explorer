#!/bin/bash
cd frontend
./build.js
cd ..
./app.py server --blueleaks-path /media/user/blueleaks/
