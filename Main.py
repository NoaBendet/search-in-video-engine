# Main.py 
from video_scene_extractor import json_creation
# from video_search_by_image import search_by_image
# from video_search_by_video import search_by_video

# def choose_model():
#     # ask the user if he wants to
#     # search the video using an image model (this will perform what you did above and
#     # you don’t need to change that part anymore) or using a video model (what you will do now).
#     print("Welcome to Video Search Engine!🎬")
#     print("To provide you with the best results, please let us know how you'd like to search the video:\n- Type 'i' to search using an image model 🖼.\n- Type 'v' to search using a video model 🎞.")
#     input_word = input()
#     while(input_word.lower() != 'i' and input_word.lower() != 'v'):
#         print("Invalid input. Please type 'i' to search using an image model or 'v' to search using a video model.")
#         input_word = input()
#     if input_word == 'i':
#         return search_by_image
#     else:
#         return search_by_video
    

def Main():
    json_creation(model_path="./moondream-2b-int8.mf", query="super mario movie trailer",output_scene_images_dir="scene_images",output_json_file_str="scene_captions.json")
    # choose_model()


if __name__ == "__main__":
    Main()