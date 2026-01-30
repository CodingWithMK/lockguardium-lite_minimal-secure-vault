"""
LockGuardium Lite - Dialog Components
Modal dialogs for Add, Edit, and Delete operations
"""

import customtkinter as ctk
from typing import Optional, Callable, Dict
import os
import sys

# Add parent directories to path for imports
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from ui.theme import Colors, Fonts, Dimensions, Styles


class BaseDialog(ctk.CTkToplevel):
    """Base dialog class with common functionality."""

    def __init__(
        self,
        parent,
        title: str,
        width: int = Dimensions.DIALOG_WIDTH,
        height: int = Dimensions.DIALOG_HEIGHT,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)

        self.result = None

        # Configure window
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        self.configure(fg_color=Colors.BG_PRIMARY)

        # Make modal
        self.transient(parent)
        self.grab_set()

        # Center on parent
        self.update_idletasks()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Handle close
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

    def _on_cancel(self):
        """Handle cancel/close."""
        self.result = None
        self.destroy()

    def _on_submit(self):
        """Handle submit - override in subclasses."""
        self.destroy()

    def get_result(self):
        """Wait for dialog and return result."""
        self.wait_window()
        return self.result


class AddPasswordDialog(BaseDialog):
    """Dialog for adding a new password entry."""

    def __init__(self, parent, prefilled_password: str = "", **kwargs):
        super().__init__(parent, title="Add New Password", height=450, **kwargs)

        self.password_visible = False
        self.prefilled_password = prefilled_password

        self._create_widgets()

    def _create_widgets(self):
        """Create dialog widgets."""
        # Main content frame
        content = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        content.pack(fill="both", expand=True, padx=30, pady=20)

        # Header
        header = ctk.CTkLabel(
            content,
            text="➕ Add New Password",
            font=Fonts.heading(),
            text_color=Colors.GREEN_PRIMARY,
        )
        header.pack(anchor="w", pady=(0, 20))

        # Service/Website
        service_label = ctk.CTkLabel(
            content,
            text="Service/Website:",
            font=Fonts.body(),
            text_color=Colors.GREEN_PRIMARY,
        )
        service_label.pack(anchor="w", pady=(0, 5))

        self.service_entry = ctk.CTkEntry(
            content,
            placeholder_text="e.g., Google, GitHub, Netflix",
            height=40,
            **Styles.ENTRY,
        )
        self.service_entry.pack(fill="x", pady=(0, 15))

        # Email
        email_label = ctk.CTkLabel(
            content, text="Email:", font=Fonts.body(), text_color=Colors.GREEN_PRIMARY
        )
        email_label.pack(anchor="w", pady=(0, 5))

        self.email_entry = ctk.CTkEntry(
            content,
            placeholder_text="e.g., user@example.com",
            height=40,
            **Styles.ENTRY,
        )
        self.email_entry.pack(fill="x", pady=(0, 15))

        # Username
        username_label = ctk.CTkLabel(
            content,
            text="Username:",
            font=Fonts.body(),
            text_color=Colors.GREEN_PRIMARY,
        )
        username_label.pack(anchor="w", pady=(0, 5))

        self.username_entry = ctk.CTkEntry(
            content, placeholder_text="e.g., johndoe123", height=40, **Styles.ENTRY
        )
        self.username_entry.pack(fill="x", pady=(0, 15))

        # Password
        password_label = ctk.CTkLabel(
            content,
            text="Password:",
            font=Fonts.body(),
            text_color=Colors.GREEN_PRIMARY,
        )
        password_label.pack(anchor="w", pady=(0, 5))

        password_frame = ctk.CTkFrame(content, fg_color=Colors.TRANSPARENT)
        password_frame.pack(fill="x", pady=(0, 20))

        self.password_entry = ctk.CTkEntry(
            password_frame,
            placeholder_text="Enter password",
            show="•",
            height=40,
            **Styles.ENTRY,
        )
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Pre-fill password if provided
        if self.prefilled_password:
            self.password_entry.insert(0, self.prefilled_password)

        self.toggle_btn = ctk.CTkButton(
            password_frame,
            text="👁",
            width=45,
            height=40,
            command=self._toggle_password,
            **Styles.BUTTON_SECONDARY,
        )
        self.toggle_btn.pack(side="right")

        # Error label
        self.error_label = ctk.CTkLabel(
            content, text="", font=Fonts.small(), text_color=Colors.ERROR
        )
        self.error_label.pack(anchor="w")

        # Buttons
        buttons_frame = ctk.CTkFrame(content, fg_color=Colors.TRANSPARENT)
        buttons_frame.pack(fill="x", pady=(10, 0))

        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=self._on_cancel,
            width=120,
            height=40,
            **Styles.BUTTON_SECONDARY,
        )
        cancel_btn.pack(side="left")

        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Save",
            command=self._on_submit,
            width=120,
            height=40,
            **Styles.BUTTON_PRIMARY,
        )
        save_btn.pack(side="right")

    def _toggle_password(self):
        """Toggle password visibility."""
        self.password_visible = not self.password_visible
        self.password_entry.configure(show="" if self.password_visible else "•")
        self.toggle_btn.configure(text="🙈" if self.password_visible else "👁")

    def _on_submit(self):
        """Validate and submit."""
        service = self.service_entry.get().strip()
        email = self.email_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        # Validation
        if not service:
            self.error_label.configure(text="Service is required")
            return

        if not password:
            self.error_label.configure(text="Password is required")
            return

        self.result = {
            "service": service,
            "email": email,
            "username": username,
            "password": password,
        }
        self.destroy()


