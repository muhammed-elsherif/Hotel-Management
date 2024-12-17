import tkinter as tk
from tkinter import messagebox
from config import db, cursor


# ---------------------------- Database Functions ---------------------------- #

def search_customer(customer_id):
    """Search for a customer by ID."""
    query = "SELECT * FROM customers WHERE customerId = %s"
    cursor.execute(query, (customer_id,))
    result = cursor.fetchone()
    if result:
        return {
            "customer_id": result[0],
            "name": result[1],
            "contact_info": result[2],
            "payment_method": result[3],
        }
    return None


def update_customer_info(customer_id, name, contact_info, payment_method):
    """Update customer information in the database."""
    query = """
    UPDATE customers
    SET name = %s, contactInfo = %s, paymentMethod = %s
    WHERE customerId = %s
    """
    cursor.execute(query, (name, contact_info, payment_method, customer_id))
    db.commit()
    return "Customer information updated successfully."


def add_customer_info(name, contact_info, payment_method):
    """Add a new customer to the database."""
    try:
        query = """
        INSERT INTO customers (name, contactInfo, paymentMethod)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (name, contact_info, payment_method))
        db.commit()
        return cursor.lastrowid
    except Exception as e:
        return f"Error adding customer info: {e}"


# ---------------------------- UI Functions ---------------------------- #

def setup_customer_management_ui(parent_frame, switch_page_callback):
    """Set up the customer management UI."""
    frame = tk.Frame(parent_frame)
    frame.pack()

    tk.Label(frame, text="Customer Management", font=("Arial", 16, "bold")).pack(pady=10)

    # Input for Customer ID
    tk.Label(frame, text="Enter Customer ID:", font=("Arial", 12)).pack(pady=5)
    customer_id_entry = tk.Entry(frame, font=("Arial", 12))
    customer_id_entry.pack(pady=5)

    result_frame = tk.Frame(frame)
    result_frame.pack(pady=10)

    # Buttons
    tk.Button(
        frame,
        text="Search",
        font=("Arial", 12),
        command=lambda: handle_search_customer(customer_id_entry.get(), result_frame),
    ).pack(pady=10)

    update_button = tk.Button(
        frame, text="Update Information", font=("Arial", 12), state=tk.DISABLED
    )
    update_button.pack(pady=10)

    # "Go Back" Button
    tk.Button(
        frame,
        text="Go Back",
        font=("Arial", 12),
        command=lambda: switch_page_callback("navbar"),
    ).pack(pady=10)

    return frame, update_button


def handle_search_customer(customer_id, result_frame):
    """Handle customer search and display results."""
    customer_id = customer_id.strip()
    if not customer_id.isdigit():
        messagebox.showerror("Error", "Please enter a valid Customer ID.")
        return

    customer = search_customer(int(customer_id))
    if customer:
        for widget in result_frame.winfo_children():
            widget.destroy()

        tk.Label(result_frame, text=f"Name: {customer['name']}", font=("Arial", 12)).pack()
        tk.Label(result_frame, text=f"Contact: {customer['contact_info']}", font=("Arial", 12)).pack()
        tk.Label(result_frame, text=f"Payment Method: {customer['payment_method']}", font=("Arial", 12)).pack()

        # Enable the "Update Information" button with the customer data
        handle_update_button(result_frame, customer)
    else:
        messagebox.showerror("Error", "Customer not found.")


def handle_update_button(result_frame, customer):
    """Enable and configure the Update Information button."""
    update_button = tk.Button(
        result_frame,
        text="Update Information",
        font=("Arial", 12),
        command=lambda: show_update_customer_form(customer),
    )
    update_button.pack(pady=10)


def show_update_customer_form(customer):
    """Display a form to update customer information."""
    update_window = tk.Toplevel()
    update_window.title("Update Customer Information")
    update_window.geometry("400x300")

    tk.Label(
        update_window,
        text="Update Customer Information",
        font=("Arial", 14, "bold"),
    ).pack(pady=10)

    # Input Fields
    tk.Label(update_window, text="Name:", font=("Arial", 12)).pack()
    name_entry = tk.Entry(update_window, font=("Arial", 12))
    name_entry.insert(0, customer["name"])
    name_entry.pack(pady=5)

    tk.Label(update_window, text="Contact Info:", font=("Arial", 12)).pack()
    contact_entry = tk.Entry(update_window, font=("Arial", 12))
    contact_entry.insert(0, customer["contact_info"])
    contact_entry.pack(pady=5)

    tk.Label(update_window, text="Payment Method:", font=("Arial", 12)).pack()
    payment_entry = tk.Entry(update_window, font=("Arial", 12))
    payment_entry.insert(0, customer["payment_method"])
    payment_entry.pack(pady=5)

    # Save Button
    tk.Button(
        update_window,
        text="Save",
        font=("Arial", 12),
        command=lambda: handle_save_customer_update(
            customer["customer_id"], name_entry, contact_entry, payment_entry, update_window
        ),
    ).pack(pady=10)


def handle_save_customer_update(customer_id, name_entry, contact_entry, payment_entry, update_window):
    """Handle saving updated customer information."""
    name = name_entry.get().strip()
    contact_info = contact_entry.get().strip()
    payment_method = payment_entry.get().strip()

    if name and contact_info and payment_method:
        message = update_customer_info(customer_id, name, contact_info, payment_method)
        messagebox.showinfo("Update Success", message)
        update_window.destroy()
    else:
        messagebox.showerror("Error", "All fields are required.")


# ---------------------------- Application Entry Point ---------------------------- #

def customer_management_app(parent_frame, switch_page_callback):
    """Main function to initialize the Customer Management App."""
    frame, update_button = setup_customer_management_ui(parent_frame, switch_page_callback)
    return frame
