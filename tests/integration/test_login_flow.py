# Test login behavior
def test_login_valid_email(client):
    resp = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert resp.status_code in (200, 302)
    if resp.status_code == 200:
        assert b"welcome" in resp.data.lower()


def test_login_invalid_email(client):
    resp = client.post("/showSummary", data={"email": "unknown@mail.com"})
    assert resp.status_code in (302, 303)

def test_points_displayed_on_welcome_page(client, mock_club, mock_competitions):
    """Check that the user's points are displayed on the welcome page."""
    response = client.post("/showSummary", data={"email": mock_club["email"]})
    assert response.status_code == 200
    assert str(mock_club["points"]) in response.text
