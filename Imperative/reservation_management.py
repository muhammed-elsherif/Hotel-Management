import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from customer_management import Customer
from config import db, cursor

class Reservartion:
    def __init__(self, room_number, room_type, price):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price

class ReservationSystem:
    def __init__(self, parent_frame, room):
        self.parent_frame = parent_frame
        self.room = room
        self.frame = tk.Frame(self.parent_frame)

        self.frame.pack()

        self.show_customer_form()
          
    def show_customer_form(self):
        customer_form = tk.Toplevel(self.frame)
        customer_form.title("Customer Information")

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

        def submit_customer_info():
            name = name_entry.get()
            contact = contact_entry.get()
            payment_method = payment_combobox.get()

            if not all([name, contact, payment_method]):
                messagebox.showerror("Error", "All fields are required.")
                return

            response = Customer.add_customer_info(name, contact, payment_method)
            if isinstance(response, int):
                customer_id = response
                print(f"Customer ID: {customer_id}")
                room_number = self.room
                self.create_reservation(customer_id, room_number)
                customer_form.destroy()
            else:
                messagebox.showerror("Error", response)

        tk.Button(customer_form, text="Submit", font=("Arial", 12), command=submit_customer_info).grid(row=3, columnspan=2, pady=10)
    
    def create_reservation(self, customer_id, room_number):
        try:
            query = """
            INSERT INTO reservations (customerId, roomNumber, checkInDate, checkOutDate)
            VALUES (%s, %s, CURDATE(), NULL)
            """
            cursor.execute(query, (customer_id, room_number))
            db.commit()
            self.book_room()

            messagebox.showinfo("Reservation", f"Room {room_number} booked successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error creating reservation: {e}")

    def book_room(self):
        query = "UPDATE rooms SET availability = FALSE WHERE roomNumber = %s"
        cursor.execute(query, (self.room,))
        db.commit()
        return f"Room {self.room} has been booked successfully."
