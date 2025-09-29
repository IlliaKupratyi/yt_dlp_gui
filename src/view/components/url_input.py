from typing import Callable

import customtkinter as ctk

class URLInput(ctk.CTkFrame):
    def __init__(self, parent, on_enter: Callable[[str], None]):
        super().__init__(parent)
        self.on_enter = on_enter

        self.label = ctk.CTkLabel(self, text="YouTube URL:", font=("Arial", 14))
        self.entry = ctk.CTkEntry(self, placeholder_text="https://youtube.com/watch?v=...", width=500)

        self.entry.bind("<Return>", lambda e: self.on_enter(self.entry.get()))

        self.label.pack(side="left", padx=10)
        self.entry.pack(side="left", padx=10, fill="x", expand=True)

    def get_url(self) -> str:
        return self.entry.get().strip()