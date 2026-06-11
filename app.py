from flask import Flask, session, request, jsonify, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
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

migrate = Migrate(app, db)


# ----------------------- MODELS -----------------------
class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    wedding_rsvp = db.Column(db.String(20), nullable=False, server_default="pending")
    dinner_option = db.Column(db.String(50), nullable=False, server_default="pending")
    cocktail_rsvp = db.Column(db.String(20), nullable=False, server_default="pending")
    song_request = db.Column(db.String(200), nullable=True)
    login_count = db.Column(db.Integer, default=0, nullable=False)


# Populate database from guest list
def seed_database():
    with app.app_context():

        # Add new guests
        for name in guest_names:
            if not Guest.query.filter_by(name=name).first():
                db.session.add(
                    Guest(
                        name=name,
                        wedding_rsvp="pending",
                        dinner_option="pending",
                        cocktail_rsvp="pending",
                        song_request=""
                    )
                )

        # Remove guests no longer in guest_names
        for guest in Guest.query.all():
            if guest.name not in guest_names:
                db.session.delete(guest)

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
        return redirect(url_for('login', next='/rsvpage'))

    raw_group = guest_names.get(name)

    if isinstance(raw_group, list):
        group_numbers = raw_group
        is_multi_group = True
    else:
        group_numbers = [raw_group]
        is_multi_group = False

    group_members = Guest.query.filter(
        Guest.name.in_(
            [
                g_name
                for g_name, g_num in guest_names.items()
                if (
                    g_num in group_numbers
                    if isinstance(g_num, int)
                    else any(x in group_numbers for x in g_num)
                )
            ]
        )
    ).all()

    for member in group_members:
        suffix = member.name.replace(' ', '_')

        wedding_rsvp = request.form.get(f"wedding_rsvp_{suffix}")
        cocktail_rsvp = request.form.get(f"cocktail_rsvp_{suffix}")
        song_request = request.form.get(f"song_request_{suffix}", "").strip().title()
        dinner_option = request.form.get(f"dinner_option_{suffix}")

        if wedding_rsvp:
            member.wedding_rsvp = wedding_rsvp

        if member.wedding_rsvp == "not_going":
            member.cocktail_rsvp = "Not Attending"
            member.song_request = None
            member.dinner_option = "Not Attending"

        else:
            if cocktail_rsvp:
                member.cocktail_rsvp = cocktail_rsvp

            if song_request:
                member.song_request = song_request

            if not is_multi_group and dinner_option:
                member.dinner_option = dinner_option

    db.session.commit()

    flash(f"Thanks {name}, your RSVP was updated!")
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

    # -----------------------
    # GET
    # -----------------------
    if request.method == 'GET':
        next_page = request.args.get('next')

        if next_page:
            session['next'] = next_page  # 🔥 STORE IT

        return render_template('main_pages/login.html')

    # -----------------------
    # POST
    # -----------------------
    name = request.form.get('name', '').strip()

    if not name:
        flash("Please enter your name.")
        return redirect(url_for('login'))

    name_lower = name.lower()

    # validate guest list
    if not any(name_lower == g.lower().strip() for g in guest_names):
        flash("Sorry, you're not on the guest list.")
        return redirect(url_for('login'))

    guest = Guest.query.filter(
        db.func.lower(Guest.name) == name_lower
    ).first()

    if not guest:
        flash("Guest not found in database.")
        return redirect(url_for('login'))

    # -----------------------
    # LOGIN SUCCESS
    # -----------------------
    guest.login_count += 1
    db.session.commit()

    session['guest_id'] = guest.id

    # 🔥 THE IMPORTANT PART
    next_page = session.pop('next', None)

    if not next_page or not next_page.startswith('/'):
        next_page = url_for('home')

    return redirect(next_page)

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
        return redirect(url_for('login', next=request.path))

    name_clean = name.strip().lower()

    # admin redirect
    if name_clean == "bkadmin":
        return redirect(url_for('checkstatus'))

    raw_group = guest_names.get(name)

    # normalize current user's group(s)
    if isinstance(raw_group, list):
        group_numbers = raw_group
    else:
        group_numbers = [raw_group]

    # build group members
    group_members = []

    for guest_name, group in guest_names.items():

        # normalize each guest's group(s)
        guest_groups = group if isinstance(group, list) else [group]

        # check overlap between user's groups and this guest's groups
        if any(g in group_numbers for g in guest_groups):

            g = Guest.query.filter_by(name=guest_name).first()
            if not g:
                continue

            group_members.append({
                "name": g.name,
                "wedding_rsvp": g.wedding_rsvp,
                "dinner_option": g.dinner_option,
                "cocktail_rsvp": g.cocktail_rsvp,
                "song_request": g.song_request,

                # 🔥 important fix: per-member flag
                "has_multiple_groups": isinstance(group, list)
            })

    return render_template(
        'main_pages/rsvp.html',
        name=name,
        group_members=group_members
    )

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

    if not guest:
        return redirect(url_for('login', next=request.path))

    all_guests = sorted(
        Guest.query.all(),
        key=lambda g: g.name.split()[-1].lower()
    )

    # ONLY ADMIN SEES THIS
    if name and name.strip().lower() == "bkadmin":

        wedding_totals = {
            "going": sum(1 for g in all_guests if g.wedding_rsvp == "going"),
            "not_going": sum(1 for g in all_guests if g.wedding_rsvp == "not_going")
        }

        kids_meal_total = sum(
            1 for g in all_guests
            if g.wedding_rsvp == "going"
            and g.dinner_option in [None, "", "pending"]
        )

        dinner_totals = {
            "Beef": sum(1 for g in all_guests if g.dinner_option == "Beef"),
            "Fish": sum(1 for g in all_guests if g.dinner_option == "Fish"),
            "Vegetarian": sum(1 for g in all_guests if g.dinner_option == "Vegetarian"),

            "Kids": kids_meal_total,

            "total": (
                sum(1 for g in all_guests if g.dinner_option in ["Beef", "Fish", "Vegetarian"])
                + kids_meal_total
            )
        }

        cocktail_totals = {
            "going": sum(1 for g in all_guests if g.cocktail_rsvp == "going"),
            "not_going": sum(1 for g in all_guests if g.cocktail_rsvp == "not_going")
        }

        song_counter = Counter(
            g.song_request.strip()
            for g in all_guests
            if g.song_request and g.song_request.strip() not in ["—", ""]
        )

        sorted_songs = song_counter.most_common()
        total_song_request = sum(song_counter.values())

        total_logins = sum(g.login_count for g in all_guests)

        return render_template(
            "checkstatus.html",
            guests=all_guests,
            wedding_totals=wedding_totals,
            dinner_totals=dinner_totals,
            cocktail_totals=cocktail_totals,
            sorted_songs=sorted_songs,
            total_song_request=total_song_request,
            total_logins=total_logins,
            kids_meal_total=kids_meal_total
        )

    # NON-ADMIN VIEW (optional simple page)
    return render_template("main_pages/rsvpre.html", name=name)

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
    with app.app_context():
        db.create_all()   # ensures table exists
        seed_database()
    app.run(debug=False)
