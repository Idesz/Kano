import sys
import os
import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, RichLog
from textual.binding import Binding
from textual.containers import Container, Horizontal
from agents.master_agent import MasterAgent
from core.idle_learner import IdleLearner

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

    def compose(self) -> ComposeResult:
        yield Static("KANO 🤖 - Autonomous Developer Ecosystem", id="header")
        with Horizontal(classes="main-container"):
            yield RichLog(id="log-panel", highlight=True, markup=True)
            yield Static("Ready to code...\nWaiting for input.", id="code-panel")
        with Container(id="input-container"):
            yield Input(placeholder="Enter command or prompt...", id="prompt-input")
        yield Footer()

    def on_mount(self) -> None:
        self.log_panel = self.query_one("#log-panel", RichLog)
        self.code_panel = self.query_one("#code-panel", Static)
        self.log_panel.write("[bold green]Kano System Online.[/bold green]")
        self.log_panel.write(f"[green]Available Skills: {', '.join([s['name'] for s in self.master.registry.list_skills()])}[/green]")
        self.learner.start()
        self.log_panel.write("[blue]Idle Learning active.[/blue]")
        self.query_one("#prompt-input").focus()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        user_input = event.value.strip()
        if not user_input: return

        self.query_one("#prompt-input").value = ""

        if self.pending_task:
            if user_input.lower() in ['y', 'yes', 'igen']:
                task = self.pending_task
                self.pending_task = None
                self.log_panel.write("[green]Approval received. Proceeding...[/green]")
                asyncio.create_task(self.process_request(task, approved=True))
            else:
                self.pending_task = None
                self.log_panel.write("[red]Task cancelled by user.[/red]")
            return

        self.log_panel.write(f"[bold white]> {user_input}[/bold white]")
        asyncio.create_task(self.process_request(user_input))

    async def process_request(self, user_input: str, approved: bool = False):
        self.log_panel.write("[yellow]Kano is thinking...[/yellow]")
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self.master.run, user_input, approved)

        if isinstance(result, tuple) and result[0] == "APPROVAL_REQUIRED":
            self.pending_task = user_input
            self.log_panel.write(f"[bold orange3]⚠️ SUBJECTIVE TASK DETECTED:[/bold orange3] {result[1]}")
            self.log_panel.write("[bold cyan]Proceed? (y/n)[/bold cyan]")
            return

        if isinstance(result, tuple) and len(result) == 2:
            code, status = result
            self.code_panel.update(code)
            self.log_panel.write(f"[bold blue]Status:[/bold blue] {status}")
        else:
            self.log_panel.write(f"[green]Result:[/green] {result}")

    def action_clear_log(self) -> None:
        self.log_panel.clear()

if __name__ == "__main__":
    app = KanoDashboard()
    app.run()
