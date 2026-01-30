"""
LockGuardium Lite - Login Window
Secure login screen with typewriter animation effect
"""

import customtkinter as ctk
from typing import Callable, Optional
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.theme import (
    Colors,
    Fonts,
    Dimensions,
    Styles,
    Animation,
    IS_NEW_USER,
    DEMO_MASTER_PASSWORD,
)


class LoginWindow(ctk.CTk):
    """
    Login window with animated greeting and master password entry.
    Supports both new user setup and returning user authentication.
    """

    def __init__(
        self,
        on_login_success: Optional[Callable] = None,
        is_new_user: bool = IS_NEW_USER,
    ):
        super().__init__()

        self.on_login_success = on_login_success
        self.is_new_user = is_new_user
        self.password_visible = False
        self.confirm_password_visible = False

        # Configure window
        self._configure_window()

        # Configure appearance
        ctk.set_appearance_mode("dark")

        # Create widgets
        self._create_widgets()

        # Start typewriter animation
        self.after(500, self._start_typewriter_animation)

    def _configure_window(self):
        """Configure the login window properties."""
        self.title("LockGuardium Lite")
        self.geometry(f"{Dimensions.LOGIN_WIDTH}x{Dimensions.LOGIN_HEIGHT}")
        self.resizable(False, False)
        self.configure(fg_color=Colors.BG_PRIMARY)

        # Center window on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() - Dimensions.LOGIN_WIDTH) // 2
        y = (self.winfo_screenheight() - Dimensions.LOGIN_HEIGHT) // 2
        self.geometry(f"{Dimensions.LOGIN_WIDTH}x{Dimensions.LOGIN_HEIGHT}+{x}+{y}")

    def _create_widgets(self):
        """Create all login window widgets."""
        # Main container
        self.main_frame = ctk.CTkFrame(self, fg_color=Colors.BG_PRIMARY)
        self.main_frame.pack(fill="both", expand=True, padx=40, pady=30)

        # ===== Header Section =====
        self._create_header_section()

        # ===== Password Entry Section =====
        self._create_password_section()

        # ===== Action Button =====
        self._create_action_button()

        # ===== Footer Section =====
        self._create_footer_section()

    def _create_header_section(self):
        """Create the header with lock icon and animated greeting."""
        header_frame = ctk.CTkFrame(self.main_frame, fg_color=Colors.TRANSPARENT)
        header_frame.pack(fill="x", pady=(20, 30))

        # Lock icon
        self.lock_icon = ctk.CTkLabel(
            header_frame,
            text="🔒",
            font=(Fonts.FAMILY_MONO[0], 48),
            text_color=Colors.GREEN_PRIMARY,
        )
        self.lock_icon.pack(pady=(0, 15))

        # App name (animated)
        self.app_name_label = ctk.CTkLabel(
            header_frame, text="", font=Fonts.title(), text_color=Colors.GREEN_PRIMARY
        )
        self.app_name_label.pack(pady=(0, 5))

        # Greeting text (animated)
        self.greeting_label = ctk.CTkLabel(
            header_frame,
            text="",
            font=Fonts.subheading(),
            text_color=Colors.GREEN_SECONDARY,
        )
        self.greeting_label.pack(pady=(0, 10))

    def _create_password_section(self):
        """Create the password entry fields."""
        password_frame = ctk.CTkFrame(self.main_frame, fg_color=Colors.TRANSPARENT)
        password_frame.pack(fill="x", pady=20)

        # Master password field
        master_pass_frame = ctk.CTkFrame(password_frame, fg_color=Colors.TRANSPARENT)
        master_pass_frame.pack(fill="x", pady=(0, 15))

        self.password_entry = ctk.CTkEntry(
            master_pass_frame,
            placeholder_text="Enter master password..."
            if not self.is_new_user
            else "Create master password...",
            show="•",
            height=45,
            **Styles.ENTRY,
        )
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.toggle_password_btn = ctk.CTkButton(
            master_pass_frame,
            text="👁",
            width=45,
            height=45,
            command=self._toggle_password_visibility,
            **Styles.BUTTON_SECONDARY,
        )
        self.toggle_password_btn.pack(side="right")

        # Confirm password field (only for new users)
        if self.is_new_user:
            confirm_pass_frame = ctk.CTkFrame(
                password_frame, fg_color=Colors.TRANSPARENT
            )
            confirm_pass_frame.pack(fill="x", pady=(0, 10))

            self.confirm_password_entry = ctk.CTkEntry(
                confirm_pass_frame,
                placeholder_text="Confirm master password...",
                show="•",
                height=45,
                **Styles.ENTRY,
            )
            self.confirm_password_entry.pack(
                side="left", fill="x", expand=True, padx=(0, 10)
            )

            self.toggle_confirm_btn = ctk.CTkButton(
                confirm_pass_frame,
                text="👁",
                width=45,
                height=45,
                command=self._toggle_confirm_visibility,
                **Styles.BUTTON_SECONDARY,
            )
            self.toggle_confirm_btn.pack(side="right")

        # Error message label
        self.error_label = ctk.CTkLabel(
            password_frame, text="", font=Fonts.small(), text_color=Colors.ERROR
        )
        self.error_label.pack(pady=(5, 0))

        # Bind Enter key to login
        self.password_entry.bind("<Return>", lambda e: self._handle_login())
        if self.is_new_user:
            self.confirm_password_entry.bind("<Return>", lambda e: self._handle_login())

    def _create_action_button(self):
        """Create the main action button."""
        button_frame = ctk.CTkFrame(self.main_frame, fg_color=Colors.TRANSPARENT)
        button_frame.pack(fill="x", pady=20)

        button_text = "🔐 Create Vault" if self.is_new_user else "🔓 Unlock Vault"

        self.action_button = ctk.CTkButton(
            button_frame,
            text=button_text,
            height=50,
            command=self._handle_login,
            **Styles.BUTTON_PRIMARY,
        )
        self.action_button.pack(fill="x", padx=40)

    def _create_footer_section(self):
        """Create the footer with app information."""
        footer_frame = ctk.CTkFrame(self.main_frame, fg_color=Colors.TRANSPARENT)
        footer_frame.pack(side="bottom", fill="x", pady=(20, 0))

        # Separator line
        separator = ctk.CTkFrame(footer_frame, height=1, fg_color=Colors.GREEN_MUTED)
        separator.pack(fill="x", pady=(0, 15))

        # Version and license
        version_label = ctk.CTkLabel(
            footer_frame,
            text="LockGuardium Lite v1.0  |  MIT License",
            font=Fonts.small(),
            text_color=Colors.TEXT_MUTED,
        )
        version_label.pack(pady=(0, 5))

        # Tagline
        tagline_label = ctk.CTkLabel(
            footer_frame,
            text="Secure. Local. Private.",
            font=Fonts.small(),
            text_color=Colors.GREEN_MUTED,
        )
        tagline_label.pack()

    def _start_typewriter_animation(self):
        """Start the typewriter animation sequence."""
        app_name = "LockGuardium"
        greeting = "Welcome back!" if not self.is_new_user else "Create your vault"

        self._typewriter_effect(
            self.app_name_label,
            app_name,
            callback=lambda: self.after(
                Animation.TYPEWRITER_PAUSE,
                lambda: self._typewriter_effect(self.greeting_label, greeting),
            ),
        )

    def _typewriter_effect(
        self,
        label: ctk.CTkLabel,
        text: str,
        index: int = 0,
        callback: Optional[Callable] = None,
    ):
        """
        Animate text appearing character by character.

        Args:
            label: CTkLabel to update
            text: Full text to display
            index: Current character index
            callback: Function to call when complete
        """
        if index <= len(text):
            # Show text with cursor
            display_text = text[:index] + ("_" if index < len(text) else "")
            label.configure(text=display_text)
            self.after(
                Animation.TYPEWRITER_SPEED,
                lambda: self._typewriter_effect(label, text, index + 1, callback),
            )
        else:
            # Animation complete, remove cursor
            label.configure(text=text)
            if callback:
                callback()

    def _toggle_password_visibility(self):
        """Toggle master password visibility."""
        self.password_visible = not self.password_visible
        self.password_entry.configure(show="" if self.password_visible else "•")
        self.toggle_password_btn.configure(text="🙈" if self.password_visible else "👁")

    def _toggle_confirm_visibility(self):
        """Toggle confirm password visibility."""
        self.confirm_password_visible = not self.confirm_password_visible
        self.confirm_password_entry.configure(
            show="" if self.confirm_password_visible else "•"
        )
        self.toggle_confirm_btn.configure(
            text="🙈" if self.confirm_password_visible else "👁"
        )

    def _handle_login(self):
        """Handle login/create vault action."""
        password = self.password_entry.get()

        # Validate password length
        if len(password) < 8:
            self._show_error("Password must be at least 8 characters")
            return

        if self.is_new_user:
            confirm_password = self.confirm_password_entry.get()

            # Validate passwords match
            if password != confirm_password:
                self._show_error("Passwords do not match")
                return

            # Create vault (placeholder - would call auth service)
            self._login_success()
        else:
            # Validate password (placeholder - would call auth service)
            # For demo, accept the demo password or any 8+ char password
            if password == DEMO_MASTER_PASSWORD or len(password) >= 8:
                self._login_success()
            else:
                self._show_error("Invalid master password")

    def _show_error(self, message: str):
        """Display an error message."""
        self.error_label.configure(text=message)
        # Clear error after 3 seconds
        self.after(3000, lambda: self.error_label.configure(text=""))

    def _login_success(self):
        """Handle successful login."""
        if self.on_login_success:
            self.on_login_success()
        else:
            # Default behavior: open main window
            self.destroy()
            from ui.main_window import MainWindow

            main_window = MainWindow()
            main_window.mainloop()


# For testing the login window independently
if __name__ == "__main__":
    login = LoginWindow(is_new_user=False)
    login.mainloop()
