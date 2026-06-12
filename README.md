<div align="center">

```
   ██╗     ██╗███╗   ██╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
   ██║     ██║████╗  ██║╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
██║     ██║██╔██╗ ██║ ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║
██║     ██║██║╚██╗██║ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║
███████╗██║██║ ╚████║██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║
╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝

███████╗███████╗ ██████╗████████╗ ██████╗  ██████╗ ██╗     ███████╗
██╔════╝██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
███████╗█████╗  ██║        ██║   ██║   ██║██║   ██║██║     ███████╗
╚════██║██╔══╝  ██║        ██║   ██║   ██║██║   ██║██║     ╚════██║
███████║███████╗╚██████╗   ██║   ╚██████╔╝╚██████╔╝███████╗███████║
╚══════╝╚══════╝ ╚═════╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
```

# 🛡️ Linxploit SecTools

**The Ultimate Terminal Hub for Security Researchers**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows%20%7C%20Termux-orange?style=flat-square)]()
[![Tools](https://img.shields.io/badge/Tools-50%2B%20Curated-red?style=flat-square)]()
[![Categories](https://img.shields.io/badge/Categories-9%20Domains-purple?style=flat-square)]()
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen?style=flat-square)]()
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)]()

*One terminal. 50+ tools. Every domain of offensive security — organized, searchable, one keypress from installed.*

---

