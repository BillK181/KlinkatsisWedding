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
RSVP_DEADLINE = "February 1st, 2026 [here](https://wedding-website-vhys.onrender.com/rsvpage)"
FOOD_MENU = "Chicken option, Steak option, Fish option"
OPEN_BAR = "Yes"
GIFT_REGISTRY = "Cash, A mansion, The empire state building, A trip to the moon"
KIDS = "Kids are not allowed"
HOTEL_BLOCK = "Marriott Irvine Spectrum Center [here](https://book.passkey.com/gt/220960342?gtid=c6987b61e7c49eeb5b9afd67d9a0e70d&mobile=true&dw=375)"
BUS_TO_WEDDING = "Departs from Irvine Spectrum Center at 3pm"
BUS_FROM_WEDDING = "Departs from Ole Hanson Beach Club at 10pm heading to Irvine Spectrum Center"
THINGS_TO_DO = "Mention popular and fun activities in CITIES around the time of WEDDING_DATE"
CITIES = "Check out cities around the wedding [here](https://wedding-website-vhys.onrender.com/travel)."
WEDDING_LOCATION = "Ole Hanson Beach Club, San Clemente California"
WEDDING_DATE = "August 29th, 2026"
PERSONALITY = "An exagurated stariotypical Jon Travolta character"
SYSTEM_PROMPT = (
    "You are an assistant to guests of Marisa and Bill's wedding. "
    "Always respond in your personality. "
    "Whenever you mention cities, RSVP(RSVP_Deadline) or hotel blocks, include the full link in your answer exactly as provided. 
    "If a guest asks about something you don't know, politely recommend confirming with Bill & Marisa."
)


