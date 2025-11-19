# globals.py
import os

def get_openai_key():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set in environment")
    return key

DRESS_CODE = "beachy cocktail attire"
WEDDING_COLORS = "Green & Blue"
GUEST_ARRIVAL_TIME = "4:00pm"
RSVP_DEADLINE = "February 1st, 2026 [here](https://billandmarisa/rsvpage)"
FOOD_MENU = "Chicken option, Steak option, Fish option"
OPEN_BAR = "Yes"
GIFT_REGISTRY = "Cash, A mansion, The empire state building, A trip to the moon"
KIDS = "Kids are not allowed"
HOTEL_BLOCK = "Marriott Irvine Spectrum Center [here](https://book.passkey.com/gt/220960342?gtid=c6987b61e7c49eeb5b9afd67d9a0e70d&mobile=true&dw=375)"
BUS_TO_WEDDING = "Departs from Irvine Spectrum Center at 3pm"
BUS_FROM_WEDDING = "Departs from Ole Hanson Beach Club at 10pm heading to Irvine Spectrum Center"
THINGS_TO_DO = "Mention popular and fun activities in CITIES around the time of WEDDING_DATE"
CITIES = "Check out cities around the wedding [here](https://billandmarisa/travel)."
WEDDING_LOCATION = "Ole Hanson Beach Club, San Clemente California"
WEDDING_DATE = "August 29th, 2026"
PERSONALITY = "An exagurated stariotypical Jon Travolta character"
SYSTEM_PROMPT = """You are an assistant for guests of Marisa and Bill's wedding.

- Whenever a guest asks about "cities to visit" or "things to do," always include a clickable link that is stored in the variable CITIES exactly as written.
- Whenever a guest asks about the "hotel block," always include include a clickable link that stored in HOTEL_BLOCK exactly as written.
- Whenever a guest asks about RSVP, always include include a clickable link that stored in RSVP_DEADLINE exactly as written.
- Always respond in your personality. Never give any hints as to who you are
- Do not suggest searching online unless the link variable is empty.
"""



