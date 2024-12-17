# video_scene_extractor.py 
import os
from yt_dlp import YoutubeDL
from scenedetect import open_video, SceneManager, ContentDetector, save_images
from config import YDL_OPTS, SCENE_OUTPUT_DIR, SCENE_THRESHOLD, SCENE_MIN_LENGTH, DEFAULT_VIDEO_OUTPUT_DIR

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

# Main Program
if __name__ == "__main__":
    try:
        video_file = download_video("super mario movie trailer")
        scenes = detect_scenes_and_save_frames(video_file, output_dir="scenes_images")
    except Exception as e:
        print(f"Error: {e}")
