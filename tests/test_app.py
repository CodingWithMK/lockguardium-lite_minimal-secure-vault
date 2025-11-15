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

        self.scaling_label = CTk.CTkLabel(self.sidebar, text="UI Scaling", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionmenu = CTk.CTkOptionMenu(self.sidebar_frame,
                                                    values=["75%", "80%", "85%", "90%", "95%", "100%", "110%", "120%"],
                                                    command=self.change_scaling_event
                                                    )
        self.scaling_optionmenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # ========== MAIN WINDOW WIDGETS ===========

        # Main Entry and Widgets
        self.search_entry = CTk.CTkEntry(self, placeholder="Search...")
        self.search_entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        # Greeting Label
        self.greeting_label = CTk.CTkLabel(self, width=80, height=15, text="Welcome back!", text_color="#fff")
        self.greeting_label.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # Main frame
        self.main_frame = CTk.CTkFrame(self, width=400, height=300, corner_radius=4, border_color="green", border_width=4)
        self.main_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.main_frame_title = CTk.CTkLabel(self.main_frame, width=20, height=5, text="My Passwords", text_color="#fff")
        self.main_frame_title.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.main_frame_textbox = CTk.CTkTextbox(self.main_frame, width=380, height=280, corner_radius=5, border_width=2)
        self.main_frame_textbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Tabview
        self.tabview = CTk.CTkTabview(self, width=250)
        self.tabview.grid(row=1, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Recent")
        self.tabview.add("Import")
        self.tabview.add("Export")
        self.tabview.tab("Recent").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Import").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Export").grid_columnconfigure(0, weight=1)

        




        

        