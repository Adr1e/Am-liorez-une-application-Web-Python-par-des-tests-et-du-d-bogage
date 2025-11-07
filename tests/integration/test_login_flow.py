# Test login behavior
def test_login_valid_email(client):
    resp = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert resp.status_code in (200, 302)
    if resp.status_code == 200:
        assert b"welcome" in resp.data.lower()


def test_login_invalid_email(client):
    resp = client.post("/showSummary", data={"email": "unknown@mail.com"})
    assert resp.status_code in (302, 303)

def test_points_displayed_on_welcome_page(client):
    """Ensure club points are rendered on the welcome page after login."""
    # Use a known seed email from clubs.json
    email = "john@simplylift.co"
    response = client.post("/showSummary", data={"email": email})
    assert response.status_code == 200
    # We just assert the presence of the "Points:" label to keep it stable
    assert "Points:" in response.text
