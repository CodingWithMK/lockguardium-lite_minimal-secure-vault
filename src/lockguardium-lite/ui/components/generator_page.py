"""
LockGuardium Lite - Generator Page Component
Password generator and strength checker side by side
"""

import customtkinter as ctk
from typing import Optional, Callable
import secrets
import string
import os
import sys

# Add parent directories to path for imports
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from ui.theme import Colors, Fonts, Dimensions, Styles


def generate_password(
    length: int = 16,
    use_uppercase: bool = True,
    use_lowercase: bool = True,
    use_digits: bool = True,
    use_special: bool = True,
) -> str:
    """Generate a secure random password."""
    characters = ""
    required_chars = []

    if use_uppercase:
        characters += string.ascii_uppercase
        required_chars.append(secrets.choice(string.ascii_uppercase))
    if use_lowercase:
        characters += string.ascii_lowercase
        required_chars.append(secrets.choice(string.ascii_lowercase))
    if use_digits:
        characters += string.digits
        required_chars.append(secrets.choice(string.digits))
    if use_special:
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        characters += special
        required_chars.append(secrets.choice(special))

    if not characters:
        return ""

    # Fill remaining length with random characters
    remaining_length = length - len(required_chars)
    password_chars = required_chars + [
        secrets.choice(characters) for _ in range(remaining_length)
    ]

    # Shuffle to randomize positions
    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)


def calculate_strength(password: str) -> tuple:
    """
    Calculate password strength.
    Returns (level_name, progress_value, color, tips)
    """
    if not password:
        return ("None", 0.0, Colors.TEXT_MUTED, [])

    score = 0
    tips = []

    # Length scoring
    if len(password) >= 8:
        score += 1
    else:
        tips.append("Use at least 8 characters")

    if len(password) >= 12:
        score += 1
    elif len(password) < 12:
        tips.append("Use 12+ characters for better security")

    if len(password) >= 16:
        score += 1

    # Character type scoring
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

    if has_upper:
        score += 1
    else:
        tips.append("Add uppercase letters (A-Z)")

    if has_lower:
        score += 1
    else:
        tips.append("Add lowercase letters (a-z)")

    if has_digit:
        score += 1
    else:
        tips.append("Add numbers (0-9)")

    if has_special:
        score += 1
    else:
        tips.append("Add special characters (!@#$%)")

    # Map score to level
    if score <= 2:
        return ("Weak", 0.25, Colors.STRENGTH_WEAK, tips)
    elif score <= 4:
        return ("Medium", 0.5, Colors.STRENGTH_MEDIUM, tips)
    elif score <= 6:
        return ("Good", 0.75, Colors.STRENGTH_GOOD, tips)
    else:
        return (
            "Strong",
            1.0,
            Colors.STRENGTH_STRONG,
            tips[:1] if tips else ["Great password!"],
        )


