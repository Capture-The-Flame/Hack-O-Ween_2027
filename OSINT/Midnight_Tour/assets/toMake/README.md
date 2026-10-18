## How to run challenge

**With Docker (recommended):**
Make sure to have docker running in the background. Make sure you are in the assets folder directory then type the command:

    docker-compose up --build

Site can be seen at `http://localhost:8000`

**Without Docker:**
No dependencies, Python 3 standard library only. From the `assets/app` folder run:

    python3 app.py

Site can be seen at `http://localhost:8000`

The flag and gate password are set at the top of `app/app.py`.

## Rebuilding the images and audio

Only needed if you change the pumpkin count, the GPS location, or the voicemail script. From this folder:

    pip install pillow && python3 make_images.py
    ./make_audio.sh        # macOS only (uses the built-in `say` command)
