def test_club_points_displayed_on_welcome_page(client):
    """Ensure that the club name and points are displayed after login."""
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert response.status_code == 200
    html = response.data.decode().lower()

    # Should show the club name, email, and points label
    assert "simply lift" in html
    assert "john@simplylift.co" in html
    assert "points:" in html
