import tkinter as tk
from tkinter import messagebox
from config import db, cursor

class Customer:
    def __init__(self, customer_id, name, contact_info, payment_method):
        self.customer_id = customer_id
        self.name = name
        self.contact_info = contact_info
        self.payment_method = payment_method

    @staticmethod
    def search_customer(customer_id):
        query = "SELECT * FROM customers WHERE customerId = %s"
        cursor.execute(query, (customer_id,))
        result = cursor.fetchone()
        if result:
            return Customer(result[0], result[1], result[2], result[3])
        else:
            return None

    def update_customer_info(self, name, contact_info, payment_method):
        query = """
        UPDATE customers
        SET name = %s, contactInfo = %s, paymentMethod = %s
        WHERE customerId = %s
        """
        cursor.execute(query, (name, contact_info, payment_method, self.customer_id))
        db.commit()
        return "Customer information updated successfully."
    
    @staticmethod
    def add_customer_info(name, contact_info, payment_method):
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

class CustomerManagementApp:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.frame = tk.Frame(self.parent_frame)
        self.frame.pack()
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.frame, text="Customer Management", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self.frame, text="Enter Customer ID:", font=("Arial", 12)).pack(pady=5)
        self.customer_id_entry = tk.Entry(self.frame, font=("Arial", 12))
        self.customer_id_entry.pack(pady=5)

        tk.Button(self.frame, text="Search", font=("Arial", 12), command=self.search_customer).pack(pady=10)

        self.result_frame = tk.Frame(self.frame)
        self.result_frame.pack(pady=10)

        self.update_button = tk.Button(
            self.frame, text="Update Information", font=("Arial", 12), state=tk.DISABLED, command=self.update_customer
        )
        self.update_button.pack(pady=10)

        tk.Button(self.frame, text="Go Back", command=lambda: self.parent_frame.switch_page("navbar")).pack(pady=10)

    def show(self):
        self.frame.pack()

    def hide(self):
        self.frame.pack_forget()

    def search_customer(self):
        customer_id = self.customer_id_entry.get().strip()
        if not customer_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid Customer ID.")
            return

        customer = Customer.search_customer(int(customer_id))
        if customer:
            for widget in self.result_frame.winfo_children():
                widget.destroy()

            tk.Label(self.result_frame, text=f"Name: {customer.name}", font=("Arial", 12)).pack()
            tk.Label(self.result_frame, text=f"Contact: {customer.contact_info}", font=("Arial", 12)).pack()
            tk.Label(self.result_frame, text=f"Payment Method: {customer.payment_method}", font=("Arial", 12)).pack()

            self.customer = customer
            self.update_button.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Error", "Customer not found.")

    def update_customer(self):
        update_window = tk.Toplevel(self.frame)
        update_window.title("Update Customer Information")
        update_window.geometry("400x300")

        tk.Label(update_window, text="Update Customer Information", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(update_window, text="Name:", font=("Arial", 12)).pack()
        name_entry = tk.Entry(update_window, font=("Arial", 12))
        name_entry.insert(0, self.customer.name)
        name_entry.pack(pady=5)

        tk.Label(update_window, text="Contact Info:", font=("Arial", 12)).pack()
        contact_entry = tk.Entry(update_window, font=("Arial", 12))
        contact_entry.insert(0, self.customer.contact_info)
        contact_entry.pack(pady=5)

        tk.Label(update_window, text="Payment Method:", font=("Arial", 12)).pack()
        payment_entry = tk.Entry(update_window, font=("Arial", 12))
        payment_entry.insert(0, self.customer.payment_method)
        payment_entry.pack(pady=5)

        def save_updates():
            name = name_entry.get().strip()
            contact_info = contact_entry.get().strip()
            payment_method = payment_entry.get().strip()

            if name and contact_info and payment_method:
                message = self.customer.update_customer_info(name, contact_info, payment_method)
                messagebox.showinfo("Update Success", message)
                update_window.destroy()
            else:
                messagebox.showerror("Error", "All fields are required.")

        tk.Button(update_window, text="Save", font=("Arial", 12), command=save_updates).pack(pady=10)