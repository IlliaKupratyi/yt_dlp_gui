"""
Scrollable dropdown menu with custom items.
"""
from functools import partial
from typing import Optional, Callable, Any

import customtkinter as ctk

class ScrollableOptionMenu(ctk.CTkFrame):
    """Class for scrollable dropdown menu with custom items."""
    def __init__(self,
                 parent: Any, values:list[dict[str, str]],
                 command: Optional[Callable[[str], None]] = None,
                 width:int = 200,
                 height:int = 30):
        super().__init__(parent)
        self.values = values or []
        self.command = command
        self.selected_value:dict[str, str] = self.values[0] if len(self.values) > 0 else {}
        self.is_active = False

        # Main button to toggle the menu
        self.button = ctk.CTkButton(
            self,
            text= self.selected_value['value'] if self.selected_value else "Select...",
            width=width,
            height=height,
            command=self._on_click
        )
        self.button.pack()
        self.menu_window = None

    def _on_click(self) -> None:
        """Scrollable dropdown menu with custom items."""
        if not self.is_active:
            self.is_active = True
            self._open_menu()
        else:
            self.is_active = False
            if self.menu_window:
                self.menu_window.destroy()

    def _open_menu(self) -> None:
        """Create and show the dropdown menu."""
        if self.menu_window and self.menu_window.winfo_exists():
            self.menu_window.destroy()

        # Create toplevel window safely
        try:
            root = self.winfo_toplevel()
            if root and root.winfo_exists():
                self.menu_window = ctk.CTkToplevel(root)
            else:
                self.menu_window = ctk.CTkToplevel()
        except (RuntimeError, OSError, ValueError):
            self.menu_window = ctk.CTkToplevel()

        if self.menu_window is None:
            raise RuntimeError("Failed to create CTkToplevel window")

        # Configure window as popup
        self.menu_window.wm_overrideredirect(True)
        self.menu_window.wm_geometry(f"+{self.winfo_rootx()}+{self.winfo_rooty() + 30}")
        self.menu_window.wm_attributes("-topmost", True)

        # Add scrollable frame with buttons
        scroll_frame = ctk.CTkScrollableFrame(self.menu_window, width=250)
        scroll_frame.pack()

        btn_height = 30
        for fmt in self.values:
            display_text = fmt["value"]

            btn = ctk.CTkButton(
                scroll_frame,
                text=display_text,
                command=partial(self._select, fmt)
            )
            btn.pack(pady=2, padx=5, fill="x")
            btn.update_idletasks()
            btn_height = btn.winfo_height()

        # Adjust window height based on content
        height = 200
        if len(self.values) * btn_height < 200:
            height = len(self.values) * btn_height
        if self.menu_window:
            self.menu_window.geometry(f"{250}x{height}")
        scroll_frame.configure(height=height)

    def _select(self, value:dict[str, str]) -> None:
        """Create and show the dropdown menu."""
        self.selected_value = value

        display_text = value["value"]
        self.button.configure(text=display_text)

        if self.command:
            self.command(value["id"])

        if self.menu_window:
            self.menu_window.destroy()

        self.is_active = False

    def configure(self, values:Optional[list[dict[str, str]]] = None, state:str="", **_: dict[str, Any]) -> None:
        """Update menu items or button state."""
        if values:
            self.values = values
            self.selected_value = self.values[0] if self.values else {'id': '', 'value': ''}
            self.button.configure(text=self.selected_value['value'] or "Select...")
        if state == "disabled":
            self.button.configure(state="disabled")
        elif state == "normal":
            self.button.configure(state="normal")

    def get(self) -> str:
        """Return ID of selected item."""
        return self.selected_value['id']
