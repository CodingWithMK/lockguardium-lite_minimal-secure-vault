import customtkinter
from tkinter import ttk, messagebox, simpledialog
from tests import test_generator
from tests import test_crypto

class PasswordManagerApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("LockGuardium Lite - Prototype")
        self.geometry("800x500")
        self.minsize(600, 400)

        self.password_manager = None

        # Inıtialize widget references
        self.password_listbox = None
        self.search_entry = None

        self.setup_master_password = None

        if self.password_manager is None:
            self.destroy()
            return
        
        self.setup_style()
        self.create_widgets()




if __name__ == "__main__":
    pass