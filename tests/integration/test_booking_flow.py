# Test booking routes and limits

def test_booking_page_loads(client):
    resp = client.get("/book/Spring Festival/Simply Lift")
    assert resp.status_code == 200
    assert b"spring festival" in resp.data.lower()


def test_cannot_book_more_than_12(client):
    form = {"club": "Simply Lift", "competition": "Spring Festival", "places": "13"}
    resp = client.post("/purchasePlaces", data=form)
    assert resp.status_code in (200, 400)
    assert b"12" in resp.data or b"limit" in resp.data.lower()


def test_not_enough_points(client):
    form = {"club": "Simply Lift", "competition": "Spring Festival", "places": "999"}
    resp = client.post("/purchasePlaces", data=form)
    assert resp.status_code in (200, 400)
    assert b"not enough" in resp.data.lower() or b"insufficient" in resp.data.lower()


def test_successful_booking(client):
    form = {"club": "Simply Lift", "competition": "Spring Festival", "places": "1"}
    resp = client.post("/purchasePlaces", data=form)
    assert resp.status_code in (200, 302)

def test_no_booking_link_for_past_competitions(client):
    """Force one competition in the past, then ensure booking link is hidden."""
    import server

    # Pick a known competition by name (stable even if order changes)
    comp = next(c for c in server.competitions if c["name"].lower() == "spring festival")

    # Save original value and force a past date BEFORE rendering the page
    original_date = comp["date"]
    comp["date"] = "2000-01-01 00:00:00"

    try:
        # Render welcome page
        resp = client.post("/showSummary", data={"email": "john@simplylift.co"})
        assert resp.status_code == 200
        html = resp.data.decode()

        # UI must show the unavailable hint and hide the booking link
        assert "Booking unavailable" in html
        assert "/book/Spring%20Festival/Simply%20Lift" not in html
    finally:
        # Restore original state for isolation
        comp["date"] = original_date
