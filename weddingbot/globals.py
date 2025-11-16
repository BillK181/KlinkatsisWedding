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
RSVP_DEADLINE = "February 1st, 2026"
FOOD_MENU = "Chicken option, Steak option, Fish option"
OPEN_BAR = "Yes"
GIFT_REGISTRY = "Cash, A mansion, The empire state building, A trip to the moon"
KIDS = "Kids are not allowed"
HOTEL_BLOCK = "Marriott Irvine Spectrum Center"
BUS_TO_WEDDING = "Departs from Irvine Spectrum Center at 3pm"
BUS_FROM_WEDDING = "Departs from Ole Hanson Beach Club at 10pm heading to Irvine Spectrum Center"
THINGS_TO_DO = "Mention popular and fun activities in CITIES around the time of WEDDING_DATE"
CITIES = "Link them to /travel to see information on Cities"
WEDDING_LOCATION = "Ole Hanson Beach Club, San Clemente California"
WEDDING_DATE = "August 29th, 2026"
PERSONALITY = "An exagurated stariotypical Jon Travolta character"
SYSTEM_PROMPT = (
    "You are an assistant to guests of Marisa and Bill's wedding. "
    "Always respond in your personality. "
    "If a guest asks about something you don't know, politely recommend confirming with Bill & Marisa."
)


