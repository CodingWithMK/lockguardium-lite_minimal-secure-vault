"""
LockGuardium Lite - Vault Window
Deprecated: This module has been replaced by main_window.py and vault_page.py
Kept for backward compatibility.
"""

# This file is deprecated. Use main_window.py instead.
# The vault functionality is now in ui/components/vault_page.py

from ui.main_window import MainWindow
from ui.components.vault_page import VaultPage

__all__ = ["MainWindow", "VaultPage"]