class PasswordGeneratorCard(ctk.CTkFrame):
    """Password generator card component."""

    def __init__(
        self, parent, on_save: Optional[Callable[[str], None]] = None, **kwargs
    ):
        super().__init__(parent, **kwargs)

        self.on_save = on_save
        self.generated_password = ""

        self.configure(
            fg_color=Colors.BG_SECONDARY,
            border_width=1,
            border_color=Colors.GREEN_MUTED,
            corner_radius=Dimensions.RADIUS_LARGE,
        )

        self._create_widgets()

    def _create_widgets(self):
        """Create generator widgets."""
        # Header
        header = ctk.CTkLabel(
            self,
            text="⚡ Password Generator",
            font=Fonts.subheading(),
            text_color=Colors.GREEN_PRIMARY,
        )
        header.pack(padx=20, pady=(20, 15), anchor="w")

        # Length slider
        length_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        length_frame.pack(fill="x", padx=20, pady=(0, 15))

        length_label = ctk.CTkLabel(
            length_frame,
            text="Length:",
            font=Fonts.body(),
            text_color=Colors.GREEN_PRIMARY,
        )
        length_label.pack(side="left")

        self.length_value = ctk.CTkLabel(
            length_frame,
            text="16",
            font=Fonts.body(),
            text_color=Colors.GREEN_SECONDARY,
            width=30,
        )
        self.length_value.pack(side="right")

        self.length_slider = ctk.CTkSlider(
            self,
            from_=12,
            to=64,
            number_of_steps=52,
            command=self._on_length_change,
            fg_color=Colors.BG_TERTIARY,
            progress_color=Colors.GREEN_SECONDARY,
            button_color=Colors.GREEN_PRIMARY,
            button_hover_color=Colors.GREEN_SECONDARY,
        )
        self.length_slider.pack(fill="x", padx=20, pady=(0, 20))
        self.length_slider.set(16)

        # Character options
        options_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        options_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.uppercase_var = ctk.BooleanVar(value=True)
        self.lowercase_var = ctk.BooleanVar(value=True)
        self.digits_var = ctk.BooleanVar(value=True)
        self.special_var = ctk.BooleanVar(value=True)

        options = [
            ("Uppercase (A-Z)", self.uppercase_var),
            ("Lowercase (a-z)", self.lowercase_var),
            ("Digits (0-9)", self.digits_var),
            ("Special (!@#$%^&*)", self.special_var),
        ]

        for text, var in options:
            cb = ctk.CTkCheckBox(
                options_frame,
                text=text,
                variable=var,
                font=Fonts.body(),
                text_color=Colors.GREEN_PRIMARY,
                fg_color=Colors.GREEN_SECONDARY,
                hover_color=Colors.GREEN_DARK,
                border_color=Colors.GREEN_MUTED,
                checkmark_color=Colors.BG_PRIMARY,
            )
            cb.pack(anchor="w", pady=5)

        # Generated password display
        password_frame = ctk.CTkFrame(
            self, fg_color=Colors.BG_TERTIARY, corner_radius=Dimensions.RADIUS_MEDIUM
        )
        password_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.password_display = ctk.CTkLabel(
            password_frame,
            text="Click Generate to create password",
            font=(Fonts.FAMILY_MONO[0], 14),
            text_color=Colors.TEXT_MUTED,
            wraplength=280,
        )
        self.password_display.pack(padx=15, pady=15)

        # Buttons
        buttons_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.generate_btn = ctk.CTkButton(
            buttons_frame,
            text="🔄 Generate",
            command=self._generate,
            **Styles.BUTTON_PRIMARY,
        )
        self.generate_btn.pack(side="left", padx=(0, 10))

        self.copy_btn = ctk.CTkButton(
            buttons_frame, text="📋 Copy", command=self._copy, **Styles.BUTTON_SECONDARY
        )
        self.copy_btn.pack(side="left", padx=(0, 10))

        self.save_btn = ctk.CTkButton(
            buttons_frame, text="💾 Save", command=self._save, **Styles.BUTTON_SECONDARY
        )
        self.save_btn.pack(side="left")

    def _on_length_change(self, value):
        """Handle length slider change."""
        self.length_value.configure(text=str(int(value)))

    def _generate(self):
        """Generate a new password."""
        length = int(self.length_slider.get())

        self.generated_password = generate_password(
            length=length,
            use_uppercase=self.uppercase_var.get(),
            use_lowercase=self.lowercase_var.get(),
            use_digits=self.digits_var.get(),
            use_special=self.special_var.get(),
        )

        if self.generated_password:
            self.password_display.configure(
                text=self.generated_password, text_color=Colors.GREEN_PRIMARY
            )
        else:
            self.password_display.configure(
                text="Select at least one character type", text_color=Colors.ERROR
            )

    def _copy(self):
        """Copy password to clipboard."""
        if self.generated_password:
            self.clipboard_clear()
            self.clipboard_append(self.generated_password)

            # Visual feedback
            original_text = self.copy_btn.cget("text")
            self.copy_btn.configure(text="✓ Copied!")
            self.after(1500, lambda: self.copy_btn.configure(text=original_text))

    def _save(self):
        """Save password to vault."""
        if self.generated_password and self.on_save:
            self.on_save(self.generated_password)


