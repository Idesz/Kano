import sys
import os
import asyncio
import psutil
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, RichLog
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from agents.master_agent import MasterAgent
from core.idle_learner import IdleLearner

class HardwareMonitor(Static):
    def on_mount(self) -> None:
        self.set_interval(2.0, self.update_stats)

    def update_stats(self) -> None:
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        self.update(f"CPU: {cpu}% | RAM: {ram}% | Sandbox: Active")

class KanoDashboard(App):
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", show=True),
        Binding("ctrl+l", "clear_log", "Clear Log", show=True),
    ]

    def __init__(self):
        super().__init__()
        self.master = MasterAgent()
        self.learner = IdleLearner()
        self.pending_task = None
        self.max_log_lines = 5000 # Log Rotation

    def compose(self) -> ComposeResult:
        yield Static("KANO 🤖 - FLAWLESS EDITION", id="header")
        yield HardwareMonitor(id="monitor")
        with Horizontal(classes="main-container"):
            yield RichLog(id="log-panel", highlight=True, markup=True, max_lines=self.max_log_lines)
            yield Static("System Core: Flawless\nWaiting for orders.", id="code-panel")
        with Container(id="input-container"):
            yield Input(placeholder="Execute command...", id="prompt-input")
        yield Footer()

    def on_mount(self) -> None:
        self.log_panel = self.query_one("#log-panel", RichLog)
        self.code_panel = self.query_one("#code-panel", Static)
        self.log_panel.write("[bold green]System initialized with perfectionist safeguards.[/bold green]")
        self.learner.start()
        self.query_one("#prompt-input").focus()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        user_input = event.value.strip()
        if not user_input: return
        self.query_one("#prompt-input").value = ""

        if self.pending_task:
            if user_input.lower() in ['y', 'yes', 'igen']:
                task = self.pending_task
                self.pending_task = None
                asyncio.create_task(self.process_request(task, approved=True))
            else:
                self.pending_task = None
                self.log_panel.write("[red]Aborted.[/red]")
            return

        self.log_panel.write(f"[bold white]> {user_input}[/bold white]")
        asyncio.create_task(self.process_request(user_input))

    async def process_request(self, user_input: str, approved: bool = False):
        self.log_panel.write("[yellow]Processing...[/yellow]")
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self.master.run, user_input, approved)

        if isinstance(result, tuple) and result[0] == "APPROVAL_REQUIRED":
            self.pending_task = user_input
            self.log_panel.write(f"[bold orange3]⚠️ SUBJECTIVE DECISION:[/bold orange3] {result[1]}")
            self.log_panel.write("[bold cyan]Approve? (y/n)[/bold cyan]")
            return

        if isinstance(result, tuple) and len(result) == 2:
            code, status = result
            self.code_panel.update(code)
            self.log_panel.write(f"[bold blue]Status:[/bold blue] {status}")
        else:
            self.log_panel.write(f"[green]Output:[/green] {result}")

    def action_clear_log(self) -> None:
        self.log_panel.clear()

if __name__ == "__main__":
    app = KanoDashboard()
    app.run()
