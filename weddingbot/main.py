# === Imports ===
from openai import OpenAI
from . import globals

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

messages = [
    {
        "role": "system",
        "content": f"""
{globals.SYSTEM_PROMPT}

WEDDING DETAILS
---------------
Dress Code: {globals.DRESS_CODE}
Wedding Location: {globals.WEDDING_LOCATION}
Wedding Date: {globals.WEDDING_DATE}
Wedding Colors: {globals.WEDDING_COLORS}
Guest Arrival Time: {globals.GUEST_ARRIVAL_TIME}
RSVP Deadline: {globals.RSVP_DEADLINE}

Food Menu: {globals.FOOD_MENU}
Open Bar: {globals.OPEN_BAR}
Kids Policy: {globals.KIDS}
Gift Registry: {globals.GIFT_REGISTRY}

Hotel Block: {globals.HOTEL_BLOCK}
Bus To Wedding: {globals.BUS_TO_WEDDING}
Bus From Wedding: {globals.BUS_FROM_WEDDING}

Things To Do Instruction: {globals.THINGS_TO_DO}
Local cities to visit: {globals.CITIES}

Personality: {globals.PERSONALITY}
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
