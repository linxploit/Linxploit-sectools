#!/usr/bin/env python3

from __future__ import annotations

import os
import platform
import re
import shutil
import subprocess
import sys
import textwrap
from dataclasses import dataclass, field
from typing import Callable, Optional

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TextColumn
from rich.prompt import Prompt
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()

SYSTEM: str = platform.system().lower()
IS_LINUX: bool = SYSTEM == "linux"
IS_MAC: bool = SYSTEM == "darwin"
IS_WINDOWS: bool = SYSTEM == "windows"


def detect_pkg_manager() -> Optional[str]:
    for pm in ("apt-get", "apt", "pacman", "dnf", "yum", "brew", "pip3"):
        if shutil.which(pm):
            return pm
    return None


PKG_MANAGER: Optional[str] = detect_pkg_manager()


@dataclass
class Tool:
    name: str
    description: str
    command: str
    install_apt: str = ""
    install_brew: str = ""
    install_pip: str = ""
    install_pacman: str = ""
    install_dnf: str = ""
    install_manual: str = ""
    linux_only: bool = False
    tags: list[str] = field(default_factory=list)


@dataclass
class Category:
    name: str
    icon: str
    color: str
    tools: list[Tool]


CATEGORIES: list[Category] = [
    Category("Information Gathering", "🔍", "cyan", [
        Tool("nmap", "Network port scanner & host discovery", "nmap",
             install_apt="nmap", install_brew="nmap",
             install_pacman="nmap", install_dnf="nmap",
             tags=["network", "scan", "port", "host", "discovery", "recon", "fingerprint"]),
        Tool("masscan", "High-speed TCP port scanner", "masscan",
             install_apt="masscan", install_brew="masscan",
             install_pacman="masscan", linux_only=True,
             tags=["network", "scan", "port", "fast", "recon"]),
        Tool("theHarvester", "Email, domain, IP & name OSINT gathering", "theHarvester",
             install_apt="theharvester", install_pip="theHarvester",
             install_brew="theharvester",
             tags=["osint", "email", "domain", "recon", "gather"]),
        Tool("recon-ng", "Full-featured web reconnaissance framework", "recon-ng",
             install_apt="recon-ng", install_pip="recon-ng",
             tags=["osint", "recon", "framework", "web", "domain"]),
        Tool("whois", "Domain / IP WHOIS lookup", "whois",
             install_apt="whois", install_brew="whois",
             install_pacman="whois", install_dnf="whois",
             tags=["osint", "domain", "lookup", "recon", "whois"]),
        Tool("dnsrecon", "DNS enumeration & brute-force", "dnsrecon",
             install_apt="dnsrecon", install_pip="dnsrecon",
             tags=["dns", "recon", "enum", "brute", "domain"]),
        Tool("subfinder", "Subdomain discovery using passive sources", "subfinder",
             install_manual="https://github.com/projectdiscovery/subfinder",
             tags=["subdomain", "recon", "osint", "domain", "passive"]),
        Tool("shodan", "Shodan CLI — search internet-facing devices", "shodan",
             install_pip="shodan",
             tags=["osint", "iot", "recon", "internet", "shodan", "search"]),
        Tool("amass", "In-depth DNS enumeration & attack surface mapping", "amass",
             install_apt="amass", install_brew="amass",
             install_manual="https://github.com/owasp-amass/amass",
             tags=["dns", "recon", "osint", "subdomain", "domain", "map"]),
        Tool("maltego", "Visual link-analysis OSINT platform", "maltego",
             install_manual="https://www.maltego.com/downloads/",
             tags=["osint", "recon", "visual", "link", "graph"]),
    ]),

    Category("Wireless Attacks", "📡", "magenta", [
        Tool("aircrack-ng", "Wi-Fi network auditing suite (WEP/WPA crack)", "aircrack-ng",
             install_apt="aircrack-ng", install_brew="aircrack-ng",
             install_pacman="aircrack-ng", linux_only=True,
             tags=["wifi", "wireless", "crack", "wep", "wpa", "audit"]),
        Tool("airodump-ng", "Packet capture for 802.11 frames", "airodump-ng",
             install_apt="aircrack-ng", linux_only=True,
             tags=["wifi", "wireless", "capture", "packet", "802.11"]),
        Tool("aireplay-ng", "Inject / replay Wi-Fi frames for deauth attacks", "aireplay-ng",
             install_apt="aircrack-ng", linux_only=True,
             tags=["wifi", "wireless", "deauth", "inject", "replay", "attack"]),
        Tool("kismet", "Wireless network detector & IDS", "kismet",
             install_apt="kismet", install_brew="kismet", linux_only=True,
             tags=["wifi", "wireless", "detect", "ids", "monitor", "802.11"]),
        Tool("wifite", "Automated Wi-Fi auditing tool", "wifite",
             install_apt="wifite", install_pip="wifite2", linux_only=True,
             tags=["wifi", "wireless", "auto", "audit", "crack", "wpa"]),
        Tool("hashcat", "GPU-accelerated password/hash cracker", "hashcat",
             install_apt="hashcat", install_brew="hashcat",
             install_pacman="hashcat",
             tags=["crack", "password", "hash", "gpu", "wpa", "wifi", "brute"]),
        Tool("hcxdumptool", "Capture PMKID & EAPOL from Wi-Fi networks", "hcxdumptool",
             install_apt="hcxdumptool",
             install_manual="https://github.com/ZerBea/hcxdumptool",
             linux_only=True,
             tags=["wifi", "wireless", "capture", "pmkid", "eapol", "handshake"]),
        Tool("bettercap", "Swiss-army knife for network attacks & monitoring", "bettercap",
             install_apt="bettercap", install_brew="bettercap",
             install_manual="https://www.bettercap.org/installation/",
             tags=["mitm", "network", "wireless", "attack", "sniff", "arp", "wifi"]),
    ]),

    Category("Web Attacks", "🌐", "blue", [
        Tool("sqlmap", "Automated SQL injection & database takeover", "sqlmap",
             install_apt="sqlmap", install_pip="sqlmap",
             tags=["sql", "injection", "web", "database", "exploit", "sqli"]),
        Tool("nikto", "Web server vulnerability scanner", "nikto",
             install_apt="nikto", install_brew="nikto",
             install_pacman="nikto",
             tags=["web", "scan", "vulnerability", "server", "cve"]),
        Tool("gobuster", "Directory/file & DNS brute-forcer", "gobuster",
             install_apt="gobuster", install_brew="gobuster",
             install_manual="https://github.com/OJ/gobuster",
             tags=["web", "brute", "directory", "file", "dns", "enum", "fuzz"]),
        Tool("dirb", "Web content scanner / directory brute-force", "dirb",
             install_apt="dirb", linux_only=True,
             tags=["web", "brute", "directory", "enum", "fuzz", "content"]),
        Tool("ffuf", "Fast web fuzzer written in Go", "ffuf",
             install_apt="ffuf", install_brew="ffuf",
             install_manual="https://github.com/ffuf/ffuf",
             tags=["web", "fuzz", "enum", "directory", "brute", "fast"]),
        Tool("burpsuite", "Web app security testing platform (GUI)", "burpsuite",
             install_manual="https://portswigger.net/burp/communitydownload",
             tags=["web", "proxy", "intercept", "scan", "exploit", "gui", "burp"]),
        Tool("wpscan", "WordPress vulnerability scanner", "wpscan",
             install_apt="wpscan", install_brew="wpscan",
             tags=["web", "wordpress", "cms", "scan", "vulnerability", "plugin"]),
        Tool("nuclei", "Fast vulnerability scanner using community templates", "nuclei",
             install_manual="https://github.com/projectdiscovery/nuclei",
             install_brew="nuclei",
             tags=["web", "scan", "vulnerability", "template", "fast", "cve"]),
        Tool("zaproxy", "OWASP ZAP web app security scanner", "zap.sh",
             install_manual="https://www.zaproxy.org/download/",
             tags=["web", "owasp", "scan", "proxy", "exploit", "gui", "zap"]),
        Tool("commix", "Command injection exploiter", "commix",
             install_apt="commix", install_pip="commix",
             tags=["web", "command", "injection", "exploit", "rce", "os"]),
        Tool("xsstrike", "Advanced XSS detection & exploitation suite", "xsstrike",
             install_pip="xsstrike",
             install_manual="https://github.com/s0md3v/XSStrike",
             tags=["web", "xss", "exploit", "scan", "injection", "javascript"]),
    ]),

    Category("Password Cracking", "🔐", "yellow", [
        Tool("hashcat", "GPU-accelerated password & hash cracking", "hashcat",
             install_apt="hashcat", install_brew="hashcat",
             install_pacman="hashcat",
             tags=["crack", "password", "hash", "gpu", "brute", "dictionary", "md5", "sha"]),
        Tool("john", "John the Ripper — CPU-based password cracker", "john",
             install_apt="john", install_brew="john",
             install_pacman="john",
             tags=["crack", "password", "hash", "cpu", "brute", "dictionary", "shadow"]),
        Tool("hydra", "Fast login brute-forcer (SSH, FTP, HTTP, …)", "hydra",
             install_apt="hydra", install_brew="hydra",
             install_pacman="hydra",
             tags=["brute", "password", "login", "ssh", "ftp", "http", "service", "crack"]),
        Tool("medusa", "Parallel network login auditor", "medusa",
             install_apt="medusa", linux_only=True,
             tags=["brute", "password", "login", "parallel", "network", "crack", "audit"]),
        Tool("crunch", "Wordlist / custom dictionary generator", "crunch",
             install_apt="crunch", linux_only=True,
             tags=["wordlist", "dictionary", "generate", "brute", "crack", "custom"]),
        Tool("cewl", "Custom wordlist generator from web pages", "cewl",
             install_apt="cewl", install_brew="cewl",
             tags=["wordlist", "dictionary", "generate", "web", "scrape", "crack"]),
        Tool("rsmangler", "Wordlist permutation & mangling tool", "rsmangler",
             install_manual="https://github.com/digininja/RSMangler",
             tags=["wordlist", "mangle", "permute", "brute", "crack", "dictionary"]),
        Tool("haiti", "Hash type identifier", "haiti",
             install_pip="haiti-hash",
             tags=["hash", "identify", "type", "crack", "analyze"]),
    ]),

    Category("Exploitation", "💥", "red", [
        Tool("metasploit", "The world's most-used penetration testing framework", "msfconsole",
             install_manual="https://docs.metasploit.com/docs/using-metasploit/getting-started/nightly-installers.html",
             tags=["exploit", "framework", "payload", "session", "shell", "meterpreter", "pentest"]),
        Tool("searchsploit", "Offline search of Exploit-DB", "searchsploit",
             install_apt="exploitdb", install_brew="exploitdb",
             tags=["exploit", "search", "cve", "db", "offline", "lookup"]),
        Tool("pwncat-cs", "Post-exploitation platform / reverse shell handler", "pwncat-cs",
             install_pip="pwncat-cs",
             tags=["shell", "reverse", "post", "exploit", "handler", "c2"]),
        Tool("evil-winrm", "Windows Remote Management shell for pentesters", "evil-winrm",
             install_manual="gem install evil-winrm",
             tags=["windows", "shell", "winrm", "exploit", "post", "lateral"]),
        Tool("impacket", "Python classes for network protocols & attacks", "impacket-scripts",
             install_pip="impacket",
             tags=["windows", "smb", "kerberos", "exploit", "protocol", "lateral", "ntlm"]),
        Tool("crackmapexec", "Swiss-army knife for Active Directory pentests", "crackmapexec",
             install_pip="crackmapexec",
             tags=["windows", "active directory", "smb", "ldap", "exploit", "lateral", "ad"]),
        Tool("bloodhound", "Active Directory attack path visualisation", "bloodhound",
             install_manual="https://github.com/BloodHoundAD/BloodHound",
             tags=["active directory", "ad", "graph", "attack", "path", "lateral", "enum"]),
    ]),

    Category("Forensics & Analysis", "🔬", "green", [
        Tool("wireshark", "Network protocol analyser (GUI)", "wireshark",
             install_apt="wireshark", install_brew="wireshark",
             tags=["network", "capture", "packet", "analyse", "protocol", "traffic", "forensics"]),
        Tool("tshark", "Terminal version of Wireshark", "tshark",
             install_apt="tshark", install_brew="wireshark",
             tags=["network", "capture", "packet", "analyse", "cli", "traffic", "forensics"]),
        Tool("volatility3", "Memory forensics framework", "vol",
             install_pip="volatility3",
             tags=["memory", "forensics", "analyse", "ram", "dump", "malware"]),
        Tool("binwalk", "Firmware analysis & extraction tool", "binwalk",
             install_apt="binwalk", install_brew="binwalk",
             tags=["firmware", "binary", "extract", "analyse", "forensics", "reverse"]),
        Tool("foremost", "File carving / data recovery from images", "foremost",
             install_apt="foremost", linux_only=True,
             tags=["carve", "recover", "forensics", "image", "file", "disk"]),
        Tool("autopsy", "Digital forensics platform (GUI)", "autopsy",
             install_manual="https://www.autopsy.com/download/",
             tags=["forensics", "disk", "analyse", "gui", "investigate", "image"]),
        Tool("stegseek", "Lightning-fast steganography cracker", "stegseek",
             install_manual="https://github.com/RickdeJager/stegseek/releases",
             linux_only=True,
             tags=["stego", "steganography", "crack", "image", "hidden", "forensics"]),
    ]),

    Category("Reverse Engineering", "⚙️", "cyan", [
        Tool("ghidra", "NSA reverse engineering suite (GUI)", "ghidra",
             install_manual="https://ghidra-sre.org/",
             tags=["reverse", "decompile", "disassemble", "binary", "analyse", "re", "nsa"]),
        Tool("radare2", "Advanced CLI reverse engineering framework", "radare2",
             install_apt="radare2", install_brew="radare2",
             tags=["reverse", "disassemble", "debug", "binary", "analyse", "re", "cli"]),
        Tool("gdb", "GNU debugger", "gdb",
             install_apt="gdb", install_brew="gdb",
             tags=["debug", "reverse", "binary", "exploit", "breakpoint", "re"]),
        Tool("pwndbg", "GDB plugin for exploit dev & reverse engineering", "pwndbg",
             install_pip="pwndbg",
             install_manual="https://github.com/pwndbg/pwndbg",
             tags=["debug", "exploit", "reverse", "gdb", "pwn", "re", "binary"]),
        Tool("angr", "Python framework for binary analysis", "angr",
             install_pip="angr",
             tags=["binary", "analysis", "symbolic", "reverse", "python", "re", "ctf"]),
        Tool("strings", "Extract printable strings from binaries", "strings",
             install_apt="binutils", install_brew="binutils",
             tags=["binary", "strings", "analyse", "reverse", "re", "quick"]),
    ]),

    Category("Utilities", "🛠️", "white", [
        Tool("netcat", "TCP/UDP networking Swiss-army knife", "nc",
             install_apt="netcat-openbsd", install_brew="netcat",
             install_pacman="openbsd-netcat",
             tags=["network", "connect", "listen", "shell", "pivot", "utility", "tcp", "udp"]),
        Tool("socat", "Bidirectional data relay / advanced netcat", "socat",
             install_apt="socat", install_brew="socat",
             install_pacman="socat",
             tags=["network", "relay", "tunnel", "pivot", "utility", "tcp", "tls"]),
        Tool("proxychains", "Route TCP connections through proxy chains", "proxychains",
             install_apt="proxychains4", linux_only=True,
             tags=["proxy", "tunnel", "anonymise", "route", "socks", "tor"]),
        Tool("tor", "Anonymity network daemon", "tor",
             install_apt="tor", install_brew="tor",
             install_pacman="tor",
             tags=["tor", "anonymise", "proxy", "dark", "network", "route"]),
        Tool("tmux", "Terminal multiplexer — manage multiple panes", "tmux",
             install_apt="tmux", install_brew="tmux",
             install_pacman="tmux",
             tags=["terminal", "session", "multiplex", "utility", "pane"]),
        Tool("curl", "CLI HTTP client for API & web testing", "curl",
             install_apt="curl", install_brew="curl",
             tags=["http", "web", "request", "utility", "api", "test", "get", "post"]),
        Tool("jq", "Command-line JSON processor", "jq",
             install_apt="jq", install_brew="jq",
             install_pacman="jq",
             tags=["json", "parse", "utility", "api", "filter", "cli"]),
        Tool("python3", "Python 3 interpreter", "python3",
             install_apt="python3", install_brew="python3",
             install_pacman="python3",
             tags=["python", "scripting", "utility", "language", "dependency"]),
    ]),
]

