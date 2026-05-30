from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static
from textual import events

import psutil
import platform
import socket
import shutil
import os
import getpass
from datetime import datetime

class Box(Static):
    pass

class TermWatch(App):
    CSS_PATH = os.path.join(os.path.dirname(__file__), "themes", "default.tcss")

    def compose(self) -> ComposeResult:
        yield Static(id="topbar")
        with Horizontal(id="main"):
            yield Box(id="fetch")
            with Vertical(id="right"):
                yield Box(id="cpu")
                yield Box(id="memory")
                yield Box(id="network")
                yield Box(id="battery")
        with Horizontal(id="bottom"):
            yield Box(id="system")
            yield Box(id="hardware")
            yield Box(id="software")
            yield Box(id="local")

    def on_mount(self):
        self.set_interval(1, self.update_ui)

    def on_key(self, event: events.Key) -> None:
        if event.key == "ctrl+q":
            self.exit()

    def generate_bar(self, percent, width=20):
        filled_count = int((percent / 100) * width)
        return "■" * filled_count + "▱" * (width - filled_count)

    def update_ui(self):
        username = getpass.getuser()
        hostname = socket.gethostname()
        kernel = platform.release()
        
        os_name = "Arch Linux" if os.path.exists("/etc/arch-release") else platform.system()
        
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        
        battery = psutil.sensors_battery()
        battery_pct = battery.percent if battery else 100
        battery_text = f"{battery_pct}%" if battery else "AC POWER"
        
        shell = os.environ.get("SHELL", "bash").split("/")[-1]
        wm = os.environ.get("XDG_CURRENT_DESKTOP", "Hyprland")
        
        resolution = shutil.get_terminal_size()
        res_text = f"{resolution.columns}x{resolution.lines}"

        net_counters = psutil.net_io_counters()
        recv_mb = net_counters.bytes_recv / 1024 / 1024
        sent_mb = net_counters.bytes_sent / 1024 / 1024

        try:
            pkgs = int(os.popen("pacman -Q | wc -l").read().strip())
            pkg_str = f"{pkgs} (pacman)"
        except:
            pkg_str = "N/A"

        try:
            ip_addr = socket.gethostbyname(socket.gethostname())
            if ip_addr.startswith("127."):
                test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                test_socket.connect(("8.8.8.8", 80))
                ip_addr = test_socket.getsockname()[0]
                test_socket.close()
        except:
            ip_addr = "127.0.0.1"

        # 1. Header Updates
        self.query_one("#topbar").update(
            f" ❖  TERMWATCH MATRICES  ::  {datetime.now().strftime('%H:%M:%S')}  ::  [ctrl+q to exit] "
        )

        # 2. Inline Small Logo Fetch Content (Left Side)
        self.query_one("#fetch").update(f"""
   [bold #06b6d4]{username}@{hostname}[/]
 ───────────────────────────────────────
  [cyan]OS[/]           ::  {os_name}
  [cyan]KERNEL[/]       ::  {kernel}
  [cyan]DESKTOP[/]      ::  {wm}
  [cyan]SHELL[/]        ::  {shell}
  [cyan]PACKAGES[/]     ::  {pkg_str}
  [cyan]DISPLAY[/]      ::  {res_text}
 ───────────────────────────────────────
  [magenta]DISK STORAGE[/] ::  {disk.percent}%
        """.strip())

        # 3. Streamlined Horizontal Module Bars (No extra linebreaks, fits perfectly)
        self.query_one("#cpu").update(f"[bold]CPU[/]  {self.generate_bar(cpu)}  {cpu:.1f}%")
        self.query_one("#memory").update(f"[bold]RAM[/]  {self.generate_bar(memory.percent)}  {memory.percent:.1f}%")
        self.query_one("#network").update(f"[bold]NET[/]  ↓ {recv_mb:.1f} MB  |  ↑ {sent_mb:.1f} MB")
        self.query_one("#battery").update(f"[bold]BAT[/]  {self.generate_bar(battery_pct)}  {battery_text}")

        # 4. Bottom Grid Row
        self.query_one("#system").update(f"[bold #4b5563]─ HOST OS ─[/]\n{os_name}\n[dim]{kernel}[/]")
        self.query_one("#hardware").update(f"[bold #4b5563]─ RESOURCE ─[/]\nCPU: {cpu}%\nDISK: {disk.percent}%")
        self.query_one("#software").update(f"[bold #4b5563]─ ENV ─[/]\nWM: {wm}\nSH: {shell}")
        self.query_one("#local").update(f"[bold #4b5563]─ NETWORK ─[/]\n{ip_addr}\n[dim]↓ {recv_mb:.1f}M[/]")

def main():
    TermWatch().run()

if __name__ == "__main__":
    main()