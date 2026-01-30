"""
LockGuardium Lite - Settings Page Component
Application settings and preferences
"""

import customtkinter as ctk
from typing import Optional, Callable
import os
import sys

# Add parent directories to path for imports
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from ui.theme import Colors, Fonts, Dimensions, Styles, PLACEHOLDER_SETTINGS


class SettingsSection(ctk.CTkFrame):
    """A settings section with header and content."""

    def __init__(self, parent, title: str, icon: str = "", **kwargs):
        super().__init__(parent, **kwargs)

        self.configure(
            fg_color=Colors.BG_SECONDARY,
            border_width=1,
            border_color=Colors.GREEN_MUTED,
            corner_radius=Dimensions.RADIUS_LARGE,
        )

        # Header
        header = ctk.CTkLabel(
            self,
            text=f"{icon} {title}" if icon else title,
            font=Fonts.subheading(),
            text_color=Colors.GREEN_PRIMARY,
        )
        header.pack(padx=20, pady=(15, 10), anchor="w")

        # Content frame for settings
        self.content = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        self.content.pack(fill="x", padx=20, pady=(0, 20))


class SettingsPage(ctk.CTkFrame):
    """
    Settings page with various application preferences.
    """

    def __init__(
        self,
        parent,
        on_export: Optional[Callable] = None,
        on_import: Optional[Callable] = None,
        on_settings_change: Optional[Callable[[dict], None]] = None,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)

        self.on_export = on_export
        self.on_import = on_import
        self.on_settings_change = on_settings_change

        self.configure(fg_color=Colors.BG_PRIMARY)

        # Load placeholder settings
        self.settings = PLACEHOLDER_SETTINGS.copy()

        self._create_widgets()

    def _create_widgets(self):
        """Create settings page widgets."""
        # ===== Page Header =====
        header_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        header_frame.pack(fill="x", padx=30, pady=(30, 20))

        title_label = ctk.CTkLabel(
            header_frame,
            text="⚙️ Settings",
            font=Fonts.heading(),
            text_color=Colors.GREEN_PRIMARY,
        )
        title_label.pack(side="left")

        # ===== Scrollable Content =====
        content_scroll = ctk.CTkScrollableFrame(
            self, fg_color=Colors.TRANSPARENT, corner_radius=0
        )
        content_scroll.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        # ===== Security Section =====
        security_section = SettingsSection(content_scroll, "Security", "🔒")
        security_section.pack(fill="x", pady=(0, 15))

        # Auto-lock timer
        autolock_frame = ctk.CTkFrame(
            security_section.content, fg_color=Colors.TRANSPARENT
        )
        autolock_frame.pack(fill="x", pady=5)

        autolock_label = ctk.CTkLabel(
            autolock_frame,
            text="Auto-lock timer:",
            font=Fonts.body(),
            text_color=Colors.GREEN_PRIMARY,
        )
        autolock_label.pack(side="left")

        self.autolock_dropdown = ctk.CTkOptionMenu(
            autolock_frame,
            values=["1 minute", "2 minutes", "5 minutes", "10 minutes", "15 minutes"],
            command=self._on_autolock_change,
            fg_color=Colors.BG_TERTIARY,
            button_color=Colors.GREEN_DARK,
            button_hover_color=Colors.GREEN_SECONDARY,
            dropdown_fg_color=Colors.BG_SECONDARY,
            dropdown_hover_color=Colors.GREEN_DARK,
            text_color=Colors.GREEN_PRIMARY,
            font=Fonts.body(),
            width=150,
        )
        self.autolock_dropdown.pack(side="right")
        self.autolock_dropdown.set(f"{self.settings['auto_lock_minutes']} minutes")

        # Clipboard clear timer
        clipboard_frame = ctk.CTkFrame(
            security_section.content, fg_color=Colors.TRANSPARENT
        )
        clipboard_frame.pack(fill="x", pady=5)

        clipboard_label = ctk.CTkLabel(
            clipboard_frame,
            text="Clear clipboard after:",
            font=Fonts.body(),
            text_color=Colors.GREEN_PRIMARY,
        )
        clipboard_label.pack(side="left")

        self.clipboard_dropdown = ctk.CTkOptionMenu(
            clipboard_frame,
            values=["10 seconds", "30 seconds", "60 seconds", "120 seconds"],
            command=self._on_clipboard_change,
            fg_color=Colors.BG_TERTIARY,
            button_color=Colors.GREEN_DARK,
            button_hover_color=Colors.GREEN_SECONDARY,
            dropdown_fg_color=Colors.BG_SECONDARY,
            dropdown_hover_color=Colors.GREEN_DARK,
            text_color=Colors.GREEN_PRIMARY,
            font=Fonts.body(),
            width=150,
        )
        self.clipboard_dropdown.pack(side="right")
        self.clipboard_dropdown.set(
            f"{self.settings['clipboard_clear_seconds']} seconds"
        )

        # ===== Generator Section =====
        generator_section = SettingsSection(content_scroll, "Password Generator", "⚡")
        generator_section.pack(fill="x", pady=15)

        # Default password length
        length_frame = ctk.CTkFrame(
            generator_section.content, fg_color=Colors.TRANSPARENT
        )
        length_frame.pack(fill="x", pady=5)

        length_label = ctk.CTkLabel(
            length_frame,
            text="Default password length:",
            font=Fonts.body(),
            text_color=Colors.GREEN_PRIMARY,
        )
        length_label.pack(side="left")

        length_input_frame = ctk.CTkFrame(length_frame, fg_color=Colors.TRANSPARENT)
        length_input_frame.pack(side="right")

        self.length_entry = ctk.CTkEntry(
            length_input_frame, width=80, height=35, **Styles.ENTRY
        )
        self.length_entry.pack(side="left", padx=(0, 10))
        self.length_entry.insert(0, str(self.settings["default_password_length"]))
        self.length_entry.bind("<FocusOut>", self._on_length_change)

        length_hint = ctk.CTkLabel(
            length_input_frame,
            text="(min: 12)",
            font=Fonts.small(),
            text_color=Colors.TEXT_MUTED,
        )
        length_hint.pack(side="left")

        # ===== Appearance Section =====
        appearance_section = SettingsSection(content_scroll, "Appearance", "🎨")
        appearance_section.pack(fill="x", pady=15)

        # Theme
        theme_frame = ctk.CTkFrame(
            appearance_section.content, fg_color=Colors.TRANSPARENT
        )
        theme_frame.pack(fill="x", pady=5)

        theme_label = ctk.CTkLabel(
            theme_frame,
            text="Theme:",
            font=Fonts.body(),
            text_color=Colors.GREEN_PRIMARY,
        )
        theme_label.pack(side="left")

        self.theme_dropdown = ctk.CTkOptionMenu(
            theme_frame,
            values=["Dark", "Light", "System"],
            command=self._on_theme_change,
            fg_color=Colors.BG_TERTIARY,
            button_color=Colors.GREEN_DARK,
            button_hover_color=Colors.GREEN_SECONDARY,
            dropdown_fg_color=Colors.BG_SECONDARY,
            dropdown_hover_color=Colors.GREEN_DARK,
            text_color=Colors.GREEN_PRIMARY,
            font=Fonts.body(),
            width=150,
        )
        self.theme_dropdown.pack(side="right")
        self.theme_dropdown.set(self.settings["theme"].capitalize())

        # ===== Data Section =====
        data_section = SettingsSection(content_scroll, "Data Management", "💾")
        data_section.pack(fill="x", pady=15)

        # Export/Import buttons
        buttons_frame = ctk.CTkFrame(data_section.content, fg_color=Colors.TRANSPARENT)
        buttons_frame.pack(fill="x", pady=10)

        self.export_btn = ctk.CTkButton(
            buttons_frame,
            text="📤 Export Vault",
            command=self._handle_export,
            height=45,
            **Styles.BUTTON_SECONDARY,
        )
        self.export_btn.pack(side="left", padx=(0, 15))

        self.import_btn = ctk.CTkButton(
            buttons_frame,
            text="📥 Import Vault",
            command=self._handle_import,
            height=45,
            **Styles.BUTTON_SECONDARY,
        )
        self.import_btn.pack(side="left")

        # Export/Import info
        info_label = ctk.CTkLabel(
            data_section.content,
            text="Export creates an encrypted backup of your vault.\nImport restores from a previous backup.",
            font=Fonts.small(),
            text_color=Colors.TEXT_MUTED,
            justify="left",
        )
        info_label.pack(anchor="w", pady=(5, 0))

        # ===== About Section =====
        about_section = SettingsSection(content_scroll, "About", "ℹ️")
        about_section.pack(fill="x", pady=15)

        about_info = [
            ("Application:", "LockGuardium Lite"),
            ("Version:", "1.0.0"),
            ("License:", "MIT License"),
            ("Author:", "Muhammed Musab Kaya"),
        ]

        for label, value in about_info:
            row = ctk.CTkFrame(about_section.content, fg_color=Colors.TRANSPARENT)
            row.pack(fill="x", pady=3)

            label_widget = ctk.CTkLabel(
                row, text=label, font=Fonts.body(), text_color=Colors.TEXT_MUTED
            )
            label_widget.pack(side="left")

            value_widget = ctk.CTkLabel(
                row, text=value, font=Fonts.body(), text_color=Colors.GREEN_PRIMARY
            )
            value_widget.pack(side="right")

    def _on_autolock_change(self, value: str):
        """Handle auto-lock timer change."""
        minutes = int(value.split()[0])
        self.settings["auto_lock_minutes"] = minutes
        self._notify_change()

    def _on_clipboard_change(self, value: str):
        """Handle clipboard clear timer change."""
        seconds = int(value.split()[0])
        self.settings["clipboard_clear_seconds"] = seconds
        self._notify_change()

    def _on_length_change(self, event=None):
        """Handle default password length change."""
        try:
            length = int(self.length_entry.get())
            if length < 12:
                length = 12
                self.length_entry.delete(0, "end")
                self.length_entry.insert(0, "12")
            self.settings["default_password_length"] = length
            self._notify_change()
        except ValueError:
            self.length_entry.delete(0, "end")
            self.length_entry.insert(0, str(self.settings["default_password_length"]))

    def _on_theme_change(self, value: str):
        """Handle theme change."""
        theme = value.lower()
        self.settings["theme"] = theme
        ctk.set_appearance_mode(theme)
        self._notify_change()

    def _handle_export(self):
        """Handle export button click."""
        if self.on_export:
            self.on_export()
        else:
            # Placeholder: Show file dialog simulation
            print("Export vault clicked - would show file save dialog")

    def _handle_import(self):
        """Handle import button click."""
        if self.on_import:
            self.on_import()
        else:
            # Placeholder: Show file dialog simulation
            print("Import vault clicked - would show file open dialog")

    def _notify_change(self):
        """Notify listeners of settings change."""
        if self.on_settings_change:
            self.on_settings_change(self.settings)

    def get_settings(self) -> dict:
        """Get current settings."""
        return self.settings.copy()
