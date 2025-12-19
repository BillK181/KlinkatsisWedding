# globals.py
import os

def get_openai_key():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set in environment")
    return key

DRESS_CODE = "Please plan on dressy, beach formal attire. Think dress pants, suit jackets, dresses and dressy jumpsuits! A dress, suit, or jumpsuit—in lighter colors (avoiding cream and white) and breathable fabrics—are all acceptable for women to wear. If you choose to wear a beachy dress, specifically, consider a tea-length or maxi look to avoid looking too casual. Dressy sandals, chunky heels, and wedges are acceptable footwear options. For men, dress pants/slacks, button down shirts, optional tie and suit jacket is a nice touch. Avoid: tshirts, jeans, too casual pants, casual sundresses."
WEDDING_COLORS = "Greens & White"
GUEST_ARRIVAL_TIME = "3:30pm"
RSVP_DEADLINE = "June 30th, 2026"
FOOD_MENU = "Still being determined"
OPEN_BAR = "Yes"
GIFT_REGISTRY = "Cash, A mansion, The empire state building, A trip to the moon"
KIDS = "Kids are not allowed due to capacity constraints"
HOTEL_BLOCK = "Marriott Irvine Spectrum Center https://book.passkey.com/gt/220960342?gtid=c6987b61e7c49eeb5b9afd67d9a0e70d&mobile=true&dw=375"
BUS_TO_WEDDING = "Departs from Irvine Spectrum Center at 3pm"
BUS_FROM_WEDDING = "Departs from Ole Hanson Beach Club at 10:15 pm heading to Irvine Spectrum Center"
THINGS_TO_DO = "Mention popular and fun activities in CITIES around the time of WEDDING_DATE"
CITIES = "Check out cities around the wedding https://billandmarisa/travel."
WEDDING_LOCATION = "Ole Hanson Beach Club, San Clemente California"
WEDDING_DATE = "August 29th, 2026"
PERSONALITY = "A high end butler who has recently changed careers to become Bill and Marisa's Wedding Helper"
SYSTEM_PROMPT = """You are an assistant for guests of Marisa and Bill's wedding.

- Whenever a guest asks about "cities to visit" or "things to do," always include a clickable link that is stored in the variable CITIES exactly as written.
- Whenever a guest asks about the "hotel block," always include include a clickable link that stored in HOTEL_BLOCK exactly as written.
- Whenever a guest asks about RSVP, always include include a clickable link that stored in RSVP_DEADLINE exactly as written.
- Always respond in your personality
- Do not suggest searching online unless the link variable is empty.
"""



