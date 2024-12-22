# Main.py 
from video_search_by_image import search_by_image
from video_search_by_video import search_by_video

def choose_model():
    """
    Allows the user to select the model for video search.

    Returns:
        function: `search_by_image` if the user selects Search using an image model: Processes the search by analyzing an image.
                  `search_by_video` if the user selects Search using a video model: Processes the search by analyzing a video.
    """
    print("Welcome to Video Search Engine!🎬")
    print("To provide you with the best results, please let us know how you'd like to search the video:\n- Type 'i' to search using an image model 🖼.\n- Type 'v' to search using a video model 🎞.")
    input_word = input()
    while(input_word.lower() != 'i' and input_word.lower() != 'v'):
        print("Invalid input. Please type 'i' to search using an image model or 'v' to search using a video model.")
        input_word = input()
    if input_word == 'i':
        return search_by_image()
    else:
        return search_by_video()
    

def Main():
    choose_model()


if __name__ == "__main__":
    Main()