"""
LockGuardium Lite - Dashboard Page Component
Overview dashboard showing password statistics
"""

import customtkinter as ctk
from typing import Optional
import os
import sys

# Add parent directories to path for imports
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from ui.theme import Colors, Fonts, Dimensions, Styles, PLACEHOLDER_PASSWORDS


class StatCard(ctk.CTkFrame):
    """A statistics card widget for the dashboard."""

    def __init__(
        self, parent, icon: str, title: str, value: str, subtitle: str = "", **kwargs
    ):
        super().__init__(parent, **kwargs)

        self.configure(
            fg_color=Colors.BG_SECONDARY,
            border_width=1,
            border_color=Colors.GREEN_MUTED,
            corner_radius=Dimensions.RADIUS_LARGE,
        )

        # Create inner content
        self._create_content(icon, title, value, subtitle)

    def _create_content(self, icon: str, title: str, value: str, subtitle: str):
        """Create the card content."""
        # Icon and title row
        header_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        icon_label = ctk.CTkLabel(
            header_frame,
            text=icon,
            font=(Fonts.FAMILY_MONO[0], 24),
            text_color=Colors.GREEN_PRIMARY,
        )
        icon_label.pack(side="left")

        title_label = ctk.CTkLabel(
            header_frame, text=title, font=Fonts.small(), text_color=Colors.TEXT_MUTED
        )
        title_label.pack(side="left", padx=(10, 0))

        # Value
        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=(Fonts.FAMILY_MONO[0], 32, "bold"),
            text_color=Colors.GREEN_PRIMARY,
        )
        self.value_label.pack(padx=20, pady=(0, 5))

        # Subtitle
        if subtitle:
            self.subtitle_label = ctk.CTkLabel(
                self, text=subtitle, font=Fonts.small(), text_color=Colors.TEXT_MUTED
            )
            self.subtitle_label.pack(padx=20, pady=(0, 20))
        else:
            # Add bottom padding
            spacer = ctk.CTkFrame(self, height=20, fg_color=Colors.TRANSPARENT)
            spacer.pack()

    def update_value(self, value: str, subtitle: str = ""):
        """Update the card value and subtitle."""
        self.value_label.configure(text=value)
        if hasattr(self, "subtitle_label") and subtitle:
            self.subtitle_label.configure(text=subtitle)


