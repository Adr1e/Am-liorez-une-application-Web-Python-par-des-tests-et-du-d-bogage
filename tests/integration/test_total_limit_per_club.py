from datetime import datetime, timedelta


def test_total_booking_limit_per_club(client):
    """A club cannot exceed 12 booked places in total across all competitions.

    We:
    - Reset the club booking history and give enough points.
    - Force competitions into the FUTURE (to avoid 'past' guard).
    - Ensure there are ENOUGH PLACES to book 10 first (so it can succeed).
    - Then attempt +5 and assert the global 12-place cap triggers.
    """
    import server

    # Get the club by NAME (stable)
    club = next(c for c in server.clubs if c["name"].lower() == "simply lift")
    club["points"] = "50"
    club["bookings"] = []  # reset history for isolation

    # Get two competitions by NAME (stable)
    comp1 = next(c for c in server.competitions if c["name"].lower() == "spring festival")
    comp2 = next(c for c in server.competitions if c["name"].lower() == "fall classic")

    # Put them clearly in the future
    future = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")

    # Save originals to restore later
    orig1_date, orig2_date = comp1["date"], comp2["date"]
    orig1_places, orig2_places = comp1["numberOfPlaces"], comp2["numberOfPlaces"]

    # Apply future dates and enough capacity for the test
    comp1["date"], comp2["date"] = future, future
    comp1["numberOfPlaces"] = "20"  # IMPORTANT: allow booking 10
    comp2["numberOfPlaces"] = "20"

    try:
        # First booking: 10 places -> should succeed
        r1 = client.post("/purchasePlaces", data={
            "competition": comp1["name"],
            "club": club["name"],
            "places": "10"
        })
        assert r1.status_code in (200, 302)
        assert b"Great-booking complete!" in r1.data

        # Second booking: 5 places -> should hit the global cap (10 + 5 > 12)
        r2 = client.post("/purchasePlaces", data={
            "competition": comp2["name"],
            "club": club["name"],
            "places": "5"
        })
        html2 = r2.data.decode().lower()
        assert "limit of 12 total places per club reached" in html2

        # Ensure total never exceeds 12 in the stored history
        total = sum(int(b["places"]) for b in club.get("bookings", []))
        assert total <= 12
    finally:
        # Restore original state for other tests
        comp1["date"], comp2["date"] = orig1_date, orig2_date
        comp1["numberOfPlaces"], comp2["numberOfPlaces"] = orig1_places, orig2_places
