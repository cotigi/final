"""Responsable for the TFTP"""

from ..resources import resources
from ..network.network import save_to_tftp

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
 
class TFTP(Container):
    CSS_PATH = "style.tcss"

    def compose(self) -> ComposeResult:
        with Vertical(id="device-base-container"):
            with Horizontal(classes="device-container lighter-default-border"):
                yield Label("Location", classes="device-info")
                yield Label("Hostname", classes="device-info")
                yield Label("IPv4 address", classes="device-info")
                yield Static(classes="device-indicator-container")
                yield Button(
                    "Save All",
                    classes="device-test",
                    id=f"all",
                )
            for id, device in enumerate(resources.devices):
                with Horizontal(classes="device-container light-default-border", id=f"tftp-{id}-container"):
                    yield Label(device["location"], classes="device-info", id=f"tftp-{id}-location")
                    yield Label(device["name"], classes="device-info", id=f"tftp-{id}-hostname")
                    yield Label(device["ip"], classes="device-info", id=f"tftp-{id}-ip")
                    with Static(classes="device-indicator-container"):
                        yield Label(classes=f"display-off", id=f"tftp-{id}-bytes")
                        yield LoadingIndicator(classes="device-test-indicator display-off", id=f"tftp-{id}-indicator")
                    yield Button(
                        "Save",
                        classes="device-test",
                        id=f"tftp-{id}-button",
                    )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = str(event.button.id)

        if button_id != "all":
            id = button_id.split("-")[1]
            self.save_device(id)
        else:
            for id in range(len(resources.devices)):
                self.save_device(id)

    @work(thread=True)
    async def save_device(self, id):
        container = self.query_one(f"#tftp-{id}-container", Horizontal)
        indicator = self.query_one(f"#tftp-{id}-indicator", LoadingIndicator)
        bytes_label = self.query_one(f"#tftp-{id}-bytes", Label)
        hostname = self.query_one(f"#tftp-{id}-hostname", Label).content

        ip = resources.devices[int(id)]["ip"]

        container.set_classes("device-container warning-border")
        indicator.set_classes("device-test-indicator display-on")
        bytes_label.set_classes("display-off")

        status, bytes_str = await save_to_tftp(hostname, ip)

        indicator.set_classes("device-test-indicator display-off")

        if status:
            bytes_label.update(bytes_str+"B")
            bytes_label.set_classes("display-on")

            container.add_class("success-border")
        else:
            container.add_class("error-border")