ALL_TOOLS: dict[str, tuple[Tool, Category]] = {}
for _cat in CATEGORIES:
    for _tool in _cat.tools:
        ALL_TOOLS[_tool.name] = (_tool, _cat)

KEYWORD_MAP: dict[str, list[str]] = {
    "scan":             ["nmap", "masscan", "nikto", "nuclei", "zaproxy"],
    "network":          ["nmap", "masscan", "bettercap", "tshark", "wireshark", "netcat"],
    "port":             ["nmap", "masscan"],
    "host":             ["nmap", "masscan"],
    "discover":         ["nmap", "masscan", "subfinder", "amass", "dnsrecon"],
    "web":              ["nikto", "gobuster", "ffuf", "burpsuite", "sqlmap", "nuclei", "zaproxy"],
    "sql":              ["sqlmap"],
    "injection":        ["sqlmap", "commix", "xsstrike"],
    "xss":              ["xsstrike", "burpsuite"],
    "directory":        ["gobuster", "dirb", "ffuf"],
    "fuzz":             ["ffuf", "gobuster"],
    "wordpress":        ["wpscan"],
    "password":         ["hashcat", "john", "hydra", "medusa"],
    "crack":            ["hashcat", "john", "hydra"],
    "brute":            ["hydra", "medusa", "hashcat", "john", "gobuster", "ffuf"],
    "hash":             ["hashcat", "john", "haiti"],
    "wordlist":         ["crunch", "cewl", "rsmangler"],
    "wifi":             ["aircrack-ng", "wifite", "kismet", "hcxdumptool", "bettercap"],
    "wireless":         ["aircrack-ng", "wifite", "kismet", "airodump-ng"],
    "wpa":              ["aircrack-ng", "hashcat", "hcxdumptool", "wifite"],
    "deauth":           ["aireplay-ng", "bettercap"],
    "osint":            ["theHarvester", "recon-ng", "shodan", "maltego", "amass", "subfinder"],
    "email":            ["theHarvester"],
    "domain":           ["whois", "dnsrecon", "subfinder", "amass"],
    "subdomain":        ["subfinder", "amass", "dnsrecon"],
    "exploit":          ["metasploit", "searchsploit", "crackmapexec", "impacket"],
    "shell":            ["metasploit", "pwncat-cs", "netcat", "socat"],
    "windows":          ["evil-winrm", "crackmapexec", "impacket", "bloodhound"],
    "active directory": ["crackmapexec", "bloodhound", "impacket"],
    "ad":               ["crackmapexec", "bloodhound", "impacket"],
    "forensic":         ["wireshark", "volatility3", "binwalk", "autopsy", "foremost"],
    "memory":           ["volatility3"],
    "packet":           ["wireshark", "tshark"],
    "capture":          ["wireshark", "tshark", "airodump-ng"],
    "stego":            ["stegseek"],
    "reverse":          ["ghidra", "radare2", "gdb", "pwndbg", "binwalk"],
    "binary":           ["ghidra", "radare2", "gdb", "strings", "binwalk"],
    "debug":            ["gdb", "pwndbg"],
    "decompile":        ["ghidra"],
    "anon":             ["tor", "proxychains"],
    "proxy":            ["proxychains", "tor"],
}


