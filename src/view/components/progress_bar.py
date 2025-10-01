import customtkinter as ctk


class ProgressBar(ctk.CTkFrame):
    def __init__(self, parent, height: int = 20, width: int = 300):
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

    """Show indeterminate (spinning) progress bar."""
    def show_indeterminate(self, text: str = "Loading..."):
        print(f"[DEBUG] Showing indeterminate: {text}")
        self.label.configure(text=text)
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        self._show()

    """
    Show determinate progress bar with percentage.
     """
    def show_determinate(self, progress: float = 0.0, text: str = ""):

        percentage = min(100, max(0, int(progress * 100)))
        display_text = f"{text} ({percentage}%)" if text else f"{percentage}%"
        self.label.configure(text=display_text)
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(progress)
        self._show()

    """Update determinate progress without showing if already visible."""
    def update_progress(self, progress: float, text: str = ""):
        if self._is_visible:
            self.show_determinate(progress, text)

    """Hide the progress indicator."""
    def hide(self):
        self.progress_bar.stop()
        self.pack_forget()
        self._is_visible = False

    """Ensure the widget is visible."""
    def _show(self):
        if not self._is_visible:
            self.pack(pady=(0, 15))
            self._is_visible = True