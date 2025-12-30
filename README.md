# BillandMarisa.com

BillandMarisa.com is a sophisticated Flask web application designed to celebrate and streamline our wedding, featuring intuitive RSVP management, immersive travel pages, and custom-designed sections tailored for guests.  

Built with love and attention to detail, this project combines interactivity, style, and seamless navigation to make wedding planning both elegant and effortless.

---

## 🌟 Features

- 🗓️ **RSVP Form** — Guests can easily confirm or update their attendance, dinner choice, and song request. Responses are stored securely in the local SQLite database (wedding.db), with real-time validation to ensure accurate and up-to-date guest information. Log in as cs50 to view the RSVP page (will go live for all when invitations are sent)

- 🏙️ **City Pages** — Travel pages for nearby cities are generated dynamically from a list of templates, making it easy to add new cities. Each page includes images, descriptions, and links for trip planning, styled consistently with cities.css.

- 🤖 **AI-Powered Chatbot** — A conversational assistant built with the OpenAI API (`gpt-4o`). The AI-Powered Chatbot on **BillandMarisa.com** recognizes logged-in guests, addresses them by name, and answers questions about travel, the registry, schedules, and wedding logistics. The chatbot’s logic lives in `weddingbot/`, where a lightweight wrapper function (`ask_gpt`) manages API calls and maintains chat history for personalized, natural responses.

- 🔐 **Login System** — Simple name-based authentication with secure logout functionality, enabling personalized experiences for each guest and allowing the chatbot to tailor responses accordingly. 

- 💞 **Custom Design** — Multiple themed CSS files tailor the look and feel of different site sections, creating a polished, cohesive, and user-friendly interface.  

- 📅 **Countdown Timer** — A dynamic countdown displays the remaining time until the wedding, providing an engaging, real-time element for guests to enjoy.

---

## ⚙️ Tech Stack

Backend:  
- Python 3  
- Flask (Jinja2 templating)  
- SQLite (wedding.db)  

Frontend:  
- HTML  
- CSS  
- JavaScript  

---

## 🗂️ Folder Structure

ww/
│
├── .gitignore
├── README.md
├── app.py
├── guest_list.py
├── requirements.txt
│
├── instance/
│   └── wedding.db
│
├── static/
│   ├── css/
│   │   ├── accommmodations.css
│   │   ├── chatbot.css
│   │   ├── checkstatus.css
│   │   ├── cities.css
│   │   ├── countdown.css
│   │   ├── faq.css
│   │   ├── login.css
│   │   ├── mr_mrs.css
│   │   ├── registry.css
│   │   ├── rsvp.css
│   │   ├── rsvpre.css
│   │   ├── styles.css
│   │   └── travel.css
│   │
│   ├── js/
│   │   ├── chatbot.js
│   │   └── countdown.js
│   │
│   └── images/
│       ├── anaheim.jpg
│       ├── dana_point.jpg
│       ├── favicon2.png
│       ├── footerlogo.png
│       ├── gracewedding.jpg
│       ├── honeymoon.png
│       ├── irvine.jpg
│       ├── irvinemarriottt.jpg
│       ├── laguna.jpg
│       ├── load.jpg
│       ├── load_mobile.jpg
│       ├── long_beach.jpg
│       ├── los_angeles.jpg
│       ├── marisabill.png.jpg
│       ├── navlogo.png
│       ├── newport_beach.jpg
│       ├── olersvp.mp4
│       ├── oletwo.jpg
│       ├── rsvpbackground.jpg
│       ├── san_clemente.jpg
│       ├── san_diego.jpg
│       ├── southerncaliforniamap.jpg
│       ├── stephweddinng.jpg
│       ├── waves_horizontal.mp4
│       ├── waves_vertical.mp4
│       ├── wedding-bg.jpg
│       └── zackwedding.jpg
│
├── templates/
│   ├── base.html
│   ├── checkstatus.html
│   ├── main_pages/
│   │   ├── accommodations.html
│   │   ├── faq.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── mr_mrs.html
│   │   ├── registry.html
│   │   ├── rsvp.html
│   │   ├── rsvpre.html
│   │   └── travel.html
│   │
│   └── cities/
│       ├── anaheim.html
│       ├── dana_point.html
│       ├── irvine.html
│       ├── laguna.html
│       ├── long_beach.html
│       ├── los_angeles.html
│       ├── newport_beach.html
│       ├── san_clemente.html
│       └── san_diego.html
│
└── weddingbot/
    ├── __init__.py
    ├── globals.py
    └── main.py

---

## 🚀 Getting Started

### Option 1: Visit the Live Website
The site is always available at **[BillandMarisa.com](https://BillandMarisa.com)**.  
Guests can access the RSVP form, city pages, countdown timer, and AI-powered chatbot directly from their browser.  

Sign in as `"cs50"` to use personalized features, including confirming your RSVP, selecting a dinner option, submitting a song request, and chatting with the AI assistant.

### Option 2: Run Locally
If you want to run the site on your own machine for testing or development:  

1. Set Up Your Environment

Create and activate a virtual environment (recommended):

python3 -m venv venv
source venv/bin/activate  # macOS / Linux
# or
venv\Scripts\activate     # Windows

2. Install Dependencies

pip install flask
pip install flask_sqlalchemy  # if using SQLAlchemy

3. Run the App

Make sure you’re in the project’s root folder (where app.py is), then run:

flask run
# or
python app.py

By default, it will run at:
http://127.0.0.1:5000


4. Sign In

Sign in as "cs50"

---

## 🧩 How It Works

### Templates & Routing
- Each HTML file under `templates/` corresponds to a route in `app.py` and extends `base.html` for consistent headers, footers, and navigation.  
- Flask uses Jinja2 templating to inject server-side dynamic content, including personalized greetings, RSVP status, and chatbot interactions.  
- City pages are generated dynamically from a list of routes, allowing new city pages to be added without modifying core routing logic.

### Database (SQLite)
- Guest RSVP data is stored in `wedding.db`.  
- The RSVP form validates input and updates the database in real time, allowing guests to confirm or change their attendance, choose or update their dinner option, and submit a song request.
- Admins can view all RSVP data through the admin accout, using Python-based permissions in app.py. Additional routes—rsvp, dinner_option, and song—handle storing information and displaying totals such as attendance counts, dinner selections, and the most-requested songs.

### Chatbot
- A conversational chatbot lives in `weddingbot/` and handles guest inquiries interactively.  
- It uses the OpenAI API (via ask_gpt()) to generate natural-language responses using the gpt-4o model.
- It recognizes the logged-in guest and addresses them by name, creating a personalized experience.  
- The chatbot answers questions about travel, registry, or the wedding schedule using a keyword-based system powered by `globals.py` and `main.py`.  
- Chat history is stored in the session, and its modular design allows future expansion without altering core app functionality.

### City Pages
- All travel and city information is under `templates/cities/` and styled consistently with `static/css/cities.css`.  
- Each city page features images, descriptions, directions from the hotel, and links to make it easy for guests to plan their visit.  
- New city pages can be added by copying an existing template, updating content and images, and adding the route to the city routes list in `app.py`.

### Static Assets
- All CSS, JavaScript, and images are served from the `static/` directory, keeping styling and interactivity consistent across the site.  
- JavaScript files handle countdown timers, chatbot interactivity, and other dynamic features, while CSS ensures themed and responsive layouts.

---

## 👰🤵 About

Developed by: Bill Klinkatsis
Purpose: **BillandMarisa.com** celebrates Bill and Marisa's wedding with a creative, interactive website for guests.
Company: ThrillBill FullStack
