import json
from typing import List, Dict, Optional
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for, jsonify

# File paths for JSON data
CLUBS_PATH = "clubs.json"
COMPETITIONS_PATH = "competitions.json"

# -----------------------------
# Data access helpers
# -----------------------------
def loadClubs(path: str = CLUBS_PATH) -> List[Dict]:
    """Load clubs data from JSON."""
    with open(path) as f:
        data = json.load(f)
    return data.get("clubs", [])


def loadCompetitions(path: str = COMPETITIONS_PATH) -> List[Dict]:
    """Load competitions data from JSON."""
    with open(path) as f:
        data = json.load(f)
    return data.get("competitions", [])


def saveClubs(clubs: List[Dict], path: str = CLUBS_PATH) -> None:
    """Persist clubs to JSON."""
    with open(path, "w") as f:
        json.dump({"clubs": clubs}, f, indent=2)


def saveCompetitions(competitions: List[Dict], path: str = COMPETITIONS_PATH) -> None:
    """Persist competitions to JSON."""
    with open(path, "w") as f:
        json.dump({"competitions": competitions}, f, indent=2)


# -----------------------------
# Domain helpers
# -----------------------------
def find_club(clubs: List[Dict], name_or_email: str) -> Optional[Dict]:
    """Find a club by name or email (case-insensitive)."""
    key = name_or_email.strip().lower()
    for c in clubs:
        if c.get("name", "").lower() == key or c.get("email", "").lower() == key:
            return c
    return None


def find_competition(competitions: List[Dict], name: str) -> Optional[Dict]:
    """Find a competition by name (case-insensitive)."""
    key = name.strip().lower()
    for comp in competitions:
        if comp.get("name", "").lower() == key:
            return comp
    return None


def as_int(value, default: int = 0) -> int:
    """Safe int conversion with default."""
    try:
        return int(value)
    except Exception:
        return default


def parse_competition_dt(value: str) -> Optional[datetime]:
    """Parse 'YYYY-MM-DD HH:MM:SS' as datetime; return None on error."""
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except Exception:
        return None


def is_competition_past(comp: Dict) -> bool:
    """True if competition date is in the past."""
    dt = parse_competition_dt(comp.get("date", ""))
    if not dt:
        # If date is invalid/missing, treat as past to be safe.
        return True
    return dt < datetime.now()


def can_book_single(points: int, requested: int) -> bool:
    """Single booking must be 1..12 and points must cover it."""
    return 1 <= requested <= 12 and points >= requested


def sanitize_places(value) -> int:
    """Convert input to positive int, else raise ValueError."""
    try:
        places = int(str(value).strip())
    except Exception:
        raise ValueError("Invalid input")
    if places < 1:
        raise ValueError("Places must be positive")
    return places


def calculate_remaining_places(total: int, booked: int) -> int:
    """Compute remaining places or raise ValueError if invalid inputs."""
    if booked < 0 or booked > total:
        raise ValueError("Invalid booking numbers")
    return total - booked


def get_club_total_booked(club: Dict) -> int:
    """Sum 'places' from club['bookings'] list (history)."""
    history = club.get("bookings", [])
    try:
        return sum(as_int(b.get("places", 0), 0) for b in history)
    except Exception:
        return 0


def add_club_booking(club: Dict, competition_name: str, places: int) -> None:
    """Append a booking record to the club history."""
    if "bookings" not in club or not isinstance(club["bookings"], list):
        club["bookings"] = []
    club["bookings"].append({"competition": competition_name, "places": places})


# -----------------------------
# Flask app
# -----------------------------
app = Flask(__name__)
app.secret_key = "something_special"

# Load initial data into memory (simple JSON store)
competitions = loadCompetitions()
clubs = loadClubs()


def enrich_competitions_with_flags(items: List[Dict]) -> List[Dict]:
    """Return competitions list with 'is_past' boolean for UI."""
    enriched = []
    for comp in items:
        item = dict(comp)
        item["is_past"] = is_competition_past(comp)
        enriched.append(item)
    return enriched


@app.route("/")
def index():
    """Home page (login form)."""
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    """Login by email and show dashboard (welcome page)."""
    email = request.form.get("email", "").strip()
    club = find_club(clubs, email)
    if not club:
        flash("Unknown email.")
        return redirect(url_for("index"))

    # Compute total booked for display
    booked_total = get_club_total_booked(club)
    comps = enrich_competitions_with_flags(competitions)

    return render_template(
        "welcome.html",
        club=club,
        competitions=comps,
        booked_total=booked_total,
    )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    """Open the booking page (only if club/competition are valid)."""
    foundClub = find_club(clubs, club)
    foundCompetition = find_competition(competitions, competition)

    if foundClub and foundCompetition:
        return render_template("booking.html", club=foundClub, competition=foundCompetition)

    flash("Something went wrong, please try again.")
    if foundClub:
        # Show dashboard again if club is known
        booked_total = get_club_total_booked(foundClub)
        comps = enrich_competitions_with_flags(competitions)
        return render_template("welcome.html", club=foundClub, competitions=comps, booked_total=booked_total)

    return redirect(url_for("index"))


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    """Validate and process a booking with a global 12-place cap per club."""
    competition_name = request.form.get("competition", "")
    club_name = request.form.get("club", "")
    raw_places = request.form.get("places", "0")

    club = find_club(clubs, club_name)
    competition = find_competition(competitions, competition_name)

    errors = []
    if not club or not competition:
        errors.append("Club or competition not found.")

    # Past competitions are not bookable
    if competition and is_competition_past(competition):
        errors.append("Competition is in the past.")

    # Basic numeric checks
    places_required = as_int(raw_places, default=0)
    if places_required <= 0:
        errors.append("Invalid number of places.")
    if places_required > 12:
        errors.append("Limit is 12 places per booking.")

    remaining_places = as_int(competition.get("numberOfPlaces") if competition else 0)
    club_points = as_int(club.get("points") if club else 0)

    if places_required > remaining_places:
        errors.append("Not enough places remaining for this competition.")
    if places_required > club_points:
        errors.append("Not enough points.")

    # Global 12-place cap per club
    current_total = get_club_total_booked(club) if club else 0
    if current_total + places_required > 12:
        errors.append("Club booking limit (12 total) exceeded.")

    # If errors, show them on the dashboard
    if errors:
        for msg in errors:
            flash(msg)
        if club:
            booked_total = get_club_total_booked(club)
            comps = enrich_competitions_with_flags(competitions)
            return render_template("welcome.html", club=club, competitions=comps, booked_total=booked_total)
        return redirect(url_for("index"))

    # Apply state changes if everything is valid
    competition["numberOfPlaces"] = str(remaining_places - places_required)
    club["points"] = str(club_points - places_required)
    add_club_booking(club, competition_name, places_required)

    # Persist and render success
    saveCompetitions(competitions)
    saveClubs(clubs)

    flash("Great-booking complete!")
    booked_total = get_club_total_booked(club)
    comps = enrich_competitions_with_flags(competitions)
    return render_template("welcome.html", club=club, competitions=comps, booked_total=booked_total)


@app.route("/points")
def public_points():
    """Public JSON endpoint: list all clubs with points."""
    data = [{"name": c.get("name"), "points": as_int(c.get("points"), 0)} for c in clubs]
    return jsonify(data)


@app.route("/logout")
def logout():
    """Logout and redirect to home."""
    return redirect(url_for("index"))
