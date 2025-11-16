# === Imports ===
from openai import OpenAI
from weddingbot.globals import (
    get_openai_key,
    SYSTEM_PROMPT,
    DRESS_CODE,
    WEDDING_COLORS,
    GUEST_ARRIVAL_TIME,
    RSVP_DEADLINE,
    FOOD_MENU,
    OPEN_BAR,
    GIFT_REGISTRY,
    KIDS,
    HOTEL_BLOCK,
    BUS_TO_WEDDING,
    BUS_FROM_WEDDING,
    THINGS_TO_DO,
    CITIES,
    WEDDING_LOCATION,
    WEDDING_DATE,
    PERSONALITY
)

# === Client Setup ===
client = None  # Will initialize when needed

def get_client():
    """Create OpenAI client using environment variable key."""
    global client
    if client is None:
        key = get_openai_key()
        client = OpenAI(api_key=key)
    return client

# === Helper Function to Call GPT ===
def ask_gpt(messages: list) -> str:
    client = get_client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    return response.choices[0].message.content.strip()

# === Main Program ===
def main():
    # Initialize messages with system prompt and wedding details
    messages = [
        {
            "role": "system",
            "content": f"""
{SYSTEM_PROMPT}

WEDDING DETAILS
---------------
Dress Code: {DRESS_CODE}
Wedding Location: {WEDDING_LOCATION}
Wedding Date: {WEDDING_DATE}
Wedding Colors: {WEDDING_COLORS}
Guest Arrival Time: {GUEST_ARRIVAL_TIME}
RSVP Deadline: {RSVP_DEADLINE}

Food Menu: {FOOD_MENU}
Open Bar: {OPEN_BAR}
Kids Policy: {KIDS}
Gift Registry: {GIFT_REGISTRY}

Hotel Block: {HOTEL_BLOCK}
Bus To Wedding: {BUS_TO_WEDDING}
Bus From Wedding: {BUS_FROM_WEDDING}

Things To Do Instruction: {THINGS_TO_DO}
Local cities to visit: {CITIES}

Personality: {PERSONALITY}
"""
        }
    ]

    print("Weddingbot: Ready to chat! Type 'exit' to quit.")

    try:
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("Weddingbot: See you next time!")
                break
            if not user_input:
                continue

            # Add user message
            messages.append({"role": "user", "content": user_input})

            try:
                # Get GPT reply
                reply = ask_gpt(messages)
                print(f"Weddingbot:\n{reply}")

                # Store assistant response
                messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                print(f"Oops! Something went wrong: {e}")

    except KeyboardInterrupt:
        print("\nWeddingbot: See you next time!")


if __name__ == "__main__":
    main()
