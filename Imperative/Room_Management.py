import tkinter as tk
from tkinter import messagebox
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="hotel_management"
)
cursor = db.cursor()

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

    def book_room(self):
        if self.check_room_status() == "Available":
            query = "UPDATE rooms SET availability = FALSE WHERE roomNumber = %s"
            cursor.execute(query, (self.room_number,))
            db.commit()
            return f"Room {self.room_number} has been booked successfully."
        else:
            return f"Room {self.room_number} is already booked."

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

        self.book_button = tk.Button(button_frame, text="Book Room", font=("Arial", 12), width=15, bg="lightblue", command=self.book_room)
        self.book_button.grid(row=0, column=0, padx=10)

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

    def book_room(self):
        room_number = self.selected_room.get()
        room = self.get_room_by_number(room_number)
        if room:
            result = room.book_room()
            messagebox.showinfo("Booking", result)
            self.check_status()

    def release_room(self):
        room_number = self.selected_room.get()
        room = self.get_room_by_number(room_number)
        if room:
            result = room.release_room()
            messagebox.showinfo("Release", result)
            self.check_status()

    def check_status(self):
        room_number = self.selected_room.get()
        room = self.get_room_by_number(room_number)
        if room:
            status = room.check_room_status()
            self.status_label.config(text=f"Status: Room {room_number} is {status}.")

    def show(self):
        self.frame.pack()

    def hide(self):
        self.frame.pack_forget()

