# Test for homepage route

def test_homepage_returns_200(client):
    # The home page should load correctly
    resp = client.get("/")
    assert resp.status_code == 200
