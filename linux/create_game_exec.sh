#!/bin/bash

source "game_env/bin/activate"
pyinstaller --onefile --windowed --add-data "assets/:assets/" main.py
deactivate