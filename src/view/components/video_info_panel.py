import customtkinter as ctk

from src.core.dataclass.subtitle import Subtitles

class VideoInfoPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.title_label = ctk.CTkLabel(self, text="Media information", font=("Arial", 16, "bold"))
        self.formats_label = ctk.CTkLabel(self, text="Formats: —", font=("Consolas", 11))
        self.subtitles_label = ctk.CTkLabel(self, text="Subtitles: —", font=("Consolas", 11))

        self.title_label.pack(pady=(5, 10))
        self.formats_label.pack(anchor="w", padx=10)
        self.subtitles_label.pack(anchor="w", padx=10)

    """
    Update video information
    """
    def update_info(self, formats: list[dict[str, str]], subtitles: Subtitles) -> None:
        format_count = len(formats)
        subtitle_count = len(subtitles.subtitles)

        self.formats_label.configure(text=f"Formats: {format_count}")
        self.subtitles_label.configure(text=f"Subtitles: {subtitle_count}")