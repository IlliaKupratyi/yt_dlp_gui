from typing import Any

import customtkinter as ctk

"""Displays video title or media info."""
class VideoInfoPanel(ctk.CTkFrame):
    def __init__(self, parent: Any):
        super().__init__(parent)

        self.title_label = ctk.CTkLabel(
            self,
            text="Media information",
            font=("Arial", 20, "bold"),
            wraplength=700,
            justify="center"
        )
        self.title_label.pack(pady=(10, 15))

    """Update displayed title."""
    def set_title(self, title: str) -> None:
        self.title_label.configure(text=title)