def is_installed(tool: Tool) -> bool:
    return shutil.which(tool.command) is not None


def build_install_cmd(tool: Tool) -> Optional[str]:
    pm = PKG_MANAGER
    if pm in ("apt", "apt-get") and tool.install_apt:
        return f"sudo {pm} install -y {tool.install_apt}"
    if pm == "brew" and tool.install_brew:
        return f"brew install {tool.install_brew}"
    if pm == "pacman" and tool.install_pacman:
        return f"sudo pacman -S --noconfirm {tool.install_pacman}"
    if pm in ("dnf", "yum") and tool.install_dnf:
        return f"sudo {pm} install -y {tool.install_dnf}"
    if tool.install_pip:
        return f"pip3 install {tool.install_pip}"
    return None


def run_install(tool: Tool) -> None:
    cmd = build_install_cmd(tool)
    if cmd:
        console.print(f"\n[bold cyan]▶[/bold cyan] Running: [bold]{cmd}[/bold]")
        result = subprocess.run(cmd, shell=True)
        if result.returncode == 0:
            console.print("[bold green]✔  Installation succeeded.[/bold green]")
        else:
            console.print("[bold red]✘  Installation failed — check output above.[/bold red]")
    elif tool.install_manual:
        console.print(f"\n[bold yellow]⚠[/bold yellow]  No automatic installer for this tool.")
        console.print(f"   Manual install: [bold]{tool.install_manual}[/bold]")
    else:
        console.print("[bold red]  No known install method for this platform.[/bold red]")
    Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")


