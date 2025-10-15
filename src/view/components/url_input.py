"""Input field for YouTube URLs with real-time validation."""

from typing import Callable, Any, cast
import customtkinter as ctk

from src.core.utils.link_parser import validate_youtube_url

class URLInput(ctk.CTkFrame):
    """Class for URL input."""
    def __init__(self, parent: Any, on_enter: Callable[[str], None]):
        super().__init__(parent)
        self.on_enter = on_enter

        self.label = ctk.CTkLabel(self, text="YouTube URL:", font=("Arial", 14))

        self.url_var = ctk.StringVar()
        # noinspection PyTypeChecker
        self.url_var.trace_add("write", self._on_url_change)

        self.entry = ctk.CTkEntry(
            self,
            textvariable=self.url_var,
            placeholder_text="https://youtube.com/watch?v=...",
            width=500
        )

        self.label_error = ctk.CTkLabel(self, text="Error with fetching video. Check URL and try again.", font=("Arial", 10), text_color="Red")

        self._last_processed_url = ""

        self.label.pack(side="left", padx=10)
        self.entry.pack(side="left", padx=10, fill="x", expand=True)
        self.url_state="normal"

    def _on_url_change(self, *_: tuple[Any, ...]) -> None:
        """Validate URL on every change and trigger callback if valid and new."""
        current_url = self.url_var.get().strip()

        validated_url = validate_youtube_url(current_url)

        if not validated_url:
            self.set_error()
            return

        if validated_url != self._last_processed_url:
            self.set_normal()
            self._last_processed_url = validated_url
            self.on_enter(validated_url)

    def get_url(self) -> str:
        """Return current URL as stripped string."""
        value = self.url_var.get()
        return cast(str, value).strip()

    def set_error(self) -> None:
        """Show error message if not already in error state."""
        if not self.url_state == "error":
            self.label_error.pack(pady=10)
            self.url_state="error"

    def set_normal(self) -> None:
        """Hide error message if currently showing."""
        if self.url_state == "error":
            self.label_error.pack_forget()
            self.url_state="normal"
