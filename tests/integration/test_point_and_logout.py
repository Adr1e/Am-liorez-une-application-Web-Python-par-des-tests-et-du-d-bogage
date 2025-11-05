# Check /points and /logout endpoints

def test_book_invalid_names(client):
    resp = client.get("/book/UnknownComp/UnknownClub")
    assert resp.status_code in (302, 303)


def test_invalid_places(client):
    # Invalid or empty place values
    for bad in ["-1", "0", "abc", "", None]:
        form = {"club": "Simply Lift", "competition": "Spring Festival", "places": bad}
        resp = client.post("/purchasePlaces", data=form)
        assert resp.status_code in (200, 400, 302, 303)


def test_points_json(client):
    resp = client.get("/points")
    assert resp.status_code == 200
    assert resp.is_json
    data = resp.get_json()
    assert isinstance(data, list)
    assert all("name" in c and "points" in c for c in data)


def test_logout_redirect(client):
    resp = client.get("/logout")
    assert resp.status_code in (302, 303)