class EditPasswordDialog(BaseDialog):
    """Dialog for editing an existing password entry."""

    def __init__(self, parent, password_data: dict, **kwargs):
        super().__init__(parent, title="Edit Password", height=450, **kwargs)

        self.password_data = password_data
        self.password_visible = False

        self._create_widgets()

    def _create_widgets(self):
        """Create dialog widgets."""
        # Main content frame
        content = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        content.pack(fill="both", expand=True, padx=30, pady=20)

        # Header
        header = ctk.CTkLabel(
            content,
            text="✏️ Edit Password",
            font=Fonts.heading(),
            text_color=Colors.GREEN_PRIMARY,
        )
        header.pack(anchor="w", pady=(0, 20))

        # Service/Website
        service_label = ctk.CTkLabel(
            content,
            text="Service/Website:",
            font=Fonts.body(),
            text_color=Colors.GREEN_PRIMARY,
        )
        service_label.pack(anchor="w", pady=(0, 5))

        self.service_entry = ctk.CTkEntry(content, height=40, **Styles.ENTRY)
        self.service_entry.pack(fill="x", pady=(0, 15))
        self.service_entry.insert(0, self.password_data.get("service", ""))

        # Email
        email_label = ctk.CTkLabel(
            content, text="Email:", font=Fonts.body(), text_color=Colors.GREEN_PRIMARY
        )
        email_label.pack(anchor="w", pady=(0, 5))

        self.email_entry = ctk.CTkEntry(content, height=40, **Styles.ENTRY)
        self.email_entry.pack(fill="x", pady=(0, 15))
        self.email_entry.insert(0, self.password_data.get("email", ""))

        # Username
        username_label = ctk.CTkLabel(
            content,
            text="Username:",
            font=Fonts.body(),
            text_color=Colors.GREEN_PRIMARY,
        )
        username_label.pack(anchor="w", pady=(0, 5))

        self.username_entry = ctk.CTkEntry(content, height=40, **Styles.ENTRY)
        self.username_entry.pack(fill="x", pady=(0, 15))
        self.username_entry.insert(0, self.password_data.get("username", ""))

        # Password
        password_label = ctk.CTkLabel(
            content,
            text="Password:",
            font=Fonts.body(),
            text_color=Colors.GREEN_PRIMARY,
        )
        password_label.pack(anchor="w", pady=(0, 5))

        password_frame = ctk.CTkFrame(content, fg_color=Colors.TRANSPARENT)
        password_frame.pack(fill="x", pady=(0, 20))

        self.password_entry = ctk.CTkEntry(
            password_frame, show="•", height=40, **Styles.ENTRY
        )
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.password_entry.insert(0, self.password_data.get("password", ""))

        self.toggle_btn = ctk.CTkButton(
            password_frame,
            text="👁",
            width=45,
            height=40,
            command=self._toggle_password,
            **Styles.BUTTON_SECONDARY,
        )
        self.toggle_btn.pack(side="right")

        # Error label
        self.error_label = ctk.CTkLabel(
            content, text="", font=Fonts.small(), text_color=Colors.ERROR
        )
        self.error_label.pack(anchor="w")

        # Buttons
        buttons_frame = ctk.CTkFrame(content, fg_color=Colors.TRANSPARENT)
        buttons_frame.pack(fill="x", pady=(10, 0))

        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=self._on_cancel,
            width=120,
            height=40,
            **Styles.BUTTON_SECONDARY,
        )
        cancel_btn.pack(side="left")

        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Save Changes",
            command=self._on_submit,
            width=140,
            height=40,
            **Styles.BUTTON_PRIMARY,
        )
        save_btn.pack(side="right")

    def _toggle_password(self):
        """Toggle password visibility."""
        self.password_visible = not self.password_visible
        self.password_entry.configure(show="" if self.password_visible else "•")
        self.toggle_btn.configure(text="🙈" if self.password_visible else "👁")

    def _on_submit(self):
        """Validate and submit."""
        service = self.service_entry.get().strip()
        email = self.email_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        # Validation
        if not service:
            self.error_label.configure(text="Service is required")
            return

        if not password:
            self.error_label.configure(text="Password is required")
            return

        self.result = {
            "id": self.password_data.get("id"),
            "service": service,
            "email": email,
            "username": username,
            "password": password,
        }
        self.destroy()


