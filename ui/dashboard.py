from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Input, RichLog
from textual.binding import Binding

class KanoDashboard(App):
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", show=True),
        Binding("ctrl+l", "clear_log", "Clear Log", show=True),
    ]

    def compose(self) -> ComposeResult:
        yield Static("KANO 🤖 - Autonomous Developer Ecosystem", id="header")
        with Container(classes="main-container"):
            yield RichLog(id="log-panel", highlight=True, markup=True)
            yield Static("Ready to code...\nWaiting for input.", id="code-panel")
        with Container(id="input-container"):
            yield Input(placeholder="Enter command or prompt...", id="prompt-input")
        yield Footer()

    def on_mount(self) -> None:
        self.log_panel = self.query_one("#log-panel", RichLog)
        self.code_panel = self.query_one("#code-panel", Static)
        self.log_panel.write("[bold green]System Initialized...[/bold green]")
        self.log_panel.write("[bold green]Ollama connection established.[/bold green]")
        self.query_one("#prompt-input").focus()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        command = event.value.strip()
        if command:
            self.log_panel.write(f"[bold white]> {command}[/bold white]")
            self.query_one("#prompt-input").value = ""
            # Here we would normally trigger the Master Agent
            self.log_panel.write(f"[yellow]Processing: {command}...[/yellow]")
            # For demo purposes
            if "hello" in command.lower():
                self.log_panel.write("[green]Kano: Hello! How can I assist you today?[/green]")

    def action_clear_log(self) -> None:
        self.log_panel.clear()

if __name__ == "__main__":
    app = KanoDashboard()
    app.run()
