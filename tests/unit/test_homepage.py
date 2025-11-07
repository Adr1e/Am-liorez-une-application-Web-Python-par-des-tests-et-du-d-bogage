# Check homepage returns 200
def test_homepage_ok(client):
    resp = client.get("/")
    assert resp.status_code == 200
    # Basic text check
    text = resp.data.lower()
    assert b"welcome" in text or b"index" in text or b"gudlft" in text
