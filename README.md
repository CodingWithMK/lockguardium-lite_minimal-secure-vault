# LockGuardium Lite

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-green?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)

**A minimal, secure, offline-first password vault application**

*Secure. Local. Private.*

</div>

---

## Overview

LockGuardium Lite is a desktop password manager built with Python that prioritizes security and privacy. Unlike cloud-based password managers, LockGuardium Lite stores all your credentials locally on your device, encrypted with industry-standard cryptographic algorithms.

### Key Features

- **AES-128 Encryption** - Your passwords are encrypted using Fernet (AES-128-CBC with HMAC-SHA256)
- **Strong Key Derivation** - Master password protection with PBKDF2-HMAC-SHA256 (200,000 iterations)
- **Offline-First** - No cloud sync, no accounts, complete data ownership
- **Modern GUI** - Clean, dark-themed interface built with CustomTkinter
- **Password Generator** - Create strong passwords with customizable options
- **Strength Checker** - Real-time password strength analysis
- **Cross-Platform** - Works on Windows, macOS, and Linux

---

## Screenshots

The application features a sleek, security-focused design with a black and green color scheme:

- **Login Window** - Animated typewriter greeting with master password entry
- **Dashboard** - Overview of stored passwords with quick stats
- **Vault** - Searchable password table with add/edit/delete functionality
- **Generator** - Password generation with strength checking

---

## Security Architecture

LockGuardium Lite implements a multi-layer security approach:

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY FLOW                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Master Password ──► PBKDF2-HMAC-SHA256 ──► Derived Key    │
│        │                    │                    │          │
│        │              200,000 iterations         │          │
│        │                    │                    │          │
│        ▼                    ▼                    ▼          │
│   [User Input]     [16-byte Salt]        [Fernet Cipher]   │
│                     (CSPRNG)              AES-128-CBC       │
│                         │                      │            │
│                         ▼                      ▼            │
│                    [salt.bin]          [Encrypted Vault]    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Cryptographic Specifications

| Component | Implementation | Standard |
|-----------|----------------|----------|
| **Salt** | 16 bytes from `os.urandom()` | CSPRNG |
| **Key Derivation** | PBKDF2-HMAC-SHA256 | NIST SP 800-132 |
| **Iterations** | 200,000 | OWASP 2023 Recommended |
| **Encryption** | Fernet (AES-128-CBC + HMAC) | Authenticated Encryption |
| **Integrity** | HMAC-SHA256 | Tamper-evident |

---

## Development Status

LockGuardium Lite is currently in **active development**. Below is the current implementation status:

### Completed Features

| Component | Status | Description |
|-----------|--------|-------------|
| **Core Cryptography** | ✅ Complete | Encryption, decryption, key derivation |
| **Password Generator** | ✅ Complete | Configurable length and character types |
| **Login Window** | ✅ Complete | Typewriter animation, master password entry |
| **Main Window** | ✅ Complete | Sidebar navigation, page management |
| **Dashboard** | ✅ Complete | Stats cards, recent activity |
| **Vault Page** | ✅ Complete | Password table, search, CRUD operations |
| **Generator Page** | ✅ Complete | Generator + strength checker side-by-side |
| **Settings Page** | ✅ Complete | Auto-lock, clipboard, theme settings |
| **Dialogs** | ✅ Complete | Add/Edit/Delete modal dialogs |

### In Progress

| Component | Status | Description |
|-----------|--------|-------------|
| **Backend Integration** | 🔄 In Progress | Connect GUI to crypto/storage services |
| **SQLite Storage** | 🔄 In Progress | Persistent encrypted database |
| **Auth Service** | 🔄 In Progress | Master password verification |
| **Vault Service** | 🔄 In Progress | CRUD operations with encryption |

### Planned Features

| Feature | Priority | Description |
|---------|----------|-------------|
| Export/Import | High | Encrypted vault backup and restore |
| Browser Extension | Medium | Auto-fill passwords in browsers |
| Password History | Medium | Track password changes over time |
| Categories/Tags | Low | Organize passwords by category |
| Two-Factor Auth | Low | Additional master password security |

### Overall Progress

```
Frontend (GUI):     ████████████████████ 100%
Backend (Core):     ████████░░░░░░░░░░░░  40%
Integration:        ████░░░░░░░░░░░░░░░░  20%
Testing:            ██░░░░░░░░░░░░░░░░░░  10%
─────────────────────────────────────────────
Total:              ████████░░░░░░░░░░░░  42%
```

---

## Installation

### Prerequisites

- Python 3.10 or higher
- pip or uv package manager

