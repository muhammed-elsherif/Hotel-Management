import tkinter as tk
from tkinter import messagebox
from billing_management import Billing
import reservation_management
from config import db, cursor

class Room:
    def __init__(self, room_number, room_type, price):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price

    def check_room_status(self):
        query = "SELECT availability FROM rooms WHERE roomNumber = %s"
        cursor.execute(query, (self.room_number,))
        result = cursor.fetchone()
        return "Available" if result and result[0] else "Booked"

    def release_room(self):
        if self.check_room_status() == "Booked":
            query = "UPDATE rooms SET availability = TRUE WHERE roomNumber = %s"
            cursor.execute(query, (self.room_number,))
            db.commit()
            return f"Room {self.room_number} is now available."
        else:
            return f"Room {self.room_number} is already available."

class RoomManagementApp:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.frame = tk.Frame(self.parent_frame)
        self.frame.pack()
        
        cursor.execute("SELECT roomNumber, roomType, price FROM rooms")
        rooms_data = cursor.fetchall()
        self.rooms = [Room(room[0], room[1], room[2]) for room in rooms_data]

        self.create_widgets()

    def create_widgets(self):
        title_frame = tk.Frame(self.frame)
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="Hotel Management System", font=("Arial", 16, "bold")).pack()

        main_frame = tk.Frame(self.frame)
        main_frame.pack(pady=20)

        tk.Label(main_frame, text="Select Room:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
        self.selected_room = tk.StringVar()
        room_numbers = [room.room_number for room in self.rooms]
        self.selected_room.set(room_numbers[0] if room_numbers else "")
        self.room_menu = tk.OptionMenu(main_frame, self.selected_room, *room_numbers)
        self.room_menu.grid(row=0, column=1, padx=10, pady=10)

        button_frame = tk.Frame(self.frame)
        button_frame.pack(pady=20)

        self.book_button = tk.Button(button_frame, text="Add Room", font=("Arial", 12), width=15, bg="lightblue", command=self.add_room)
        self.book_button.grid(row=0, column=0, padx=10)

        self.book_button = tk.Button(button_frame, text="Book Room", font=("Arial", 12), width=15, bg="lightblue", command=self.show_customer_form)
        self.book_button.grid(row=1, column=1, padx=10)

        self.release_button = tk.Button(button_frame, text="Release Room", font=("Arial", 12), width=15, bg="lightgreen", command=self.release_room)
        self.release_button.grid(row=0, column=1, padx=10)

        self.status_button = tk.Button(button_frame, text="Check Status", font=("Arial", 12), width=15, bg="lightgray", command=self.check_status)
        self.status_button.grid(row=1, column=0, padx=10, pady=10)

        self.status_label = tk.Label(self.frame, text="Status: ", font=("Arial", 12), fg="white")
        self.status_label.pack(pady=20)

    def get_room_by_number(self, room_number):
        for room in self.rooms:
            if room.room_number == int(room_number):
                return room
        return None

    def show_customer_form(self):
        room_number = self.selected_room.get()
        room = self.get_room_by_number(room_number)
        if room and not room.check_room_status() == "Booked":
            reservation_window = reservation_management.ReservationSystem(self.frame, room_number)
        else:
            messagebox.showerror("Error", "Room is not booked or unavailable.")

    def release_room(self):
        room_number = self.selected_room.get()
        room = self.get_room_by_number(room_number)
        if room and room.check_room_status() == "Booked":
            result = room.release_room()
            reservation_id, customer_id = self.get_reservation_details(room_number)
            messagebox.showinfo("Release", result)
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
                room.release_room()
                messagebox.showinfo("Success", f"Room {room_number} has been released.")
                self.check_status()
        else:
            messagebox.showerror("Error", "Room is not booked or unavailable.")

            self.check_status()

    def get_reservation_details(self, room_number):
        query = "SELECT reservationId, customerId FROM reservations WHERE roomNumber = %s"
        cursor.execute(query, (room_number,))
        return cursor.fetchone()

    def check_status(self):
        room_number = self.selected_room.get()
        room = self.get_room_by_number(room_number)
        if room:
            status = room.check_room_status()
            self.status_label.config(text=f"Status: Room {room_number} is {status}.")
            if status == "Booked":
                return False
            else:
                return True
                
    def show(self):
        self.frame.pack()

    def hide(self):
        self.frame.pack_forget()

    def add_room(self):
        add_room_window = tk.Toplevel(self.frame)
        add_room_window.title("Add Room")
        add_room_window.geometry("400x300")
        add_room_window.resizable(False, False)

        tk.Label(add_room_window, text="Room Type:").pack(pady=(10, 0))
        room_type_entry = tk.Entry(add_room_window, width=30)
        room_type_entry.pack(pady=5)

        tk.Label(add_room_window, text="Price:").pack(pady=(10, 0))
        price_entry = tk.Entry(add_room_window, width=30)
        price_entry.pack(pady=5)

        tk.Label(add_room_window, text="Availability:").pack(pady=(10, 0))
        availability_var = tk.StringVar(add_room_window)
        availability_var.set("Available")
        availability_menu = tk.OptionMenu(add_room_window, availability_var, "Available", "Unavailable")
        availability_menu.pack(pady=5)

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
                add_room_window.destroy()
            except Exception as e:
                messagebox.showerror("Database Error", f"Error: {e}")

        submit_button = tk.Button(add_room_window, text="Add Room", command=submit_room, bg="green", fg="green")
        submit_button.pack(pady=20)