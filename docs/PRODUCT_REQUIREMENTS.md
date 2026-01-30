# LockGuardium Lite - Product Requirements Document (PRD)

**Document Version:** 1.0  
**Created:** January 2026  
**Product:** LockGuardium Lite GUI  
**Framework:** CustomTkinter (Python)  
**Status:** Implementation Ready

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Design System](#2-design-system)
3. [Window Architecture](#3-window-architecture)
4. [User Stories](#4-user-stories)
5. [Technical Requirements](#5-technical-requirements)
6. [UI Wireframes](#6-ui-wireframes)
7. [Acceptance Criteria](#7-acceptance-criteria)
8. [Implementation Notes](#8-implementation-notes)

---

## 1. Executive Summary

### 1.1 Product Vision

LockGuardium Lite is a secure, offline-first password vault application designed to provide users with a visually compelling, security-focused experience. The GUI emphasizes trust and security through a dark "Matrix-style" aesthetic with green accents.

### 1.2 Key Requirements

| Requirement | Specification |
|-------------|---------------|
| **Framework** | CustomTkinter (Python) |
| **Theme** | Black background, green text/accents |
| **Minimum Window Size** | 960x480 pixels |
| **Responsive** | Yes, resizable with proper scaling |
| **Login Animation** | Typewriter effect (100ms/character) |
| **Auto-lock Timer** | 1, 2, 5, 10, 15 minutes |

### 1.3 Target Users

- Privacy-conscious individuals who prefer local password storage
- Users who value security aesthetics and visual trust indicators
- Power users managing multiple credentials

---

## 2. Design System

### 2.1 Color Palette

| Element | Color Code | CSS Variable | Usage |
|---------|------------|--------------|-------|
| **Background Primary** | `#0D0D0D` | `--bg-primary` | Main window background |
| **Background Secondary** | `#1A1A1A` | `--bg-secondary` | Cards, sidebar, frames |
| **Background Tertiary** | `#252525` | `--bg-tertiary` | Input fields, hover states |
| **Primary Green** | `#00FF41` | `--green-primary` | Main text, active elements |
| **Secondary Green** | `#00CC33` | `--green-secondary` | Buttons, highlights |
| **Muted Green** | `#2D5A27` | `--green-muted` | Borders, disabled states |
| **Dark Green** | `#0A3D0A` | `--green-dark` | Button hover states |
| **Text Muted** | `#4A7A4A` | `--text-muted` | Placeholder text, hints |
| **Error Red** | `#FF3333` | `--error` | Warnings, weak passwords |
| **Warning Orange** | `#FFA500` | `--warning` | Medium strength |
| **Success Green** | `#00FF00` | `--success` | Strong passwords, success states |

### 2.2 Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| **Logo/Title** | Consolas/Monaco | 28px | Bold |
| **Headings** | Consolas/Monaco | 18-20px | Bold |
| **Body Text** | Consolas/Monaco | 14px | Normal |
| **Labels** | Consolas/Monaco | 12px | Normal |
| **Buttons** | Consolas/Monaco | 14px | Bold |

### 2.3 Component Styling

```
Buttons:
  - Background: #00CC33 (hover: #0A3D0A)
  - Text: #0D0D0D (hover: #00FF41)
  - Border Radius: 6px
  - Padding: 10px 20px

Input Fields:
  - Background: #252525
  - Border: 1px solid #2D5A27
  - Text: #00FF41
  - Placeholder: #4A7A4A
  - Focus Border: #00CC33

Cards/Frames:
  - Background: #1A1A1A
  - Border: 1px solid #2D5A27
  - Border Radius: 8px
  - Padding: 16px
```

---

## 3. Window Architecture

### 3.1 Login Window

**Purpose:** Authenticate users and provide secure vault access

**Dimensions:** 500x450 pixels (fixed, centered on screen)

**Components:**
1. **Animated Greeting Area**
   - Typewriter effect displays "LockGuardium" first
   - Then types "Welcome back!" (returning user) or "Create your vault" (new user)
   - Animation speed: 100ms per character
   - Positioned above center (upper 40% of window)

2. **Password Entry Section**
   - Single password field for returning users
   - Password + Confirm password for new users
   - Show/hide toggle button (eye icon) adjacent to each field
   - Minimum 8 characters for master password

3. **Action Button**
   - "Unlock Vault" for returning users
   - "Create Vault" for new users

4. **App Information Footer**
   - Version number
   - "Secure. Local. Private." tagline
   - MIT License indicator

5. **Security Indicators**
   - Lock icon in greeting area
   - Subtle encryption badge/indicator

### 3.2 Main Vault Window

**Purpose:** Primary application interface for password management

**Dimensions:** 
- Minimum: 960x480 pixels
- Default: 1100x600 pixels
- Resizable: Yes

**Layout Structure:**
```
┌──────────────────────────────────────────────────────────────┐
│                        Title Bar                              │
├────────────┬─────────────────────────────────────────────────┤
│            │                                                  │
│  Sidebar   │              Content Area                        │
│  (Toggle)  │              (Pages)                             │
│            │                                                  │
│            │                                                  │
└────────────┴─────────────────────────────────────────────────┘
```

### 3.3 Sidebar Component

**Behavior:** Collapsible (show/hide with toggle button)

**Elements (top to bottom):**
1. Toggle button (hamburger menu icon)
2. App logo/name (when expanded)
3. Navigation buttons:
   - Dashboard (📊)
   - Vault (🔒)
   - Generator (⚡)
   - Settings (⚙️)
4. Theme selector dropdown (System/Dark/Light)
5. Lock/Logout button at bottom

**States:**
- Expanded: ~200px width, shows icons + text
- Collapsed: ~60px width, shows icons only

### 3.4 Page Components

#### Dashboard Page
- Total passwords count card
- Last added password card (service name + date)
- Last modified password card (service name + date)
- Quick action buttons

#### Vault Page
- Search bar at top
- Password table with columns: Service, Email, Username, Password
- Action buttons: Add, Edit, Delete
- Per-row: Copy button, Reveal password button

#### Generator Page (Split View)
- **Left Panel: Password Generator**
  - Length slider (min 12, max 64)
  - Character type toggles (checkboxes)
  - Generated password display
  - Generate, Copy, Save to Vault buttons
  
- **Right Panel: Strength Checker**
  - Password input field
  - Strength progress bar (colored by level)
  - Strength label (Weak/Medium/Good/Strong)
  - Improvement tips

#### Settings Page
- Auto-close timer dropdown (1, 2, 5, 10, 15 minutes)
- Clipboard clear timer dropdown (10, 30, 60, 120 seconds)
- Default password length setting
- Theme appearance dropdown
- Export vault button
- Import vault button
- About section

---

## 4. User Stories

### 4.1 Login Window User Stories

| ID | Priority | User Story | Acceptance Criteria |
|----|----------|------------|---------------------|
| LW-01 | P0 | As a new user, I want to see an animated greeting that types "LockGuardium" then "Create your vault" so I feel the app is modern and welcoming | Typewriter effect at 100ms/char, pause between phrases |
| LW-02 | P0 | As a new user, I want to create a master password with confirmation so my vault is securely initialized | Two password fields shown, must match, min 8 chars |
| LW-03 | P0 | As a returning user, I want to see "Welcome back!" in the greeting so I know I'm recognized | Different text for returning vs new users |
| LW-04 | P0 | As a returning user, I want to enter my master password to unlock my vault | Single password field, unlock button |
| LW-05 | P1 | As a user, I want to toggle password visibility so I can verify what I typed | Eye icon button toggles show/hide for each field |
| LW-06 | P2 | As a user, I want to see app information at the bottom so I know the version and can trust the app | Footer shows "v1.0", "MIT License", tagline |
| LW-07 | P2 | As a user, I want the dark green theme to make me feel secure | Black background, green accents, lock icons |

### 4.2 Dashboard User Stories

| ID | Priority | User Story | Acceptance Criteria |
|----|----------|------------|---------------------|
| DB-01 | P0 | As a user, I want to see the total count of my saved passwords so I know how many credentials I have | Card displays count with icon |
| DB-02 | P0 | As a user, I want to see which password was last added so I can verify recent additions | Card shows service name and date |
| DB-03 | P0 | As a user, I want to see which password was last modified so I know what was recently updated | Card shows service name and date |
| DB-04 | P1 | As a user, I want to click on cards to navigate to the vault so I have quick access | Cards are clickable, navigate to vault page |

### 4.3 Vault Page User Stories

| ID | Priority | User Story | Acceptance Criteria |
|----|----------|------------|---------------------|
| VP-01 | P0 | As a user, I want to view all my passwords in a table so I can find credentials easily | Table with Service, Email, Username, Password columns |
| VP-02 | P0 | As a user, I want passwords to be masked by default so others cannot see them over my shoulder | Passwords show as "••••••••" |
| VP-03 | P0 | As a user, I want to reveal individual passwords so I can see them when needed | Eye button per row toggles visibility |
| VP-04 | P0 | As a user, I want to add a new password so I can store new credentials | "Add" button opens dialog with fields |
| VP-05 | P0 | As a user, I want to edit an existing password so I can update changed credentials | "Edit" button opens pre-filled dialog |
| VP-06 | P0 | As a user, I want to delete a password so I can remove outdated entries | "Delete" button with confirmation dialog |
| VP-07 | P1 | As a user, I want to copy a password to clipboard so I can paste it elsewhere | Copy button per row, shows confirmation |
| VP-08 | P1 | As a user, I want to search/filter passwords so I can find specific entries quickly | Search bar filters table in real-time |

### 4.4 Password Generator User Stories

| ID | Priority | User Story | Acceptance Criteria |
|----|----------|------------|---------------------|
| PG-01 | P0 | As a user, I want to set password length with minimum 12 characters so I can control complexity | Slider from 12 to 64 |
| PG-02 | P0 | As a user, I want to toggle uppercase letters (A-Z) so I can customize character types | Checkbox, checked by default |
| PG-03 | P0 | As a user, I want to toggle lowercase letters (a-z) so I can customize character types | Checkbox, checked by default |
| PG-04 | P0 | As a user, I want to toggle digits (0-9) so I can customize character types | Checkbox, checked by default |
| PG-05 | P0 | As a user, I want to toggle special characters so I can customize character types | Checkbox, checked by default |
| PG-06 | P0 | As a user, I want to generate a password so I get a secure random string | "Generate" button creates password |
| PG-07 | P0 | As a user, I want to see the generated password in a display area so I can review it | Text field shows generated password |
| PG-08 | P1 | As a user, I want to copy the generated password so I can use it elsewhere | "Copy" button copies to clipboard |
| PG-09 | P1 | As a user, I want to save a generated password directly to my vault so I don't have to switch pages | "Save to Vault" opens add dialog with password pre-filled |

### 4.5 Strength Checker User Stories

| ID | Priority | User Story | Acceptance Criteria |
|----|----------|------------|---------------------|
| SC-01 | P0 | As a user, I want to enter any password to check its strength | Entry field accepts any input |
| SC-02 | P0 | As a user, I want to see a strength level label so I know how secure my password is | Shows: Weak, Medium, Good, or Strong |
| SC-03 | P0 | As a user, I want to see a colored progress bar so I can quickly gauge strength | Red (weak) → Orange (medium) → Yellow (good) → Green (strong) |
| SC-04 | P1 | As a user, I want real-time strength updates as I type so feedback is instant | Updates on each keystroke |
| SC-05 | P2 | As a user, I want to see improvement tips so I know how to make my password stronger | Tips like "Add special characters" |

### 4.6 Sidebar User Stories

| ID | Priority | User Story | Acceptance Criteria |
|----|----------|------------|---------------------|
| SB-01 | P0 | As a user, I want to toggle sidebar visibility so I can maximize content space | Toggle button expands/collapses sidebar |
| SB-02 | P0 | As a user, I want navigation buttons in the sidebar so I can switch between pages | Dashboard, Vault, Generator, Settings buttons |
| SB-03 | P1 | As a user, I want to see which page is currently active so I know where I am | Active button is highlighted |
| SB-04 | P1 | As a user, I want to change theme appearance from the sidebar so it's easily accessible | Dropdown with System/Dark/Light options |
| SB-05 | P2 | As a user, I want to lock/logout from the sidebar so I can secure my vault quickly | Lock button returns to login screen |

### 4.7 Settings User Stories

| ID | Priority | User Story | Acceptance Criteria |
|----|----------|------------|---------------------|
| ST-01 | P0 | As a user, I want to set an auto-close timer so my vault locks after inactivity | Dropdown: 1, 2, 5, 10, 15 minutes |
| ST-02 | P1 | As a user, I want to set clipboard clear timer so copied passwords don't persist | Dropdown: 10, 30, 60, 120 seconds |
| ST-03 | P1 | As a user, I want to set default password length so the generator uses my preference | Number input, minimum 12 |
| ST-04 | P1 | As a user, I want to export my vault so I can create backups | "Export" button saves encrypted file |
| ST-05 | P1 | As a user, I want to import a vault backup so I can restore my passwords | "Import" button loads encrypted file |
| ST-06 | P2 | As a user, I want to change theme in settings so I have a central place for preferences | Dropdown mirrors sidebar option |

---

## 5. Technical Requirements

### 5.1 File Structure

```
src/lockguardium-lite/
├── app.py                      # Main application entry point
├── ui/
│   ├── __init__.py
│   ├── theme.py                # Color palette, fonts, styling constants
│   ├── login_window.py         # Login/setup window with typewriter
│   ├── main_window.py          # Main vault window container
│   ├── components/
│   │   ├── __init__.py
│   │   ├── sidebar.py          # Collapsible sidebar navigation
│   │   ├── dashboard.py        # Dashboard page component
│   │   ├── vault_page.py       # Password list/table page
│   │   ├── generator_page.py   # Generator + strength checker
│   │   ├── settings_page.py    # Settings page
│   │   └── dialogs.py          # Add/Edit/Delete modal dialogs
```

### 5.2 Placeholder Data

```python
PLACEHOLDER_PASSWORDS = [
    {
        "id": 1,
        "service": "Google",
        "email": "user@gmail.com",
        "username": "user123",
        "password": "G00gl3P@ss!",
        "created_at": "2025-01-15",
        "modified_at": "2025-01-20"
    },
    {
        "id": 2,
        "service": "GitHub",
        "email": "dev@company.com",
        "username": "developer",
        "password": "GitHubS3cur3#",
        "created_at": "2025-01-10",
        "modified_at": "2025-01-10"
    },
    {
        "id": 3,
        "service": "Netflix",
        "email": "user@gmail.com",
        "username": "moviefan",
        "password": "N3tfl!xFun$",
        "created_at": "2025-01-05",
        "modified_at": "2025-01-18"
    },
    {
        "id": 4,
        "service": "Amazon",
        "email": "shop@email.com",
        "username": "shopper",
        "password": "Amaz0nPr!me",
        "created_at": "2025-01-01",
        "modified_at": "2025-01-01"
    },
    {
        "id": 5,
        "service": "Twitter/X",
        "email": "social@email.com",
        "username": "tweeter",
        "password": "Tw33t3r@X!",
        "created_at": "2024-12-20",
        "modified_at": "2025-01-22"
    }
]
```

### 5.3 Password Strength Algorithm

```python
def calculate_strength(password: str) -> tuple[str, float]:
    """
    Returns (level_name, progress_value)
    - progress_value: 0.0 to 1.0
    - level_name: "Weak", "Medium", "Good", "Strong"
    """
    score = 0
    
    # Length scoring
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if len(password) >= 16:
        score += 1
    
    # Character type scoring
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 1
    
    # Map score to level
    if score <= 2:
        return ("Weak", 0.25)
    elif score <= 4:
        return ("Medium", 0.5)
    elif score <= 6:
        return ("Good", 0.75)
    else:
        return ("Strong", 1.0)
```

### 5.4 Strength Colors

| Level | Progress Value | Bar Color | Text Color |
|-------|---------------|-----------|------------|
| Weak | 0.25 | `#FF3333` | `#FF3333` |
| Medium | 0.50 | `#FFA500` | `#FFA500` |
| Good | 0.75 | `#CCFF00` | `#CCFF00` |
| Strong | 1.00 | `#00FF00` | `#00FF00` |

### 5.5 Window Specifications

| Window | Size | Resizable | Position |
|--------|------|-----------|----------|
| Login | 500x450 | No | Centered |
| Main | 960x480 (min) | Yes | Centered initially |
| Dialogs | 450x350 | No | Centered on parent |

---

## 6. UI Wireframes

### 6.1 Login Window - Returning User

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                          🔒                                  ║
║                                                              ║
║                    LockGuardium_                             ║
║                    Welcome back!                             ║
║                                                              ║
║           ┌────────────────────────────────┐ ┌────┐         ║
║           │ Enter master password...       │ │ 👁 │         ║
║           └────────────────────────────────┘ └────┘         ║
║                                                              ║
║                  ┌─────────────────────┐                     ║
║                  │   🔓 Unlock Vault   │                     ║
║                  └─────────────────────┘                     ║
║                                                              ║
║  ────────────────────────────────────────────────────────    ║
║           LockGuardium Lite v1.0 | MIT License               ║
║              Secure. Local. Private.                         ║
╚══════════════════════════════════════════════════════════════╝
```

### 6.2 Login Window - New User

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                          🔒                                  ║
║                                                              ║
║                    LockGuardium_                             ║
║                  Create your vault                           ║
║                                                              ║
║           ┌────────────────────────────────┐ ┌────┐         ║
║           │ Create master password...      │ │ 👁 │         ║
║           └────────────────────────────────┘ └────┘         ║
║                                                              ║
║           ┌────────────────────────────────┐ ┌────┐         ║
║           │ Confirm master password...     │ │ 👁 │         ║
║           └────────────────────────────────┘ └────┘         ║
║                                                              ║
║                  ┌─────────────────────┐                     ║
║                  │   🔐 Create Vault   │                     ║
║                  └─────────────────────┘                     ║
║                                                              ║
║  ────────────────────────────────────────────────────────    ║
║           LockGuardium Lite v1.0 | MIT License               ║
║              Secure. Local. Private.                         ║
╚══════════════════════════════════════════════════════════════╝
```

### 6.3 Main Window - Dashboard

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  LockGuardium Lite                                                      _ □ X ║
╠═════════════╤═════════════════════════════════════════════════════════════════╣
║             │                                                                  ║
║  ☰  Menu    │                      📊 DASHBOARD                               ║
║             │                                                                  ║
║  ─────────  │   ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐║
║             │   │                  │ │                  │ │                  │║
║  📊 Dashboard│   │   🔐 TOTAL       │ │   ➕ LAST ADDED  │ │   ✏️ LAST MODIFIED│║
║  (active)   │   │                  │ │                  │ │                  │║
║             │   │       5          │ │   Twitter/X      │ │   Twitter/X      │║
║  🔒 Vault    │   │   Passwords      │ │   Jan 22, 2025   │ │   Jan 22, 2025   │║
║             │   │                  │ │                  │ │                  │║
║  ⚡ Generator│   └──────────────────┘ └──────────────────┘ └──────────────────┘║
║             │                                                                  ║
║  ⚙️ Settings │                                                                  ║
║             │                                                                  ║
║  ─────────  │                                                                  ║
║             │                                                                  ║
║  🎨 Theme   │                                                                  ║
║  [Dark   ▾] │                                                                  ║
║             │                                                                  ║
║  🔒 Lock    │                                                                  ║
╚═════════════╧═════════════════════════════════════════════════════════════════╝
```

### 6.4 Main Window - Vault Page

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  LockGuardium Lite                                                      _ □ X ║
╠═════════════╤═════════════════════════════════════════════════════════════════╣
║             │  🔍 [Search passwords...                    ]                   ║
║  ☰  Menu    │                                                                  ║
║             │  ┌─────────────────────────────────────────────────────────────┐║
║  ─────────  │  │ Service      │ Email              │ Username   │ Password   │║
║             │  ├──────────────┼────────────────────┼────────────┼────────────┤║
║  📊 Dashboard│  │ Google       │ user@gmail.com     │ user123    │ ••••• 👁 📋│║
║             │  │ GitHub       │ dev@company.com    │ developer  │ ••••• 👁 📋│║
║  🔒 Vault    │  │ Netflix      │ user@gmail.com     │ moviefan   │ ••••• 👁 📋│║
║  (active)   │  │ Amazon       │ shop@email.com     │ shopper    │ ••••• 👁 📋│║
║             │  │ Twitter/X    │ social@email.com   │ tweeter    │ ••••• 👁 📋│║
║  ⚡ Generator│  └─────────────────────────────────────────────────────────────┘║
║             │                                                                  ║
║  ⚙️ Settings │          ┌────────┐  ┌────────┐  ┌────────┐                     ║
║             │          │ + Add  │  │ ✏️ Edit │  │ 🗑️ Delete│                     ║
║  ─────────  │          └────────┘  └────────┘  └────────┘                     ║
║             │                                                                  ║
║  🎨 [Dark ▾]│                                                                  ║
║  🔒 Lock    │                                                                  ║
╚═════════════╧═════════════════════════════════════════════════════════════════╝
```

### 6.5 Main Window - Generator Page

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  LockGuardium Lite                                                      _ □ X ║
╠═════════════╤═════════════════════════════════════════════════════════════════╣
║             │                                                                  ║
║  ☰  Menu    │   ┌─────────────────────────────┐  ┌─────────────────────────┐  ║
║             │   │    ⚡ PASSWORD GENERATOR    │  │   🔍 STRENGTH CHECKER   │  ║
║  ─────────  │   │                             │  │                         │  ║
║             │   │  Length: 16                 │  │  Password:              │  ║
║  📊 Dashboard│   │  ════════════●══════  [16]  │  │  [____________________] │  ║
║             │   │                             │  │                         │  ║
║  🔒 Vault    │   │  [✓] Uppercase (A-Z)       │  │  Strength:              │  ║
║             │   │  [✓] Lowercase (a-z)       │  │  ████████████░░░ GOOD   │  ║
║  ⚡ Generator│   │  [✓] Digits (0-9)          │  │                         │  ║
║  (active)   │   │  [✓] Special (!@#$%^&*)    │  │  Tips:                  │  ║
║             │   │                             │  │  • Add more length      │  ║
║  ⚙️ Settings │   │  ┌───────────────────────┐ │  │  • Mix character types  │  ║
║             │   │  │  xK9#mL2$pQ7@nR4!bZ  │ │  │                         │  ║
║  ─────────  │   │  └───────────────────────┘ │  └─────────────────────────┘  ║
║             │   │                             │                               ║
║  🎨 [Dark ▾]│   │  [Generate] [Copy] [Save]  │                               ║
║  🔒 Lock    │   └─────────────────────────────┘                               ║
╚═════════════╧═════════════════════════════════════════════════════════════════╝
```

### 6.6 Main Window - Settings Page

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  LockGuardium Lite                                                      _ □ X ║
╠═════════════╤═════════════════════════════════════════════════════════════════╣
║             │                                                                  ║
║  ☰  Menu    │                       ⚙️ SETTINGS                                ║
║             │                                                                  ║
║  ─────────  │   ┌─────────────────────────────────────────────────────────┐   ║
║             │   │  🔒 Security                                            │   ║
║  📊 Dashboard│   │                                                         │   ║
║             │   │  Auto-lock timer:           [5 minutes          ▾]     │   ║
║  🔒 Vault    │   │  Clear clipboard after:    [30 seconds         ▾]     │   ║
║             │   │                                                         │   ║
║  ⚡ Generator│   └─────────────────────────────────────────────────────────┘   ║
║             │                                                                  ║
║  ⚙️ Settings │   ┌─────────────────────────────────────────────────────────┐   ║
║  (active)   │   │  ⚡ Generator                                           │   ║
║             │   │                                                         │   ║
║  ─────────  │   │  Default password length:   [16                 ]      │   ║
║             │   │                                                         │   ║
║  🎨 [Dark ▾]│   └─────────────────────────────────────────────────────────┘   ║
║             │                                                                  ║
║  🔒 Lock    │   ┌─────────────────────────────────────────────────────────┐   ║
║             │   │  💾 Data                                                │   ║
║             │   │                                                         │   ║
║             │   │  [  📤 Export Vault  ]     [  📥 Import Vault  ]       │   ║
║             │   │                                                         │   ║
║             │   └─────────────────────────────────────────────────────────┘   ║
╚═════════════╧═════════════════════════════════════════════════════════════════╝
```

### 6.7 Add/Edit Password Dialog

```
╔══════════════════════════════════════════════════════════════╗
║  ➕ Add New Password                                    ✕    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   Service/Website:                                           ║
║   ┌────────────────────────────────────────────────────┐    ║
║   │                                                    │    ║
║   └────────────────────────────────────────────────────┘    ║
║                                                              ║
║   Email:                                                     ║
║   ┌────────────────────────────────────────────────────┐    ║
║   │                                                    │    ║
║   └────────────────────────────────────────────────────┘    ║
║                                                              ║
║   Username:                                                  ║
║   ┌────────────────────────────────────────────────────┐    ║
║   │                                                    │    ║
║   └────────────────────────────────────────────────────┘    ║
║                                                              ║
║   Password:                                                  ║
║   ┌────────────────────────────────────────────┐ ┌────┐    ║
║   │                                            │ │ 👁 │    ║
║   └────────────────────────────────────────────┘ └────┘    ║
║                                                              ║
║            ┌──────────────┐    ┌──────────────┐             ║
║            │    Cancel    │    │     Save     │             ║
║            └──────────────┘    └──────────────┘             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 7. Acceptance Criteria

### 7.1 Login Window

- [ ] Typewriter animation completes within 3 seconds
- [ ] Animation types "LockGuardium" then pauses, then types second line
- [ ] Password field accepts input and masks characters
- [ ] Eye button toggles password visibility
- [ ] Login button validates password (placeholder: any 8+ chars)
- [ ] Error message shown for invalid password
- [ ] Footer displays version and license info
- [ ] Window is centered on screen
- [ ] Cannot be resized

### 7.2 Main Window

- [ ] Opens after successful login
- [ ] Minimum size is 960x480
- [ ] Responsive - elements resize properly
- [ ] Sidebar can be toggled (show/hide)
- [ ] All navigation buttons work
- [ ] Active page is highlighted in sidebar
- [ ] Theme dropdown changes appearance
- [ ] Lock button returns to login screen

### 7.3 Dashboard

- [ ] Shows total password count
- [ ] Shows last added password with date
- [ ] Shows last modified password with date
- [ ] Uses placeholder data initially

### 7.4 Vault Page

- [ ] Displays all passwords in table format
- [ ] Passwords are masked by default
- [ ] Individual reveal buttons work per row
- [ ] Copy button copies password to clipboard
- [ ] Add button opens add dialog
- [ ] Edit button opens edit dialog with data
- [ ] Delete button shows confirmation
- [ ] Search filters table in real-time

### 7.5 Generator Page

- [ ] Length slider has minimum of 12
- [ ] All character type checkboxes work
- [ ] Generate button creates password
- [ ] Generated password is displayed
- [ ] Copy button works
- [ ] Save to Vault opens add dialog with password

### 7.6 Strength Checker

- [ ] Accepts password input
- [ ] Updates strength in real-time
- [ ] Progress bar color matches strength level
- [ ] Shows correct label (Weak/Medium/Good/Strong)

### 7.7 Settings

- [ ] Auto-lock dropdown works (1, 2, 5, 10, 15 min)
- [ ] Clipboard clear dropdown works (10, 30, 60, 120 sec)
- [ ] Default length input accepts numbers >= 12
- [ ] Export button shows file dialog (placeholder)
- [ ] Import button shows file dialog (placeholder)

---

## 8. Implementation Notes

### 8.1 Dependencies

```toml
# pyproject.toml
dependencies = [
    "cryptography>=46.0.3",
    "customtkinter>=5.2.2",
]
```

### 8.2 CustomTkinter Configuration

```python
# Set appearance before creating any widgets
customtkinter.set_appearance_mode("dark")  # Default to dark
customtkinter.set_default_color_theme("green")  # Use green theme

# Custom colors will override theme defaults
```

### 8.3 Typewriter Animation Implementation

```python
def typewriter_effect(label, text, index=0, callback=None):
    """
    Animate text appearing character by character.
    
    Args:
        label: CTkLabel to update
        text: Full text to display
        index: Current character index
        callback: Function to call when complete
    """
    if index <= len(text):
        label.configure(text=text[:index] + "_")
        label.after(100, lambda: typewriter_effect(label, text, index + 1, callback))
    else:
        label.configure(text=text)
        if callback:
            callback()
```

### 8.4 Placeholder Data Management

All placeholder data should be defined in a central location and easily replaceable when integrating with the actual backend services.

```python
# ui/placeholder_data.py
PLACEHOLDER_PASSWORDS = [...]
IS_NEW_USER = False  # Toggle to test both flows
MASTER_PASSWORD = "placeholder"  # For demo purposes
```

### 8.5 Future Integration Points

The UI is designed to be integrated with the existing backend:

- `core/crypto.py` - For encryption/decryption
- `core/storage.py` - For database operations
- `services/auth_service.py` - For authentication
- `services/vault_service.py` - For CRUD operations

The UI components use placeholder data and callbacks that can be easily replaced with actual service calls.

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Jan 2026 | Product Team | Initial PRD creation |

---

*This document serves as the complete specification for the LockGuardium Lite GUI implementation.*
