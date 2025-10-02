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

        self.label_error = ctk.CTkLabel(self, text="Error with fetching video. Check URL and try again.", font=("Arial", 10), text_color="Red")

        self._last_processed_url = ""

        self.label.pack(side="left", padx=10)
        self.entry.pack(side="left", padx=10, fill="x", expand=True)
        self.url_state="normal"

    def _on_url_change(self, *args):
        current_url = self.url_var.get().strip()

        if current_url != self._last_processed_url:
            self._last_processed_url = current_url
            self.on_enter(current_url)

    def get_url(self) -> str:
        return self.url_var.get().strip()

    def set_error(self):
        if not self.url_state.__eq__("error"):
            self.label_error.pack(pady=10)
            self.url_state="error"

    def set_normal(self):
        if self.url_state.__eq__("error"):
            self.label_error.pack_forget()
            self.url_state="normal"