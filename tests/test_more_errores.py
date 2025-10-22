# tests/test_more_errors.py
# Additional tests to cover missing error branches and routes

def test_login_unknown_email_redirects(client):
    # If email is not found, user should be redirected to index
    r = client.post("/showSummary", data={"email": "nobody@example.com"})
    assert r.status_code in (302, 303)


def test_book_with_invalid_names_redirects_to_index(client):
    # Booking with invalid club or competition should redirect to index
    r = client.get("/book/UnknownComp/UnknownClub")
    assert r.status_code in (302, 303)


def test_purchase_invalid_places_value(client):
    # Should show error when places is not a valid number
    r = client.post("/purchasePlaces", data={
        "club": "Simply Lift",
        "competition": "Spring Festival",
        "places": "abc",  # invalid number
    })
    assert r.status_code in (200, 400)
    assert b"invalid number of places" in r.data.lower()


def test_purchase_with_unknown_entities_redirects(client):
    # Should redirect to index if club or competition not found
    r = client.post("/purchasePlaces", data={
        "club": "Unknown Club",
        "competition": "Spring Festival",
        "places": "1",
    })
    assert r.status_code in (302, 303)


def test_points_endpoint_json(client):
    # Public /points should return valid JSON with list of clubs
    r = client.get("/points")
    assert r.status_code == 200
    assert r.is_json
    data = r.get_json()
    assert isinstance(data, list)
    assert all("name" in c and "points" in c for c in data)


def test_logout_redirects(client):
    # Logout should redirect back to index
    r = client.get("/logout")
    assert r.status_code in (302, 303)
