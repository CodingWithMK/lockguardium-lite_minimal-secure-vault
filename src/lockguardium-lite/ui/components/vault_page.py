"""
LockGuardium Lite - Vault Page Component
Password list view with CRUD operations
"""

import customtkinter as ctk
from typing import Optional, Callable, Dict, List
import os
import sys

# Add parent directories to path for imports
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from ui.theme import Colors, Fonts, Dimensions, Styles, PLACEHOLDER_PASSWORDS


class PasswordRow(ctk.CTkFrame):
    """A single password entry row in the vault table."""

    def __init__(
        self,
        parent,
        password_data: dict,
        on_reveal: Optional[Callable] = None,
        on_copy: Optional[Callable] = None,
        on_select: Optional[Callable] = None,
        is_selected: bool = False,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)

        self.password_data = password_data
        self.on_reveal = on_reveal
        self.on_copy = on_copy
        self.on_select = on_select
        self.is_revealed = False
        self.is_selected = is_selected

        self.configure(
            fg_color=Colors.GREEN_DARK if is_selected else Colors.BG_TERTIARY,
            corner_radius=Dimensions.RADIUS_SMALL,
            height=50,
        )

        self._create_content()

        # Bind click to select
        self.bind("<Button-1>", self._handle_click)

    def _create_content(self):
        """Create the row content."""
        # Configure grid columns
        self.grid_columnconfigure(0, weight=2)  # Service
        self.grid_columnconfigure(1, weight=3)  # Email
        self.grid_columnconfigure(2, weight=2)  # Username
        self.grid_columnconfigure(3, weight=2)  # Password
        self.grid_columnconfigure(4, weight=0)  # Actions

        # Service
        service_label = ctk.CTkLabel(
            self,
            text=self.password_data.get("service", ""),
            font=Fonts.body(),
            text_color=Colors.GREEN_PRIMARY,
            anchor="w",
        )
        service_label.grid(row=0, column=0, padx=(15, 10), pady=12, sticky="w")
        service_label.bind("<Button-1>", self._handle_click)

        # Email
        email_label = ctk.CTkLabel(
            self,
            text=self.password_data.get("email", ""),
            font=Fonts.body(),
            text_color=Colors.GREEN_PRIMARY,
            anchor="w",
        )
        email_label.grid(row=0, column=1, padx=10, pady=12, sticky="w")
        email_label.bind("<Button-1>", self._handle_click)

        # Username
        username_label = ctk.CTkLabel(
            self,
            text=self.password_data.get("username", ""),
            font=Fonts.body(),
            text_color=Colors.GREEN_PRIMARY,
            anchor="w",
        )
        username_label.grid(row=0, column=2, padx=10, pady=12, sticky="w")
        username_label.bind("<Button-1>", self._handle_click)

        # Password (masked)
        password_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        password_frame.grid(row=0, column=3, padx=10, pady=8, sticky="w")

        self.password_label = ctk.CTkLabel(
            password_frame,
            text="••••••••",
            font=Fonts.body(),
            text_color=Colors.GREEN_PRIMARY,
            anchor="w",
        )
        self.password_label.pack(side="left")

        # Actions
        actions_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        actions_frame.grid(row=0, column=4, padx=(5, 15), pady=8, sticky="e")

        # Reveal button
        self.reveal_btn = ctk.CTkButton(
            actions_frame,
            text="👁",
            width=35,
            height=35,
            command=self._toggle_reveal,
            fg_color=Colors.TRANSPARENT,
            hover_color=Colors.GREEN_DARK,
            text_color=Colors.GREEN_PRIMARY,
            font=(Fonts.FAMILY_MONO[0], 14),
        )
        self.reveal_btn.pack(side="left", padx=2)

        # Copy button
        self.copy_btn = ctk.CTkButton(
            actions_frame,
            text="📋",
            width=35,
            height=35,
            command=self._handle_copy,
            fg_color=Colors.TRANSPARENT,
            hover_color=Colors.GREEN_DARK,
            text_color=Colors.GREEN_PRIMARY,
            font=(Fonts.FAMILY_MONO[0], 14),
        )
        self.copy_btn.pack(side="left", padx=2)

    def _toggle_reveal(self):
        """Toggle password visibility."""
        self.is_revealed = not self.is_revealed

        if self.is_revealed:
            self.password_label.configure(text=self.password_data.get("password", ""))
            self.reveal_btn.configure(text="🙈")
        else:
            self.password_label.configure(text="••••••••")
            self.reveal_btn.configure(text="👁")

        if self.on_reveal:
            self.on_reveal(self.password_data, self.is_revealed)

    def _handle_copy(self):
        """Copy password to clipboard."""
        password = self.password_data.get("password", "")
        self.clipboard_clear()
        self.clipboard_append(password)

        # Visual feedback
        original_text = self.copy_btn.cget("text")
        self.copy_btn.configure(text="✓")
        self.after(1500, lambda: self.copy_btn.configure(text=original_text))

        if self.on_copy:
            self.on_copy(self.password_data)

    def _handle_click(self, event=None):
        """Handle row click for selection."""
        if self.on_select:
            self.on_select(self.password_data)

    def set_selected(self, selected: bool):
        """Update the selection state."""
        self.is_selected = selected
        self.configure(fg_color=Colors.GREEN_DARK if selected else Colors.BG_TERTIARY)


