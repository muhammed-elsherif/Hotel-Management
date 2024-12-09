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

def fetch_rooms():
    cursor.execute("SELECT roomNumber, roomType, price FROM rooms")
    return cursor.fetchall()

def check_room_status(room_number):
    query = "SELECT availability FROM rooms WHERE roomNumber = %s"
    cursor.execute(query, (room_number,))
    result = cursor.fetchone()
    return "Available" if result and result[0] else "Booked"

def book_room(room_number):
    if check_room_status(room_number) == "Available":
        query = "UPDATE rooms SET availability = FALSE WHERE roomNumber = %s"
        cursor.execute(query, (room_number,))
        db.commit()
        return f"Room {room_number} has been booked successfully."
    else:
        return f"Room {room_number} is already booked."

def release_room(room_number):
    if check_room_status(room_number) == "Booked":
        query = "UPDATE rooms SET availability = TRUE WHERE roomNumber = %s"
        cursor.execute(query, (room_number,))
        db.commit()
        return f"Room {room_number} is now available."
    else:
        return f"Room {room_number} is already available."

def create_room_management_ui(root):
    frame = tk.Frame(root)
    frame.pack()

    rooms = fetch_rooms()
    room_numbers = [room[0] for room in rooms]

    def update_status_label():
        room_number = selected_room.get()
        status = check_room_status(room_number)
        status_label.config(text=f"Status: Room {room_number} is {status}.")

    def handle_book_room():
        room_number = selected_room.get()
        result = book_room(room_number)
        messagebox.showinfo("Booking", result)
        update_status_label()

    def handle_release_room():
        room_number = selected_room.get()
        result = release_room(room_number)
        messagebox.showinfo("Release", result)
        update_status_label()

    title_frame = tk.Frame(frame)
    title_frame.pack(pady=10)
    tk.Label(title_frame, text="Hotel Management System", font=("Arial", 16, "bold")).pack()

    main_frame = tk.Frame(frame)
    main_frame.pack(pady=20)

    tk.Label(main_frame, text="Select Room:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
    selected_room = tk.StringVar()
    selected_room.set(room_numbers[0] if room_numbers else "")
    room_menu = tk.OptionMenu(main_frame, selected_room, *room_numbers)
    room_menu.grid(row=0, column=1, padx=10, pady=10)

    button_frame = tk.Frame(frame)
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Book Room", font=("Arial", 12), width=15, bg="lightblue", command=handle_book_room).grid(row=0, column=0, padx=10)
    tk.Button(button_frame, text="Release Room", font=("Arial", 12), width=15, bg="lightgreen", command=handle_release_room).grid(row=0, column=1, padx=10)
    tk.Button(button_frame, text="Check Status", font=("Arial", 12), width=15, bg="lightgray", command=update_status_label).grid(row=1, column=0, padx=10, pady=10)

    status_label = tk.Label(frame, text="Status: ", font=("Arial", 12), fg="white")
    status_label.pack(pady=20)

    return frame

def main():
    root = tk.Tk()
    root.title("Hotel Management System")
    root.geometry("500x400")
    root.resizable(False, False)

    room_management_frame = create_room_management_ui(root)
    room_management_frame.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
