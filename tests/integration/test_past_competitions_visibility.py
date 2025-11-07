def test_past_competition_hides_booking_button_and_blocks_booking(client):
    # Make a known competition clearly in the past
    import server
    assert server.competitions, "No seeded competitions"
    comp = server.competitions[0]
    original_date = comp["date"]
    comp["date"] = "2000-01-01 00:00:00"  # past date

    try:
        # Login
        resp = client.post("/showSummary", data={"email": "john@simplylift.co"})
        assert resp.status_code == 200
        html = resp.data.decode().lower()

        # UI should not show booking link
        assert "booking unavailable" in html
        assert "book places" not in html

        # Direct access to /book should be refused (render welcome with flash)
        resp2 = client.get(f"/book/{comp['name']}/Simply Lift")
        assert resp2.status_code == 200
        html2 = resp2.data.decode().lower()
        assert "booking unavailable" in html2
    finally:
        comp["date"] = original_date
