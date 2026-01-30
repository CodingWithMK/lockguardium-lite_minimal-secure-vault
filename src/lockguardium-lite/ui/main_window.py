"""
LockGuardium Lite - Main Vault Window
Primary application window with navigation and page management
"""

import customtkinter as ctk
from typing import Optional, Callable
import os
import sys
from datetime import datetime

# Add parent directories to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.theme import Colors, Fonts, Dimensions, Styles, PLACEHOLDER_PASSWORDS
from ui.components.sidebar import Sidebar
from ui.components.dashboard import DashboardPage
from ui.components.vault_page import VaultPage
from ui.components.generator_page import GeneratorPage
from ui.components.settings_page import SettingsPage
from ui.components.dialogs import (
    AddPasswordDialog,
    EditPasswordDialog,
    DeleteConfirmDialog,
    MessageDialog,
)


class MainWindow(ctk.CTk):
    """
    Main vault window with sidebar navigation and page container.
    """

    def __init__(self, on_lock: Optional[Callable] = None):
        super().__init__()

        self.on_lock_callback = on_lock
        self.current_page = "dashboard"
        self.pages = {}

        # Auto-lock timer
        self.auto_lock_after_id = None
        self.auto_lock_minutes = 5

        # Configure window
        self._configure_window()

        # Configure appearance
        ctk.set_appearance_mode("dark")

        # Create layout
        self._create_layout()

        # Show initial page
        self._show_page("dashboard")

        # Start activity tracking for auto-lock
        self._reset_auto_lock_timer()
        self._bind_activity_events()

    def _configure_window(self):
        """Configure the main window properties."""
        self.title("LockGuardium Lite")
        self.geometry(
            f"{Dimensions.MAIN_DEFAULT_WIDTH}x{Dimensions.MAIN_DEFAULT_HEIGHT}"
        )
        self.minsize(Dimensions.MAIN_MIN_WIDTH, Dimensions.MAIN_MIN_HEIGHT)
        self.configure(fg_color=Colors.BG_PRIMARY)

        # Center window on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() - Dimensions.MAIN_DEFAULT_WIDTH) // 2
        y = (self.winfo_screenheight() - Dimensions.MAIN_DEFAULT_HEIGHT) // 2
        self.geometry(
            f"{Dimensions.MAIN_DEFAULT_WIDTH}x{Dimensions.MAIN_DEFAULT_HEIGHT}+{x}+{y}"
        )

    def _create_layout(self):
        """Create the main layout with sidebar and content area."""
        # Configure grid
        self.grid_columnconfigure(0, weight=0)  # Sidebar
        self.grid_columnconfigure(1, weight=1)  # Content
        self.grid_rowconfigure(0, weight=1)

        # ===== Sidebar =====
        self.sidebar = Sidebar(
            self,
            on_page_change=self._on_page_change,
            on_lock=self._on_lock,
            on_theme_change=self._on_theme_change,
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # ===== Content Area =====
        self.content_frame = ctk.CTkFrame(
            self, fg_color=Colors.BG_PRIMARY, corner_radius=0
        )
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # ===== Create Pages =====
        self._create_pages()

    def _create_pages(self):
        """Create all page components."""
        # Dashboard page
        self.pages["dashboard"] = DashboardPage(self.content_frame)

        # Vault page
        self.pages["vault"] = VaultPage(
            self.content_frame,
            on_add=self._on_add_password,
            on_edit=self._on_edit_password,
            on_delete=self._on_delete_password,
        )

        # Generator page
        self.pages["generator"] = GeneratorPage(
            self.content_frame, on_save_password=self._on_save_from_generator
        )

        # Settings page
        self.pages["settings"] = SettingsPage(
            self.content_frame,
            on_export=self._on_export,
            on_import=self._on_import,
            on_settings_change=self._on_settings_change,
        )

        # Initially hide all pages
        for page in self.pages.values():
            page.grid_remove()

    def _show_page(self, page_id: str):
        """Show a specific page and hide others."""
        # Hide current page
        if self.current_page in self.pages:
            self.pages[self.current_page].grid_remove()

        # Show new page
        if page_id in self.pages:
            self.pages[page_id].grid(row=0, column=0, sticky="nsew")
            self.current_page = page_id

        # Refresh page data if needed
        if page_id == "dashboard":
            self.pages["dashboard"].refresh()
        elif page_id == "vault":
            self.pages["vault"].refresh()

    def _on_page_change(self, page_id: str):
        """Handle page change from sidebar."""
        self._show_page(page_id)
        self._reset_auto_lock_timer()

    def _on_lock(self):
        """Handle lock action."""
        # Cancel auto-lock timer
        if self.auto_lock_after_id:
            self.after_cancel(self.auto_lock_after_id)

        if self.on_lock_callback:
            self.on_lock_callback()
        else:
            # Default: destroy main window and show login
            self.destroy()
            from ui.login_window import LoginWindow

            login = LoginWindow()
            login.mainloop()

    def _on_theme_change(self, theme: str):
        """Handle theme change."""
        self._reset_auto_lock_timer()

    # ===== Password CRUD Operations =====

    def _on_add_password(self):
        """Handle add password action."""
        dialog = AddPasswordDialog(self)
        result = dialog.get_result()

        if result:
            # Add to placeholder data with new ID
            new_id = max((p.get("id", 0) for p in PLACEHOLDER_PASSWORDS), default=0) + 1
            today = datetime.now().strftime("%Y-%m-%d")

            new_password = {
                "id": new_id,
                **result,
                "created_at": today,
                "modified_at": today,
            }

            PLACEHOLDER_PASSWORDS.append(new_password)
            self.pages["vault"].add_password(new_password)

            # Show success message
            MessageDialog(self, "Success", "Password added successfully!", icon="✅")

        self._reset_auto_lock_timer()

    def _on_edit_password(self, password_data: dict):
        """Handle edit password action."""
        dialog = EditPasswordDialog(self, password_data)
        result = dialog.get_result()

        if result:
            # Update placeholder data
            today = datetime.now().strftime("%Y-%m-%d")
            result["modified_at"] = today

            for i, p in enumerate(PLACEHOLDER_PASSWORDS):
                if p.get("id") == result.get("id"):
                    PLACEHOLDER_PASSWORDS[i] = {**p, **result}
                    break

            self.pages["vault"].update_password(result.get("id"), result)

            # Show success message
            MessageDialog(self, "Success", "Password updated successfully!", icon="✅")

        self._reset_auto_lock_timer()

    def _on_delete_password(self, password_data: dict):
        """Handle delete password action."""
        dialog = DeleteConfirmDialog(self, password_data)
        result = dialog.get_result()

        if result:
            # Remove from placeholder data
            password_id = password_data.get("id")
            for i, p in enumerate(PLACEHOLDER_PASSWORDS):
                if p.get("id") == password_id:
                    PLACEHOLDER_PASSWORDS.pop(i)
                    break

            self.pages["vault"].delete_password(password_id)

            # Show success message
            MessageDialog(self, "Success", "Password deleted successfully!", icon="✅")

        self._reset_auto_lock_timer()

    def _on_save_from_generator(self, password: str):
        """Handle save password from generator."""
        dialog = AddPasswordDialog(self, prefilled_password=password)
        result = dialog.get_result()

        if result:
            # Add to placeholder data with new ID
            new_id = max((p.get("id", 0) for p in PLACEHOLDER_PASSWORDS), default=0) + 1
            today = datetime.now().strftime("%Y-%m-%d")

            new_password = {
                "id": new_id,
                **result,
                "created_at": today,
                "modified_at": today,
            }

            PLACEHOLDER_PASSWORDS.append(new_password)
            self.pages["vault"].add_password(new_password)

            # Show success message
            MessageDialog(self, "Success", "Password saved to vault!", icon="✅")

        self._reset_auto_lock_timer()

    # ===== Settings Operations =====

    def _on_export(self):
        """Handle export vault action."""
        # Placeholder: would show file dialog
        MessageDialog(
            self,
            "Export",
            "Vault export would save an encrypted backup file.\n\n(Placeholder - not implemented)",
            icon="📤",
        )
        self._reset_auto_lock_timer()

    def _on_import(self):
        """Handle import vault action."""
        # Placeholder: would show file dialog
        MessageDialog(
            self,
            "Import",
            "Vault import would restore from an encrypted backup.\n\n(Placeholder - not implemented)",
            icon="📥",
        )
        self._reset_auto_lock_timer()

    def _on_settings_change(self, settings: dict):
        """Handle settings change."""
        # Update auto-lock timer if changed
        if settings.get("auto_lock_minutes") != self.auto_lock_minutes:
            self.auto_lock_minutes = settings.get("auto_lock_minutes", 5)
            self._reset_auto_lock_timer()

    # ===== Auto-lock Timer =====

    def _bind_activity_events(self):
        """Bind events to track user activity."""
        self.bind("<Key>", self._on_activity)
        self.bind("<Motion>", self._on_activity)
        self.bind("<Button>", self._on_activity)

    def _on_activity(self, event=None):
        """Handle user activity - reset auto-lock timer."""
        self._reset_auto_lock_timer()

    def _reset_auto_lock_timer(self):
        """Reset the auto-lock timer."""
        # Cancel existing timer
        if self.auto_lock_after_id:
            self.after_cancel(self.auto_lock_after_id)

        # Set new timer
        timeout_ms = self.auto_lock_minutes * 60 * 1000
        self.auto_lock_after_id = self.after(timeout_ms, self._on_lock)


# For testing the main window independently
if __name__ == "__main__":
    main = MainWindow()
    main.mainloop()
