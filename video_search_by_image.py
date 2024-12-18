import json
from pathlib import Path
import webbrowser
from config import OUTPUT_JSON_FILE_NAME, SCENE_OUTPUT_DIR, THRESHOLD
from fuzzywuzzy import fuzz
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt
from PIL import Image
import os


def ask_user_for_search():
    """
    Uses prompt_toolkit to auto-complete user input based on words from captions.
    :param json_file_path: Path to JSON file containing captions.
    :return: User input with autocomplete functionality.
    """
    json_file_path = Path(OUTPUT_JSON_FILE_NAME)
    # Load unique words from the captions
    words_list = load_caption_words(json_file_path)
    word_completer = WordCompleter(words_list, ignore_case=True)

    # Prompt user input with autocomplete
    input_word = prompt("Search the video using a word: ", completer=word_completer)
    while not input_word.strip():
        print("Please type a word.")
        input_word = prompt("Search the video using a word: ", completer=word_completer)
    return input_word


def load_caption_words():
    """Load all words from the captions in the JSON file."""
    json_file_path = Path(OUTPUT_JSON_FILE_NAME)
    words_set = set()  # To store unique words
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            scene_captions = json.load(f)
            for caption in scene_captions.values():
                words = caption.lower().split()
                words_set.update(words)
    except json.JSONDecodeError:
        print("Error: JSON file is invalid.") 

    return list(words_set)


def find_matched_captions(input_word):
    # in later use fuzzy search to find similar words
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


def generate_collage(images_path_list):
    # create a collage of the images
    # display the collage on the screen
    # save collage.png file
    # Assuming images_list contains paths to images
    if not images_path_list:
        print("No images found for the given search term.")
        return

    # Define collage dimensions
    collage_width = 800
    collage_height = 600
    output_file = "collage.png"

    create_collage(images_path_list, collage_width, collage_height, output_file)
    webbrowser.open(output_file)


def create_collage(images_path_list, collage_width, collage_height, output_file):
    """
    Creates a collage of images from a folder.
    image_folder: Path to the folder containing images.
    collage_width: Width of the final collage image.
    collage_height: Height of the final collage image.
    output_file: Path to save the output collage image.
    """
    # Load images into a list of PIL Image objects
    images = []
    for image_path in images_path_list:
        image_PIL = Image.open(image_path).convert('RGB')
        images.append(image_PIL)

    # Calculate grid size (rows and columns)
    num_images = len(images)
    
    if num_images == 0:
        print("No images found for the given search term.")
        return

    if num_images == 1:
        cols = 1
    else:
        cols = int(num_images ** 0.5) + 1 
    rows = (num_images // cols)
    if num_images % cols:
        rows += 1
    
    # Resize images to fit into the grid
    thumb_width = collage_width // cols
    thumb_height = collage_height // rows
    resized_images = []
    for img in images:
        resized_img = img.resize((thumb_width, thumb_height))
        resized_images.append(resized_img)

    # Create a blank canvas for the collage
    collage = Image.new('RGB', (collage_width, collage_height), color=(255, 255, 255))

    # Paste images into the collage
    x_offset = 0
    y_offset = 0
    for img in resized_images:
        collage.paste(img, (x_offset, y_offset))
        x_offset += thumb_width
        if x_offset >= collage_width:
            x_offset = 0
            y_offset += thumb_height

    # Save the collage
    collage.save(output_file)
    print(f"Collage created and saved to {output_file}")
    

def search_by_image():
    input = ask_user_for_search()
    matched_scenes_list = find_matched_captions(input)
    generate_collage(matched_scenes_list)

if __name__ == "__main__":
    search_by_image()