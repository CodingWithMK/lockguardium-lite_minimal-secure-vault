"""
LockGuardium Lite - Dialogs
Re-exports dialog components from ui/components/dialogs.py
"""

# Re-export dialogs from components
from ui.components.dialogs import (
    BaseDialog,
    AddPasswordDialog,
    EditPasswordDialog,
    DeleteConfirmDialog,
    MessageDialog,
)

__all__ = [
    "BaseDialog",
    "AddPasswordDialog",
    "EditPasswordDialog",
    "DeleteConfirmDialog",
    "MessageDialog",
]
