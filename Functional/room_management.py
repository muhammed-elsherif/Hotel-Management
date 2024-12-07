import tkinter as tk
from tkinter import messagebox

def create_room(room_number, room_type, price):
    return {"roomNumber": room_number, "roomType": room_type, "price": price, "availability": True}

def book_room(room):
    if room["availability"]:
        new_room = {**room, "availability": False}
        messagebox.showinfo("Room Booked", f"Room {room['roomNumber']} has been booked.")
        return new_room
    else:
        messagebox.showwarning("Booking Error", f"Room {room['roomNumber']} is already booked.")
        return room

def release_room(room):
    if not room["availability"]:
        new_room = {**room, "availability": True}
        messagebox.showinfo("Room Released", f"Room {room['roomNumber']} is now available.")
        return new_room
    else:
        messagebox.showwarning("Release Error", f"Room {room['roomNumber']} is already available.")
        return room

def check_status(room):
    return "Available" if room["availability"] else "Booked"

class RoomManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")

        self.rooms = [
            create_room(101, "Single", 100),
            create_room(102, "Double", 150),
            create_room(201, "Suite", 300),
        ]

        tk.Label(root, text="Select Room:").grid(row=0, column=0, padx=10, pady=10)
        self.selected_room = tk.StringVar(root)
        room_numbers = [room['roomNumber'] for room in self.rooms]
        self.room_menu = tk.OptionMenu(root, self.selected_room, *room_numbers)
        self.room_menu.grid(row=0, column=1, padx=10, pady=10)
        # self.room_listbox = tk.Listbox(root, height=10, width=50)
        # self.room_listbox.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # self.refresh_room_list()

        self.book_button = tk.Button(root, text="Book Room", command=self.book_selected_room)
        self.book_button.grid(row=1, column=0, padx=5, pady=5)

        self.release_button = tk.Button(root, text="Release Room", command=self.release_selected_room)
        self.release_button.grid(row=1, column=1, padx=5, pady=5)

        self.status_button = tk.Button(root, text="Check Status", command=self.check_selected_room_status)
        self.status_button.grid(row=1, column=2, padx=5, pady=5)

    def refresh_room_list(self):
        self.room_listbox.delete(0, tk.END)
        for room in self.rooms:
            status = check_status(room)
            self.room_listbox.insert(tk.END, f"Room {room['roomNumber']} ({room['roomType']}): ${room['price']} - {status}")

    def get_selected_room(self):
        selected_index = self.room_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "No room selected!")
            return None
        return selected_index[0]

    def book_selected_room(self):
        index = self.get_selected_room()
        if index is not None:
            self.rooms[index] = book_room(self.rooms[index])
            self.refresh_room_list()

    def release_selected_room(self):
        index = self.get_selected_room()
        if index is not None:
            self.rooms[index] = release_room(self.rooms[index])
            self.refresh_room_list()

    def check_selected_room_status(self):
        index = self.get_selected_room()
        if index is not None:
            status = check_status(self.rooms[index])
            room_number = self.rooms[index]["roomNumber"]
            messagebox.showinfo("Room Status", f"Room {room_number} is {status}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RoomManagementApp(root)
    root.mainloop()