class VaultPage(ctk.CTkFrame):
    """
    Vault page showing all saved passwords with search and CRUD operations.
    """

    def __init__(
        self,
        parent,
        on_add: Optional[Callable] = None,
        on_edit: Optional[Callable] = None,
        on_delete: Optional[Callable] = None,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)

        self.on_add = on_add
        self.on_edit = on_edit
        self.on_delete = on_delete

        self.configure(fg_color=Colors.BG_PRIMARY)

        # Load placeholder data
        self.passwords = PLACEHOLDER_PASSWORDS.copy()
        self.filtered_passwords = self.passwords.copy()
        self.selected_password = None
        self.password_rows: List[PasswordRow] = []

        # Create widgets
        self._create_widgets()

    def _create_widgets(self):
        """Create all vault page widgets."""
        # ===== Header with Search and Actions =====
        header_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        header_frame.pack(fill="x", padx=30, pady=(30, 20))

        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="🔒 Password Vault",
            font=Fonts.heading(),
            text_color=Colors.GREEN_PRIMARY,
        )
        title_label.pack(side="left")

        # Actions (right side)
        actions_frame = ctk.CTkFrame(header_frame, fg_color=Colors.TRANSPARENT)
        actions_frame.pack(side="right")

        self.add_btn = ctk.CTkButton(
            actions_frame,
            text="➕ Add",
            width=100,
            height=38,
            command=self._handle_add,
            **Styles.BUTTON_PRIMARY,
        )
        self.add_btn.pack(side="left", padx=5)

        self.edit_btn = ctk.CTkButton(
            actions_frame,
            text="✏️ Edit",
            width=100,
            height=38,
            command=self._handle_edit,
            **Styles.BUTTON_SECONDARY,
        )
        self.edit_btn.pack(side="left", padx=5)

        self.delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️ Delete",
            width=100,
            height=38,
            command=self._handle_delete,
            **Styles.BUTTON_DANGER,
        )
        self.delete_btn.pack(side="left", padx=5)

        # ===== Search Bar =====
        search_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        search_frame.pack(fill="x", padx=30, pady=(0, 15))

        search_icon = ctk.CTkLabel(
            search_frame,
            text="🔍",
            font=(Fonts.FAMILY_MONO[0], 16),
            text_color=Colors.GREEN_PRIMARY,
        )
        search_icon.pack(side="left", padx=(0, 10))

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search passwords...",
            height=40,
            **Styles.ENTRY,
        )
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self._on_search)

        # ===== Table Container =====
        table_container = ctk.CTkFrame(
            self,
            fg_color=Colors.BG_SECONDARY,
            border_width=1,
            border_color=Colors.GREEN_MUTED,
            corner_radius=Dimensions.RADIUS_LARGE,
        )
        table_container.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        # Table header
        header_row = ctk.CTkFrame(
            table_container, fg_color=Colors.BG_TERTIARY, corner_radius=0
        )
        header_row.pack(fill="x", padx=2, pady=(2, 0))

        header_row.grid_columnconfigure(0, weight=2)  # Service
        header_row.grid_columnconfigure(1, weight=3)  # Email
        header_row.grid_columnconfigure(2, weight=2)  # Username
        header_row.grid_columnconfigure(3, weight=2)  # Password
        header_row.grid_columnconfigure(4, weight=0)  # Actions

        headers = ["Service", "Email", "Username", "Password", "Actions"]
        weights = [2, 3, 2, 2, 0]
        padx_values = [(15, 10), 10, 10, 10, (5, 15)]

        for i, (header, padx) in enumerate(zip(headers, padx_values)):
            label = ctk.CTkLabel(
                header_row,
                text=header,
                font=Fonts.small(),
                text_color=Colors.TEXT_MUTED,
                anchor="w",
            )
            label.grid(row=0, column=i, padx=padx, pady=12, sticky="w")

        # Scrollable password list
        self.password_list = ctk.CTkScrollableFrame(
            table_container, fg_color=Colors.TRANSPARENT, corner_radius=0
        )
        self.password_list.pack(fill="both", expand=True, padx=2, pady=(5, 2))

        # Populate password rows
        self._populate_password_list()

    def _populate_password_list(self):
        """Populate the password list with rows."""
        # Clear existing rows
        for row in self.password_rows:
            row.destroy()
        self.password_rows.clear()

        # Create rows for each password
        for password_data in self.filtered_passwords:
            row = PasswordRow(
                self.password_list,
                password_data=password_data,
                on_reveal=self._on_reveal,
                on_copy=self._on_copy,
                on_select=self._on_select,
                is_selected=(password_data == self.selected_password),
            )
            row.pack(fill="x", pady=3)
            self.password_rows.append(row)

        # Show empty state if no passwords
        if not self.filtered_passwords:
            empty_label = ctk.CTkLabel(
                self.password_list,
                text="No passwords found",
                font=Fonts.body(),
                text_color=Colors.TEXT_MUTED,
            )
            empty_label.pack(pady=50)

    def _on_search(self, event=None):
        """Filter passwords based on search query."""
        query = self.search_entry.get().lower()

        if query:
            self.filtered_passwords = [
                p
                for p in self.passwords
                if query in p.get("service", "").lower()
                or query in p.get("email", "").lower()
                or query in p.get("username", "").lower()
            ]
        else:
            self.filtered_passwords = self.passwords.copy()

        self._populate_password_list()

    def _on_select(self, password_data: dict):
        """Handle password row selection."""
        self.selected_password = password_data

        # Update row selection states
        for row in self.password_rows:
            row.set_selected(row.password_data == password_data)

    def _on_reveal(self, password_data: dict, is_revealed: bool):
        """Handle password reveal."""
        pass  # Could log or track reveals

    def _on_copy(self, password_data: dict):
        """Handle password copy."""
        pass  # Could log or clear clipboard after timeout

    def _handle_add(self):
        """Handle add password button click."""
        if self.on_add:
            self.on_add()

    def _handle_edit(self):
        """Handle edit password button click."""
        if self.selected_password and self.on_edit:
            self.on_edit(self.selected_password)
        elif not self.selected_password:
            # Show selection required message
            pass

    def _handle_delete(self):
        """Handle delete password button click."""
        if self.selected_password and self.on_delete:
            self.on_delete(self.selected_password)
        elif not self.selected_password:
            # Show selection required message
            pass

    def add_password(self, password_data: dict):
        """Add a new password to the list."""
        self.passwords.append(password_data)
        self.filtered_passwords = self.passwords.copy()
        self._populate_password_list()

    def update_password(self, password_id: int, updated_data: dict):
        """Update an existing password."""
        for i, p in enumerate(self.passwords):
            if p.get("id") == password_id:
                self.passwords[i] = {**p, **updated_data}
                break

        self.filtered_passwords = self.passwords.copy()
        self._on_search()  # Re-apply search filter

    def delete_password(self, password_id: int):
        """Delete a password from the list."""
        self.passwords = [p for p in self.passwords if p.get("id") != password_id]
        self.filtered_passwords = self.passwords.copy()
        self.selected_password = None
        self._on_search()  # Re-apply search filter

    def refresh(self):
        """Refresh the password list."""
        self._populate_password_list()
