import logging

import customtkinter as ctk
from typing import List, Dict, Optional, Any

from src.core.config.flag_config import AVAILABLE_PRESETS, AVAILABLE_THUMBNAILS_FORMATS
from src.core.dataclass.subtitle import Subtitles
from src.core.exceptions.exception import FlagValidatorError
from src.core.flags.base_flag import BaseFlag
from src.core.flags.convert_thumbnails_flag import ConvertThumbnailsFlag
from src.core.flags.format_flag import FormatFlag
from src.core.flags.ignore_errors_flag import IgnoreErrorsFlag
from src.core.flags.no_overwrites_flag import NoOverwritesFlag
from src.core.flags.preset_alias_flag import PresetAliasFlag
from src.core.flags.write_subs_flag import WriteSubsFlag
from src.core.flags.sub_langs_flag import SubLangsFlag
from src.core.flags.write_thumbnail_flag import WriteThumbnailFlag
from src.core.flags.embed_thumbnail_flag import EmbedThumbnailFlag
from src.core.flags.write_link_flag import WriteLinkFlag
from src.core.utils.format_util import presets_to_dict, formats_to_dict, filter_by_unique_values
from src.view.components.scrollable_option_menu import ScrollableOptionMenu

logger = logging.getLogger("yt_dlp_gui")

