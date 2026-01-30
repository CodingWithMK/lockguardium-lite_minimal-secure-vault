"""
LockGuardium Lite - Main Application Entry Point
Secure Password Vault Application
"""

import customtkinter as ctk
import os
import sys

# Add the src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from ui.theme import Colors, IS_NEW_USER


class LockGuardiumApp:
    """
    Main application controller.
    Manages the application lifecycle and window transitions.
    """

    def __init__(self):
        self.current_window = None
        self.is_authenticated = False

        # Configure global appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

    def run(self):
        """Start the application."""
        self._show_login()

    def _show_login(self):
        """Show the login window."""
        # Destroy current window if exists
        if self.current_window:
            self.current_window.destroy()

        # Check if this is a new user (placeholder - would check if vault exists)
        is_new_user = IS_NEW_USER

        # Create login window
        self.current_window = LoginWindow(
            on_login_success=self._on_login_success, is_new_user=is_new_user
        )
        self.current_window.mainloop()

    def _on_login_success(self):
        """Handle successful login."""
        self.is_authenticated = True

        # Destroy login window
        if self.current_window:
            self.current_window.destroy()

        # Show main vault window
        self._show_main()

    def _show_main(self):
        """Show the main vault window."""
        self.current_window = MainWindow(on_lock=self._on_lock)
        self.current_window.mainloop()

    def _on_lock(self):
        """Handle lock action from main window."""
        self.is_authenticated = False

        # Destroy main window
        if self.current_window:
            self.current_window.destroy()

        # Show login window
        self._show_login()


def main():
    """Main entry point."""
    app = LockGuardiumApp()
    app.run()


if __name__ == "__main__":
    main()
