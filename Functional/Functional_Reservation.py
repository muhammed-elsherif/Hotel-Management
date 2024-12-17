def check_room_availability(connection, room_number: int, check_in: str, check_out: str) -> bool:
    """Check if a room is available in the given date range."""
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT * FROM reservations 
    WHERE room_number = %s AND (
        (check_in_date <= %s AND check_out_date >= %s) OR
        (check_in_date <= %s AND check_out_date >= %s)
    )
    """
    cursor.execute(query, (room_number, check_out, check_in, check_in, check_out))
    result = cursor.fetchall()
    return len(result) == 0


def book_room(connection, customer_id: int, room_number: int, check_in: str, check_out: str) -> str:
    """Book a room if available."""
    if check_room_availability(connection, room_number, check_in, check_out):
        cursor = connection.cursor()
        query = "INSERT INTO reservations (customer_id, room_number, check_in_date, check_out_date) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (customer_id, room_number, check_in, check_out))
        connection.commit()
        return "Room booked successfully!"
    else:
        return "Room is not available for the selected dates."


def check_in_guest(connection, reservation_id: int) -> str:
    """Mark a room as checked-in."""
    cursor = connection.cursor()
    query = "UPDATE reservations SET status = 'checked-in' WHERE reservation_id = %s"
    cursor.execute(query, (reservation_id,))
    connection.commit()
    return "Guest checked in successfully!"


def check_out_guest(connection, reservation_id: int) -> str:
    """Mark a room as available after check-out."""
    cursor = connection.cursor()
    query = "UPDATE reservations SET status = 'checked-out' WHERE reservation_id = %s"
    cursor.execute(query, (reservation_id,))
    connection.commit()
    return "Guest checked out successfully!"