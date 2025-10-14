"""
The element witch displays video title or media info
"""

from typing import Any

import customtkinter as ctk

class VideoInfoPanel(ctk.CTkFrame):
    """Displays video title or media info."""
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

    def set_title(self, title: str) -> None:
        """Update displayed title."""
        self.title_label.configure(text=title)
