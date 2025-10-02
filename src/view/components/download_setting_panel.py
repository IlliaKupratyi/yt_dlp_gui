import customtkinter as ctk
from typing import List, Dict, Optional

from src.core.config.config import AVAILABLE_PRESETS, AVAILABLE_THUMBNAILS_FORMATS
from src.core.dataclass.subtitle import Subtitles
from src.core.flags.base_flag import BaseFlag
from src.core.flags.convert_thumbnails_flag import ConvertThumbnailsFlag
from src.core.flags.format_flag import FormatFlag
from src.core.flags.preset_alias_flag import PresetAliasFlag
from src.core.flags.write_subs_flag import WriteSubsFlag
from src.core.flags.sub_langs_flag import SubLangsFlag
from src.core.flags.write_thumbnail_flag import WriteThumbnailFlag
from src.core.flags.embed_thumbnail_flag import EmbedThumbnailFlag
from src.core.flags.write_link_flag import WriteLinkFlag
from src.utils.format_lister import presets_to_dict, formats_to_dict
from src.view.components.scrollable_option_menu import ScrollableOptionMenu


class DownloadSettingsPanel(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTk):
        super().__init__(parent)
        self.parent = parent
        self.formats: List[Dict[str, str]] = []
        self.subtitles: Optional[Subtitles] = None
        self.is_initialized = False

        self.scrollable = ctk.CTkScrollableFrame(self, width=600, height=400)
        self.scrollable.pack(fill="both", expand=True, padx=10, pady=10)

        self.title = ctk.CTkLabel(self.scrollable, text="Download settings", font=("Arial", 16, "bold"))
        self.title.pack(pady=(10, 15))

        # === 1. Formats ===
        self.format_frame = ctk.CTkFrame(self.scrollable)
        self.format_frame.pack(pady=5, padx=10, fill="x")

        ctk.CTkLabel(self.format_frame, text="Format:", font=("Arial", 12)).grid(
                    row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 10))

        self.presets = presets_to_dict(AVAILABLE_PRESETS)

        self.use_preset_var = ctk.BooleanVar(value=True)
        self.preset_radio = ctk.CTkRadioButton(
            self.format_frame,
            text="Use preset",
            variable=self.use_preset_var,
            value=True,
            command=self._on_preset_toggle
        )

        self.preset_radio.grid(row=1, column=0, sticky="w", padx=10, pady=(5, 10))

        self.use_format_var = ctk.BooleanVar(value=False)
        self.format_radio = ctk.CTkRadioButton(
            self.format_frame,
            text="Choose from formats list",
            variable=self.use_preset_var,
            value=False,
            command=self._on_preset_toggle
        )
        self.format_radio.grid(row=2, column=0, sticky="w", padx=10, pady=(5, 10))

        self.preset_dropdown = ScrollableOptionMenu(
            self.format_frame,
            values=list(self.presets),
            width=250
        )
        self.preset_dropdown.grid(row=1, column=1, sticky="w", padx=10, pady=(5, 10))

        self.format_dropdown = ScrollableOptionMenu(
            self.format_frame,
            width=250,
            values=[]
        )
        self.format_dropdown.configure(state="disabled")
        self.format_dropdown.grid(row=2, column=1, sticky="w", padx=10, pady=(5, 10))

        # === 2. Subtitles ===
        self.subtitles_frame = ctk.CTkFrame(self.scrollable)
        self.subtitles_frame.pack(pady=5, padx=10, fill="x")

        self.write_subs_var = ctk.BooleanVar(value=False)
        self.write_subs_check = ctk.CTkCheckBox(
            self.subtitles_frame,
            text="Download subtitles",
            variable=self.write_subs_var,
            command=self._on_subs_toggle
        )
        self.write_subs_check.pack(anchor="w", padx=10, pady=(5, 0))

        self.lang_frame = ctk.CTkFrame(self.subtitles_frame)
        self.lang_frame.pack(anchor="w", padx=20, pady=(5, 10), fill="x")
        self.lang_checkboxes = {}

        # === 3. Thumbnails ===
        self.thumbnail_frame = ctk.CTkFrame(self.scrollable)
        self.thumbnail_frame.pack(pady=5, padx=10, fill="x")

        self.write_thumb_var = ctk.BooleanVar(value=False)
        self.write_thumb_check = ctk.CTkCheckBox(
            self.thumbnail_frame,
            text="Download thumbnail",
            variable=self.write_thumb_var,
            command=self._on_thumb_toggle
        )
        self.write_thumb_check.pack(anchor="w", padx=10, pady=(5, 0))

        self.thumb_format_var = ctk.StringVar(value="jpg")
        self.thumb_format_dropdown = ctk.CTkOptionMenu(
            self.thumbnail_frame,
            values=AVAILABLE_THUMBNAILS_FORMATS,
            variable=self.thumb_format_var,
            width=120,
            state="normal"
        )
        self.thumb_format_dropdown.pack(anchor="w", padx=20, pady=(5, 10))

        self.embed_thumb_var = ctk.BooleanVar(value=False)
        self.embed_thumb_check = ctk.CTkCheckBox(
            self.thumbnail_frame,
            text="Embed thumbnail to video",
            variable=self.embed_thumb_var
        )
        self.embed_thumb_check.pack(anchor="w", padx=20, pady=(0, 10))

        # === 4. Save link ===
        self.write_link_var = ctk.BooleanVar(value=False)
        self.write_link_check = ctk.CTkCheckBox(
            self.scrollable,
            text="Save link to video",
            variable=self.write_link_var
        )
        self.write_link_check.pack(pady=(10, 20), padx=10, anchor="w")

    """Update available formats and subtitles languages"""
    def update_video_info(self, formats: List[Dict[str, str]], subtitles: Subtitles):
        self.formats = formats
        self.subtitles = subtitles

        self.format_dropdown.configure(values=formats_to_dict(formats))

        self._update_subtitles_langs()

        self.is_initialized = True

    """Update checkboxes subtitles languages"""
    def _update_subtitles_langs(self):
        for widget in self.lang_checkboxes.values():
            widget.destroy()
        self.lang_checkboxes.clear()

        all_langs = set()
        if self.subtitles:
            for sub in self.subtitles.subtitles:
                all_langs.add(sub["Language"])

        for lang in sorted(all_langs):
            var = ctk.BooleanVar(value=False)
            cb = ctk.CTkCheckBox(self.lang_frame, text=lang, variable=var)
            cb.pack(anchor="w", pady=1)
            self.lang_checkboxes[lang] = cb

        if len(self.lang_checkboxes) == 0:
            self.lang_frame.pack_forget()
            self.write_subs_check.configure(text="Download subtitles (no available)")
            self.write_subs_var.set(False)
            self.write_subs_check.configure(state="disabled")
        else:
            self.lang_frame.pack(anchor="w", padx=20, pady=(5, 10), fill="x")
            self.write_subs_check.configure(text="Download subtitles")
            self.write_subs_check.configure(state="normal")

    def _on_preset_toggle(self):
        if self.use_preset_var.get():
            self.preset_dropdown.configure(state="normal")
            self.format_dropdown.configure(state="disabled")
        else:
            self.format_dropdown.configure(state="normal")
            self.preset_dropdown.configure(state="disabled")

    def _on_subs_toggle(self):
        if self.write_subs_var.get():
            self.lang_frame.pack(anchor="w", padx=20, pady=(5, 10), fill="x")
        else:
            self.lang_frame.pack_forget()

    def _on_thumb_toggle(self):
        if self.write_thumb_var.get():
            self.thumb_format_dropdown.configure(state="normal")
        else:
            self.thumb_format_dropdown.configure(state="disabled")

    def get_flags(self) -> list[BaseFlag]:
        flags:list[BaseFlag] = [self._get_format_flag()]

        flags.extend(self._get_subs_flag())

        # Thumbnails
        if self.write_thumb_var.get():
            flags.append(WriteThumbnailFlag())
            flags.append(ConvertThumbnailsFlag(self.thumb_format_var.get()))

        # Embed thumbnail
        if self.embed_thumb_var.get():
            flags.append(EmbedThumbnailFlag())

        # Save link
        if self.write_link_var.get():
            flags.append(WriteLinkFlag())

        return flags

    def _get_format_flag(self) -> BaseFlag:
        if self.use_preset_var.get():
            return PresetAliasFlag(self.preset_dropdown.get())
        else:
            return FormatFlag(self.format_dropdown.get())

    def _get_subs_flag(self) -> list[BaseFlag]:
        flags:list[BaseFlag] = []
        if self.write_subs_var.get():
            flags.append(WriteSubsFlag())
            selected_langs = [lang for lang, var in self.lang_checkboxes.items() if var.get()]
            if selected_langs:
                flags.append(SubLangsFlag(selected_langs))

        return flags