def visible_tools(cat: Category) -> list[Tool]:
    if IS_MAC or IS_WINDOWS:
        return [t for t in cat.tools if not t.linux_only]
    return list(cat.tools)


def status_badge(tool: Tool) -> Text:
    if is_installed(tool):
        return Text("[ ✔ ]", style="bold green")
    return Text("[ ✘ ]", style="bold red")


def global_stats() -> tuple[int, int]:
    total = sum(len(cat.tools) for cat in CATEGORIES)
    installed = sum(1 for cat in CATEGORIES for t in cat.tools if is_installed(t))
    return installed, total


def recommend_tools(query: str) -> list[tuple[Tool, Category]]:
    q = query.lower()
    scores: dict[str, int] = {}
    for keyword, names in KEYWORD_MAP.items():
        if keyword in q:
            for n in names:
                scores[n] = scores.get(n, 0) + 2
    words = re.findall(r"\w+", q)
    for cat in CATEGORIES:
        for tool in cat.tools:
            for w in words:
                if any(w in tag for tag in tool.tags):
                    scores[tool.name] = scores.get(tool.name, 0) + 1
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    results: list[tuple[Tool, Category]] = []
    for name, _ in ranked[:8]:
        if name in ALL_TOOLS:
            results.append(ALL_TOOLS[name])
    return results


