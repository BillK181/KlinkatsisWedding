# === Imports ===

from openai import OpenAI
# ^ This comes from the OpenAI Python SDK docs.
# You install the library with `pip install openai`.
# "OpenAI" is the client class provided by the library.

from .globals import (
    key, SYSTEM_PROMPT, DRESS_CODE, WEDDING_LOCATION, WEDDING_DATE, PERSONALITY,
    HOTEL_BLOCK, BUS_TO_WEDDING, BUS_FROM_WEDDING, THINGS_TO_DO, CITIES, KIDS,
    WEDDING_COLORS, GUEST_ARRIVAL_TIME, RSVP_DEADLINE, FOOD_MENU, OPEN_BAR,
    GIFT_REGISTRY
)
# ^ This is a Python relative import (notice the dot).
# It just pulls constants from your own "globals.py" file.
# This part is your own project design — not from OpenAI.


# === Client Setup ===

client = OpenAI(api_key=key)
# ^ From OpenAI docs. Creates a "client" object to talk to the API.
# You pass in your API key so the server knows who you are.


# === Helper Function to Call GPT ===

def ask_gpt(messages: list) -> str:
    # ^ "def" is Python syntax for defining a function.
    # ": list" is a type hint (says `messages` should be a list).
    # "-> str" means the function will return a string.

    response = client.chat.completions.create(
        model="gpt-4o",     # <- From OpenAI docs: name of the model to use
        messages=messages   # <- Must be a list of dicts with "role" and "content"
    )
    # ^ This exact method ("chat.completions.create") comes from OpenAI’s SDK.
    # You’d find it in their docs.

    return response.choices[0].message.content.strip()
    # ^ Also from OpenAI docs: "choices[0].message.content" is where the reply text lives.
    # ".strip()" is just plain Python (removes extra whitespace).


# === Main Program ===

def main():
    # This is a normal Python function.

    # Build the initial system prompt
    messages = [{
        "role": "system",  # <- Required by OpenAI: "system" gives context/instructions
        "content": f"{SYSTEM_PROMPT}\n\n{DRESS_CODE}\n\n{WEDDING_LOCATION}\n\n"
                   f"{WEDDING_DATE}\n\n{PERSONALITY}\n\n{HOTEL_BLOCK}\n\n"
                   f"{BUS_TO_WEDDING}\n\n{BUS_FROM_WEDDING}\n\n{THINGS_TO_DO}\n\n"
                   f"{CITIES}\n\n{KIDS}\n\n{WEDDING_COLORS}\n\n{GUEST_ARRIVAL_TIME}\n\n"
                   f"{RSVP_DEADLINE}\n\n{FOOD_MENU}\n\n{OPEN_BAR}\n\n{GIFT_REGISTRY}"
    }]
    # ^ This is both OpenAI docs + your own design.
    # "messages" must be a list of dicts with "role" and "content".
    # The f-string (f"...") is just Python string formatting — inserts your constants.

    print("Weddingbot: \nA?")
    # ^ Plain Python: print to console. "\n" means new line.

    try:
        while True:  # <- Infinite loop, standard Python.
            user_input = input("You: ").strip()
            # ^ input() is built-in Python: waits for user typing.
            # .strip() is Python: removes spaces before/after.

            if user_input.lower() in ["exit", "quit"]:
                # ^ .lower() makes it lowercase (Python string method).
                # in [...] checks if it matches.
                print("Weddingbot: See you next time!")
                break  # <- exit loop.

            if not user_input:
                continue  # <- skip empty lines.

            # Add the user's message to conversation history
            messages.append({"role": "user", "content": user_input})
            # ^ Append = plain Python list method.
            # The dict format {"role": ..., "content": ...} is from OpenAI API rules.

            try:
                reply = ask_gpt(messages)  # <- Call your helper function
                print(f"Weddingbot:\n{reply}")
                # ^ f-string again: inserts the reply.

                messages.append({"role": "assistant", "content": reply})
                # ^ Append assistant’s reply to the conversation history
                # so next round GPT has context.

            except Exception as e:
                # ^ Standard Python error handling.
                print(f"Oops! Something went wrong: {e}")

    except KeyboardInterrupt:
        # ^ Handles Ctrl+C.
        print("\nWeddingbot: See you next time!")


# === Run Program if File is Main ===

if __name__ == "__main__":
    main()
# ^ This is a standard Python idiom.
# It makes sure main() only runs if this file is executed directly.
