import tkinter as tk
import room_management
import customer_management
class NavigationBar(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.pack(side=tk.TOP, fill=tk.X)
        self.pages = {}
        self.setup_ui()

    def setup_ui(self):
        tk.Button(self, text="Room Management", command=lambda: self.switch_page("room_management")).pack(side=tk.LEFT, padx=10)
        tk.Button(self, text="Customer Management", command=lambda: self.switch_page("customer_management")).pack(side=tk.LEFT, padx=10)

    def switch_page(self, page_name):
        for page in self.pages.values():
            page.hide()

        if page_name in self.pages:
            self.pages[page_name].show()
        else:
            tk.messagebox.showerror("Error", f"Page '{page_name}' not found.")
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("800x600")

        self.navbar = NavigationBar(self.root)

        # Initialize pages and add them to the navigation bar
        self.navbar.pages["room_management"] = room_management.create_room_management_ui(self.root)
        # self.navbar.pages["customer_management"] = customer_management.setup_customer_management_ui(self.root)

        # Show the default page
        # self.navbar.switch_page("room_management")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()