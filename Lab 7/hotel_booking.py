import re


def nights_stayed(days):
    if not isinstance(days, str):
        return None
    match = re.fullmatch(r"\s*([0-9]{1,6})\s*-\s*([0-9]{1,6})\s*", days)
    if match is None:
        return None
    check_in, check_out = map(int, match.groups())
    if check_out <= check_in:
        return None
    return check_out - check_in


def room_floor(room_code):
    if not isinstance(room_code, str):
        return None
    if re.fullmatch(r"[A-Za-z]+-[0-9]+", room_code) is None:
        return None
    number = room_code.split("-")[1]
    return int(number[0])


def booking_label(names_csv):
    if not isinstance(names_csv, str):
        return None
    names = [name.strip() for name in names_csv.split(",") if name.strip()]
    if not names:
        return None
    lead = names[0]
    return lead[0].upper() + lead[1:] + " +" + str(len(names) - 1)


def main():
    print("==== Running nights_stayed ====")
    user_input = input("Enter check-in and check-out day (e.g. 12-15): ")
    result = nights_stayed(user_input)
    print("Nights:", result if result is not None else "Invalid input")

    print("\n==== Running room_floor ====")
    user_input = input("Enter a room code (e.g. D-305): ")
    result = room_floor(user_input)
    print("Floor:", result if result is not None else "Invalid input")

    print("\n==== Running booking_label ====")
    user_input = input("Enter guest names as CSV (e.g. ravi, priya): ")
    result = booking_label(user_input)
    print("Booking Label:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
