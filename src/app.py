import customtkinter as ctk
from core.controller.app_controller import AppController
from view.main_window import MainWindow

class App:
    def __init__(self):

        self.root = ctk.CTk()
        self.controller = AppController()
        self.height = 700
        self.width = 1200
        self.main_window = MainWindow(self.root, self.controller, width=self.width)

    def run(self):
        self.root.title("yt-dlp GUI")
        self.root.minsize(1200, 700)

        self.main_window.setup()
        self.root.mainloop()