import customtkinter as ctk
from typing import Optional

"""
A temporary popup notification that auto-hides after a delay.
Appears in the bottom-right corner of the screen by default.
"""
class ToastNotification:


    def __init__(
            self,
            message: str,
            duration: int = 3000,
            parent: Optional[ctk.CTk] = None,
            width: int = 300,
            height: int = 60
    ):
        self.duration = duration
        self.window = ctk.CTkToplevel(parent or ctk.CTk())
        self.window.wm_overrideredirect(True)
        self.window.wm_attributes("-topmost", True)
        self.window.wm_attributes("-alpha", 0.9)

        # Configure appearance
        self.window.configure(fg_color=("gray90", "gray20"))  # Light/Dark theme

        # Create content
        label = ctk.CTkLabel(
            self.window,
            text=message,
            font=("Arial", 14, "bold"),
            text_color=("gray10", "gray90"),
            wraplength=width - 20
        )
        label.pack(expand=True, padx=15, pady=15)

        # Position in bottom-right corner
        self._position_window(width, height, parent)

        # Auto-hide after delay
        # noinspection PyTypeChecker
        self.window.after(duration, self.hide)

    """Position window in bottom-right corner of parent or screen."""
    def _position_window(self, width: int, height: int, parent: Optional[ctk.CTk]):
        if parent and parent.winfo_viewable():
            # Position relative to parent window
            x = parent.winfo_rootx() + parent.winfo_width() - width - 80
            y = parent.winfo_rooty() + parent.winfo_height() - height - 20
        else:
            # Position relative to screen
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            x = screen_width - width - 50
            y = screen_height - height - 80  # Above taskbar

        self.window.geometry(f"{width}x{height}+{x}+{y}")

    """Hide and destroy the notification."""
    def hide(self):
        if self.window.winfo_exists():
            self.window.destroy()