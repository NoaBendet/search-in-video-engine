import json
from pathlib import Path
from config import OUTPUT_JSON_FILE_NAME, THRESHOLD
from fuzzywuzzy import fuzz
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt
from image_helpers import generate_collage
from video_scene_extractor import json_creation
import string


def ask_user_for_search():
    """
    Uses prompt_toolkit to auto-complete user input based on words from captions.
    
    Returns: 
        User input with autocomplete functionality.
    """
    json_file_path = Path(OUTPUT_JSON_FILE_NAME)
    # Load unique words from the captions
    words_list = load_caption_words()
    word_completer = WordCompleter(words_list, ignore_case=True)

    # Prompt user input with autocomplete
    input_word = prompt("Search the video using a word: ", completer=word_completer)
    while not input_word.strip():
        print("Please type a word.")
        input_word = prompt("Search the video using a word: ", completer=word_completer)
    return input_word


def load_caption_words():
    """Load all words from the captions in the JSON file, removing punctuation."""
    json_file_path = Path(OUTPUT_JSON_FILE_NAME)
    words_set = set()  # To store unique words
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            scene_captions = json.load(f)
            for caption in scene_captions.values():
                words = caption.lower().split()
                cleaned_words = [word.strip(string.punctuation) for word in words]
                words_set.update(cleaned_words)
    except json.JSONDecodeError:
        print("Error: JSON file is invalid.") 

    return list(words_set)


def find_matched_captions(input_word):
    """
    Finds and returns a list of scene paths with captions matching the input word using fuzzy search.

    Parameters:
        input_word (str): The word or phrase to search for within scene captions.

    Returns:
        list: A list of scene paths where the captions have a similarity score above the defined `THRESHOLD`.
    """
    matched_scenes = []
    json_file_path = Path(OUTPUT_JSON_FILE_NAME)

    with open(json_file_path, 'r', encoding='utf-8') as f:
        try:
            scene_captions = json.load(f)
            for scene_path, caption in scene_captions.items():
                similarity = fuzz.partial_ratio(input_word.lower(), caption.lower())
                if similarity >= THRESHOLD:
                    matched_scenes.append(scene_path)
        
        except json.JSONDecodeError:
            print("Error: JSON file is invalid.")
            return matched_scenes
        
    return matched_scenes


def search_by_image():
    """
    This function facilitates a search process based on video input, image to text model and user request.
    Returns: 
        a collage based on extracted video frames.
    """
    json_creation(model_path="./moondream-2b-int8.mf", query="super mario movie trailer",output_scene_images_dir="scene_images",output_json_file_str="scene_captions.json")
    input = ask_user_for_search()
    matched_scenes_list = find_matched_captions(input)
    generate_collage(matched_scenes_list)
