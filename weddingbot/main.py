# === Imports ===
from openai import OpenAI
from .globals import (
    get_openai_key, SYSTEM_PROMPT, DRESS_CODE, WEDDING_LOCATION, WEDDING_DATE, PERSONALITY,
    HOTEL_BLOCK, BUS_TO_WEDDING, BUS_FROM_WEDDING, THINGS_TO_DO, CITIES, KIDS,
    WEDDING_COLORS, GUEST_ARRIVAL_TIME, RSVP_DEADLINE, FOOD_MENU, OPEN_BAR,
    GIFT_REGISTRY
)

# === Client Setup ===
client = None  # Will initialize when needed

def create_client():
    """Create OpenAI client using environment variable key."""
    key = get_openai_key()
    return OpenAI(api_key=key)

# === Helper Function to Call GPT ===
def ask_gpt(messages: list) -> str:
    global client
    if client is None:
        client = create_client()  # lazy initialization
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    return response.choices[0].message.content.strip()

# === Main Program ===
def main():
    global client
    client = create_client()  # initialize client

    messages = [{
        "role": "system",
        "content": f"{SYSTEM_PROMPT}\n\n{DRESS_CODE}\n\n{WEDDING_LOCATION}\n\n"
                   f"{WEDDING_DATE}\n\n{PERSONALITY}\n\n{HOTEL_BLOCK}\n\n"
                   f"{BUS_TO_WEDDING}\n\n{BUS_FROM_WEDDING}\n\n{THINGS_TO_DO}\n\n"
                   f"{CITIES}\n\n{KIDS}\n\n{WEDDING_COLORS}\n\n{GUEST_ARRIVAL_TIME}\n\n"
                   f"{RSVP_DEADLINE}\n\n{FOOD_MENU}\n\n{OPEN_BAR}\n\n{GIFT_REGISTRY}"
    }]

    print("Weddingbot: Ready to chat! Type 'exit' to quit.")

    try:
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("Weddingbot: See you next time!")
                break
            if not user_input:
                continue

            messages.append({"role": "user", "content": user_input})

            try:
                reply = ask_gpt(messages)
                print(f"Weddingbot:\n{reply}")
                messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                print(f"Oops! Something went wrong: {e}")

    except KeyboardInterrupt:
        print("\nWeddingbot: See you next time!")

if __name__ == "__main__":
    main()
