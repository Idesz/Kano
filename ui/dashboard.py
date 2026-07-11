import sys
import os
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

            # Run Master Agent logic
            self.log_panel.write("[yellow]Thinking...[/yellow]")
            decision = self.master.classify_intent(user_input)
            self.log_panel.write(f"[blue]Action: {decision.get('target')}[/blue]")
            self.log_panel.write(f"[blue]Reason: {decision.get('reason')}[/blue]")

            # Simple simulation for now
            self.log_panel.write("[green]Operation completed.[/green]")

    def action_clear_log(self) -> None:
        self.log_panel.clear()

if __name__ == "__main__":
    app = KanoDashboard()
    app.run()
