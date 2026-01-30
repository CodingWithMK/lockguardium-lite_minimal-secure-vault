"""
LockGuardium Lite - Main Entry Point
A minimal, secure password vault application
"""

import sys
import os

# Add the src directory to path
sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "src", "lockguardium-lite"
    ),
)

from app import main


if __name__ == "__main__":
    main()