### Option 1: Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/CodingWithMK/lockguardium-lite.git
cd lockguardium-lite

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Run the application
uv run python main.py
```

### Option 2: Using pip

```bash
# Clone the repository
git clone https://github.com/CodingWithMK/lockguardium-lite.git
cd lockguardium-lite

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# Or install from pyproject.toml:
pip install cryptography>=46.0.3 customtkinter>=5.2.2

# Run the application
python main.py
```

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `cryptography` | >=46.0.3 | Encryption and key derivation |
| `customtkinter` | >=5.2.2 | Modern GUI framework |

---

## Usage

### Starting the Application

```bash
python main.py
```

### First-Time Setup

1. Launch the application
2. You'll see the animated login screen with "Create your vault" message
3. Enter a master password (minimum 8 characters)
4. Confirm your master password
5. Click "Create Vault" to initialize your password vault

### Returning User

1. Launch the application
2. You'll see "Welcome back!" greeting
3. Enter your master password
4. Click "Unlock Vault" to access your passwords

### Main Features

#### Dashboard
- View total password count
- See recently added passwords
- See recently modified passwords
- Quick action buttons for common tasks

#### Password Vault
- Browse all saved passwords in a table view
- Search/filter passwords by service, email, or username
- Click the 👁 button to reveal individual passwords
- Click the 📋 button to copy passwords to clipboard
- Use Add/Edit/Delete buttons to manage entries

#### Password Generator
- Set password length (12-64 characters)
- Toggle character types:
  - Uppercase letters (A-Z)
  - Lowercase letters (a-z)
  - Digits (0-9)
  - Special characters (!@#$%^&*)
- Generate, copy, or save directly to vault

#### Strength Checker
- Enter any password to check its strength
- Real-time strength indicator (Weak/Medium/Good/Strong)
- Color-coded progress bar
- Tips for improving password strength

#### Settings
- **Auto-lock timer**: 1, 2, 5, 10, or 15 minutes
- **Clipboard clear**: 10, 30, 60, or 120 seconds
- **Default password length**: Set generator default
- **Theme**: Dark, Light, or System
- **Export/Import**: Backup and restore vault (coming soon)

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Submit password / Confirm action |
| `Escape` | Cancel dialog / Close |

---

## Project Structure

```
lockguardium-lite/
├── main.py                      # Application entry point
├── pyproject.toml               # Project configuration
├── LICENSE                      # MIT License
├── README.md                    # This file
├── PRODUCT_REQUIREMENTS.md      # Detailed PRD
├── CODEBASE_ANALYSIS.md         # Technical documentation
│
├── src/lockguardium-lite/
│   ├── app.py                   # Main application controller
│   │
│   ├── core/                    # Core functionality
│   │   ├── crypto.py            # Encryption/decryption
│   │   ├── generator.py         # Password generation
│   │   ├── storage.py           # Data persistence
│   │   ├── models.py            # Data models
│   │   └── utils.py             # Utility functions
│   │
│   ├── services/                # Business logic
│   │   ├── auth_service.py      # Authentication
│   │   └── vault_service.py     # Vault operations
│   │
│   └── ui/                      # User interface
│       ├── theme.py             # Colors, fonts, styles
│       ├── login_window.py      # Login screen
│       ├── main_window.py       # Main vault window
│       └── components/
│           ├── sidebar.py       # Navigation sidebar
│           ├── dashboard.py     # Dashboard page
│           ├── vault_page.py    # Password list
│           ├── generator_page.py # Generator + checker
│           ├── settings_page.py # Settings
│           └── dialogs.py       # Modal dialogs
│
└── tests/                       # Test files
    ├── test.py                  # CLI prototype
    ├── test_crypto.py           # Crypto tests
    └── test_generator.py        # Generator tests
```

---

## Technical Documentation

For detailed technical documentation, see:

- **[CODEBASE_ANALYSIS.md](CODEBASE_ANALYSIS.md)** - Comprehensive analysis from architect, developer, and product manager perspectives
- **[PRODUCT_REQUIREMENTS.md](PRODUCT_REQUIREMENTS.md)** - Detailed user stories and acceptance criteria

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
# Clone and setup
git clone https://github.com/CodingWithMK/lockguardium-lite.git
cd lockguardium-lite
uv sync

# Run the app
uv run python main.py

# Run individual components for testing
uv run python src/lockguardium-lite/ui/login_window.py
uv run python src/lockguardium-lite/ui/main_window.py
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Document functions with docstrings

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Muhammed Musab Kaya

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## Acknowledgments

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern and customizable Python UI library
- [cryptography](https://cryptography.io/) - Cryptographic recipes and primitives for Python
- [Python](https://python.org) - The programming language that powers this application

---

<div align="center">

**LockGuardium Lite** - *Your passwords, your device, your control.*

Made with security in mind

</div>
