# Unit tests for pure helper functions (no Flask, no JSON)

import pytest
from server import can_book, sanitize_places, calculate_remaining_places


# --- can_book() ---
@pytest.mark.parametrize(
    "points, requested, expected",
    [
        (13, 1, True),
        (12, 12, True),
        (3, 4, False),
        (0, 1, False),
        (5, 13, False),
    ],
)
def test_can_book(points, requested, expected):
    # Check rule: max 12 places, enough points
    assert can_book(points, requested) is expected


# --- sanitize_places() ---
@pytest.mark.parametrize("raw, expected", [("1", 1), ("12", 12), (" 3 ", 3)])
def test_sanitize_places_valid(raw, expected):
    # Valid input -> int
    assert sanitize_places(raw) == expected


@pytest.mark.parametrize("raw", ["-1", "0", "abc", "", None])
def test_sanitize_places_invalid(raw):
    # Invalid input -> raise error
    with pytest.raises(ValueError):
        sanitize_places(raw)


# --- calculate_remaining_places() ---
@pytest.mark.parametrize(
    "total, booked, expected",
    [
        (10, 3, 7),
        (5, 0, 5),
        (12, 12, 0),
    ],
)
def test_remaining_places_ok(total, booked, expected):
    # Correct remaining calculation
    assert calculate_remaining_places(total, booked) == expected


@pytest.mark.parametrize("total, booked", [(10, -1), (5, 10)])
def test_remaining_places_invalid(total, booked):
    # Negative or too high -> error
    with pytest.raises(ValueError):
        calculate_remaining_places(total, booked)
