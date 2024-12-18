def search_by_video():
    pass

def connect_to_gemini():
    pass

def generate_prompt_by_user_input(user_input):
    pass

def ask_user_input():
    print("Using a video model. What would you like me to find in the video?")
    user_input = input()
    while not user_input.strip():
        print("Please type a word.")
        user_input = input()
    return user_input

def chat_with_gemini(prompt):
    pass