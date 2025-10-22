# Test for login feature

def test_login_with_valid_email_shows_summary(client):
    # Login with a valid email should show the welcome page
    resp = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert resp.status_code in (200, 302)
    if resp.status_code == 200:
        assert b"welcome" in resp.data.lower() or b"summary" in resp.data.lower()
