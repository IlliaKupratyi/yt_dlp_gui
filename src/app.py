import customtkinter as ctk
from core.controller.app_controller import AppController
from view.main_window import MainWindow

class App:
    def __init__(self):
        ctk.set_appearance_mode("light")

        self.root = ctk.CTk()
        self.controller = AppController()  # ← Ваш контроллер без изменений!
        self.main_window = MainWindow(self.root, self.controller)

    def run(self):
        self.root.title("yt-dlp GUI")
        self.root.minsize(1200, 700)

        self.main_window.setup()
        self.root.mainloop()