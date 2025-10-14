"""
Button with states: normal, waiting, loading
"""
from typing import Optional, Callable, Any

import customtkinter as ctk

class ControlButton(ctk.CTkButton):
    """Class for button with states: normal, waiting, loading"""
    def __init__(self,
                 parent: Any,
                 text: str = "Download",
                 command: Optional[Callable[[], None]] = None,
                 width: int = 150,
                 height: int = 40):
        self._original_command = command
        self._original_text = text

        super().__init__(
            parent,
            text=text,
            command=self._on_click,
            width=width,
            height=height
        )
        self._state = "normal"
        self.set_waiting()

    def _on_click(self) -> None:
        """Handle button click"""
        if self._state == "normal" and self._original_command:
            self._original_command()
        self.set_loading()

    def set_normal(self) -> None:
        """Set button to normal (ready) state."""
        self.configure(
            text=self._original_text,
            command=self._on_click,
            state="normal"
        )
        self._state = "normal"

    def set_loading(self, text: str = "Downloading...") -> None:
        """Set button to normal (ready) state."""
        self.configure(
            text=text,
            command=None,
            state="disabled"
        )
        self._state = "loading"

    def set_waiting(self, text: str = "Enter video URL") -> None:
        """Set button to waiting state."""
        self.configure(
            text=text,
            command=None,
            state="disabled"
        )
        self._state = "waiting"


    def get_state(self) -> str:
        """Execute original command and switch to loading state."""
        return self._state