def search_tools(query: str) -> list[tuple[Tool, Category]]:
    q = query.lower()
    results: list[tuple[Tool, Category]] = []
    for cat in CATEGORIES:
        for tool in cat.tools:
            if (q in tool.name.lower()
                    or q in tool.description.lower()
                    or any(q in tag for tag in tool.tags)):
                results.append((tool, cat))
    return results


def render_banner() -> Panel:
    art = Text(justify="center")
    art.append("\n")
    art.append("██╗     ██╗███╗   ██╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗\n", style="bold red")
    art.append("██║     ██║████╗  ██║╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝\n", style="bold red")
    art.append("██║     ██║██╔██╗ ██║ ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   \n", style="bold red")
    art.append("██║     ██║██║╚██╗██║ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   \n", style="bold red")
    art.append("███████╗██║██║ ╚████║██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   \n", style="bold red")
    art.append("╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   \n", style="bold red")
    art.append("\n")
    art.append("███████╗███████╗ ██████╗████████╗ ██████╗  ██████╗ ██╗     ███████╗\n", style="red")
    art.append("██╔════╝██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝\n", style="red")
    art.append("███████╗█████╗  ██║        ██║   ██║   ██║██║   ██║██║     ███████╗\n", style="red")
    art.append("╚════██║██╔══╝  ██║        ██║   ██║   ██║██║   ██║██║     ╚════██║\n", style="red")
    art.append("███████║███████╗╚██████╗   ██║   ╚██████╔╝╚██████╔╝███████╗███████║\n", style="red")
    art.append("╚══════╝╚══════╝ ╚═════╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝\n", style="red")
    art.append("\n")
    art.append("All-in-One Security Research Toolkit Hub", style="bold white")
    art.append("   ·   ", style="dim")
    art.append("linxploit.xyz", style="bold cyan")
    art.append("\n")
    art.append(f"Platform: {platform.system()}   ", style="dim")
    art.append(f"Pkg manager: {PKG_MANAGER or 'none detected'}   ", style="dim")
    art.append(f"Python: {sys.version.split()[0]}", style="dim")
    return Panel(art, border_style="red", expand=True)


