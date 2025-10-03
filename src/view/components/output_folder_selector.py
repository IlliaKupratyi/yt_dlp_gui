import customtkinter as ctk
from pathlib import Path
from typing import Callable, Optional, Any, cast

"""
UI component for selecting an output folder.
"""
class OutputFolderSelector(ctk.CTkFrame):
    def __init__(
            self,
            parent: Any,
            label_text: str = "Save to:",
            default_path: str = "",
            on_change: Optional[Callable[[str], None]] = None,
            width: int = 500,
    ):

        super().__init__(parent, fg_color="transparent")
        self.on_change = on_change

        self.label = ctk.CTkLabel(self, text=label_text, font=("Arial", 14))

        self.entry = ctk.CTkEntry(
            self,
            placeholder_text="Choose folder...",
            width=width - 100 # Leave space for the button
        )
        if default_path:
            self.entry.insert(0, default_path)

        self.browse_button = ctk.CTkButton(
            self,
            text="Browse...",
            width=80,
            command=self._select_folder
        )

        # Arrange widgets horizontally using pack
        self.label.pack(side="left", padx=(0, 10))
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.browse_button.pack(side="left")

        # Bind events for manual input (Enter key or focus loss)
        self.entry.bind("<Return>", self._on_entry_change)
        self.entry.bind("<FocusOut>", self._on_entry_change)

    """
    Open system folder dialog and update the entry with selected path.
    """
    def _select_folder(self) -> None:
        current = self.entry.get()

        # Use current path if valid, otherwise default to user's home directory
        initial_dir = current if current and Path(current).exists() else str(Path.home())

        folder = ctk.filedialog.askdirectory(
            title="Select download folder",
            initialdir=initial_dir
        )
        if folder:
            self.entry.delete(0, "end")
            self.entry.insert(0, folder)
            self._trigger_change(folder)

    """
    Handle manual path input (via Enter or focus loss).
    """
    def _on_entry_change(self) -> None:
        path = self.entry.get().strip()
        if path:
            self._trigger_change(path)

    """
    Call the on_change callback if it exists.
    """
    def _trigger_change(self, path: str) -> None:
        if self.on_change:
            self.on_change(path)

    """
    Return the current folder path from the entry field.
    """
    def get_path(self) -> str:
        value = self.entry.get()
        return cast(str, value).strip()

    """
    Set the folder path and trigger callback.
    """
    def set_path(self, path: str) -> None:
        self.entry.delete(0, "end")
        self.entry.insert(0, path)
        self._trigger_change(path)