import os
from dotenv import load_dotenv
import google.generativeai as genai
import cv2
import os
import numpy as np
from config import EXTRACTED_IMAGES_DIR
from image_helpers import generate_collage

def ask_user_input():
    print("Using a video model. What would you like me to find in the video?")
    user_input = input()
    while not user_input.strip():
        print("Please type a word.")
        user_input = input()
    return user_input


def connect_to_gemini():
    """
    Connect to Gemini API using API key from .env file
    Returns configured Gemini model
    """
    try:
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model

    except ValueError as ve:
        print(f"Error: {ve}")
        raise  
    except Exception as e:
        print(f"An unexpected error occurred while connecting to Gemini: {e}")
        raise


def chat_with_gemini(user_input):
    model = connect_to_gemini()
    prompt = f"""
    You are a video search engine. You are given a video and you need to find the best scenes that match the user input. 
    User input: {user_input}
    return ONLY by this format:
    [[start1, end1], [start2, end2], [start3, end3], ...]
    start and end are numbers which represent seconds in the video.
    """
    # TODO: add the video ! 
    response = model.generate_content(prompt, max_output_tokens=148, temperature=0.4) 
    print(response.text) # TODO: delete before commit
    return response


def extract_frames_from_video(time_ranges, timestamp_period=3, video_path="./The Super Mario Bros. Movie ｜ Official Trailer.mp4"):
    """
    Extracts frames from the video based on given time ranges.
    
    Args:
        time_ranges (list): List of time ranges in seconds (e.g., [[start1, end1], [start2, end2]]).
        timestamp_period (int): The period in seconds to extract frames. Defaults to 3. (make sure that the extracted frames are not too close to each other)
        video_path (str): Path to the video mp4 file.
    
    Returns:
        str: The folder where the images are extracted and saved.
    """
    # Ensure the video file exists
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"The video file '{video_path}' was not found.")
    
    output_dir = EXTRACTED_IMAGES_DIR 
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the video
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        raise ValueError(f"Could not open the video file '{video_path}'.")
    
    frames_per_second = video.get(cv2.CAP_PROP_FPS)
    extracted_files = []

    for time_range in time_ranges:
        if not time_range or len(time_range) != 2:
            continue
        start, end = time_range
        start = int(start)
        end = int(end)
        if start < 0 or end < 0 or start > end:
            continue    
        for time in np.arange(start, end + 1, timestamp_period):  # Extract frames every 1 second
            frame_number = int(time * frames_per_second)
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_number) 
            success, frame = video.read()
            if success:
                # Save the frame as an image file
                output_file = os.path.join(output_dir, f"frame_{int(time)}s.jpg")
                cv2.imwrite(output_file, frame)
                extracted_files.append(output_file)
            else:
                print(f"Warning: Could not extract frame at {time} seconds.")

    video.release()  
    return output_dir


def create_collage(frame_paths, output_path):
    """
    Creates a collage from a list of frame paths.
    Args:
        frame_paths (list): A list of paths to frame images.
        output_path (str): Path to save the final collage.
    """
    pass


def search_by_video():
    user_input = ask_user_input()
    response = chat_with_gemini(user_input)
    extract_frames_from_video(response.text)
    directory_name = create_collage(response.text)
    generate_collage(os.listdir(directory_name))

if __name__ == "__main__":
    search_by_video()