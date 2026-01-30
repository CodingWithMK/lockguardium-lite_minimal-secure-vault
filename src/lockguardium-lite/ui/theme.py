"""
LockGuardium Lite - Theme Configuration
Black and green security-focused color palette
"""

# =============================================================================
# COLOR PALETTE
# =============================================================================


class Colors:
    """Color constants for the application theme."""

    # Background colors
    BG_PRIMARY = "#0D0D0D"  # Main window background (near black)
    BG_SECONDARY = "#1A1A1A"  # Cards, sidebar, frames
    BG_TERTIARY = "#252525"  # Input fields, hover states
    BG_DARK = "#050505"  # Darker accents

    # Green palette (Matrix-style)
    GREEN_PRIMARY = "#00FF41"  # Main text, active elements (bright green)
    GREEN_SECONDARY = "#00CC33"  # Buttons, highlights
    GREEN_MUTED = "#2D5A27"  # Borders, disabled states
    GREEN_DARK = "#0A3D0A"  # Button hover states
    GREEN_GLOW = "#00FF4180"  # Glow effects (with transparency)

    # Text colors
    TEXT_PRIMARY = "#00FF41"  # Primary text (green)
    TEXT_SECONDARY = "#00CC33"  # Secondary text
    TEXT_MUTED = "#4A7A4A"  # Placeholder, hints
    TEXT_DARK = "#1A3D1A"  # Disabled text

    # Status colors
    ERROR = "#FF3333"  # Errors, weak passwords
    WARNING = "#FFA500"  # Warnings, medium strength
    SUCCESS = "#00FF00"  # Success, strong passwords
    INFO = "#00CCFF"  # Information

    # Strength indicator colors
    STRENGTH_WEAK = "#FF3333"
    STRENGTH_MEDIUM = "#FFA500"
    STRENGTH_GOOD = "#CCFF00"
    STRENGTH_STRONG = "#00FF00"

    # Special
    TRANSPARENT = "transparent"
    WHITE = "#FFFFFF"
    BLACK = "#000000"


# =============================================================================
# TYPOGRAPHY
# =============================================================================


class Fonts:
    """Font configurations for the application."""

    # Font families (with fallbacks)
    FAMILY_MONO = ("Consolas", "Monaco", "Courier New", "monospace")
    FAMILY_SANS = ("Segoe UI", "Helvetica", "Arial", "sans-serif")

    # Font sizes
    SIZE_TITLE = 28
    SIZE_HEADING = 20
    SIZE_SUBHEADING = 16
    SIZE_BODY = 14
    SIZE_SMALL = 12
    SIZE_TINY = 10

    # Pre-configured font tuples for CustomTkinter
    @staticmethod
    def title():
        return (Fonts.FAMILY_MONO[0], Fonts.SIZE_TITLE, "bold")

    @staticmethod
    def heading():
        return (Fonts.FAMILY_MONO[0], Fonts.SIZE_HEADING, "bold")

    @staticmethod
    def subheading():
        return (Fonts.FAMILY_MONO[0], Fonts.SIZE_SUBHEADING, "bold")

    @staticmethod
    def body():
        return (Fonts.FAMILY_MONO[0], Fonts.SIZE_BODY, "normal")

    @staticmethod
    def small():
        return (Fonts.FAMILY_MONO[0], Fonts.SIZE_SMALL, "normal")

    @staticmethod
    def button():
        return (Fonts.FAMILY_MONO[0], Fonts.SIZE_BODY, "bold")


# =============================================================================
# DIMENSIONS
# =============================================================================


class Dimensions:
    """Size and spacing constants."""

    # Window sizes
    LOGIN_WIDTH = 500
    LOGIN_HEIGHT = 500

    MAIN_MIN_WIDTH = 960
    MAIN_MIN_HEIGHT = 480
    MAIN_DEFAULT_WIDTH = 1100
    MAIN_DEFAULT_HEIGHT = 650

    DIALOG_WIDTH = 450
    DIALOG_HEIGHT = 400

    # Sidebar
    SIDEBAR_EXPANDED_WIDTH = 200
    SIDEBAR_COLLAPSED_WIDTH = 60

    # Padding and margins
    PAD_NONE = 0
    PAD_TINY = 4
    PAD_SMALL = 8
    PAD_MEDIUM = 16
    PAD_LARGE = 24
    PAD_XLARGE = 32

    # Border radius
    RADIUS_SMALL = 4
    RADIUS_MEDIUM = 8
    RADIUS_LARGE = 12

    # Border width
    BORDER_THIN = 1
    BORDER_MEDIUM = 2
    BORDER_THICK = 3


# =============================================================================
# COMPONENT STYLES
# =============================================================================


