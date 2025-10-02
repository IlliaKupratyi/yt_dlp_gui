import threading

import customtkinter as ctk

from src.core.config.config import DATA_DIR
from src.core.controller.app_controller import AppController
from src.core.exception import YTDLRuntimeError
from src.core.flags.output_paths_flag import OutputPathsFlag
from src.view.components.control_button import ControlButton
from src.view.components.download_setting_panel import DownloadSettingsPanel
from src.view.components.notification import ToastNotification
from src.view.components.progress_bar import ProgressBar
from src.view.components.output_folder_selector import OutputFolderSelector
from src.view.components.url_input import URLInput
from src.view.components.video_info_panel import VideoInfoPanel


class MainWindow:
    def __init__(self, root: ctk.CTk, controller: AppController, width: int = 800):
        self.root = root
        self.controller = controller

        self.scrollable_frame = ctk.CTkScrollableFrame(root, width=width, fg_color="transparent")
        self.scrollable_frame.pack(fill="both", expand=True)

        self.url_input = URLInput(self.scrollable_frame, self.on_url_enter)

        self.video_info = VideoInfoPanel(self.scrollable_frame)
        self.output_selector = OutputFolderSelector(
            self.scrollable_frame,
            label_text="Save to:",
            default_path=DATA_DIR,
            on_change=self._on_output_folder_change
        )

        self.output_folder = DATA_DIR

        self.download_settings = DownloadSettingsPanel(self.scrollable_frame)

        self.download_button = ControlButton(
            self.scrollable_frame,
            text="Download Video",
            command=self.on_download,
            width=180,
            height=30
        )

        self.progress_indicator = ProgressBar(self.scrollable_frame)

    def setup(self):
        self.url_input.pack(pady=(20, 10))
        self.video_info.pack(pady=(10, 15), padx=20, fill="x")
        self.output_selector.pack(pady=(0, 15), padx=20, fill="x")

    def on_url_enter(self, url: str):
        self.progress_indicator.show_indeterminate("Fetching video info...")

        def load_task():
            try:
                def on_output(line: str):
                    # noinspection PyTypeChecker
                    self.root.after(0, lambda: self.progress_indicator.label.configure(text=f"Loading... {line}"))
                self.controller.setup_video_properties(url=url.strip(), on_output=on_output)
                self.video_info.update_info(self.controller.get_formats(), self.controller.get_subtitles())
                self.download_button.set_normal()
                # noinspection PyTypeChecker
                self.root.after(0, self._on_video_info_loaded)
            except YTDLRuntimeError as e:
                self._on_video_info_error()
            except Exception as e:
                print(e)
        threading.Thread(target=load_task, daemon=True).start()

    def on_download(self):
        if not self.controller.url:
            return

        self._set_flags()

        self.progress_indicator.show_indeterminate("Downloading video...")
        def on_output(line: str):
            # noinspection PyTypeChecker
            self.root.after(0, lambda: self.progress_indicator.label.configure(text=f"Loading... {line}"))

        def on_complete(result: dict):
            self._finish_download()

        self.controller.start_downloading(
            on_output=on_output,
            on_complete=on_complete
        )

    def _show_download_settings(self):
        self.progress_indicator.pack_forget()

        self.download_settings.pack(pady=(0, 15), padx=20, fill="x")

        self.progress_indicator.pack(pady=(0, 15))

        self.download_settings.update_video_info(
            self.controller.get_formats(),
            self.controller.get_subtitles()
        )

    def _on_output_folder_change(self, folder: str):
        self.output_folder = folder

    def _on_video_info_loaded(self):
        self.video_info.update_info(self.controller.get_formats(), self.controller.get_subtitles())
        self.url_input.set_normal()
        self._show_download_settings()
        self.download_button.set_normal()
        self.progress_indicator.hide()
        self.download_button.pack()

    def _on_video_info_error(self):
        self.url_input.set_error()
        self.progress_indicator.hide()

    def _set_flags(self):
        self.controller.add_flag(OutputPathsFlag(self.output_folder))

        for flag in self.download_settings.get_flags():
            self.controller.add_flag(flag)

    def _finish_download(self):
        self.progress_indicator.hide()
        self.download_button.set_normal()
        ToastNotification(
            message="✅ Video downloaded successfully!",
            duration=3000,
            parent=self.root
        )