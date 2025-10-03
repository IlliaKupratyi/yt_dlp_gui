from typing import Optional, Callable, Any

import customtkinter as ctk

class ControlButton(ctk.CTkButton):
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

    """Handle button click"""
    def _on_click(self) -> None:
        if self._state == "normal" and self._original_command:
            self._original_command()
        self.set_loading()

    """Set button to normal (ready) state."""
    def set_normal(self) -> None:
        self.configure(
            text=self._original_text,
            command=self._on_click,
            state="normal"
        )
        self._state = "normal"

    """Set button to loading state (disabled)."""
    def set_loading(self, text: str = "Downloading...") -> None:
        self.configure(
            text=text,
            command=None,
            state="disabled"
        )
        self._state = "loading"

    def set_waiting(self, text: str = "Enter video URL") -> None:
        self.configure(
            text=text,
            command=None,
            state="disabled"
        )
        self._state = "waiting"

    def get_state(self) -> str:
        return self._state