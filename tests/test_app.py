import customtkinter as CTk
import tkinter as tk
import tkinter.messagebox

CTk.set_appearance_mode("system")
CTk.set_default_color_theme("dark-blue")

class LockGuardiumLiteApp(CTk):
    def __init__(self):
        super.__init__()

        # Window properities
        self.title("LockGuardium Lite")
        self.geometry("1280x720")

        # Grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Sidebar frame
        self.sidebar_frame = CTk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = CTk.CTkLabel(self.sidebar_frame, text="LockGuardium Lite", font=CTk.CTkFont(size=20, weight="bold"))
        self.sidebar_button_1 = CTk.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = CTk.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = CTk.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_label = CTk.CTkButton(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionmenu = CTk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionmenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        

        

        