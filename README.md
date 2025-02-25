# Python Game

The python modules required to run the game are all inside the virtualenv `game/` folder.

Activate virtualenv with `.\game\Scripts\activate` in Windows.

Run the game via `python main.py`.

Scale texture images: `ffmpeg -i grass.png -vf scale=50:50 grass_scaled.png`.

Install required packages from requirements file `pip install -r requirements.txt`.