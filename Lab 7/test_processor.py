from hypothesis import given, strategies as st
from hotel_booking import nights_stayed, room_floor, booking_label


@given(st.text() | st.none())
def test_nights_stayed_no_crash(s):
    nights_stayed(s)


@given(st.text() | st.none())
def test_room_floor_no_crash(s):
    room_floor(s)


@given(st.text() | st.none())
def test_booking_label_no_crash(s):
    booking_label(s)


@given(st.one_of(st.text(), st.none(), st.integers(), st.floats()))
def test_all_functions_survive_any_type(value):
    for function in (nights_stayed, room_floor, booking_label):
        function(value)


@given(st.one_of(st.text(), st.none(), st.integers(), st.floats()))
def test_return_types(value):
    nights = nights_stayed(value)
    floor = room_floor(value)
    label = booking_label(value)
    assert nights is None or isinstance(nights, int)
    assert floor is None or isinstance(floor, int)
    assert label is None or isinstance(label, str)


@st.composite
def valid_day_ranges(draw):
    check_in = draw(st.integers(min_value=1, max_value=999_998))
    nights = draw(st.integers(min_value=1, max_value=999_999 - check_in))
    return check_in, nights


@given(valid_day_ranges())
def test_nights_stayed_valid(day_range):
    check_in, nights = day_range
    check_out = check_in + nights
    assert nights_stayed(f"{check_in}-{check_out}") == nights


@given(
    prefix=st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", min_size=1, max_size=5),
    floor=st.integers(min_value=0, max_value=9),
    suffix=st.integers(min_value=0, max_value=999_999),
)
def test_room_floor_valid(prefix, floor, suffix):
    assert room_floor(f"{prefix}-{floor}{suffix:06d}") == floor


@given(
    first=st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", min_size=1, max_size=20),
    others=st.lists(
        st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", min_size=1, max_size=20),
        max_size=10,
    ),
)
def test_booking_label_valid(first, others):
    names = [first] + others
    expected = first[0].upper() + first[1:] + " +" + str(len(others))
    assert booking_label(", ".join(names)) == expected


def test_known_bad_inputs_return_none():
    assert nights_stayed("") is None
    assert nights_stayed("-") is None
    assert nights_stayed("15-12") is None
    assert nights_stayed(None) is None
    assert nights_stayed("¹-²") is None
    assert room_floor("") is None
    assert room_floor("D-x") is None
    assert room_floor("a-b") is None
    assert room_floor(None) is None
    assert room_floor("D-²") is None
    assert booking_label("") is None
    assert booking_label(",") is None
    assert booking_label(None) is None
