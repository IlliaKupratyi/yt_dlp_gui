import customtkinter as ctk

class VideoInfoPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.title_label = ctk.CTkLabel(
            self,
            text="📹 Media information",
            font=("Arial", 20, "bold"),
            wraplength=700,
            justify="center"
        )

        self.title_label.pack(pady=(10, 15))

    def set_title(self, title: str):
        self.title_label.configure(text=title)