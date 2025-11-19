from flask import Flask, session, request, jsonify, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
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


# RSVP submission
@app.route('/rsvp', methods=['POST'])
def rsvp():
    guest, name = get_current_guest()
    if not guest:
        flash("Error: Guest not found in database.")
        return redirect(url_for('rsvpage'))

    rsvp_status = request.form.get('rsvp')
    if not rsvp_status:
        flash('Please select an RSVP option.')
        return redirect(url_for('rsvpage'))

    guest.rsvp_status = rsvp_status
    db.session.commit()

    flash(f"Thanks {name}, you RSVP'd: {rsvp_status.capitalize()}")
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
    rsvp_status = guest.rsvp_status if guest else None

    if name and name.strip().lower() == "cs50":
        return render_template('main_pages/rsvp.html', name=name, rsvp_status=rsvp_status)

    return render_template('main_pages/rsvpre.html', name=name, rsvp_status=rsvp_status)



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
    if name != "Bill Klinkatsis":
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
    "irvine", "san_diego", "los_angeles", "anaheim"
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