class DashboardPage(ctk.CTkFrame):
    """
    Dashboard page showing password statistics and recent activity.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.configure(fg_color=Colors.BG_PRIMARY)

        # Load placeholder data
        self.passwords = PLACEHOLDER_PASSWORDS

        # Create widgets
        self._create_widgets()

    def _create_widgets(self):
        """Create all dashboard widgets."""
        # ===== Page Header =====
        header_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        header_frame.pack(fill="x", padx=30, pady=(30, 20))

        title_label = ctk.CTkLabel(
            header_frame,
            text="📊 Dashboard",
            font=Fonts.heading(),
            text_color=Colors.GREEN_PRIMARY,
        )
        title_label.pack(side="left")

        # ===== Statistics Cards =====
        cards_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        cards_frame.pack(fill="x", padx=30, pady=10)

        # Configure grid
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="cards")

        # Total passwords card
        total_count = len(self.passwords)
        self.total_card = StatCard(
            cards_frame,
            icon="🔐",
            title="TOTAL",
            value=str(total_count),
            subtitle="Passwords Stored",
        )
        self.total_card.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nsew")

        # Last added card
        last_added = self._get_last_added()
        self.added_card = StatCard(
            cards_frame,
            icon="➕",
            title="LAST ADDED",
            value=last_added["service"],
            subtitle=last_added["date"],
        )
        self.added_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Last modified card
        last_modified = self._get_last_modified()
        self.modified_card = StatCard(
            cards_frame,
            icon="✏️",
            title="LAST MODIFIED",
            value=last_modified["service"],
            subtitle=last_modified["date"],
        )
        self.modified_card.grid(row=0, column=2, padx=(10, 0), pady=10, sticky="nsew")

        # ===== Quick Actions =====
        actions_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        actions_frame.pack(fill="x", padx=30, pady=(20, 10))

        actions_title = ctk.CTkLabel(
            actions_frame,
            text="Quick Actions",
            font=Fonts.subheading(),
            text_color=Colors.GREEN_PRIMARY,
        )
        actions_title.pack(anchor="w", pady=(0, 15))

        buttons_frame = ctk.CTkFrame(actions_frame, fg_color=Colors.TRANSPARENT)
        buttons_frame.pack(fill="x")

        quick_actions = [
            ("➕ Add Password", self._on_add_password),
            ("⚡ Generate Password", self._on_generate_password),
            ("🔍 Search Vault", self._on_search_vault),
        ]

        for text, command in quick_actions:
            btn = ctk.CTkButton(
                buttons_frame,
                text=text,
                height=45,
                command=command,
                **Styles.BUTTON_SECONDARY,
            )
            btn.pack(side="left", padx=(0, 15))

        # ===== Recent Activity =====
        activity_frame = ctk.CTkFrame(
            self,
            fg_color=Colors.BG_SECONDARY,
            border_width=1,
            border_color=Colors.GREEN_MUTED,
            corner_radius=Dimensions.RADIUS_LARGE,
        )
        activity_frame.pack(fill="both", expand=True, padx=30, pady=(20, 30))

        activity_header = ctk.CTkFrame(activity_frame, fg_color=Colors.TRANSPARENT)
        activity_header.pack(fill="x", padx=20, pady=(15, 10))

        activity_title = ctk.CTkLabel(
            activity_header,
            text="📋 Recent Activity",
            font=Fonts.subheading(),
            text_color=Colors.GREEN_PRIMARY,
        )
        activity_title.pack(side="left")

        # Activity list
        activity_list = ctk.CTkFrame(activity_frame, fg_color=Colors.TRANSPARENT)
        activity_list.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Show recent activities (placeholder)
        activities = [
            ("Twitter/X password was modified", "Jan 22, 2025"),
            ("Google password was modified", "Jan 20, 2025"),
            ("Netflix password was modified", "Jan 18, 2025"),
            ("Google password was added", "Jan 15, 2025"),
            ("GitHub password was added", "Jan 10, 2025"),
        ]

        for activity, date in activities:
            row = ctk.CTkFrame(activity_list, fg_color=Colors.TRANSPARENT)
            row.pack(fill="x", pady=5)

            bullet = ctk.CTkLabel(
                row, text="•", font=Fonts.body(), text_color=Colors.GREEN_SECONDARY
            )
            bullet.pack(side="left", padx=(0, 10))

            text = ctk.CTkLabel(
                row, text=activity, font=Fonts.body(), text_color=Colors.GREEN_PRIMARY
            )
            text.pack(side="left")

            date_label = ctk.CTkLabel(
                row, text=date, font=Fonts.small(), text_color=Colors.TEXT_MUTED
            )
            date_label.pack(side="right")

    def _get_last_added(self) -> dict:
        """Get the most recently added password."""
        if not self.passwords:
            return {"service": "None", "date": "-"}

        # Sort by created_at (descending)
        sorted_passwords = sorted(
            self.passwords, key=lambda x: x.get("created_at", ""), reverse=True
        )
        latest = sorted_passwords[0]
        return {
            "service": latest.get("service", "Unknown"),
            "date": latest.get("created_at", "-"),
        }

    def _get_last_modified(self) -> dict:
        """Get the most recently modified password."""
        if not self.passwords:
            return {"service": "None", "date": "-"}

        # Sort by modified_at (descending)
        sorted_passwords = sorted(
            self.passwords, key=lambda x: x.get("modified_at", ""), reverse=True
        )
        latest = sorted_passwords[0]
        return {
            "service": latest.get("service", "Unknown"),
            "date": latest.get("modified_at", "-"),
        }

    def _on_add_password(self):
        """Handle add password quick action."""
        # This would trigger the add dialog
        print("Add password clicked")

    def _on_generate_password(self):
        """Handle generate password quick action."""
        # This would navigate to generator page
        print("Generate password clicked")

    def _on_search_vault(self):
        """Handle search vault quick action."""
        # This would navigate to vault page with search focus
        print("Search vault clicked")

    def refresh(self):
        """Refresh the dashboard with updated data."""
        # In a real implementation, this would reload data from the vault service
        pass
