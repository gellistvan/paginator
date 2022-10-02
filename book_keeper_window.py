import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import winsound


class BookKeeperWindow(tk.Tk):
    _book_path_entry: ttk.Entry
    _book_path_browse_button: ttk.Button
    _dictionary_path_entry: ttk.Entry
    _dictionary_book_path_browse_button: ttk.Button

    _find_names_check_button: ttk.Checkbutton
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

    _process_button: ttk.Button

    def __init__(self):
        super().__init__()

        self.title("Book keeper")
        self.geometry("450x650")
        self.resizable(False, False)
        self.iconbitmap("assets/icons/icons8-audio-book-50.ico")

        self._init_source_frame()
        self._init_config_frame()
        self._init_design_frame()
        self._init_output_frame()

        # progress_bar = ttk.Progressbar(
        #     self,
        #     orient='horizontal',
        #     mode='indeterminate'
        # )
        # progress_bar.pack(fill='x', expand=True, padx=10, pady=10)

        self._process_button = ttk.Button(self, text="Process", command=self.process_button_pressed)
        self._process_button.pack(fill='x', expand=True, padx=10, pady=10)

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

        self._book_path_browse_button = ttk.Button(book_path_frame, text="Browse", command=lambda: self.on_browse_txt_button_pressed(book_path_frame.book_path))
        self._book_path_browse_button.pack(fill=tk.BOTH, expand=True, padx=2)

        dictionary_path_frame = ttk.Frame(source_frame)
        dictionary_path_frame.pack(padx=0, pady=0, fill='x', expand=True)

        dictionary_path_label = ttk.Label(dictionary_path_frame, text="Dictionary file path:")
        dictionary_path_label.pack(fill='x', expand=True)

        dictionary_path_frame.dictionary_path = tk.StringVar()
        self._dictionary_path_entry = ttk.Entry(dictionary_path_frame, textvariable=dictionary_path_frame.dictionary_path)
        self._dictionary_path_entry.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=2, ipady=1)

        self._dictionary_path_browse_button = ttk.Button(dictionary_path_frame, text="Browse", command=lambda: self.on_browse_txt_button_pressed(dictionary_path_frame.dictionary_path))
        self._dictionary_path_browse_button.pack(fill=tk.BOTH, expand=True, padx=2)

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

        self._cover_path_browse_button = ttk.Button(cover_path_frame, text="Browse", command=lambda: self.on_browse_png_button_pressed(cover_path_frame.cover_path))
        self._cover_path_browse_button.pack(fill=tk.BOTH, expand=True, padx=2)

        background_music_path_frame = ttk.Frame(design_frame)
        background_music_path_frame.pack(padx=0, pady=0, fill='x', expand=True)

        background_music_path_label = ttk.Label(background_music_path_frame, text="Background music path:")
        background_music_path_label.pack(fill='x', expand=True)

        background_music_path_frame.background_music_path = tk.StringVar()
        self._background_music_path_entry = ttk.Entry(background_music_path_frame, textvariable=background_music_path_frame.background_music_path)
        self._background_music_path_entry.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=2, ipady=1)

        self._preview_button = ttk.Button(background_music_path_frame, text="Preview", command=self.on_preview_button_pressed)
        self._preview_button.pack(fill=tk.Y, padx=2, side=tk.LEFT)

        self._background_music_path_browse_button = ttk.Button(background_music_path_frame, text="Browse",
                                                               command=lambda: self.on_browse_mp3_button_pressed(background_music_path_frame.background_music_path))
        self._background_music_path_browse_button.pack(fill=tk.Y, padx=2, side=tk.LEFT)

        volume_frame = ttk.Frame(design_frame)
        volume_frame.pack(padx=0, pady=0, fill='x', expand=True)

        music_volume_frame = ttk.Frame(volume_frame)
        music_volume_frame.pack(padx=0, pady=0, fill='x', expand=True, side=tk.LEFT)
        music_volume_label = ttk.Label(music_volume_frame, text="Music volume:")
        music_volume_label.pack(fill='x', expand=True)
        self._music_volume_scale = ttk.Scale(music_volume_frame, from_=0, to=100, orient="horizontal")
        self._music_volume_scale.pack(fill='x', expand=True, padx=5)

        voice_volume_frame = ttk.Frame(volume_frame)
        voice_volume_frame.pack(padx=0, pady=0, fill='x', expand=True, side=tk.RIGHT)
        voice_volume_label = ttk.Label(voice_volume_frame, text="Voice volume:")
        voice_volume_label.pack(fill='x', expand=True)
        self._voice_volume_scale = ttk.Scale(voice_volume_frame, from_=0, to=100, orient="horizontal")
        self._voice_volume_scale.pack(fill='x', expand=True, padx=5)

    def _init_config_frame(self):
        config_frame = ttk.LabelFrame(self, text="Configuration")
        config_frame.pack(padx=10, pady=10, fill='both', expand=True)

        config_frame.is_find_names_checked = tk.BooleanVar(value=False)
        self._find_names_check_button = ttk.Checkbutton(config_frame, text="Find names", command=lambda: self.on_find_names_check_changed(config_frame.is_find_names_checked),
                                            variable=config_frame.is_find_names_checked, onvalue=True, offvalue=False)
        self._find_names_check_button.pack(pady=10, fill='both', expand=True)

        delimiter_sequence_frame = ttk.Frame(config_frame)
        delimiter_sequence_frame.pack(padx=0, pady=0, fill='x', expand=True)

        delimiter_sequence_label = ttk.Label(delimiter_sequence_frame, text="Delimiter sequence:")
        delimiter_sequence_label.pack(fill='x', expand=True)

        self._delimiter_sequence_entry = ttk.Entry(delimiter_sequence_frame)
        self._delimiter_sequence_entry.pack(fill='x', expand=True, padx=2, ipady=1)

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

        self._output_path_browse_button = ttk.Button(output_path_frame, text="Browse", command=lambda: self.on_browse_folder_button_pressed(output_path_frame.output_path))
        self._output_path_browse_button.pack(fill=tk.BOTH, expand=True, padx=2)

    def on_browse_txt_button_pressed(self, path: tk.StringVar):
        filetypes = (
            ("Text files: ", "*.txt"),
            ("All files: ", "*.*")
        )

        filename = filedialog.askopenfilename(filetypes=filetypes)
        path.set(filename)

    def on_browse_png_button_pressed(self, path: tk.StringVar):
        filetypes = (
            ("PNG files: ", "*.png"),
            ("All files: ", "*.*")
        )

        filename = filedialog.askopenfilename(filetypes=filetypes)
        path.set(filename)

    def on_browse_mp3_button_pressed(self, path: tk.StringVar):
        filetypes = (
            ("MP3 files: ", "*.mp3"),
            ("All files: ", "*.*")
        )

        filename = filedialog.askopenfilename(filetypes=filetypes)
        path.set(filename)

    def on_browse_folder_button_pressed(self, path: tk.StringVar):
        filename = filedialog.askdirectory()
        path.set(filename)

    def process_button_pressed(self):
        print("Process button pressed.")
        self.config(cursor="watch")
        self.disable_all_widgets(True)

        # call book_keeper here

        self.config(cursor="watch")
        self.disable_all_widgets(True)

    def on_preview_button_pressed(self):
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)

    def on_find_names_check_changed(self, is_checked: tkinter.BooleanVar):
        state = "disabled" if (is_checked.get()) else "enabled"

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

    def disable_all_widgets(self, disable: bool):
        state = "disabled" if (disable) else "enabled"

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


window = BookKeeperWindow()
window.mainloop()
