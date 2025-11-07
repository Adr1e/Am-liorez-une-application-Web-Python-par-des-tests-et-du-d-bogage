def test_past_competition_hides_booking_button_and_blocks_booking(client):
    import server
    assert server.competitions, "No seeded competitions"

    comp = server.competitions[0]
    original_date = comp["date"]
    comp["date"] = "2000-01-01 00:00:00"  # force past

    # Build expected link path for this comp/club
    from urllib.parse import quote
    comp_name = comp["name"]
    club_name = "Simply Lift"
    book_path = f"/book/{quote(comp_name)}/{quote(club_name)}".lower()

    try:
        # Login
        resp = client.post("/showSummary", data={"email": "john@simplylift.co"})
        assert resp.status_code == 200
        html = resp.data.decode().lower()

        # Link to book for this competition should be hidden
        assert book_path not in html, f"Booking link should be hidden for past competition: {book_path}"

        # Direct access to /book should be refused (no form)
        resp2 = client.get(f"/book/{comp_name}/{club_name}")
        assert resp2.status_code == 200
        html2 = resp2.data.decode().lower()
        assert "<form" not in html2 or "booking unavailable" in html2
    finally:
        # Restore original date to avoid side effects
        comp["date"] = original_date
