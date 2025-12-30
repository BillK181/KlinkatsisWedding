from flask import Flask, session, request, jsonify, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from collections import Counter
from weddingbot.main import (
    ask_gpt, SYSTEM_PROMPT, DRESS_CODE, WEDDING_LOCATION, WEDDING_DATE,
    PERSONALITY, HOTEL_BLOCK, BUS_TO_WEDDING, BUS_FROM_WEDDING, THINGS_TO_DO,
    CITIES, KIDS, WEDDING_COLORS, GUEST_ARRIVAL_TIME, RSVP_DEADLINE,
    FOOD_MENU, OPEN_BAR, GIFT_REGISTRY
)
from guest_list import guest_names

app = Flask(__name__)
app.secret_key = "12345"

# Configure SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wedding.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# ----------------------- MODELS -----------------------
class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    rsvp_status = db.Column(db.String(20), nullable=True)
    dinner_option = db.Column(db.String(50), nullable=True)
    song_request = db.Column(db.String(200), nullable=True)
    login_count = db.Column(db.Integer, default=0, nullable=False)


# Populate database from guest list (only once!)
with app.app_context():
    db.create_all()
    for name in guest_names:
        if not Guest.query.filter_by(name=name).first():
            db.session.add(Guest(name=name))
    db.session.commit()


# ----------------------- HELPERS -----------------------
def get_current_guest():
    """Returns the current logged-in guest and their name, or (None, None) if not logged in."""
    guest_id = session.get('guest_id')
    guest = Guest.query.get(guest_id) if guest_id else None
    if not guest:
        return None, None  # Not logged in
    return guest, guest.name


# ----------------------- ROUTES WITHOUT PAGES -----------------------

# Get guest name (for JS)
@app.route("/get_name")
def get_name():
    guest, name = get_current_guest()
    return jsonify({"name": name})


# Logout
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('guest_id', None)
    return redirect(url_for('login'))

# RSVP
@app.route('/rsvp', methods=['POST'])
def rsvp():
    guest, name = get_current_guest()
    if not guest:
        flash("Error: Guest not found in database.")
        return redirect(url_for('rsvpage'))

    group_number = guest_names.get(name)
    group_members = Guest.query.filter(
        Guest.name.in_([g_name for g_name, g_num in guest_names.items() if g_num == group_number])
    ).all()

    for member in group_members:
        form_key = f"rsvp_{member.name.replace(' ', '_')}"
        rsvp_value = request.form.get(form_key)
        if rsvp_value:
            member.rsvp_status = rsvp_value

    db.session.commit()
    flash(f"Thanks {name}, your group RSVP has been updated!")
    return redirect(url_for('rsvpage'))


# RSVP Status
@app.route("/rsvp-status")
def rsvp_status():
    guests = Guest.query.all()  # or however you fetch your guests

    # RSVP totals
    rsvp_totals = {
        "going": sum(1 for g in guests if g.rsvp_status == "going"),
        "not_going": sum(1 for g in guests if g.rsvp_status == "not_going")
    }

    # Dinner totals
    dinner_totals = {
        "Chicken": sum(1 for g in guests if g.dinner_option == "Chicken"),
        "Beef": sum(1 for g in guests if g.dinner_option == "Beef"),
        "Vegetarian": sum(1 for g in guests if g.dinner_option == "Vegetarian"),
        "Vegan": sum(1 for g in guests if g.dinner_option == "Vegan"),
        "total": sum(1 for g in guests if g.dinner_option)
    }

    # Song request counts
    song_requests = [g.song_request.strip() for g in all_guests if g.song_request]

    song_request = song_counter.items()
    total_song_request = sum(song_counter.values())

    total_logins = sum(g.login_count for g in guests)

    return render_template(
        "check_status.html",
        guests=guests,
        rsvp_totals=rsvp_totals,
        dinner_totals=dinner_totals,
        song_request=song_request
    )


@app.route('/song_request', methods=['POST'])
def song_request():
    guest, name = get_current_guest()
    if not guest:
        flash("Error: Guest not found in database.")
        return redirect(url_for('rsvpage'))

    group_number = guest_names.get(name)
    group_members = Guest.query.filter(
        Guest.name.in_([g_name for g_name, g_num in guest_names.items() if g_num == group_number])
    ).all()

    for member in group_members:
        safe_name = member.name.replace(" ", "_")
        form_key = f"song_request_{safe_name}"
        song_value = request.form.get(form_key)

        if song_value and song_value.strip():  # make sure it's not empty
            member.song_request = song_value.strip()

    db.session.commit()
    flash("Song requests updated!")
    return redirect(url_for('rsvpage'))




# Chatbot
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message")
    guest, name = get_current_guest()

    if not user_input:
        return jsonify({"response": "Please type something!"}), 400

    try:
        # Build system prompt
        system_prompt = "\n\n".join([
            SYSTEM_PROMPT, DRESS_CODE, WEDDING_LOCATION, WEDDING_DATE,
            PERSONALITY, HOTEL_BLOCK, BUS_TO_WEDDING, BUS_FROM_WEDDING,
            THINGS_TO_DO, CITIES, KIDS, WEDDING_COLORS, GUEST_ARRIVAL_TIME,
            RSVP_DEADLINE, FOOD_MENU, OPEN_BAR, GIFT_REGISTRY,
            f"Current guest interacting: {name}"
        ])

        # Get previous chat history from session
        chat_history = session.get('chat_history', [{"role": "system", "content": system_prompt}])

        # Append user message
        chat_history.append({"role": "user", "content": f"{name} says: {user_input}"})

        # Call GPT
        reply = ask_gpt(chat_history)

        # Save GPT's reply
        chat_history.append({"role": "assistant", "content": reply})
        session['chat_history'] = chat_history

        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500