def render_stats_bar() -> Text:
    installed, total = global_stats()
    pct = int(installed / total * 100) if total else 0
    bar_len = 30
    filled = int(bar_len * pct / 100)
    bar = Text()
    bar.append("  Arsenal: [", style="dim")
    bar.append("█" * filled, style="bold green")
    bar.append("░" * (bar_len - filled), style="dim")
    bar.append("] ", style="dim")
    bar.append(f"{pct}%", style="bold white")
    bar.append(f"  ({installed}/{total} tools installed)", style="dim")
    return bar


def render_main_table() -> Table:
    table = Table(
        box=box.ROUNDED,
        border_style="dim",
        header_style="bold cyan",
        show_header=True,
        expand=True,
        title="[bold red]Categories[/bold red]",
        title_justify="left",
    )
    table.add_column("#", justify="right", style="bold cyan", width=4)
    table.add_column("Category", min_width=28)
    table.add_column("Progress", min_width=22)
    table.add_column("Tools", justify="center", width=7)

    for i, cat in enumerate(CATEGORIES, 1):
        vis = visible_tools(cat)
        inst = sum(1 for t in vis if is_installed(t))
        total_v = len(vis)
        bar_len = 12
        filled = int(bar_len * inst / total_v) if total_v else 0
        prog = Text()
        prog.append("█" * filled, style="bold green")
        prog.append("░" * (bar_len - filled), style="dim")
        prog.append(f"  {inst}/{total_v}", style="dim")

        label = Text()
        label.append(f"{cat.icon}  ", style="")
        label.append(cat.name, style=f"bold {cat.color}")

        table.add_row(str(i), label, prog, str(total_v))

    return table