class Styles:
    """Pre-configured styles for CustomTkinter widgets."""

    # Button styles
    BUTTON_PRIMARY = {
        "fg_color": Colors.GREEN_SECONDARY,
        "hover_color": Colors.GREEN_DARK,
        "text_color": Colors.BG_PRIMARY,
        "text_color_disabled": Colors.TEXT_DARK,
        "border_width": 0,
        "corner_radius": Dimensions.RADIUS_MEDIUM,
        "font": Fonts.button(),
    }

    BUTTON_SECONDARY = {
        "fg_color": Colors.BG_TERTIARY,
        "hover_color": Colors.GREEN_DARK,
        "text_color": Colors.GREEN_PRIMARY,
        "text_color_disabled": Colors.TEXT_DARK,
        "border_width": 1,
        "border_color": Colors.GREEN_MUTED,
        "corner_radius": Dimensions.RADIUS_MEDIUM,
        "font": Fonts.button(),
    }

    BUTTON_DANGER = {
        "fg_color": Colors.ERROR,
        "hover_color": "#CC0000",
        "text_color": Colors.WHITE,
        "border_width": 0,
        "corner_radius": Dimensions.RADIUS_MEDIUM,
        "font": Fonts.button(),
    }

    BUTTON_ICON = {
        "fg_color": Colors.TRANSPARENT,
        "hover_color": Colors.BG_TERTIARY,
        "text_color": Colors.GREEN_PRIMARY,
        "border_width": 0,
        "corner_radius": Dimensions.RADIUS_SMALL,
        "width": 40,
        "height": 40,
    }

    # Entry styles
    ENTRY = {
        "fg_color": Colors.BG_TERTIARY,
        "text_color": Colors.GREEN_PRIMARY,
        "placeholder_text_color": Colors.TEXT_MUTED,
        "border_width": 1,
        "border_color": Colors.GREEN_MUTED,
        "corner_radius": Dimensions.RADIUS_MEDIUM,
        "font": Fonts.body(),
    }

    # Frame styles
    FRAME_CARD = {
        "fg_color": Colors.BG_SECONDARY,
        "border_width": 1,
        "border_color": Colors.GREEN_MUTED,
        "corner_radius": Dimensions.RADIUS_LARGE,
    }

    FRAME_TRANSPARENT = {
        "fg_color": Colors.TRANSPARENT,
        "border_width": 0,
    }

    # Label styles
    LABEL_TITLE = {
        "text_color": Colors.GREEN_PRIMARY,
        "font": Fonts.title(),
    }

    LABEL_HEADING = {
        "text_color": Colors.GREEN_PRIMARY,
        "font": Fonts.heading(),
    }

    LABEL_BODY = {
        "text_color": Colors.GREEN_PRIMARY,
        "font": Fonts.body(),
    }

    LABEL_MUTED = {
        "text_color": Colors.TEXT_MUTED,
        "font": Fonts.small(),
    }


# =============================================================================
# ANIMATION SETTINGS
# =============================================================================


class Animation:
    """Animation timing constants."""

    TYPEWRITER_SPEED = 100  # milliseconds per character
    TYPEWRITER_PAUSE = 500  # pause between phrases
    FADE_DURATION = 200  # fade in/out duration
    SIDEBAR_TOGGLE = 150  # sidebar expand/collapse


# =============================================================================
# PLACEHOLDER DATA
# =============================================================================

PLACEHOLDER_PASSWORDS = [
    {
        "id": 1,
        "service": "Google",
        "email": "user@gmail.com",
        "username": "user123",
        "password": "G00gl3P@ss!",
        "created_at": "2025-01-15",
        "modified_at": "2025-01-20",
    },
    {
        "id": 2,
        "service": "GitHub",
        "email": "dev@company.com",
        "username": "developer",
        "password": "GitHubS3cur3#",
        "created_at": "2025-01-10",
        "modified_at": "2025-01-10",
    },
    {
        "id": 3,
        "service": "Netflix",
        "email": "user@gmail.com",
        "username": "moviefan",
        "password": "N3tfl!xFun$",
        "created_at": "2025-01-05",
        "modified_at": "2025-01-18",
    },
    {
        "id": 4,
        "service": "Amazon",
        "email": "shop@email.com",
        "username": "shopper",
        "password": "Amaz0nPr!me",
        "created_at": "2025-01-01",
        "modified_at": "2025-01-01",
    },
    {
        "id": 5,
        "service": "Twitter/X",
        "email": "social@email.com",
        "username": "tweeter",
        "password": "Tw33t3r@X!",
        "created_at": "2024-12-20",
        "modified_at": "2025-01-22",
    },
]

# Placeholder settings
PLACEHOLDER_SETTINGS = {
    "auto_lock_minutes": 5,
    "clipboard_clear_seconds": 30,
    "default_password_length": 16,
    "theme": "dark",
}

# Is this a new user? (for demo purposes)
IS_NEW_USER = False

# Demo master password (for placeholder)
DEMO_MASTER_PASSWORD = "demo1234"
