# video_scene_extractor.py 
import json
import os
from pathlib import Path
import re
from yt_dlp import YoutubeDL
from scenedetect import open_video, SceneManager, ContentDetector, save_images
from config import OUTPUT_JSON_FILE_NAME, VIDEO_TO_DOWNLOAD, YDL_OPTS, SCENE_OUTPUT_DIR, SCENE_THRESHOLD, SCENE_MIN_LENGTH, DEFAULT_VIDEO_OUTPUT_DIR
import moondream as md
from PIL import Image

def download_video(query, output_dir=DEFAULT_VIDEO_OUTPUT_DIR):
    """
    A function to search for a video on YouTube and download it.
    query is the search term, and output_dir is where the video will be saved
    the function returns the name of the downloaded file.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    #Download the best quality video, Avoid downloading playlists, and name the file based on the title of the video
    ydl_opts = YDL_OPTS.copy()
    ydl_opts['outtmpl'] = os.path.join(output_dir, '%(title)s.%(ext)s')
    
    with YoutubeDL(ydl_opts) as ydl:
        print(f"Searching for: {query}")
        # extracts information about videos based on the query 
        search_results = ydl.extract_info(f"ytsearch:{query}", download=False)
        
        # Checks if the search_results dictionary contains a key called 'entries', which is a list of search results.
        if 'entries' in search_results and search_results['entries']:
            first_result = search_results['entries'][0]
            print(f"Found: {first_result['title']} ({first_result['webpage_url']})")
            ydl.download([first_result['webpage_url']]) # Downloads the video using its URL.
            return ydl.prepare_filename(first_result)
        else:
            raise Exception("No results found for the query.")

def detect_scenes_and_save_frames(video_path, output_dir=SCENE_OUTPUT_DIR, threshold=SCENE_THRESHOLD, min_scene_length=SCENE_MIN_LENGTH):
    """
    Detects scenes in a video using PySceneDetect and saves a frame image for each detected scene.

    Args:
        video_path (str): Path to the video file.
        output_dir (str): Directory where scene images will be saved.
        threshold (float): Sensitivity for scene detection (default is SCENE_THRESHOLD).
        min_scene_length (int): Minimum length of a scene in frames (default is SCENE_MIN_LENGTH).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video = open_video(video_path)
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold, min_scene_len=min_scene_length))
    scene_manager.detect_scenes(video, show_progress=True)

    scene_list = scene_manager.get_scene_list() # Get the list of detected scenes

    save_images(scene_list, video, num_images=1, output_dir=output_dir)
    print(f"Detected {len(scene_list)} scenes.")
    return scene_list

# def extract_scene_number(filename):
#     """
#     Extracts the scene number from a filename. 
#     The first numeric group following 'scene' is considered the scene number.
    
#     Args:
#         filename (str): The name of the file.
        
#     Returns:
#         int: The scene number if found, otherwise None.
#     """
#     filename = filename.lower()
#     parts = filename.split()
#     # Search for the part containing 'scene' and extract the number
#     for part in parts:
#         if 'scene' in part:
#             chars = []  # Reset for each potential match
#             seen_digits = False
#             for char in part:
#                 if char.isdigit():
#                     chars.append(char)
#                     seen_digits = True
#                 elif seen_digits:  
#                     break
            
#             # Join and convert to int if any digits were found
#             number = ''.join(chars)
#             if number.isdigit():
#                 return int(number)
#     return None


def generate_scene_captions(model_path, scenes_directory, output_json_file):
    """
    Generate captions for all scenes in the directory and save them to a JSON file.
    """
    scene_captions = {}

    # Initialize model
    try:
        model = md.vl(model=model_path)
        print("Model initialized")
    except Exception as e:
        print(f"Error initializing model: {e}")
        return
    
    # Get all image files
    image_files = list(Path(scenes_directory).glob("*.jpg")) + list(Path(scenes_directory).glob("*.png"))
    
    for image_path in image_files:
        try:
            # scene_number = extract_scene_number(image_path.name)
            # if scene_number is None:
            #     print(f"Skipping {image_path.name} - no scene number found")
            #     continue
            
            image = Image.open(image_path)
            encoded_image = model.encode_image(image)
            caption = model.caption(encoded_image)["caption"]
            
            # Store in dictionary
            scene_captions[str(image_path)] = caption
            print(f"Processed scene {image_path}")
            
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
    
    output_path = output_json_file
    with open(output_path, 'w') as f:
        # Sort by scene number before saving
        sorted_captions = dict(sorted(scene_captions.items()))
        json.dump(sorted_captions, f, indent=2)
    
    print(f"Saved captions to {output_path}")
    return output_path

def json_creation(model_path, query = VIDEO_TO_DOWNLOAD, output_scene_images_dir = SCENE_OUTPUT_DIR, output_json_file_str = OUTPUT_JSON_FILE_NAME):
    try:
        file_path = Path(output_json_file_str)
        if not file_path.exists():
            video_file = download_video(query)
            detect_scenes_and_save_frames(video_file, output_dir = output_scene_images_dir)
            generate_scene_captions(model_path, output_scene_images_dir, output_json_file_str)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    json_creation(model_path="./moondream-2b-int8.mf", query="super mario movie trailer",output_scene_images_dir="scene_images",output_json_file_str="scene_captions.json")
