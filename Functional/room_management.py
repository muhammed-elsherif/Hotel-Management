import tkinter as tk
from tkinter import messagebox
# from billing_management import Billing
import reservation_management
from config import db, cursor


def fetch_rooms():
    """Fetch room data from the database."""
    cursor.execute("SELECT roomNumber, roomType, price FROM rooms")
    rooms_data = cursor.fetchall()
    return [{"room_number": room[0], "room_type": room[1], "price": room[2]} for room in rooms_data]


def check_room_status(room_number):
    """Check the status of a room."""
    query = "SELECT availability FROM rooms WHERE roomNumber = %s"
    cursor.execute(query, (room_number,))
    result = cursor.fetchone()
    return "Available" if result and result[0] else "Booked"


def release_room(room_number):
    """Release a booked room."""
    status = check_room_status(room_number)
    if status == "Booked":
        query = "UPDATE rooms SET availability = TRUE WHERE roomNumber = %s"
        cursor.execute(query, (room_number,))
        db.commit()
        return f"Room {room_number} is now available."
    return f"Room {room_number} is already available."


def create_room_management_ui(parent_frame):
    """Create the main UI for room management."""
    frame = tk.Frame(parent_frame)
    frame.pack()

    # Fetch initial room data
    rooms = fetch_rooms()

    # Selected room variable
    selected_room = tk.StringVar()
    room_numbers = [room["room_number"] for room in rooms]
    if room_numbers:
        selected_room.set(room_numbers[0])

    # Create widgets
    create_title(frame)
    create_main_frame(frame, rooms, selected_room)
    create_buttons(frame, parent_frame, rooms, selected_room)
    status_label = tk.Label(frame, text="Status: ", font=("Arial", 12), fg="white")
    status_label.pack(pady=20)

    return {"frame": frame, "rooms": rooms, "selected_room": selected_room, "status_label": status_label}


def create_title(frame):
    """Create the title section."""
    title_frame = tk.Frame(frame)
    title_frame.pack(pady=10)
    tk.Label(title_frame, text="Hotel Management System", font=("Arial", 16, "bold")).pack()


def create_main_frame(frame, rooms, selected_room):
    """Create the main dropdown menu for selecting rooms."""
    main_frame = tk.Frame(frame)
    main_frame.pack(pady=20)

    tk.Label(main_frame, text="Select Room:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
    room_numbers = [room["room_number"] for room in rooms]
    tk.OptionMenu(main_frame, selected_room, *room_numbers).grid(row=0, column=1, padx=10, pady=10)


def create_buttons(frame, parent_frame, rooms, selected_room):
    """Create the buttons for room actions."""
    button_frame = tk.Frame(frame)
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Add Room", font=("Arial", 12), width=15, bg="lightblue",
              command=lambda: add_room_window(parent_frame, rooms)).grid(row=0, column=0, padx=10)

    tk.Button(button_frame, text="Book Room", font=("Arial", 12), width=15, bg="lightblue",
              command=lambda: show_customer_form(parent_frame, rooms, selected_room.get())).grid(row=1, column=1, padx=10)

    tk.Button(button_frame, text="Release Room", font=("Arial", 12), width=15, bg="lightgreen",
              command=lambda: handle_release_room(rooms, selected_room.get())).grid(row=0, column=1, padx=10)

    tk.Button(button_frame, text="Check Status", font=("Arial", 12), width=15, bg="lightgray",
              command=lambda: check_status(rooms, selected_room.get(), frame)).grid(row=1, column=0, padx=10, pady=10)


def show_customer_form(parent_frame, rooms, selected_room):
    """Show the customer form for booking a room."""
    room = get_room_by_number(rooms, selected_room)
    if room and check_room_status(selected_room) == "Available":
        reservation_management.reservation_system(parent_frame, selected_room)
    else:
        messagebox.showerror("Error", "Room is not available or already booked.")


def handle_release_room(rooms, room_number):
    """Handle releasing a room."""
    room = get_room_by_number(rooms, room_number)
    if room and check_room_status(room_number) == "Booked":
        result = release_room(room_number)
        reservation_id, customer_id = get_reservation_details(room_number)
        messagebox.showinfo("Release", result)

        # Billing process
        billing = Billing(reservation_id, customer_id)
        bill_details = billing.fetch_bill()

        if not bill_details:
            messagebox.showerror("Error", "No billing information found.")
            return

        total, taxes, discounts, payment_status = bill_details
        confirm = messagebox.askyesno(
            "Billing Confirmation",
            f"Total: ${total}\nTaxes: ${taxes}\nDiscounts: ${discounts}\n\nConfirm payment to release the room?"
        )

        if confirm:
            billing.update_payment_status("Paid")
            release_room(room_number)
            messagebox.showinfo("Success", f"Room {room_number} has been released.")
    else:
        messagebox.showerror("Error", "Room is not booked or unavailable.")


def get_reservation_details(room_number):
    """Get reservation details for a room."""
    query = "SELECT reservationId, customerId FROM reservations WHERE roomNumber = %s"
    cursor.execute(query, (room_number,))
    return cursor.fetchone()


def check_status(rooms, room_number, frame):
    """Check the status of a room and update the status label."""
    room = get_room_by_number(rooms, room_number)
    if room:
        status = check_room_status(room_number)
        frame.children['!label'].config(text=f"Status: Room {room_number} is {status}.")
        return status == "Available"


def get_room_by_number(rooms, room_number):
    """Get a room object by its number."""
    for room in rooms:
        if room["room_number"] == int(room_number):
            return room
    return None


def add_room_window(parent_frame, rooms):
    """Show a window for adding a new room."""
    window = tk.Toplevel(parent_frame)
    window.title("Add Room")
    window.geometry("400x300")
    window.resizable(False, False)

    tk.Label(window, text="Room Type:").pack(pady=(10, 0))
    room_type_entry = tk.Entry(window, width=30)
    room_type_entry.pack(pady=5)

    tk.Label(window, text="Price:").pack(pady=(10, 0))
    price_entry = tk.Entry(window, width=30)
    price_entry.pack(pady=5)

    tk.Label(window, text="Availability:").pack(pady=(10, 0))
    availability_var = tk.StringVar(window)
    availability_var.set("Available")
    tk.OptionMenu(window, availability_var, "Available", "Unavailable").pack(pady=5)

    def submit_room():
        room_type = room_type_entry.get()
        price = price_entry.get()
        availability = availability_var.get()

        if not room_type or not price:
            messagebox.showwarning("Input Error", "Please fill in all fields")
            return

        try:
            price = float(price)
            availability_bool = True if availability == "Available" else False
        except ValueError:
            messagebox.showwarning("Input Error", "Price must be a valid number")
            return

        query = "INSERT INTO rooms (roomType, price, availability) VALUES (%s, %s, %s)"
        values = (room_type, price, availability_bool)
        try:
            cursor.execute(query, values)
            db.commit()
            messagebox.showinfo("Success", "Room added successfully!")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", f"Error: {e}")

    tk.Button(window, text="Add Room", command=submit_room, bg="green", fg="white").pack(pady=20)
