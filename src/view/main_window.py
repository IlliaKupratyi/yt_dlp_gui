import threading

import customtkinter as ctk

from src.core.controller.app_controller import AppController
from src.view.components.download_setting_panel import DownloadSettingsPanel
from src.view.components.progress_bar import ProgressBar
from src.view.components.url_input import URLInput
from src.view.components.video_info_panel import VideoInfoPanel


class MainWindow:
    def __init__(self, root: ctk.CTk, controller: AppController):
        self.root = root
        self.controller = controller

        self.url_input = URLInput(root, self.on_url_enter)
        self.video_info = VideoInfoPanel(root)
        self.download_settings = DownloadSettingsPanel(root, controller)
        self.progress_bar = ProgressBar(root)

    def setup(self):
        self.url_input.pack(pady=(20, 10))
        self.video_info.pack(pady=(10, 15), padx=20, fill="x")
        self.progress_bar.pack(pady=(0, 15))

    def on_url_enter(self, url: str):
        def load_task():
            try:
                self.controller.setup_video_properties(url.strip())
                self.video_info.update_info(self.controller.get_formats(), self.controller.get_subtitles())
                self.root.after(0, self._show_download_settings)
            except Exception as e:
                print(e)
        threading.Thread(target=load_task, daemon=True).start()

    def on_download(self):
        if not self.controller.url:
            return


        def on_output(line: str):
            pass

        def on_complete(result: dict):
            pass
        self.controller.start_downloading(
            on_output=on_output,
            on_complete=on_complete
        )

    def on_stop(self):
        pass

    def _show_download_settings(self):
        self.progress_bar.pack_forget()

        self.download_settings.pack(pady=(0, 15), padx=20, fill="x")

        self.progress_bar.pack(pady=(0, 15))

        self.download_settings.update_video_info(
            self.controller.get_formats(),
            self.controller.get_subtitles()
        )