def render_tool_table(cat: Category) -> Table:
    vis = visible_tools(cat)
    table = Table(
        box=box.ROUNDED,
        border_style=cat.color,
        header_style=f"bold {cat.color}",
        show_lines=False,
        expand=True,
        title=f"[bold {cat.color}]{cat.icon}  {cat.name}[/bold {cat.color}]",
    )
    table.add_column("#", justify="right", style="bold cyan", width=4)
    table.add_column("Status", justify="center", width=8)
    table.add_column("Tool", min_width=18, style="bold white")
    table.add_column("Description")

    for i, tool in enumerate(vis, 1):
        badge = status_badge(tool)
        desc = textwrap.shorten(tool.description, width=58)
        table.add_row(str(i), badge, tool.name, Text(desc, style="dim"))

    return table


def render_tool_detail(tool: Tool, cat: Category) -> Panel:
    inst = is_installed(tool)
    cmd = build_install_cmd(tool)
    content = Text()
    content.append(f"\n  {tool.name}\n", style=f"bold {cat.color}")
    content.append(f"  {tool.description}\n\n", style="white")
    content.append("  Status    : ", style="dim")
    if inst:
        content.append("Installed ✔\n", style="bold green")
    else:
        content.append("Not installed ✘\n", style="bold red")
    content.append(f"  Binary    : ", style="dim")
    content.append(f"{tool.command}\n", style="cyan")
    if tool.linux_only:
        content.append("  Platform  : ", style="dim")
        content.append("Linux only\n", style="yellow")
    if cmd:
        content.append("  Install   : ", style="dim")
        content.append(f"{cmd}\n", style="dim white")
    if tool.install_manual:
        content.append("  Manual    : ", style="dim")
        content.append(f"{tool.install_manual}\n", style="dim white")
    content.append("  Tags      : ", style="dim")
    content.append(", ".join(tool.tags) + "\n", style="dim")
    content.append("\n")
    if not inst:
        content.append("  [i] Install    ", style="bold cyan")
    content.append("  [b] Back", style="bold cyan")
    return Panel(content, border_style=cat.color, expand=False)


def render_search_results(query: str, results: list[tuple[Tool, Category]]) -> Table:
    table = Table(
        box=box.SIMPLE_HEAVY,
        border_style="dim",
        header_style="bold white",
        expand=True,
        title=f"[bold white]Results for:[/bold white] [cyan]{query}[/cyan]",
    )
    table.add_column("#", justify="right", style="bold cyan", width=4)
    table.add_column("Status", justify="center", width=8)
    table.add_column("Tool", min_width=18, style="bold white")
    table.add_column("Category", min_width=22)
    table.add_column("Description")

    for i, (tool, cat) in enumerate(results, 1):
        badge = status_badge(tool)
        cat_text = Text(f"{cat.icon} {cat.name}", style=f"dim {cat.color}")
        desc = Text(textwrap.shorten(tool.description, width=45), style="dim")
        table.add_row(str(i), badge, tool.name, cat_text, desc)

    return table


def screen_tool_detail(tool: Tool, cat: Category) -> None:
    while True:
        console.clear()
        console.print(render_banner())
        console.print(render_tool_detail(tool, cat))
        console.print()
        inst = is_installed(tool)
        raw = Prompt.ask("[bold yellow]Choice[/bold yellow]", default="b").strip().lower()
        if raw == "i" and not inst:
            run_install(tool)
        elif raw == "b":
            break


def screen_category(cat: Category) -> None:
    while True:
        console.clear()
        console.print(render_banner())
        console.print(render_tool_table(cat))
        console.print()
        console.print(f"  [bold cyan][a][/bold cyan] Install all missing in this category   "
                      f"[bold cyan][b][/bold cyan] Back")
        console.print()
        raw = Prompt.ask("[bold yellow]Select tool number or action[/bold yellow]", default="b").strip().lower()
        vis = visible_tools(cat)
        if raw == "b":
            break
        elif raw == "a":
            missing = [t for t in vis if not is_installed(t)]
            if not missing:
                console.print("[bold green]  All tools in this category are already installed.[/bold green]")
                Prompt.ask("[dim]Press Enter to continue[/dim]", default="")
            else:
                for tool in missing:
                    console.print(f"\n[bold cyan]▶[/bold cyan] [bold]{tool.name}[/bold]")
                    run_install(tool)
        elif raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(vis):
                screen_tool_detail(vis[idx], cat)


