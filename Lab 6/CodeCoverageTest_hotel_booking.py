import pytest
from hotel_booking import booking_cost, cancellation_refund, room_upgrade


# ---------- booking_cost ----------
def test_standard_two_nights():
    assert booking_cost("standard", 2, 2, False) == 4000


def test_unknown_room_raises():
    with pytest.raises(ValueError, match="unknown room"):
        booking_cost("penthouse", 1, 1, False)


def test_invalid_nights_raises():
    with pytest.raises(ValueError, match="invalid nights"):
        booking_cost("standard", 0, 1, False)


def test_peak_season_surcharge():
    # 2000 + 500 = 2500 per night x 2
    assert booking_cost("standard", 2, 2, True) == 5000


def test_extra_guests_charge():
    # 2000 + (4-2)*500*1
    assert booking_cost("standard", 1, 4, False) == 3000


def test_long_stay_discount():
    # 2000*7 = 14000, minus 10% = 12600
    assert booking_cost("standard", 7, 2, False) == 12600


# ---------- cancellation_refund ----------
def test_full_refund():
    assert cancellation_refund(1000, 10, False) == 1000


def test_half_refund():
    assert cancellation_refund(1000, 3, False) == 500


def test_no_refund():
    assert cancellation_refund(1000, 1, False) == 0


def test_member_bonus_refund():
    assert cancellation_refund(1000, 3, True) == 750


# ---------- room_upgrade ----------
def test_no_rooms_free():
    assert room_upgrade("standard", True, 0) == "standard"


def test_standard_member_upgrade():
    assert room_upgrade("standard", True, 5) == "deluxe"


def test_deluxe_member_upgrade():
    assert room_upgrade("deluxe", True, 5) == "suite"


def test_suite_member_no_upgrade():
    assert room_upgrade("suite", True, 5) == "suite"
