import difflib

# Predefined prompts
prompts = ["hello", "hi", "hey"]

# Test input
user_input = "hello"

# Finding the closest match
closest_prompt = difflib.get_close_matches(user_input, prompts, n=1, cutoff=0.5)

if closest_prompt:
    print(f"Closest prompt: {closest_prompt[0]}")
else:
    print("No close match found")