class StrengthCheckerCard(ctk.CTkFrame):
    """Password strength checker card component."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.configure(
            fg_color=Colors.BG_SECONDARY,
            border_width=1,
            border_color=Colors.GREEN_MUTED,
            corner_radius=Dimensions.RADIUS_LARGE,
        )

        self._create_widgets()

    def _create_widgets(self):
        """Create strength checker widgets."""
        # Header
        header = ctk.CTkLabel(
            self,
            text="🔍 Strength Checker",
            font=Fonts.subheading(),
            text_color=Colors.GREEN_PRIMARY,
        )
        header.pack(padx=20, pady=(20, 15), anchor="w")

        # Password entry
        entry_label = ctk.CTkLabel(
            self,
            text="Enter password to check:",
            font=Fonts.small(),
            text_color=Colors.TEXT_MUTED,
        )
        entry_label.pack(padx=20, anchor="w")

        self.password_entry = ctk.CTkEntry(
            self,
            placeholder_text="Type a password...",
            height=40,
            show="",
            **Styles.ENTRY,
        )
        self.password_entry.pack(fill="x", padx=20, pady=(5, 20))
        self.password_entry.bind("<KeyRelease>", self._check_strength)

        # Strength indicator
        strength_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        strength_frame.pack(fill="x", padx=20, pady=(0, 10))

        strength_label = ctk.CTkLabel(
            strength_frame,
            text="Strength:",
            font=Fonts.body(),
            text_color=Colors.GREEN_PRIMARY,
        )
        strength_label.pack(side="left")

        self.strength_value = ctk.CTkLabel(
            strength_frame, text="None", font=Fonts.body(), text_color=Colors.TEXT_MUTED
        )
        self.strength_value.pack(side="right")

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self,
            height=20,
            corner_radius=Dimensions.RADIUS_SMALL,
            fg_color=Colors.BG_TERTIARY,
            progress_color=Colors.TEXT_MUTED,
        )
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 20))
        self.progress_bar.set(0)

        # Tips section
        tips_header = ctk.CTkLabel(
            self,
            text="Tips to improve:",
            font=Fonts.small(),
            text_color=Colors.TEXT_MUTED,
        )
        tips_header.pack(padx=20, anchor="w", pady=(0, 5))

        self.tips_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        self.tips_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.tips_labels = []
        for i in range(4):
            tip_label = ctk.CTkLabel(
                self.tips_frame,
                text="",
                font=Fonts.small(),
                text_color=Colors.TEXT_MUTED,
                anchor="w",
            )
            tip_label.pack(anchor="w", pady=2)
            self.tips_labels.append(tip_label)

    def _check_strength(self, event=None):
        """Check password strength in real-time."""
        password = self.password_entry.get()
        level, progress, color, tips = calculate_strength(password)

        # Update strength label
        self.strength_value.configure(text=level, text_color=color)

        # Update progress bar
        self.progress_bar.configure(progress_color=color)
        self.progress_bar.set(progress)

        # Update tips
        for i, label in enumerate(self.tips_labels):
            if i < len(tips):
                label.configure(text=f"• {tips[i]}")
            else:
                label.configure(text="")


class GeneratorPage(ctk.CTkFrame):
    """
    Generator page with password generator and strength checker side by side.
    """

    def __init__(
        self, parent, on_save_password: Optional[Callable[[str], None]] = None, **kwargs
    ):
        super().__init__(parent, **kwargs)

        self.on_save_password = on_save_password
        self.configure(fg_color=Colors.BG_PRIMARY)

        self._create_widgets()

    def _create_widgets(self):
        """Create generator page widgets."""
        # ===== Page Header =====
        header_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        header_frame.pack(fill="x", padx=30, pady=(30, 20))

        title_label = ctk.CTkLabel(
            header_frame,
            text="⚡ Password Generator & Strength Checker",
            font=Fonts.heading(),
            text_color=Colors.GREEN_PRIMARY,
        )
        title_label.pack(side="left")

        # ===== Content Area (Side by Side) =====
        content_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        content_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        # Configure grid for side-by-side layout
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # Password Generator Card (Left)
        self.generator_card = PasswordGeneratorCard(
            content_frame, on_save=self._handle_save
        )
        self.generator_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")

        # Strength Checker Card (Right)
        self.strength_card = StrengthCheckerCard(content_frame)
        self.strength_card.grid(row=0, column=1, padx=(10, 0), sticky="nsew")

    def _handle_save(self, password: str):
        """Handle save password request."""
        if self.on_save_password:
            self.on_save_password(password)