# ----------------------- MAIN PAGES -----------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            flash("Please enter your name.")
            return redirect(url_for('login'))

        name_lower = name.lower()
        if not any(name_lower == guest_name.lower().strip() for guest_name in guest_names):
            flash("Sorry, you're not on the guest list. Please ensure your name matches the invitation.")
            return redirect(url_for('login'))

        guest = Guest.query.filter(db.func.lower(Guest.name) == name_lower).first()
        if not guest:
            flash("Error: Guest not found in database.")
            return redirect(url_for('login'))

        #  track login count
        guest.login_count += 1
        db.session.commit()

        session['guest_id'] = guest.id
        return redirect(url_for('home'))

    return render_template('main_pages/login.html')


@app.route('/')
def home():
    guest, name = get_current_guest()
    if not guest:
        return redirect(url_for('login'))
    return render_template('main_pages/index.html', name=name)


@app.route('/mr-mrs', methods=['GET'])
def mr_mrs():
    _, name = get_current_guest()
    return render_template('main_pages/mr_mrs.html', name=name)


@app.route('/rsvpage', methods=['GET'])
def rsvpage():
    guest, name = get_current_guest()
    if not guest:
        return redirect(url_for('login'))

    # Admin view
    if name and name.strip().lower() == "bkadmin":
        all_guests = Guest.query.order_by(Guest.name).all()

        # RSVP totals
        rsvp_totals = {
            "going": sum(1 for g in all_guests if g.rsvp_status == "going"),
            "not_going": sum(1 for g in all_guests if g.rsvp_status == "not_going")
        }

        # Dinner totals
        dinner_totals = {
            "Chicken": sum(1 for g in all_guests if g.dinner_option == "Chicken"),
            "Beef": sum(1 for g in all_guests if g.dinner_option == "Beef"),
            "Vegetarian": sum(1 for g in all_guests if g.dinner_option == "Vegetarian"),
            "Vegan": sum(1 for g in all_guests if g.dinner_option == "Vegan")
        }

        # Song request counts, sorted most to least
        song_requests = [
            g.song_request.strip()
            for g in all_guests
            if g.song_request
        ]

        # Total logins
        total_logins = sum(g.login_count for g in all_guests)

        return render_template(
            'checkstatus.html',
            name=name,
            guests=all_guests,
            rsvp_totals=rsvp_totals,
            dinner_totals=dinner_totals,
            song_requests=song_requests,
            total_logins=total_logins  
        )


    # Special groups
    if name and name.strip().lower() in ["cs50"]:
        group_number = guest_names.get(name)
        group_members = [
            {"name": guest_name,
             "rsvp_status": Guest.query.filter_by(name=guest_name).first().rsvp_status}
            for guest_name, group in guest_names.items() if group == group_number
        ]
        return render_template('main_pages/rsvp.html', name=name, group_members=group_members)

    # Regular guest view
    group_number = guest_names.get(name)
    group_members = [
        {"name": guest_name, 
         "rsvp_status": Guest.query.filter_by(name=guest_name).first().rsvp_status}
        for guest_name, group in guest_names.items() if group == group_number
    ]
    return render_template('main_pages/rsvpre.html', name=name, group_members=group_members)

@app.route('/travel', methods=['GET'])
def travel():
    _, name = get_current_guest()
    return render_template('main_pages/travel.html', name=name)


@app.route('/registry', methods=['GET'])
def registry():
    _, name = get_current_guest()
    return render_template('main_pages/registry.html', name=name)


@app.route('/faq', methods=['GET'])
def faq():
    _, name = get_current_guest()
    return render_template('main_pages/faq.html', name=name)


@app.route('/checkstatus', methods=['GET'])
def checkstatus():
    guest, name = get_current_guest()
    if name != "bkadmin":
        return redirect(url_for('rsvpage'))

    all_guests = Guest.query.order_by(Guest.name).all()
    return render_template('checkstatus.html', name=name, guests=all_guests)

@app.route('/accommodations', methods=['GET'])
def accommodations():
    _, name = get_current_guest()
    return render_template('main_pages/accommodations.html', name=name)


# ----------------------- CITY PAGES -----------------------
city_routes = [
    "laguna", "newport_beach", "dana_point", "san_clemente",
    "irvine", "san_diego", "los_angeles", "anaheim", "long_beach"
]

for city in city_routes:
    route_name = city
    template_path = f"cities/{city}.html"

    def make_route(template):
        def route():
            _, name = get_current_guest()
            return render_template(template, name=name)
        return route

    app.add_url_rule(f'/{route_name}', route_name, make_route(template_path), methods=['GET'])


# ----------------------- RUN -----------------------
if __name__ == "__main__":
    app.run(debug=True)
