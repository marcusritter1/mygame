#!/bin/bash

python3 -m venv game_env
source "game_env/bin/activate"
pip install -r requirements.txt
deactivate