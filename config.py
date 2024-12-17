# config.py

# YouTube Downloader Options
YDL_OPTS = {
    'format': 'best',
    'noplaylist': True,
    'outtmpl': './%(title)s.%(ext)s',
}

# Scene Detection Settings
SCENE_OUTPUT_DIR = "scenes_images"
SCENE_THRESHOLD = 30.0
SCENE_MIN_LENGTH = 15

# General Output Directories
DEFAULT_VIDEO_OUTPUT_DIR = "./"