[Features](#-features) · [Installation](#-installation) · [Usage](#-usage) · [Categories](#-tool-categories) · [Recommender](#-smart-recommender) · [Docker](#-docker) · [Ethics](#-ethical-use)

</div>

---

## 🔍 Overview

**Linxploit SecTools** is a zero-dependency terminal hub built for security researchers, penetration testers, and red teamers who are tired of hunting for tools across scattered GitHub repos and wikis.

It organizes **50+ battle-tested open-source tools** across 9 offensive security domains into a single, clean TUI. Every tool shows live install status on launch. Missing a tool? One keypress installs it. Want everything in a category? One keypress handles that too. Not sure what tool you need? Describe the task — the built-in recommender tells you exactly what to reach for.

No `pip install`, no bloated dependencies, no setup overhead. Pure Python 3 stdlib. Works on Linux, macOS, Windows, and Termux.

---

## ✨ Features

| Capability | Detail |
|---|---|
| **9 Security Domains** | Information Gathering, Wireless, Web, Password Cracking, Exploitation, Phishing, Forensics, Reverse Engineering, Utilities |
| **Live Install Status** | `[ ✔ ]` installed · `[ ✘ ]` missing — verified on every screen load |
| **One-Key Install** | Install a single tool or the entire category in one keystroke |
| **Keyword Search** | Find tools by name, description, or tag instantly |
| **Smart Recommender** | Describe a task in plain English → get tool suggestions |
| **Platform-Aware** | Linux-only tools auto-hidden on macOS/Windows — no broken installs |
| **Zero Dependencies** | Pure Python 3 stdlib — nothing to install to run the hub itself |
| **Docker Ready** | Kali Linux base image with all tools pre-installed |
| **Cross-Platform** | Linux, macOS, Windows (PowerShell), Termux (Android) |
| **Extensible** | Add any tool in one line following the `Tool(...)` pattern |

---

## 🖥️ Installation

### Linux / macOS

```bash
# Clone the repository
git clone https://github.com/linxploit/Linxploit-sectools.git
cd Linxploit-sectools

# Install (creates launcher in /usr/local/bin or ~/bin)
chmod +x install.sh
./install.sh

# Launch
sectoolkit
```

**Or run directly without installing:**

```bash
python3 toolkit.py
```

### Termux (Android)

```bash
pkg update && pkg upgrade -y
pkg install python git -y
git clone https://github.com/linxploit/Linxploit-sectools.git
cd Linxplot-sectools
python3 toolkit.py
```

### Windows (PowerShell — run as Administrator)

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
.\install.ps1
# Open a new terminal, then:
sectoolkit
```

### Requirements

- Python **3.8** or newer
- A system package manager: `apt` / `apt-get`, `brew`, `pacman`, or `dnf`
- `pip3` is used as fallback for Python-based tools

---

## 🚀 Usage

### Navigation

```
┌─────────────────────────────────────────────┐
│         LINXPLOIT SECTOOLS — Main Menu      │
├─────────────────────────────────────────────┤
│  [1–9]  Open a category                     │
│  [s]    Search tools by keyword             │
│  [r]    Get recommendations for a task      │
│  [q]    Quit                                │
└─────────────────────────────────────────────┘

Inside a category:
  [1–N]  View / install a specific tool
  [a]    Install ALL missing tools in this category
  [b]    Back to main menu

Inside a tool view:
  [i]    Install (if not already installed)
  [b]    Back
```

### Keyboard Shortcuts at a Glance

| Key | Action |
|---|---|
| `1`–`9` | Open category |
| `s` | Search all tools |
| `r` | Smart task recommender |
| `a` | Install all missing in category |
| `i` | Install selected tool |
| `b` | Back |
| `q` | Quit |

---

## 📦 Tool Categories

### 🔍 Information Gathering
`nmap` · `masscan` · `theHarvester` · `recon-ng` · `whois` · `dnsrecon` · `subfinder` · `shodan` · `amass` · `maltego`

### 📡 Wireless Attacks
`aircrack-ng` · `airodump-ng` · `aireplay-ng` · `kismet` · `wifite` · `hashcat` · `hcxdumptool` · `bettercap`

### 🌐 Web Attacks
`sqlmap` · `nikto` · `gobuster` · `dirb` · `ffuf` · `burpsuite` · `wpscan` · `nuclei` · `zaproxy` · `commix` · `xsstrike`

### 🔐 Password Cracking
`hashcat` · `john` · `hydra` · `medusa` · `crunch` · `cewl` · `rsmangler` · `haiti`

### 💥 Exploitation
`metasploit` · `searchsploit` · `pwncat-cs` · `evil-winrm` · `impacket` · `crackmapexec` · `bloodhound`

### 🎣 Phishing & Social Engineering
`setoolkit` · `gophish` · `evilginx2` · `zphisher` · `king-phisher`

### 🔬 Forensics & Analysis
`wireshark` · `tshark` · `volatility3` · `binwalk` · `foremost` · `autopsy` · `stegseek`

### ⚙️ Reverse Engineering
`ghidra` · `radare2` · `gdb` · `pwndbg` · `angr` · `strings`

### 🛠️ Utilities
`netcat` · `socat` · `proxychains` · `tor` · `tmux` · `curl` · `jq` · `python3`

> **Note:** Tools requiring a GUI (Wireshark, Burp Suite, Ghidra, Maltego, Autopsy) are listed with manual download links and hidden in Docker mode.

---

## 🤖 Smart Recommender

The built-in recommender maps plain-English task descriptions to the right tools. No memorizing tool names.

```
What do you want to do?  scan a network
  → nmap, masscan, netcat

What do you want to do?  find subdomains of a target
  → subfinder, amass, dnsrecon, theHarvester

What do you want to do?  crack wifi passwords
  → aircrack-ng, hashcat, hcxdumptool, wifite

What do you want to do?  brute force a login page
  → hydra, medusa, burpsuite, ffuf

What do you want to do?  test for sql injection
  → sqlmap, commix, burpsuite

What do you want to do?  analyse a memory dump
  → volatility3, strings, binwalk

What do you want to do?  enumerate active directory
  → bloodhound, crackmapexec, impacket, evil-winrm
```

---

## 🐳 Docker

Run the full toolkit with all tools pre-installed inside a Kali Linux container:

```bash
# Build
docker build -t linxploit-sectools .

# Run interactive session
docker run -it --rm linxploit-sectools

# With network access (for active scanning)
docker run -it --rm --network host linxploit-sectools
```

> GUI tools (Wireshark, Ghidra, Burp Suite, Autopsy, Maltego) are excluded from Docker builds. The hub lists them with direct download links.

---

## 🔧 Extending SecTools

Adding a new tool takes one line in `toolkit.py`:

```python
Tool(
    "mytool",
    "Short description of what this tool does",
    "binary-name",
    install_apt="mytool",
    install_brew="mytool",
    install_pacman="mytool",
    tags=["keyword1", "keyword2", "category-tag"]
),
```

Add it to the appropriate `CATEGORIES` list and it immediately gains live status detection, one-key install, and search/recommender indexing.

---

## ⚙️ Architecture

```
toolkit.py
  │
  ├── CATEGORIES{}              # Tool registry — 9 domains, 50+ tools
  ├── Tool(dataclass)           # name, description, binary, install cmds, tags
  │
  ├── check_installed()         # Binary detection via shutil.which()
  ├── render_menu()             # TUI rendering — pure stdlib
  ├── install_tool()            # Subprocess install via apt/brew/pacman/dnf/pip
  │
  ├── search_tools()            # Keyword search across name/description/tags
  ├── recommender()             # Task → tool mapping via tag scoring
  │
  └── platform_filter()         # Hides Linux-only tools on macOS/Windows
```

---

## 🔒 Ethical Use

This toolkit is intended **exclusively** for:

- Authorized penetration testing engagements
- Security research on infrastructure you own or have explicit written permission to test
- CTF competitions and lab environments
- Security awareness training and academic study

**Do not use any tool installed through this hub against systems you do not own or lack explicit authorization to test.** Unauthorized access to computer systems violates the Computer Fraud and Abuse Act (CFAA), the UK Computer Misuse Act, and equivalent laws in your jurisdiction.

The authors assume **zero liability** for misuse. You are solely responsible for ensuring your usage is lawful.

---

## 📁 Project Structure

```
sectools/
├── toolkit.py          # Core hub — TUI, registry, installer, recommender
├── install.sh          # Linux/macOS launcher installer
├── install.ps1         # Windows PowerShell installer
├── Dockerfile          # Kali Linux base + all tools
├── requirements.txt    # Empty — zero runtime dependencies
├── README.md           # This file
├── .gitignore          # Python + OS exclusions
└── LICENSE             # MIT License
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/add-new-tool`
3. Add your tool to the correct category in `toolkit.py` using the `Tool(...)` pattern above
4. Test install detection and one-key install on at least one platform
5. Open a Pull Request with a brief description of the tool and why it belongs

All contributions should add tools that are open-source, actively maintained, and relevant to legitimate security research.

---

## 📄 License

Released under the **MIT License** — see [LICENSE](LICENSE) for full terms.

```
MIT License
Copyright (c) 2026 Hamid | Linxploit
```

---

<div align="center">

Built by **Mindless** · [Linxploit](https://linxploit.xyz) · [Portfolio](https://linxploit.xyz/founder) · [GitHub](https://github.com/linxploit)

*For authorized security research only.*

</div>
