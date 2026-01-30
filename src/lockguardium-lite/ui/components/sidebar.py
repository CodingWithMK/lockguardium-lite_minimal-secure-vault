"""
LockGuardium Lite - Collapsible Sidebar Component
Navigation sidebar with toggle functionality
"""

import customtkinter as ctk
from typing import Callable, Optional
import os
import sys

# Add parent directories to path for imports
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from ui.theme import Colors, Fonts, Dimensions, Styles


class Sidebar(ctk.CTkFrame):
    """
    Collapsible sidebar with navigation buttons and theme selector.
    """

    def __init__(
        self,
        parent,
        on_page_change: Optional[Callable[[str], None]] = None,
        on_lock: Optional[Callable] = None,
        on_theme_change: Optional[Callable[[str], None]] = None,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)

        self.on_page_change = on_page_change
        self.on_lock = on_lock
        self.on_theme_change = on_theme_change

        self.is_expanded = True
        self.current_page = "dashboard"

        # Configure frame
        self.configure(
            fg_color=Colors.BG_SECONDARY,
            corner_radius=0,
            width=Dimensions.SIDEBAR_EXPANDED_WIDTH,
        )

        # Navigation buttons
        self.nav_buttons = {}

        # Create widgets
        self._create_widgets()

        # Set initial active state
        self._set_active_button("dashboard")

    def _create_widgets(self):
        """Create all sidebar widgets."""
        # ===== Toggle Button =====
        self.toggle_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        self.toggle_frame.pack(fill="x", padx=10, pady=(15, 10))

        self.toggle_btn = ctk.CTkButton(
            self.toggle_frame,
            text="☰",
            width=40,
            height=40,
            command=self._toggle_sidebar,
            fg_color=Colors.TRANSPARENT,
            hover_color=Colors.BG_TERTIARY,
            text_color=Colors.GREEN_PRIMARY,
            font=(Fonts.FAMILY_MONO[0], 20),
        )
        self.toggle_btn.pack(side="left")

        self.menu_label = ctk.CTkLabel(
            self.toggle_frame,
            text="Menu",
            font=Fonts.subheading(),
            text_color=Colors.GREEN_PRIMARY,
        )
        self.menu_label.pack(side="left", padx=(10, 0))

        # ===== Separator =====
        self.separator1 = ctk.CTkFrame(self, height=1, fg_color=Colors.GREEN_MUTED)
        self.separator1.pack(fill="x", padx=15, pady=10)

        # ===== Navigation Buttons =====
        self.nav_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        self.nav_frame.pack(fill="x", padx=10)

        nav_items = [
            ("dashboard", "📊", "Dashboard"),
            ("vault", "🔒", "Vault"),
            ("generator", "⚡", "Generator"),
            ("settings", "⚙️", "Settings"),
        ]

        for page_id, icon, label in nav_items:
            btn_frame = ctk.CTkFrame(self.nav_frame, fg_color=Colors.TRANSPARENT)
            btn_frame.pack(fill="x", pady=3)

            btn = ctk.CTkButton(
                btn_frame,
                text=f"{icon}  {label}" if self.is_expanded else icon,
                anchor="w" if self.is_expanded else "center",
                height=45,
                command=lambda p=page_id: self._navigate_to(p),
                fg_color=Colors.TRANSPARENT,
                hover_color=Colors.GREEN_DARK,
                text_color=Colors.GREEN_PRIMARY,
                font=Fonts.body(),
            )
            btn.pack(fill="x")
            self.nav_buttons[page_id] = {"button": btn, "icon": icon, "label": label}

        # ===== Spacer =====
        spacer = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        spacer.pack(fill="both", expand=True)

        # ===== Bottom Section =====
        self.bottom_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        self.bottom_frame.pack(fill="x", padx=10, pady=(0, 15))

        # Separator
        self.separator2 = ctk.CTkFrame(
            self.bottom_frame, height=1, fg_color=Colors.GREEN_MUTED
        )
        self.separator2.pack(fill="x", pady=(0, 15))

        # Theme selector
        self.theme_frame = ctk.CTkFrame(self.bottom_frame, fg_color=Colors.TRANSPARENT)
        self.theme_frame.pack(fill="x", pady=(0, 10))

        self.theme_icon = ctk.CTkLabel(
            self.theme_frame, text="🎨", font=(Fonts.FAMILY_MONO[0], 16)
        )
        self.theme_icon.pack(side="left", padx=(5, 10))

        self.theme_dropdown = ctk.CTkOptionMenu(
            self.theme_frame,
            values=["Dark", "Light", "System"],
            command=self._change_theme,
            fg_color=Colors.BG_TERTIARY,
            button_color=Colors.GREEN_DARK,
            button_hover_color=Colors.GREEN_SECONDARY,
            dropdown_fg_color=Colors.BG_SECONDARY,
            dropdown_hover_color=Colors.GREEN_DARK,
            text_color=Colors.GREEN_PRIMARY,
            font=Fonts.small(),
            width=120,
        )
        self.theme_dropdown.pack(side="left", fill="x", expand=True)
        self.theme_dropdown.set("Dark")

        # Lock button
        self.lock_btn = ctk.CTkButton(
            self.bottom_frame,
            text="🔒  Lock" if self.is_expanded else "🔒",
            height=40,
            command=self._handle_lock,
            fg_color=Colors.GREEN_DARK,
            hover_color=Colors.GREEN_MUTED,
            text_color=Colors.GREEN_PRIMARY,
            font=Fonts.body(),
        )
        self.lock_btn.pack(fill="x", pady=(10, 0))

    def _toggle_sidebar(self):
        """Toggle sidebar between expanded and collapsed states."""
        self.is_expanded = not self.is_expanded

        if self.is_expanded:
            self.configure(width=Dimensions.SIDEBAR_EXPANDED_WIDTH)
            self.menu_label.pack(side="left", padx=(10, 0))
            self.theme_dropdown.pack(side="left", fill="x", expand=True)
            self.lock_btn.configure(text="🔒  Lock")

            # Update nav buttons
            for page_id, data in self.nav_buttons.items():
                data["button"].configure(
                    text=f"{data['icon']}  {data['label']}", anchor="w"
                )
        else:
            self.configure(width=Dimensions.SIDEBAR_COLLAPSED_WIDTH)
            self.menu_label.pack_forget()
            self.theme_dropdown.pack_forget()
            self.lock_btn.configure(text="🔒")

            # Update nav buttons
            for page_id, data in self.nav_buttons.items():
                data["button"].configure(text=data["icon"], anchor="center")

    def _navigate_to(self, page_id: str):
        """Navigate to a specific page."""
        self.current_page = page_id
        self._set_active_button(page_id)

        if self.on_page_change:
            self.on_page_change(page_id)

    def _set_active_button(self, active_page: str):
        """Highlight the active navigation button."""
        for page_id, data in self.nav_buttons.items():
            if page_id == active_page:
                data["button"].configure(
                    fg_color=Colors.GREEN_DARK, text_color=Colors.GREEN_PRIMARY
                )
            else:
                data["button"].configure(
                    fg_color=Colors.TRANSPARENT, text_color=Colors.GREEN_PRIMARY
                )

    def _change_theme(self, theme: str):
        """Handle theme change."""
        theme_map = {"Dark": "dark", "Light": "light", "System": "system"}

        ctk.set_appearance_mode(theme_map.get(theme, "dark"))

        if self.on_theme_change:
            self.on_theme_change(theme_map.get(theme, "dark"))

    def _handle_lock(self):
        """Handle lock button click."""
        if self.on_lock:
            self.on_lock()