"""UI panel for configuring download options (format, subtitles, thumbnail, etc.)."""
class DownloadSettingsPanel(ctk.CTkFrame):
    def __init__(self, parent: Any):
        super().__init__(parent)
        self.parent = parent
        self.formats: List[Dict[str, str]] = []
        self.subtitles: Optional[Subtitles] = None
        self.is_initialized = False

        self.title = ctk.CTkLabel(self, text="Download settings", font=("Arial", 16, "bold"))
        self.title.pack(pady=(10, 15))

        self._init_format_section()
        self._init_subtitles_section()
        self._init_thumbnail_section()
        self._init_other_options()

        logger.info("DownloadSettingsPanel initialized")

    def _init_format_section(self) -> None:
        self.format_frame = ctk.CTkFrame(self)
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

    def _init_subtitles_section(self) -> None:
        self.subtitles_frame = ctk.CTkFrame(self)
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
        self.lang_checkboxes: dict[str, ctk.CTkCheckBox] = {}

    def _init_thumbnail_section(self) -> None:
        self.thumbnail_frame = ctk.CTkFrame(self)
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
        self.thumb_format_dropdown.configure(state="disabled")
        self.thumb_format_dropdown.pack(anchor="w", padx=20, pady=(5, 10))

        self.embed_thumb_var = ctk.BooleanVar(value=False)
        self.embed_thumb_check = ctk.CTkCheckBox(
            self.thumbnail_frame,
            text="Embed thumbnail to video",
            variable=self.embed_thumb_var
        )
        self.embed_thumb_check.pack(anchor="w", padx=20, pady=(0, 10))

    def _init_other_options(self) -> None:
        # Save link
        self.write_link_var = ctk.BooleanVar(value=False)
        self.write_link_check = ctk.CTkCheckBox(
            self,
            text="Save link to video",
            variable=self.write_link_var
        )
        self.write_link_check.pack(pady=(10, 20), padx=10, anchor="w")

        # Ignore errors
        self.ignore_errors_var = ctk.BooleanVar(value=True)
        self.ignore_errors_check = ctk.CTkCheckBox(
            self,
            text="Continue downloading while errors",
            variable=self.ignore_errors_var
        )
        self.ignore_errors_check.pack(anchor="w", padx=10, pady=(0, 10))

        # No overwrite
        self.no_overwrite_files_var = ctk.BooleanVar(value=False)
        self.no_overwrite_files_check = ctk.CTkCheckBox(
            self,
            text="Do not overwrite files",
            variable=self.no_overwrite_files_var
        )
        self.no_overwrite_files_check.pack(anchor="w", padx=10, pady=(0, 10))

    """Update available formats and subtitles languages"""
    def update_video_info(self, formats: List[Dict[str, str]], subtitles: Subtitles) -> None:
        self.formats = formats
        self.subtitles = subtitles

        self.format_dropdown.configure(values=filter_by_unique_values(formats_to_dict(formats)))

        self._update_subtitles_langs()

        self.is_initialized = True

    """Update checkboxes subtitles languages"""
    def _update_subtitles_langs(self) -> None:
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

    """Toggle between preset and manual format selection."""
    def _on_preset_toggle(self) -> None:
        if self.use_preset_var.get():
            self.preset_dropdown.configure(state="normal")
            self.format_dropdown.configure(state="disabled")
        else:
            self.format_dropdown.configure(state="normal")
            self.preset_dropdown.configure(state="disabled")

    """Show/hide language checkboxes."""
    def _on_subs_toggle(self) -> None:
        if self.write_subs_var.get():
            self.lang_frame.pack(anchor="w", padx=20, pady=(5, 10), fill="x")
        else:
            self.lang_frame.pack_forget()

    """Enable/disable thumbnail format dropdown."""
    def _on_thumb_toggle(self) -> None:
        if self.write_thumb_var.get():
            self.thumb_format_dropdown.configure(state="normal")
        else:
            self.thumb_format_dropdown.configure(state="disabled")

    """Generate yt-dlp flags based on current UI state."""
    def get_flags(self) -> list[BaseFlag]:

        flags: list[BaseFlag] = []
        flag = self._get_format_flag()

        if flag is not None:
            flags.append(flag)

        flags.extend(self._get_subs_flag())

        # Thumbnails
        if self.write_thumb_var.get():
            try:
                flags.append(WriteThumbnailFlag())
                flags.append(ConvertThumbnailsFlag(self.thumb_format_var.get()))
            except FlagValidatorError:
                logger.error("DownloadSettingsPanel. Thumbnails flag validation failed")


        # Embed thumbnail
        if self.embed_thumb_var.get():
            try:
                flags.append(EmbedThumbnailFlag())
            except FlagValidatorError:
                logger.error("DownloadSettingsPanel. Embed thumbnail flag validation failed")

        # Save link
        if self.write_link_var.get():
            try:
                flags.append(WriteLinkFlag())
            except FlagValidatorError:
                logger.error("DownloadSettingsPanel. Link flag validation failed")

        # Ignore errors
        if self.ignore_errors_var.get():
            try:
                flags.append(IgnoreErrorsFlag())
            except FlagValidatorError:
                logger.error("DownloadSettingsPanel. Ignore error flag validation failed")

        # No overwrite files
        if self.no_overwrite_files_var.get():
            try:
                flags.append(NoOverwritesFlag())
            except FlagValidatorError:
                logger.error("DownloadSettingsPanel. No overwrites flag validation failed")

        return flags

    """Return format-related flag based on user selection."""
    def _get_format_flag(self) -> BaseFlag | None:
        if self.use_preset_var.get():
            try:
                return PresetAliasFlag(self.preset_dropdown.get())
            except FlagValidatorError:
                logger.error("DownloadSettingsPanel. Preset alias flag validation failed")
        else:
            try:
                return FormatFlag(self.format_dropdown.get())
            except FlagValidatorError:
                logger.error("DownloadSettingsPanel. Format flag validation failed")
        return None

    """Return subtitle-related flags."""
    def _get_subs_flag(self) -> list[BaseFlag]:
        flags:list[BaseFlag] = []
        if self.write_subs_var.get():
            try:
                flags.append(WriteSubsFlag())
            except FlagValidatorError:
                logger.error("DownloadSettingsPanel. WriteSubs flag validation failed")
            selected_langs = []
            for lang, checkbox in self.lang_checkboxes.items():
                var = checkbox.cget("variable")
                if var.get():
                    selected_langs.append(lang)
            if selected_langs:
                try:
                    flags.append(SubLangsFlag(selected_langs))
                except FlagValidatorError:
                    logger.error("DownloadSettingsPanel. Selected languages flag validation failed")

        return flags