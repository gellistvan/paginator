from book_keeper import BookKeeper

from tktooltip import ToolTip

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import winsound
from pathlib import Path
from threading import Thread
from typing import Callable


class BookKeeperWindow(tk.Tk):
    _book_path_entry: ttk.Entry
    _book_path_browse_button: ttk.Button
    _dictionary_path_entry: ttk.Entry
    _dictionary_book_path_browse_button: ttk.Button
    _estimation_label: ttk.Label

    _find_names_check_button: ttk.Checkbutton
    _sleep_check_button: ttk.Checkbutton
    _is_find_names_checked: tk.StringVar
    _is_sleep_checked: tk.StringVar
    _music_volume_scale: ttk.Scale
    _voice_volume_scale: ttk.Scale
    _delimiter_sequence_entry: ttk.Entry

    _cover_path_entry: ttk.Entry
    _cover_path_browse_button: ttk.Button
    _background_music_path_entry: ttk.Entry
    _background_music_path_browse_button: ttk.Button
    _preview_button: ttk.Button

    _output_path_entry: ttk.Entry
    _output_path_browse_button: ttk.Button

    _progress_bar: ttk.Progressbar
    _progress_percentage_label: ttk.Label
    _progress_state_label: ttk.Label
    _process_button: ttk.Button
    _stop_button: ttk.Button
    _about_button: ttk.Button

    _is_processing: bool
    _is_stop_processing_requested: bool
    _is_exit_requested: bool
    _kill_video_chapter_generating_process: Callable = None

    _APP_NAME = "Book Keeper"
    _APP_VERSION = "1.0"

    _filedialog_types = {
        "text": (("Text files: ", "*.txt"), ("All files: ", "*.*")),
        "picture": (("PNG files: ", "*.png"), ("All files: ", "*.*")),
        "audio": (("MP3 files: ", "*.mp3"), ("All files: ", "*.*"))
    }

    def __init__(self):
        super().__init__()

        self._is_processing = self._is_stop_processing_requested = self._is_exit_requested = False

        self.title(self._APP_NAME)
        self.geometry("450x640")
        self.resizable(False, False)
        self.iconbitmap("assets/icons/icons8-audio-book-50.ico")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self._init_source_frame()
        self._init_config_frame()
        self._init_design_frame()
        self._init_output_frame()
        self._init_process_control_frame()

        self.show_estimation()

    def _init_source_frame(self):
        source_frame = ttk.LabelFrame(self, text="Source")
        source_frame.pack(padx=10, pady=10, fill='both', expand=True)

        book_path_frame = ttk.Frame(source_frame)
        book_path_frame.pack(padx=0, pady=0, fill='x', expand=True)

        book_path_label = ttk.Label(book_path_frame, text="Book file path:")
        book_path_label.pack(fill='x', expand=True)

        book_path_frame.book_path = tk.StringVar()
        self._book_path_entry = ttk.Entry(book_path_frame, textvariable=book_path_frame.book_path)
        self._book_path_entry.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=2, ipady=1)
        self._book_path_entry.bind("<FocusOut>", self.show_estimation)

        self._book_path_browse_button = ttk.Button(book_path_frame, text="Browse...",
                                                   command=lambda: self.on_file_browser_button_pressed("text", book_path_frame.book_path, self._book_path_entry))
        self._book_path_browse_button.pack(fill=tk.BOTH, expand=True, padx=2)

        dictionary_path_frame = ttk.Frame(source_frame)
        dictionary_path_frame.pack(padx=0, pady=0, fill='x', expand=True)

        dictionary_path_label = ttk.Label(dictionary_path_frame, text="Dictionary file path:")
        dictionary_path_label.pack(fill='x', expand=True)

        dictionary_path_frame.dictionary_path = tk.StringVar()
        self._dictionary_path_entry = ttk.Entry(dictionary_path_frame, textvariable=dictionary_path_frame.dictionary_path)
        self._dictionary_path_entry.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=2, ipady=1)

        self._dictionary_path_browse_button = ttk.Button(dictionary_path_frame, text="Browse...",
                                                         command=lambda: self.on_file_browser_button_pressed("text", dictionary_path_frame.dictionary_path, self._dictionary_path_entry))
        self._dictionary_path_browse_button.pack(fill=tk.BOTH, expand=True, padx=2)

        self._estimation_label = ttk.Label(source_frame)
        self._estimation_label.pack(fill='x', expand=True, pady=5)

    def _init_config_frame(self):
        config_frame = ttk.LabelFrame(self, text="Configuration")
        config_frame.pack(padx=10, pady=10, fill='both', expand=True)

        checkbox_frame = ttk.Frame(config_frame)
        checkbox_frame.pack(padx=0, pady=5, fill='x', expand=True)

        self._is_find_names_checked = tk.StringVar(checkbox_frame, "off")
        self._find_names_check_button = ttk.Checkbutton(checkbox_frame, text="Find names", variable=self._is_find_names_checked, onvalue="on", offvalue="off")
        self._find_names_check_button.pack(fill='x', expand=True, side=tk.LEFT)

        self._is_sleep_checked = tk.StringVar()
        self._sleep_check_button = ttk.Checkbutton(checkbox_frame, text="Put computer to sleep", variable=self._is_sleep_checked, onvalue="on", offvalue="off")
        self._sleep_check_button.pack(fill='x', expand=True, side=tk.RIGHT)

        delimiter_sequence_frame = ttk.Frame(config_frame)
        delimiter_sequence_frame.pack(fill='x', expand=True)

        delimiter_sequence_label = ttk.Label(delimiter_sequence_frame, text="Delimiter sequence:")
        delimiter_sequence_label.pack(fill='x', expand=True)

        self._delimiter_sequence_entry = ttk.Entry(delimiter_sequence_frame)
        self._delimiter_sequence_entry.pack(padx=2, ipady=1, side=tk.LEFT)

    def _init_design_frame(self):
        design_frame = ttk.LabelFrame(self, text="Design")
        design_frame.pack(padx=10, pady=10, fill='both', expand=True)

        cover_path_frame = ttk.Frame(design_frame)
        cover_path_frame.pack(padx=0, pady=0, fill='x', expand=True)

        cover_path_label = ttk.Label(cover_path_frame, text="Cover image path:")
        cover_path_label.pack(fill='x', expand=True)

        cover_path_frame.cover_path = tk.StringVar()
        self._cover_path_entry = ttk.Entry(cover_path_frame, textvariable=cover_path_frame.cover_path)
        self._cover_path_entry.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=2, ipady=1)

        self._cover_path_browse_button = ttk.Button(cover_path_frame, text="Browse...",
                                                    command=lambda: self.on_file_browser_button_pressed("picture", cover_path_frame.cover_path, self._cover_path_entry))
        self._cover_path_browse_button.pack(fill=tk.BOTH, expand=True, padx=2)

        background_music_path_frame = ttk.Frame(design_frame)
        background_music_path_frame.pack(padx=0, pady=0, fill='x', expand=True)

        background_music_path_label = ttk.Label(background_music_path_frame, text="Background music path:")
        background_music_path_label.pack(fill='x', expand=True)

        background_music_path_frame.background_music_path = tk.StringVar()
        self._background_music_path_entry = ttk.Entry(background_music_path_frame, textvariable=background_music_path_frame.background_music_path)
        self._background_music_path_entry.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=2, ipady=1)

        self._background_music_path_browse_button\
            = ttk.Button(background_music_path_frame, text="Browse...",
                         command=lambda: self.on_file_browser_button_pressed("audio", background_music_path_frame.background_music_path, self._background_music_path_entry))
        self._background_music_path_browse_button.pack(fill=tk.Y, padx=2, side=tk.LEFT)

        self._preview_button = ttk.Button(background_music_path_frame, text="▶ Preview", command=self.on_preview_button_pressed)
        self._preview_button.pack(fill=tk.Y, padx=2, side=tk.LEFT)

        volume_frame = ttk.Frame(design_frame)
        volume_frame.pack(padx=0, pady=0, fill='x', expand=True)
        VOL_FORMAT = '{: .2f}'

        music_volume_frame = ttk.Frame(volume_frame)
        music_volume_frame.pack(padx=0, pady=0, fill='x', expand=True, side=tk.LEFT)
        music_volume_label = ttk.Label(music_volume_frame, text="Music volume:")
        music_volume_label.pack(fill='x', expand=True)
        self._music_volume_scale = ttk.Scale(music_volume_frame, from_=0, to=1, orient="horizontal")
        self._music_volume_scale.pack(fill='x', expand=True, padx=5)
        ToolTip(self._music_volume_scale, msg=lambda: VOL_FORMAT.format(self._music_volume_scale.get()))
        self._music_volume_scale.bind("<MouseWheel>", lambda event: self.on_mouse_wheel_scrolled_within_volume_scale(event, self._music_volume_scale))

        voice_volume_frame = ttk.Frame(volume_frame)
        voice_volume_frame.pack(padx=0, pady=0, fill='x', expand=True, side=tk.RIGHT)
        voice_volume_label = ttk.Label(voice_volume_frame, text="Voice volume:")
        voice_volume_label.pack(fill='x', expand=True)
        self._voice_volume_scale = ttk.Scale(voice_volume_frame, from_=0, to=5, orient="horizontal")
        self._voice_volume_scale.pack(fill='x', expand=True, padx=5)
        ToolTip(self._voice_volume_scale, msg=lambda: VOL_FORMAT.format(self._voice_volume_scale.get()))
        self._voice_volume_scale.bind("<MouseWheel>", lambda event: self.on_mouse_wheel_scrolled_within_volume_scale(event, self._voice_volume_scale))

    def _init_output_frame(self):
        output_frame = ttk.LabelFrame(self, text="Output")
        output_frame.pack(padx=10, pady=10, fill='both', expand=True)

        output_path_frame = ttk.Frame(output_frame)
        output_path_frame.pack(fill='x', expand=True)

        output_path_label = ttk.Label(output_path_frame, text="Save to:")
        output_path_label.pack(fill='x', expand=True)

        output_path_frame.output_path = tk.StringVar()
        self._output_path_entry = ttk.Entry(output_path_frame, textvariable=output_path_frame.output_path)
        self._output_path_entry.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=2, ipady=1)

        self._output_path_browse_button = ttk.Button(output_path_frame, text="Browse...",
                                                     command=lambda: self.on_folder_browser_button_pressed(output_path_frame.output_path, self._output_path_entry))
        self._output_path_browse_button.pack(fill=tk.BOTH, expand=True, padx=2)

    def _init_process_control_frame(self):
        progress_bar_frame = ttk.Frame(self)
        progress_bar_frame.pack(padx=5, pady=10, fill='x', expand=True)

        self._progress_bar = ttk.Progressbar(
            progress_bar_frame,
            orient='horizontal',
            mode='determinate'
        )
        self._progress_bar.pack(fill=tk.X, expand=True, padx=2, ipady=1)

        self._progress_percentage_label = ttk.Label(progress_bar_frame, text="")
        self._progress_percentage_label.pack(fill=tk.X, padx=2, side=tk.RIGHT)

        self._progress_state_label = ttk.Label(progress_bar_frame, text="")
        self._progress_state_label.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        process_control_frame = ttk.Frame(self)
        process_control_frame.pack(padx=5, pady=5, fill='x', expand=True)

        self._stop_button = ttk.Button(process_control_frame, text="Stop", command=self.on_stop_button_pressed)
        self._stop_button.pack(fill=tk.Y, padx=4, side=tk.RIGHT)
        self._stop_button.config(state="disabled")

        self._process_button = ttk.Button(process_control_frame, text="Process", command=self.on_process_button_pressed)
        self._process_button.pack(fill=tk.Y, padx=4, side=tk.RIGHT)

        def show_about_window():
            MSG = self._APP_NAME + "\n\nVersion: " + self._APP_VERSION + "\nAuthors: István Gellai, Olivér Megyeri"
            tk.messagebox.showinfo("About " + self._APP_NAME, MSG)
        self._about_button = ttk.Button(process_control_frame, text="About", command=show_about_window)
        self._about_button.pack(fill=tk.Y, padx=4, side=tk.LEFT)

    def on_file_browser_button_pressed(self, file_type: str, path: tk.StringVar, entry: ttk.Entry):
        filename = filedialog.askopenfilename(filetypes=self._filedialog_types[file_type])
        path.set(filename)
        entry.xview_moveto(1)

        if file_type == "text":
            self.show_estimation()

    @staticmethod
    def on_folder_browser_button_pressed(path: tk.StringVar, entry: ttk.Entry):
        filename = filedialog.askdirectory()
        path.set(filename)
        entry.xview_moveto(1)

    @staticmethod
    def on_mouse_wheel_scrolled_within_volume_scale(event, vol_scale):
        SCROLL_DELTA = event.delta / 120
        STEP = abs(vol_scale.cget("to") - vol_scale.cget("from")) / 5

        if SCROLL_DELTA > 0:
            if vol_scale.get() + STEP > vol_scale.cget("to"):
                vol_scale.set(vol_scale.cget("to"))
            else:
                vol_scale.set(vol_scale.get() + STEP)
        else:
            if vol_scale.get() - STEP < vol_scale.cget("from"):
                vol_scale.set(vol_scale.cget("from"))
            else:
                vol_scale.set(vol_scale.get() - STEP)

    def on_preview_button_pressed(self):
        book_keeper = BookKeeper()
        book_keeper.background_music = ""
        if Path(self._background_music_path_entry.get()).is_file():
            book_keeper.background_music = self._background_music_path_entry.get()
            book_keeper.music_weight = str(self._voice_volume_scale.get()) + ' ' + str(self._music_volume_scale.get())

        try:
            preview_path = book_keeper.GeneratePreview()
            winsound.PlaySound(preview_path, winsound.SND_ASYNC)
        except Exception as e:
            tk.messagebox.showerror(self._APP_NAME, str(e))

    def on_close(self):
        if self._is_processing:
            self._is_exit_requested = True
            self.on_stop_button_pressed()
        else:
            self.destroy()

    def on_stop_button_pressed(self):
        self._is_stop_processing_requested = True
        if self._kill_video_chapter_generating_process:
            self._kill_video_chapter_generating_process()

        self._progress_state_label.config(text="Stopping...")
        self._progress_percentage_label.config(text="")
        self._progress_bar.config(mode="indeterminate")
        self._progress_bar.start()

    def on_process_button_pressed(self):
        book_keeper = BookKeeper()
        book_keeper.set_progress_bar_callback = self.set_progress_bar
        book_keeper.is_stop_progressing_requested_callback = self.is_stop_processing_requested
        book_keeper.input_path = self._book_path_entry.get()
        book_keeper.image_path = self._cover_path_entry.get()
        book_keeper.collect_names = (self._is_find_names_checked.get() == "on")
        book_keeper.trigger_sleep = (self._is_sleep_checked.get() == "on")
        book_keeper.music_weight = str(self._voice_volume_scale.get()) + ' ' + str(
            self._music_volume_scale.get())
        if self._output_path_entry.get():
            book_keeper.output_path = self._output_path_entry.get()
        if self._background_music_path_entry.get():
            book_keeper.background_music = self._background_music_path_entry.get().replace(".mp3", "")
        if self._dictionary_path_entry.get():
            book_keeper.dictionary_path = self._dictionary_path_entry.get()
        if self._delimiter_sequence_entry.get():
            book_keeper.chapter_delimiter = self._delimiter_sequence_entry.get()

        process_thread = Thread(target=lambda: self.process(book_keeper))
        process_thread.start()

    def process(self, bk: BookKeeper):
        self.disable_widgets_for_processing(True)
        self._stop_button.config(state="enabled")
        self.set_progress_bar(0, 0)
        self._progress_state_label.config(text="Processing...")
        self._is_processing = True
        self._kill_video_chapter_generating_process = bk.KillVideoGeneratingProcess

        try:
            bk.Execute()

            self._progress_state_label.config(text="")
            self._stop_button.config(state="disabled")
            if self._is_stop_processing_requested:
                self._progress_bar.stop()
                self._progress_bar.config(mode="determinate")
                tk.messagebox.showinfo(self._APP_NAME, "Process aborted.")
            else:
                tk.messagebox.showinfo(self._APP_NAME, ("Dictionary" if (self._is_find_names_checked.get() == "on") else "Video") + " generated successfully.")
        except Exception as e:
            self._progress_state_label.config(text="")
            self._progress_percentage_label.config(text="")
            self._stop_button.config(state="disabled")
            tk.messagebox.showerror(self._APP_NAME, str(e))

        self.set_progress_bar(0, 0)
        self._progress_percentage_label.config(text="")
        self._progress_state_label.config(text="")
        self.disable_widgets_for_processing(False)

        self._is_processing = self._is_stop_processing_requested = self._is_exit_requested = False
        self._kill_video_chapter_generating_process = None

    def is_stop_processing_requested(self):
        return self._is_stop_processing_requested

    def set_progress_bar(self, progress: float, time_remaining: float):
        if progress > 5:
            hours = int(time_remaining / 3600)
            minutes = int ((time_remaining - hours * 3600)/60)
            seconds = int(time_remaining - hours * 3600 - minutes * 60)
            time_string = "{hours:02d}:{minutes:02d}:{seconds:02d}".format(hours = hours, minutes = minutes, seconds = seconds)
            self._progress_state_label.config(text=time_string)

        if not self._is_stop_processing_requested:
            self._progress_bar["value"] = progress
            self._progress_percentage_label.config(text=str(int(progress)) + "%")

    def disable_widgets_for_processing(self, disable: bool):
        state = "disabled" if disable else "enabled"

        self._book_path_entry.config(state=state)
        self._book_path_browse_button.config(state=state)
        self._find_names_check_button.config(state=state)
        self._dictionary_path_entry.config(state=state)
        self._dictionary_path_browse_button.config(state=state)
        self._music_volume_scale.config(state=state)
        self._voice_volume_scale.config(state=state)
        self._delimiter_sequence_entry.config(state=state)
        self._cover_path_entry.config(state=state)
        self._cover_path_browse_button.config(state=state)
        self._background_music_path_entry.config(state=state)
        self._preview_button.config(state=state)
        self._background_music_path_browse_button.config(state=state)
        self._output_path_entry.config(state=state)
        self._output_path_browse_button.config(state=state)
        self._process_button.config(state=state)
        self._about_button.config(state=state)

    def show_estimation(self, event=None):
        label_text = "Estimated video length and size: "

        if self._book_path_entry.get() != "" and Path(self._book_path_entry.get()).is_file():
            book_keeper = BookKeeper()
            book_keeper.input_path = self._book_path_entry.get()
            book_keeper_estimation = book_keeper.Estimate()
            label_text = label_text + book_keeper_estimation[0] + " / " + book_keeper_estimation[1]
        else:
            label_text = label_text + "n/a"

        self._estimation_label.config(text=label_text)


window = BookKeeperWindow()
window.mainloop()
