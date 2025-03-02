#!/bin/bash

source "game_env/bin/activate"
pip freeze > requirements.txt
deactivate