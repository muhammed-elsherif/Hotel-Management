import room_management
# import customer_management
import tkinter as tk

class NavigationBar(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.pack()
        self.pages = {}
        self.setup_ui()

    def setup_ui(self):
        tk.Button(self, text="Room Management", command=lambda: self.switch_page("room_management")).pack(side=tk.LEFT, padx=10)
        # tk.Button(self, text="Customer Management", command=lambda: self.switch_page("customer_management")).pack(side=tk.LEFT, padx=10)

    def switch_page(self, page_name):
        for page in self.pages.values():
            page.hide()
        if page_name in self.pages:
            self.pages[page_name].show()


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.navbar = NavigationBar(self.root)

        self.navbar.pages["room_management"] = room_management.create_room_management_ui(self.navbar)
        # self.navbar.pages["customer_management"] = customer_management.CustomerManagementApp(self.navbar)

        self.navbar.switch_page("room_management")


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()