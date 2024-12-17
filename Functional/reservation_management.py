import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import customer_management
from config import db, cursor


def create_reservation(customer_id, room_number):
    """Create a reservation in the database and book the room."""
    try:
        query = """
        INSERT INTO reservations (customerId, roomNumber, checkInDate, checkOutDate)
        VALUES (%s, %s, CURDATE(), NULL)
        """
        cursor.execute(query, (customer_id, room_number))
        db.commit()
        book_room(room_number)
        messagebox.showinfo("Reservation", f"Room {room_number} booked successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error creating reservation: {e}")


def book_room(room_number):
    """Mark the room as booked in the database."""
    query = "UPDATE rooms SET availability = FALSE WHERE roomNumber = %s"
    cursor.execute(query, (room_number,))
    db.commit()


def add_customer_info_and_reserve(room, customer_form, name_entry, contact_entry, payment_combobox):
    """Handle customer information submission and reservation creation."""
    name = name_entry.get()
    contact = contact_entry.get()
    payment_method = payment_combobox.get()

    if not all([name, contact, payment_method]):
        messagebox.showerror("Error", "All fields are required.")
        return

    response = customer_management.add_customer_info(name, contact, payment_method)
    if isinstance(response, int):  # Assuming a successful response returns the customer ID
        customer_id = response
        create_reservation(customer_id, room)
        customer_form.destroy()
    else:
        messagebox.showerror("Error", response)


def show_customer_form(parent_frame, room):
    """Display a form for collecting customer information."""
    customer_form = tk.Toplevel(parent_frame)
    customer_form.title("Customer Information")

    # Form fields
    tk.Label(customer_form, text="Customer Name:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
    name_entry = tk.Entry(customer_form, font=("Arial", 12))
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(customer_form, text="Contact Info:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
    contact_entry = tk.Entry(customer_form, font=("Arial", 12))
    contact_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(customer_form, text="Payment Method:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10)
    payment_methods = ["Credit Card", "Debit Card", "Cash", "UPI"]
    payment_combobox = ttk.Combobox(customer_form, values=payment_methods, font=("Arial", 12), state="readonly")
    payment_combobox.grid(row=2, column=1, padx=10, pady=10)
    payment_combobox.set("Select Payment Method")

    # Submit button
    tk.Button(
        customer_form,
        text="Submit",
        font=("Arial", 12),
        command=lambda: add_customer_info_and_reserve(room, customer_form, name_entry, contact_entry, payment_combobox)
    ).grid(row=3, columnspan=2, pady=10)


def reservation_system(parent_frame, room):
    """Launch the reservation system for a specific room."""
    frame = tk.Frame(parent_frame)
    frame.pack()

    # Open the customer form
    show_customer_form(frame, room)