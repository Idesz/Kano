import sys
import os
import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, RichLog
from textual.binding import Binding
from textual.containers import Container, Horizontal
from agents.master_agent import MasterAgent

class KanoDashboard(App):
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", show=True),
        Binding("ctrl+l", "clear_log", "Clear Log", show=True),
    ]

    def __init__(self):
        super().__init__()
        self.master = MasterAgent()

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
        self.query_one("#prompt-input").focus()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        user_input = event.value.strip()
        if user_input:
            self.log_panel.write(f"[bold white]> {user_input}[/bold white]")
            self.query_one("#prompt-input").value = ""

            # Start background task to avoid freezing UI
            asyncio.create_task(self.process_request(user_input))

    async def process_request(self, user_input: str):
        self.log_panel.write("[yellow]Kano is thinking...[/yellow]")

        # Run classification and execution in a thread to keep UI responsive
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self.master.run, user_input)

        self.log_panel.write(f"[green]Result:[/green] {result}")

        if isinstance(result, tuple) and len(result) == 2:
            code, status = result
            self.code_panel.update(code)
            self.log_panel.write(f"[bold blue]Status:[/bold blue] {status}")

    def action_clear_log(self) -> None:
        self.log_panel.clear()

if __name__ == "__main__":
    app = KanoDashboard()
    app.run()
