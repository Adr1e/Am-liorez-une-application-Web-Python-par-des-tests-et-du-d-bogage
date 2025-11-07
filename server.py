import json
from typing import List, Dict, Optional
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for, jsonify

# File paths
CLUBS_PATH = "clubs.json"
COMPETITIONS_PATH = "competitions.json"


def loadClubs(path: str = CLUBS_PATH) -> List[Dict]:
    """Load clubs data from file."""
    with open(path) as f:
        data = json.load(f)
    # Ensure bookings structure exists for each club
    clubs = data.get("clubs", [])
    for c in clubs:
        if "bookings" not in c or not isinstance(c.get("bookings"), list):
            c["bookings"] = []  # list of {competition, places, ts}
    return clubs


def loadCompetitions(path: str = COMPETITIONS_PATH) -> List[Dict]:
    """Load competitions data from file."""
    with open(path) as f:
        data = json.load(f)
    return data.get("competitions", [])


def saveClubs(clubs: List[Dict], path: str = CLUBS_PATH) -> None:
    """Persist clubs to file (includes bookings history)."""
    with open(path, "w") as f:
        json.dump({"clubs": clubs}, f, indent=2)


def saveCompetitions(competitions: List[Dict], path: str = COMPETITIONS_PATH) -> None:
    """Persist competitions to file."""
    with open(path, "w") as f:
        json.dump({"competitions": competitions}, f, indent=2)


def find_club(clubs: List[Dict], name_or_email: str) -> Optional[Dict]:
    """Find club by name or email."""
    key = name_or_email.strip().lower()
    for c in clubs:
        if c.get("name", "").lower() == key or c.get("email", "").lower() == key:
            return c
    return None


def find_competition(competitions: List[Dict], name: str) -> Optional[Dict]:
    """Find competition by name."""
    key = name.strip().lower()
    for comp in competitions:
        if comp.get("name", "").lower() == key:
            return comp
    return None


def as_int(value, default: int = 0) -> int:
    """Safe int conversion."""
    try:
        return int(value)
    except Exception:
        return default


# -------- small services (used by unit tests) --------

def can_book(points, requested):
    """True if 1 <= requested <= 12 and points >= requested."""
    try:
        p = int(points)
        r = int(requested)
    except Exception:
        return False
    return 1 <= r <= 12 and p >= r


def sanitize_places(value):
    """Return positive int or raise ValueError."""
    try:
        places = int(str(value).strip())
    except Exception as exc:
        raise ValueError("Invalid input") from exc
    if places < 1:
        raise ValueError("Places must be positive")
    return places


def calculate_remaining_places(total, booked):
    """Return total - booked or raise ValueError."""
    t = int(total)
    b = int(booked)
    if b < 0 or b > t:
        raise ValueError("Invalid booking numbers")
    return t - b


# -------- date helpers (bug 1) --------

def parse_competition_dt(value: str) -> Optional[datetime]:
    """Parse 'YYYY-MM-DD HH:MM:SS' or None."""
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except Exception:
        return None


def is_competition_past(comp: Dict) -> bool:
    """True if competition date is before now."""
    dt = parse_competition_dt(comp.get("date", ""))
    if not dt:
        return True
    return dt < datetime.now()


def enrich_competitions_with_flags(items: List[Dict]) -> List[Dict]:
    """Attach 'is_past' boolean to each competition (for UI)."""
    enriched = []
    for comp in items:
        item = dict(comp)
        item["is_past"] = is_competition_past(comp)
        enriched.append(item)
    return enriched


# -------- booking history helpers (bug 3) --------

def total_booked_for_club(club: Dict) -> int:
    """Sum of all booked places across all competitions for a club (from history)."""
    return sum(as_int(entry.get("places", 0), 0) for entry in club.get("bookings", []))


def record_booking_history(club: Dict, competition_name: str, places: int) -> None:
    """Append a booking record to the club history."""
    club.setdefault("bookings", [])
    club["bookings"].append({
        "competition": competition_name,
        "places": int(places),
        "ts": datetime.now().isoformat(timespec="seconds")
    })


# -------- app & data --------

app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


# -------- routes --------

@app.route("/")
def index():
    """Render home page."""
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    """Handle login and show dashboard."""
    email = request.form.get("email", "").strip()
    club = find_club(clubs, email)
    if not club:
        flash("Unknown email.")
        return redirect(url_for("index"))
    comps = enrich_competitions_with_flags(competitions)  # keep UI consistent
    return render_template("welcome.html", club=club, competitions=comps)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    """Render booking page only for future competitions."""
    foundClub = find_club(clubs, club)
    foundCompetition = find_competition(competitions, competition)
    if foundClub and foundCompetition and not is_competition_past(foundCompetition):
        return render_template("booking.html", club=foundClub, competition=foundCompetition)
    flash("Booking unavailable.")
    if foundClub:
        comps = enrich_competitions_with_flags(competitions)
        return render_template("welcome.html", club=foundClub, competitions=comps)
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

    # Past competitions cannot be booked (bug 1)
    if competition and is_competition_past(competition):
        errors.append("Competition is in the past.")

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

    # ---- NEW: global 12-place cap per club (bug 3) ----
    already = total_booked_for_club(club)
    if already + places_required > 12:
        errors.append("Limit of 12 total places per club reached.")

    if errors:
        for msg in errors:
            flash(msg)
        if club:
            comps = enrich_competitions_with_flags(competitions)
            return render_template("welcome.html", club=club, competitions=comps)
        return redirect(url_for("index"))

    # Apply booking changes
    competition["numberOfPlaces"] = str(remaining_places - places_required)
    club["points"] = str(club_points - places_required)

    # Record booking history on the club object
    record_booking_history(club, competition_name, places_required)

    saveCompetitions(competitions)
    saveClubs(clubs)

    flash("Great-booking complete!")
    comps = enrich_competitions_with_flags(competitions)
    return render_template("welcome.html", club=club, competitions=comps)


@app.route("/points")
def public_points():
    """Return JSON with club points."""
    data = [{"name": c.get("name"), "points": as_int(c.get("points"), 0)} for c in clubs]
    return jsonify(data)


@app.route("/logout")
def logout():
    """Logout and redirect home."""
    return redirect(url_for("index"))
