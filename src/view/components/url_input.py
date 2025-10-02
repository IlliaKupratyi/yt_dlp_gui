from typing import Callable
import customtkinter as ctk


class URLInput(ctk.CTkFrame):
    def __init__(self, parent, on_enter: Callable[[str], None]):
        super().__init__(parent)
        self.on_enter = on_enter

        self.label = ctk.CTkLabel(self, text="YouTube URL:", font=("Arial", 14))

        self.url_var = ctk.StringVar()
        self.url_var.trace_add("write", self._on_url_change)

        self.entry = ctk.CTkEntry(
            self,
            textvariable=self.url_var,
            placeholder_text="https://youtube.com/watch?v=...",
            width=500
        )

        self._last_processed_url = ""

        self.label.pack(side="left", padx=10)
        self.entry.pack(side="left", padx=10, fill="x", expand=True)

    def _on_url_change(self, *args):
        current_url = self.url_var.get().strip()

        if current_url != self._last_processed_url:
            self._last_processed_url = current_url
            self.on_enter(current_url)

    def get_url(self) -> str:
        return self.url_var.get().strip()