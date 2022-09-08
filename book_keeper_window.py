import tkinter as tk
from tkinter import ttk
import winsound

def findNamesCheckChanged():
    print("kecske")

def processButtonPressed():
    print("macska")

root = tk.Tk()
root.title("Book keeper")
root.geometry("400x600")
root.resizable(False, False)
root.iconbitmap("assets/icons/icons8-audio-book-50.ico")


sourceFrame = ttk.LabelFrame(root, text="Source")
sourceFrame.pack(padx = 10, pady = 10, fill = 'both', expand=True)

bookPathFrame = ttk.Frame(sourceFrame)
bookPathFrame.pack(padx = 0, pady = 0, fill = 'x', expand=True)

bookPathLabel = ttk.Label(bookPathFrame, text="Book file path:")
bookPathLabel.pack(fill='x', expand=True)

bookPath = tk.StringVar()
bookPathEntry = ttk.Entry(bookPathFrame, textvariable=bookPath)
bookPathEntry.pack(fill='x', expand=True)

dictionaryPathFrame = ttk.Frame(sourceFrame)
dictionaryPathFrame.pack(padx = 0, pady = 0, fill = 'x', expand=True)

dictionaryPathLabel = ttk.Label(dictionaryPathFrame, text="Dictionary file path:")
dictionaryPathLabel.pack(fill='x', expand=True)

dictionaryPath = tk.StringVar()
dictionaryPathEntry = ttk.Entry(dictionaryPathFrame, textvariable=dictionaryPath)
dictionaryPathEntry.pack(fill='x', expand=True)


designFrame = ttk.LabelFrame(root, text="Design")
designFrame.pack(padx = 10, pady = 10, fill = 'both', expand=True)

coverPathFrame = ttk.Frame(designFrame)
coverPathFrame.pack(padx = 0, pady = 0, fill = 'x', expand=True)

coverPathLabel = ttk.Label(coverPathFrame, text="Cover image path:")
coverPathLabel.pack(fill='x', expand=True)

coverPath = tk.StringVar()
coverPathEntry = ttk.Entry(coverPathFrame, textvariable=coverPath)
coverPathEntry.pack(fill='x', expand=True)

backgroundPathFrame = ttk.Frame(designFrame)
backgroundPathFrame.pack(padx = 0, pady = 0, fill = 'x', expand=True)

backgroundPathLabel = ttk.Label(backgroundPathFrame, text="Background file path:")
backgroundPathLabel.pack(fill='x', expand=True)

backgroundPath = tk.StringVar()
backgroundPathEntry = ttk.Entry(backgroundPathFrame, textvariable=backgroundPath)
backgroundPathEntry.pack(fill='x', expand=True)


configFrame = ttk.LabelFrame(root, text="Configuration")
configFrame.pack(padx = 10, pady = 10, fill = 'both', expand=True)

volumeFrame = ttk.Frame(configFrame)
volumeFrame.pack(padx = 0, pady = 0, fill = 'x', expand=True)

volumeLabel = ttk.Label(volumeFrame, text="Music volume:")
volumeLabel.pack(fill='x', expand=True)

volumeScale = ttk.Scale(volumeFrame, from_ = 0, to = 100, orient="horizontal")
volumeScale.pack(fill='x', expand=True)

delimiterSequenceFrame = ttk.Frame(configFrame)
delimiterSequenceFrame.pack(padx = 0, pady = 0, fill = 'x', expand=True)

delimiterSequenceLabel = ttk.Label(delimiterSequenceFrame, text="Delimiter sequence:")
delimiterSequenceLabel.pack(fill = 'x', expand=True)

delimiterSequence = tk.StringVar()
delimiterSequenceEntry = ttk.Entry(delimiterSequenceFrame, textvariable=delimiterSequence)
delimiterSequenceEntry.pack(fill = 'x', expand=True)

isFindNamesChecked = False
findNamesButton = ttk.Checkbutton(configFrame, text = "Find names", command = findNamesCheckChanged, variable = isFindNamesChecked, onvalue = True, offvalue = False)
findNamesButton.pack(pady = 10, fill = 'both', expand=True)


outputFrame = ttk.LabelFrame(root, text="Output")
outputFrame.pack(padx = 10, pady = 10, fill = 'both', expand=True)

outputPathFrame = ttk.Frame(outputFrame)
outputPathFrame.pack(fill = 'x', expand=True)

outputPathLabel = ttk.Label(outputPathFrame, text="Save to:")
outputPathLabel.pack(fill='x', expand=True)

outputPath = tk.StringVar()
outputPathEntry = ttk.Entry(outputPathFrame, textvariable=outputPath)
outputPathEntry.pack(fill='x', expand=True)


processButton = ttk.Button(root, text="Process", command=processButtonPressed)
processButton.pack(fill = 'x', expand=True, padx = 10, pady = 10)

root.mainloop()
