"""
Progress bar element
"""
from typing import Any

import customtkinter as ctk


class ProgressBar(ctk.CTkFrame):
    """Class for progress bar."""
    def __init__(self, parent: Any, height: int = 20, width: int = 300):
        super().__init__(parent, fg_color="transparent")
        self._is_visible = False

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self,
            width=width,
            height=height,
            mode="indeterminate"  # Default to indeterminate
        )

        # Optional label for percentage/text
        self.label = ctk.CTkLabel(self, text="", font=("Arial", 12))

        self.progress_bar.pack(pady=(0, 5))
        self.label.pack()

    def show_indeterminate(self, text: str = "Loading...") -> None:
        """Show indeterminate (spinning) progress bar."""
        self.label.configure(text=text)
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        self._show()

    def show_determinate(self, progress: float = 0.0, text: str = "") -> None:
        """Show determinate progress bar with percentage."""
        percentage = min(100, max(0, int(progress * 100)))
        display_text = f"{text} ({percentage}%)" if text else f"{percentage}%"
        self.label.configure(text=display_text)
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(progress)
        self._show()

    def update_progress(self, progress: float, text: str = "") -> None:
        """Hide the progress indicator."""
        if self._is_visible:
            self.show_determinate(progress, text)

    def hide(self) -> None:
        """Hide the progress indicator."""
        self.progress_bar.stop()
        self.pack_forget()
        self._is_visible = False

    def _show(self) -> None:
        """Ensure the widget is visible."""
        if not self._is_visible:
            self.pack(pady=(0, 15))
            self._is_visible = True
