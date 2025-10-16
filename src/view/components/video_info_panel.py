"""
The element witch displays video title or media info
"""
from typing import Any, Optional
import webbrowser
from PIL.Image import Image

import customtkinter as ctk

class VideoInfoPanel(ctk.CTkFrame):
    """Displays video title or media info."""
    def __init__(self, parent: Any):
        super().__init__(parent)

        self.video_url: Optional[str] = None

        self.thumbnail_label = ctk.CTkLabel(self, text="")
        self.thumbnail_label.pack(pady=(10, 10))
        self.thumbnail_label.bind("<Button-1>", self._on_click)

        self.title_label = ctk.CTkLabel(
            self,
            text="Media information",
            font=("Arial", 20, "bold"),
            wraplength=700,
            justify="center",
            cursor="hand2"
        )
        self.title_label.pack(pady=(0, 10))
        self.title_label.bind("<Button-1>", self._on_click)

        self.duration_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 14),
            text_color="gray"
        )
        self.duration_label.pack(pady=(0, 10))

    def set_properties(self, title: str, thumbnail: Image, duration: str, url: str) -> None:
        """Update displayed title."""
        self.title_label.configure(text=title)
        self.duration_label.configure(text=f"Duration: {duration}")
        self.video_url = url

        try:
            ctk_image = ctk.CTkImage(
                light_image=thumbnail,
                dark_image=thumbnail,
                size=(320, 180)
            )
            self.thumbnail_label.configure(image=ctk_image, text="")
        except Exception:
            self.thumbnail_label.configure(image=None, text="Thumbnail unavailable")

    def _on_click(self, event: Any) -> None:
        """Open video in web browser when clicked."""
        if self.video_url:
            webbrowser.open(self.video_url)
