# Test login behavior
def test_login_valid_email(client):
    resp = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert resp.status_code in (200, 302)
    if resp.status_code == 200:
        assert b"welcome" in resp.data.lower()


def test_login_invalid_email(client):
    resp = client.post("/showSummary", data={"email": "unknown@mail.com"})
    assert resp.status_code in (302, 303)
