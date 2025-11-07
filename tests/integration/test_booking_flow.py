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
    """Past competitions must not render the 'Book Places' link."""
    resp = client.post("/showSummary", data={"email": "john@simplylift.co"}, follow_redirects=True)
    assert resp.status_code == 200
    html = resp.data.decode("utf-8")

    # Expect at least one past competition to show "Booking unavailable"
    assert "Booking unavailable" in html
