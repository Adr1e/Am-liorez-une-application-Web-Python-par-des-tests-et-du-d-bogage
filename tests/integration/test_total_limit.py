# tests/integration/test_total_limit.py
import server

def test_total_cap_cannot_be_exceeded(client, _mock_json_files):
    """
    A club cannot book more than 12 places in total across all competitions.
    This test ensures a deterministic state: high points, empty booking history,
    and enough competition places. Then it verifies both success and rejection cases.
    """

    # -- Initialize deterministic test state (mocked JSON paths via _mock_json_files) --
    clubs = server.loadClubs()
    comps = server.loadCompetitions()

    # Reset club: ensure high points and no previous bookings
    for c in clubs:
        if c["name"] == "Simply Lift":
            c["points"] = "30"      # enough points for multiple bookings
            c["bookings"] = []      # IMPORTANT: booking total is derived from this list
            break

    # Ensure both competitions have enough available places
    for comp in comps:
        if comp["name"] == "Spring Festival":
            comp["numberOfPlaces"] = "15"
        if comp["name"] == "Fall Classic":
            comp["numberOfPlaces"] = "15"

    # Save modified data into the mock JSON files
    server.saveClubs(clubs)
    server.saveCompetitions(comps)

    # >>> IMPORTANT: reload global state used by the Flask app <<<
    # The app keeps in-memory copies of clubs and competitions,
    # so we need to refresh them after modifying the mock JSON files.
    server.clubs = server.loadClubs()
    server.competitions = server.loadCompetitions()

    # Step 1: Login as Simply Lift 
    r = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert r.status_code == 200

    # Step 2: First booking (7 places) should succeed 
    r = client.post(
        "/purchasePlaces",
        data={"competition": "Spring Festival", "club": "Simply Lift", "places": "7"},
        follow_redirects=True,
    )
    html = r.data.decode()
    assert "Great-booking complete!" in html        # success message
    assert "Booked total:" in html                  # total display visible
    assert "7/12" in html                           # total = 7 places booked

    # Step 3: Second booking (6 places) should be rejected (total 13 > 12) 
    r = client.post(
        "/purchasePlaces",
        data={"competition": "Fall Classic", "club": "Simply Lift", "places": "6"},
        follow_redirects=True,
    )
    html = r.data.decode()
    assert "Club booking limit (12 total) exceeded." in html  # rejection message
    assert "7/12" in html                                     # total remains at 7

