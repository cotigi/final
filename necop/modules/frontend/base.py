"""File responsable for frontend"""

from .devices import Devices
from .tftp import TFTP

from textual.app import (
    App,
    ComposeResult,
)
from textual.widgets import (
    Footer, 
    Header,
    Static, 
    TabbedContent,
    TabPane,
    Label,
    LoadingIndicator
)
from textual.worker import WorkerCancelled
from textual.compose import compose
import asyncio

class Base(App):
    """A Textual app to manage network configurations."""

    BINDINGS = [("q", "quit", "Quit")]
    
    CSS_PATH = "style.tcss"

    """
    def get_system_commands(self, screen: Screen) -> Iterable[SystemCommand]:
        yield from super().get_system_commands(screen)  
        yield SystemCommand(
            "Devices",
            "Show currently registered devices",
            self.devices
        )
    """
        
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
            
        yield Header()
        yield Footer()

        with TabbedContent():
            with TabPane("Devices", id="devices",):
                yield Devices()
            with TabPane("TFTP", id="tftp"):
                yield TFTP()

    def on_mount(self) -> None:
        self.theme = "catppuccin-frappe"

    async def action_quit(self) -> None:
        widgets = compose(self, self.cleanup_screen())
        await self.mount_all(widgets)

        await self.workers.wait_for_complete()
        
        self.exit()

    def cleanup_screen(self) -> ComposeResult:
        with Static(classes="cleanup-container default-bg"):
            yield Static()
            yield LoadingIndicator()
            with Static():
                yield Label("Waiting for worker completion")

