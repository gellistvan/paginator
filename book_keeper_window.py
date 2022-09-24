import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import winsound


class BookKeeperWindow:  # (tk.Tk())
    _book_path_entry: tk.Entry

    def __init__(self):
        root = tk.Tk()
        root.title("Book keeper")
        root.geometry("450x600")
        root.resizable(False, False)
        root.iconbitmap("assets/icons/icons8-audio-book-50.ico")

        self._init_source_frame(root)
        self._init_design_frame(root)
        self._init_config_frame(root)
        self._init_output_frame(root)

        process_button = ttk.Button(root, text="Process", command=lambda: self.process_button_pressed(root))
        process_button.pack(fill='x', expand=True, padx=10, pady=10)

        root.mainloop()

    def _init_source_frame(self, root):
        source_frame = ttk.LabelFrame(root, text="Source")
        source_frame.pack(padx=10, pady=10, fill='both', expand=True)

        book_path_frame = ttk.Frame(source_frame)
        book_path_frame.pack(padx=0, pady=0, fill='x', expand=True)

        book_path_label = ttk.Label(book_path_frame, text="Book file path:")
        book_path_label.pack(fill='x', expand=True)

        book_path_frame.book_path = tk.StringVar()
        self._book_path_entry = ttk.Entry(book_path_frame, textvariable=book_path_frame.book_path)
        self._book_path_entry.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=2, ipady=1)

        book_path_browse_button = ttk.Button(book_path_frame, text="Browse", command=lambda: self.on_browse_button_pressed(book_path_frame.book_path))
        book_path_browse_button.pack(fill=tk.BOTH, expand=True, padx=2)

        dictionary_path_frame = ttk.Frame(source_frame)
        dictionary_path_frame.pack(padx=0, pady=0, fill='x', expand=True)

        dictionary_path_label = ttk.Label(dictionary_path_frame, text="Dictionary file path:")
        dictionary_path_label.pack(fill='x', expand=True)

        dictionary_path_frame.dictionary_path = tk.StringVar()
        dictionary_path_entry = ttk.Entry(dictionary_path_frame, textvariable=dictionary_path_frame.dictionary_path)
        dictionary_path_entry.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=2, ipady=1)

        dictionary_path_browse_button = ttk.Button(dictionary_path_frame, text="Browse", command=lambda: self.on_browse_button_pressed(dictionary_path_frame.dictionary_path))
        dictionary_path_browse_button.pack(fill=tk.BOTH, expand=True, padx=2)

    def _init_design_frame(self, root):
        design_frame = ttk.LabelFrame(root, text="Design")
        design_frame.pack(padx=10, pady=10, fill='both', expand=True)

        cover_path_frame = ttk.Frame(design_frame)
        cover_path_frame.pack(padx=0, pady=0, fill='x', expand=True)

        cover_path_label = ttk.Label(cover_path_frame, text="Cover image path:")
        cover_path_label.pack(fill='x', expand=True)

        cover_path_frame.cover_path = tk.StringVar()
        cover_path_entry = ttk.Entry(cover_path_frame, textvariable=cover_path_frame.cover_path)
        cover_path_entry.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=2, ipady=1)

        cover_path_browse_button = ttk.Button(cover_path_frame, text="Browse", command=lambda: self.on_browse_button_pressed(cover_path_frame.cover_path))
        cover_path_browse_button.pack(fill=tk.BOTH, expand=True, padx=2)

        background_path_frame = ttk.Frame(design_frame)
        background_path_frame.pack(padx=0, pady=0, fill='x', expand=True)

        background_path_label = ttk.Label(background_path_frame, text="Background file path:")
        background_path_label.pack(fill='x', expand=True)

        background_path_frame.background_path = tk.StringVar()
        background_path_entry = ttk.Entry(background_path_frame, textvariable=background_path_frame.background_path)
        background_path_entry.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=2, ipady=1)

        background_path_browse_button = ttk.Button(background_path_frame, text="Browse", command=lambda: self.on_browse_button_pressed(background_path_frame.background_path))
        background_path_browse_button.pack(fill=tk.BOTH, expand=True, padx=2)

    def _init_config_frame(self, root):
        config_frame = ttk.LabelFrame(root, text="Configuration")
        config_frame.pack(padx=10, pady=10, fill='both', expand=True)

        volume_frame = ttk.Frame(config_frame)
        volume_frame.pack(padx=0, pady=0, fill='x', expand=True)

        volume_label = ttk.Label(volume_frame, text="Music volume:")
        volume_label.pack(fill='x', expand=True)

        volume_scale = ttk.Scale(volume_frame, from_=0, to=100, orient="horizontal")
        volume_scale.pack(fill='x', expand=True)

        delimiter_sequence_frame = ttk.Frame(config_frame)
        delimiter_sequence_frame.pack(padx=0, pady=0, fill='x', expand=True)

        delimiter_sequence_label = ttk.Label(delimiter_sequence_frame, text="Delimiter sequence:")
        delimiter_sequence_label.pack(fill='x', expand=True)

        delimiter_sequence = tk.StringVar()
        delimiter_sequence_entry = ttk.Entry(delimiter_sequence_frame, textvariable=delimiter_sequence)
        delimiter_sequence_entry.pack(fill='x', expand=True, padx=2, ipady=1)

        is_find_names_checked = False
        find_names_button = ttk.Checkbutton(config_frame, text="Find names", command=self.on_find_names_check_changed,
                                            variable=lambda: is_find_names_checked, onvalue=True, offvalue=False)
        find_names_button.pack(pady=10, fill='both', expand=True)

    def _init_output_frame(self, root):
        output_frame = ttk.LabelFrame(root, text="Output")
        output_frame.pack(padx=10, pady=10, fill='both', expand=True)

        output_path_frame = ttk.Frame(output_frame)
        output_path_frame.pack(fill='x', expand=True)

        output_path_label = ttk.Label(output_path_frame, text="Save to:")
        output_path_label.pack(fill='x', expand=True)

        output_path_frame.output_path = tk.StringVar()
        output_path_entry = ttk.Entry(output_path_frame, textvariable=output_path_frame.output_path)
        output_path_entry.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=2, ipady=1)

        output_path_browse_button = ttk.Button(output_path_frame, text="Browse", command=lambda: self.on_browse_button_pressed(output_path_frame.output_path))
        output_path_browse_button.pack(fill=tk.BOTH, expand=True, padx=2)

    def on_browse_button_pressed(self, path: tk.StringVar):
        filename = filedialog.askopenfilename()
        path.set(filename)

    def process_button_pressed(self, root):
        root.config(cursor="watch")
        print("Book file path: " + self._book_path_entry.get())
        root.config(cursor="arrow")

    def on_find_names_check_changed(self):
        print("chick-check")


window = BookKeeperWindow()
