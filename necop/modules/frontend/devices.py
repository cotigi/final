"""Responsable for the Devices panel"""

from ..resources import resources
from ..network.network import is_up

from textual.app import ComposeResult
from textual.containers import (
    Container,
    Horizontal,
    Vertical
)
from textual.widgets import (
    Label,
    Button,
    LoadingIndicator,
    Static
)
from textual import work
 
class Devices(Container):
    CSS_PATH = "style.tcss"

    def compose(self) -> ComposeResult:
        with Vertical(id="device-base-container"):
            with Horizontal(classes="device-container lighter-default-border"):
                yield Label("Location", classes="device-info")
                yield Label("Hostname", classes="device-info")
                yield Label("IPv4 address", classes="device-info")
                yield Static(classes="device-indicator-container")
                yield Button(
                    "Test All",
                    classes="device-test",
                    id=f"all",
                )
            for id, device in enumerate(resources.devices):
                with Horizontal(classes="device-container light-default-border", id=f"device-{id}-container"):
                    yield Label(device["location"], classes="device-info", id=f"device-{id}-location")
                    yield Label(device["name"], classes="device-info", id=f"device-{id}-hostname")
                    yield Label(device["ip"], classes="device-info", id=f"device-{id}-ip")
                    with Static(classes="device-indicator-container"):
                        yield LoadingIndicator(classes="device-test-indicator display_off", id=f"device-{id}-indicator")
                    yield Button(
                        "Test",
                        classes="device-test",
                        id=f"device-{id}-button",
                    )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = str(event.button.id)

        if button_id != "all":
            id = button_id.split("-")[1]
            self.test_device(id)
        else:
            for id in range(len(resources.devices)):
                self.test_device(id)

    @work(thread=True)
    async def test_device(self, id):
        container = self.query_one(f"#device-{id}-container")
        indicator = self.query_one(f"#device-{id}-indicator")

        ip = resources.devices[int(id)]["ip"]

        container.set_classes("device-container warning-border")

        indicator.remove_class("display_off")
        indicator.add_class("display_on")

        if await is_up(2, ip):
            container.add_class("success-border")
        else:
            container.add_class("error-border")

        indicator.remove_class("display_on")
        indicator.add_class("display_off")
