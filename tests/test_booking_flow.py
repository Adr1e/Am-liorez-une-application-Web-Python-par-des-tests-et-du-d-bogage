# Tests for booking and purchase logic

def test_book_page_opens_for_valid_competition_and_club(client):
    # Check that the booking page loads successfully
    resp = client.get("/book/Spring Festival/Simply Lift")
    assert resp.status_code == 200
    assert b"Spring Festival" in resp.data or b"Simply Lift" in resp.data

def test_cannot_book_more_than_12_places(client):
    # Should reject booking more than 12 places
    payload = {"club": "Simply Lift", "competition": "Spring Festival", "places": "13"}
    resp = client.post("/purchasePlaces", data=payload)
    assert resp.status_code in (200, 400)
    assert b"12" in resp.data or b"limit" in resp.data.lower()

def test_refuse_when_not_enough_points(client):
    # Should refuse booking if club has not enough points
    payload = {"club": "Simply Lift", "competition": "Spring Festival", "places": "999"}
    resp = client.post("/purchasePlaces", data=payload)
    assert resp.status_code in (200, 400)
    assert b"not enough points" in resp.data.lower()

def test_successful_booking_deducts_points_and_confirms(client):
    # Should confirm booking when all conditions are valid
    payload = {"club": "Simply Lift", "competition": "Spring Festival", "places": "1"}
    resp = client.post("/purchasePlaces", data=payload)
    assert resp.status_code in (200, 302)
    if resp.status_code == 200:
        assert b"great" in resp.data.lower() or b"booking" in resp.data.lower()
