"""
Application
"""
import customtkinter as ctk
from src.controller.app_controller import AppController
from src.view.main_window import MainWindow

class App:
    """Main application class."""
    def __init__(self) -> None:
        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.controller = AppController()
        self.height = 700
        self.width = 1200
        self.main_window = MainWindow(self.root, self.controller, width=self.width)

    def run(self) -> None:
        """Create main window and start main loop"""
        self.root.title("yt-dlp GUI")
        self.root.minsize(1200, 700)

        self.main_window.setup()
        self.root.update_idletasks()
        self.root.mainloop()