def screen_search() -> None:
    console.clear()
    console.print(render_banner())
    console.print(Rule("[bold white]🔎  Search Tools[/bold white]"))
    console.print()
    query = Prompt.ask("[bold yellow][?][/bold yellow] Enter keyword(s)", default="").strip()
    if not query:
        return
    results = search_tools(query)
    console.clear()
    console.print(render_banner())
    if not results:
        console.print(Panel("[bold red]No tools matched your query.[/bold red]", border_style="dim red"))
        Prompt.ask("[dim]Press Enter to go back[/dim]", default="")
        return
    console.print(render_search_results(query, results))
    console.print()
    raw = Prompt.ask("[bold yellow]Enter number to view tool, or Enter to go back[/bold yellow]", default="").strip()
    if raw.isdigit():
        idx = int(raw) - 1
        if 0 <= idx < len(results):
            tool, cat = results[idx]
            screen_tool_detail(tool, cat)


def screen_recommend() -> None:
    console.clear()
    console.print(render_banner())
    console.print(Rule("[bold white]💡  Tool Recommender[/bold white]"))
    console.print()
    console.print("[dim]  Describe what you want to do in plain English.[/dim]")
    console.print("[dim]  Examples: 'scan a network', 'crack wifi passwords', 'find subdomains'[/dim]")
    console.print()
    query = Prompt.ask("[bold yellow][?][/bold yellow] What do you want to do", default="").strip()
    if not query:
        return
    results = recommend_tools(query)
    console.clear()
    console.print(render_banner())
    console.print(Rule(f"[bold white]💡  Recommended for:[/bold white] [cyan]{query}[/cyan]"))
    if not results:
        console.print(Panel(
            "[yellow]No specific recommendations found.\nTry different keywords like 'scan', 'exploit', 'crack', 'reverse'.[/yellow]",
            border_style="yellow",
        ))
        Prompt.ask("[dim]Press Enter to go back[/dim]", default="")
        return

    table = Table(
        box=box.ROUNDED, border_style="dim", header_style="bold white",
        expand=True, title="[bold white]Top Matches[/bold white]",
    )
    table.add_column("#", justify="right", style="bold cyan", width=4)
    table.add_column("Status", justify="center", width=8)
    table.add_column("Tool", min_width=18, style="bold white")
    table.add_column("Category", min_width=22)
    table.add_column("Description")

    for i, (tool, cat) in enumerate(results, 1):
        badge = status_badge(tool)
        cat_text = Text(f"{cat.icon} {cat.name}", style=f"dim {cat.color}")
        desc = Text(textwrap.shorten(tool.description, width=45), style="dim")
        table.add_row(str(i), badge, tool.name, cat_text, desc)

    console.print(table)
    console.print()
    raw = Prompt.ask("[bold yellow]Enter number to view tool, or Enter to go back[/bold yellow]", default="").strip()
    if raw.isdigit():
        idx = int(raw) - 1
        if 0 <= idx < len(results):
            tool, cat = results[idx]
            screen_tool_detail(tool, cat)


def main_menu() -> None:
    while True:
        console.clear()
        console.print(render_banner())
        console.print(render_stats_bar())
        console.print()
        console.print(render_main_table())
        console.print()
        console.print(
            "  [bold cyan][1–9][/bold cyan] Open category   "
            "[bold cyan][s][/bold cyan] Search   "
            "[bold cyan][r][/bold cyan] Recommend   "
            "[bold cyan][q][/bold cyan] Quit"
        )
        console.print()
        raw = Prompt.ask("[bold yellow]Choice[/bold yellow]", default="q").strip().lower()

        if raw == "q":
            console.print("\n[bold cyan]  Stay sharp, stay legal. — Mindless × Linxploit[/bold cyan]\n")
            sys.exit(0)
        elif raw == "s":
            screen_search()
        elif raw == "r":
            screen_recommend()
        elif raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(CATEGORIES):
                screen_category(CATEGORIES[idx])


def main() -> None:
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[bold cyan]\n  Interrupted. Goodbye!\n[/bold cyan]")
        sys.exit(0)
    except Exception as exc:
        console.print_exception()
        sys.exit(1)


if __name__ == "__main__":
    main()
