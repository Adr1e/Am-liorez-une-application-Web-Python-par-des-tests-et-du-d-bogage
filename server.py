import json
from typing import List, Dict, Optional
from flask import Flask, render_template, request, redirect, flash, url_for, jsonify

CLUBS_PATH = "clubs.json"
COMPETITIONS_PATH = "competitions.json"


def loadClubs(path: str = CLUBS_PATH) -> List[Dict]:
    with open(path) as f:
        data = json.load(f)
    return data.get("clubs", [])


def loadCompetitions(path: str = COMPETITIONS_PATH) -> List[Dict]:
    with open(path) as f:
        data = json.load(f)
    return data.get("competitions", [])


def saveClubs(clubs: List[Dict], path: str = CLUBS_PATH) -> None:
    with open(path, "w") as f:
        json.dump({"clubs": clubs}, f, indent=2)


def saveCompetitions(competitions: List[Dict], path: str = COMPETITIONS_PATH) -> None:
    with open(path, "w") as f:
        json.dump({"competitions": competitions}, f, indent=2)


def find_club(clubs: List[Dict], name_or_email: str) -> Optional[Dict]:
    key = name_or_email.strip().lower()
    for c in clubs:
        if c.get("name", "").lower() == key or c.get("email", "").lower() == key:
            return c
    return None


def find_competition(competitions: List[Dict], name: str) -> Optional[Dict]:
    key = name.strip().lower()
    for comp in competitions:
        if comp.get("name", "").lower() == key:
            return comp
    return None


def as_int(value, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def can_book(points, requested):
    try:
        p = int(points)
        r = int(requested)
    except Exception:
        return False
    return 1 <= r <= 12 and p >= r


def sanitize_places(value):
    try:
        places = int(str(value).strip())
    except Exception:
        raise ValueError("Invalid input")
    if places < 1:
        raise ValueError("Places must be positive")
    return places


def calculate_remaining_places(total, booked):
    t = int(total)
    b = int(booked)
    if b < 0 or b > t:
        raise ValueError("Invalid booking numbers")
    return t - b


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    email = request.form.get("email", "").strip()
    club = find_club(clubs, email)
    if not club:
        flash("Unknown email.")
        return redirect(url_for("index"))
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = find_club(clubs, club)
    foundCompetition = find_competition(competitions, competition)
    if foundClub and foundCompetition:
        return render_template("booking.html", club=foundClub, competition=foundCompetition)
    flash("Something went wrong, please try again.")
    if foundClub:
        return render_template("welcome.html", club=foundClub, competitions=competitions)
    return redirect(url_for("index"))


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition_name = request.form.get("competition", "")
    club_name = request.form.get("club", "")
    raw_places = request.form.get("places", "0")

    club = find_club(clubs, club_name)
    competition = find_competition(competitions, competition_name)

    errors = []
    if not club or not competition:
        errors.append("Club or competition not found.")

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

    if errors:
        for msg in errors:
            flash(msg)
        if club:
            return render_template("welcome.html", club=club, competitions=competitions)
        return redirect(url_for("index"))

    competition["numberOfPlaces"] = str(remaining_places - places_required)
    club["points"] = str(club_points - places_required)
    saveCompetitions(competitions)
    saveClubs(clubs)

    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/points")
def public_points():
    data = [{"name": c.get("name"), "points": as_int(c.get("points"), 0)} for c in clubs]
    return jsonify(data)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
