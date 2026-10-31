import pytest
from hotel_booking import booking_cost, cancellation_refund, room_upgrade


# ================= booking_cost =================
def test_standard_two_nights():
    assert booking_cost("standard", 2, 2, False) == 4000


def test_unknown_room_raises():
    with pytest.raises(ValueError, match="unknown room"):
        booking_cost("penthouse", 1, 1, False)


@pytest.mark.parametrize("nights", [0, -1])
def test_invalid_nights_raises(nights):
    with pytest.raises(ValueError, match="invalid nights"):
        booking_cost("standard", nights, 1, False)


def test_one_night_is_valid_boundary():
    assert booking_cost("standard", 1, 1, False) == 2000


def test_off_peak_no_surcharge():
    assert booking_cost("deluxe", 1, 2, False) == 3500


def test_peak_season_surcharge_standard():
    assert booking_cost("standard", 2, 2, True) == 5000


def test_peak_season_surcharge_deluxe():
    # 3500 + 875 = 4375
    assert booking_cost("deluxe", 1, 2, True) == 4375


def test_suite_rate():
    assert booking_cost("suite", 1, 2, False) == 6000


def test_exactly_two_guests_no_extra_charge():
    assert booking_cost("standard", 1, 2, False) == 2000


def test_one_guest_no_extra_charge():
    assert booking_cost("standard", 1, 1, False) == 2000


def test_three_guests_extra_charge():
    assert booking_cost("standard", 1, 3, False) == 2500


def test_six_nights_no_discount_boundary():
    assert booking_cost("standard", 6, 2, False) == 12000


def test_seven_nights_discount_boundary():
    assert booking_cost("standard", 7, 2, False) == 12600


def test_all_conditions_combined():
    # rate 7500 x 7 = 52500; +2*500*7 = 59500; -10% = 53550
    assert booking_cost("suite", 7, 4, True) == 53550


# ================= cancellation_refund =================
def test_full_refund():
    assert cancellation_refund(1000, 10, False) == 1000


def test_full_refund_boundary_7_days():
    assert cancellation_refund(1000, 7, False) == 1000


def test_full_refund_member_no_bonus():
    assert cancellation_refund(1000, 7, True) == 1000


def test_half_refund_upper_boundary_6_days():
    assert cancellation_refund(1000, 6, False) == 500


def test_half_refund_lower_boundary_2_days():
    assert cancellation_refund(1000, 2, False) == 500


def test_half_refund_member_bonus():
    assert cancellation_refund(1000, 3, True) == 750


def test_no_refund_1_day():
    assert cancellation_refund(1000, 1, False) == 0


def test_no_refund_same_day():
    assert cancellation_refund(1000, 0, False) == 0


def test_no_refund_member_gets_bonus_only():
    assert cancellation_refund(1000, 1, True) == 250


# ================= room_upgrade =================
def test_no_rooms_free_member():
    assert room_upgrade("standard", True, 0) == "standard"


def test_no_rooms_free_non_member():
    assert room_upgrade("deluxe", False, 0) == "deluxe"


def test_standard_member_upgrades_to_deluxe():
    assert room_upgrade("standard", True, 3) == "deluxe"


def test_standard_non_member_no_upgrade():
    assert room_upgrade("standard", False, 3) == "standard"


def test_deluxe_member_upgrades_to_suite():
    assert room_upgrade("deluxe", True, 3) == "suite"


def test_deluxe_non_member_no_upgrade():
    assert room_upgrade("deluxe", False, 3) == "deluxe"


def test_suite_member_stays_suite():
    assert room_upgrade("suite", True, 3) == "suite"


def test_suite_non_member_stays_suite():
    assert room_upgrade("suite", False, 3) == "suite"
