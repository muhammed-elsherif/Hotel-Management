import tkinter as tk
from tkinter import messagebox

class Room:
    def __init__(self, room_number, room_type, price):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.is_available = True

    def book_room(self):
        if self.is_available:
            self.is_available = False
            return f"Room {self.room_number} has been booked."
        else:
            return f"Room {self.room_number} is already booked."

    def release_room(self):
        if not self.is_available:
            self.is_available = True
            return f"Room {self.room_number} is now available."
        else:
            return f"Room {self.room_number} is already available."

    def check_status(self):
        return "Available" if self.is_available else "Booked"

class RoomManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        
        self.rooms = [
            Room(101, "Single", 100),
            Room(102, "Double", 150),
            Room(201, "Suite", 300),
        ]
        
        tk.Label(root, text="Select Room:").grid(row=0, column=0, padx=10, pady=10)
        self.selected_room = tk.StringVar(root)
        self.selected_room.set(self.rooms[0].room_number)
        room_numbers = [room.room_number for room in self.rooms]
        self.room_menu = tk.OptionMenu(root, self.selected_room, *room_numbers)
        self.room_menu.grid(row=0, column=1, padx=10, pady=10)

        self.book_button = tk.Button(root, text="Book Room", command=self.book_room)
        self.book_button.grid(row=1, column=0, padx=10, pady=10)
        
        self.release_button = tk.Button(root, text="Release Room", command=self.release_room)
        self.release_button.grid(row=1, column=1, padx=10, pady=10)
        
        self.status_button = tk.Button(root, text="Check Status", command=self.check_status)
        self.status_button.grid(row=2, column=0, padx=10, pady=10)
        
        self.status_label = tk.Label(root, text="Status: ", font=("Arial", 12))
        self.status_label.grid(row=2, column=1, padx=10, pady=10)
    
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

    def release_room(self):
        room_number = self.selected_room.get()
        room = self.get_room_by_number(room_number)
        if room:
            result = room.release_room()
            messagebox.showinfo("Release", result)

    def check_status(self):
        room_number = self.selected_room.get()
        room = self.get_room_by_number(room_number)
        if room:
            status = room.check_status()
            self.status_label.config(text=f"Status: {status}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RoomManagementApp(root)
    root.mainloop()