class DeleteConfirmDialog(BaseDialog):
    """Confirmation dialog for deleting a password entry."""

    def __init__(self, parent, password_data: dict, **kwargs):
        super().__init__(
            parent, title="Confirm Delete", width=400, height=250, **kwargs
        )

        self.password_data = password_data

        self._create_widgets()

    def _create_widgets(self):
        """Create dialog widgets."""
        # Main content frame
        content = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        content.pack(fill="both", expand=True, padx=30, pady=20)

        # Warning icon
        warning_icon = ctk.CTkLabel(
            content,
            text="⚠️",
            font=(Fonts.FAMILY_MONO[0], 48),
            text_color=Colors.WARNING,
        )
        warning_icon.pack(pady=(10, 15))

        # Message
        message = ctk.CTkLabel(
            content,
            text=f"Are you sure you want to delete\nthe password for '{self.password_data.get('service', 'Unknown')}'?",
            font=Fonts.body(),
            text_color=Colors.GREEN_PRIMARY,
            justify="center",
        )
        message.pack(pady=(0, 10))

        # Warning text
        warning = ctk.CTkLabel(
            content,
            text="This action cannot be undone.",
            font=Fonts.small(),
            text_color=Colors.ERROR,
        )
        warning.pack(pady=(0, 20))

        # Buttons
        buttons_frame = ctk.CTkFrame(content, fg_color=Colors.TRANSPARENT)
        buttons_frame.pack(fill="x")

        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=self._on_cancel,
            width=120,
            height=40,
            **Styles.BUTTON_SECONDARY,
        )
        cancel_btn.pack(side="left", expand=True, padx=(0, 10))

        delete_btn = ctk.CTkButton(
            buttons_frame,
            text="Delete",
            command=self._on_submit,
            width=120,
            height=40,
            **Styles.BUTTON_DANGER,
        )
        delete_btn.pack(side="right", expand=True, padx=(10, 0))

    def _on_submit(self):
        """Confirm deletion."""
        self.result = True
        self.destroy()


class MessageDialog(BaseDialog):
    """Simple message dialog for notifications."""

    def __init__(self, parent, title: str, message: str, icon: str = "ℹ️", **kwargs):
        super().__init__(parent, title=title, width=350, height=200, **kwargs)

        self.message = message
        self.icon = icon

        self._create_widgets()

    def _create_widgets(self):
        """Create dialog widgets."""
        # Main content frame
        content = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        content.pack(fill="both", expand=True, padx=30, pady=20)

        # Icon
        icon_label = ctk.CTkLabel(
            content,
            text=self.icon,
            font=(Fonts.FAMILY_MONO[0], 36),
            text_color=Colors.GREEN_PRIMARY,
        )
        icon_label.pack(pady=(10, 15))

        # Message
        message_label = ctk.CTkLabel(
            content,
            text=self.message,
            font=Fonts.body(),
            text_color=Colors.GREEN_PRIMARY,
            justify="center",
            wraplength=280,
        )
        message_label.pack(pady=(0, 20))

        # OK button
        ok_btn = ctk.CTkButton(
            content,
            text="OK",
            command=self._on_submit,
            width=100,
            height=40,
            **Styles.BUTTON_PRIMARY,
        )
        ok_btn.pack()

    def _on_submit(self):
        """Close dialog."""
        self.result = True
        self.destroy()
