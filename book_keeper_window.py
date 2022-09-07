import tkinter as tk
from tkinter import ttk
import winsound

def findNamesCheckChanged():
    print("kecske")

def processButtonPressed():
    print("macska")

root = tk.Tk()
root.title("Book keeper")
root.geometry("400x500")
root.resizable(False, False)


sourceFrame = ttk.LabelFrame(root, text="Source")
sourceFrame.pack(padx = 10, pady = 10, fill = 'x', expand=True)

bookPathLabel = ttk.Label(sourceFrame, text="Book file path:")
bookPathLabel.pack(fill='x', expand=True)

bookPath = tk.StringVar()
bookPathEntry = ttk.Entry(sourceFrame, textvariable=bookPath)
bookPathEntry.pack(fill='x', expand=True)

dictionaryPathLabel = ttk.Label(sourceFrame, text="Dictionary file path:")
dictionaryPathLabel.pack(fill='x', expand=True)

dictionaryPath = tk.StringVar()
dictionaryPathEntry = ttk.Entry(sourceFrame, textvariable=dictionaryPath)
dictionaryPathEntry.pack(fill='x', expand=True)


designFrame = ttk.LabelFrame(root, text="Design")
designFrame.pack(padx = 10, pady = 10, fill = 'x', expand=True)

coverPathLabel = ttk.Label(designFrame, text="Cover image path:")
coverPathLabel.pack(fill='x', expand=True)

coverPath = tk.StringVar()
coverPathEntry = ttk.Entry(designFrame, textvariable=coverPath)
coverPathEntry.pack(fill='x', expand=True)

backgroundPathLabel = ttk.Label(designFrame, text="Background file path:")
backgroundPathLabel.pack(fill='x', expand=True)

backgroundPath = tk.StringVar()
backgroundPathEntry = ttk.Entry(designFrame, textvariable=backgroundPath)
backgroundPathEntry.pack(fill='x', expand=True)


configFrame = ttk.LabelFrame(root, text="Configuration")
configFrame.pack(padx = 10, pady = 10, fill = 'x', expand=True)

volumeLabel = ttk.Label(configFrame, text="Music volume:")
volumeLabel.pack(fill='x', expand=True)

volumeScale = ttk.Scale(configFrame, from_ = 0, to = 100, orient="horizontal")
volumeScale.pack(fill='x', expand=True)

delimiterSequenceLabel = ttk.Label(configFrame, text="Delimiter sequence file path:")
delimiterSequenceLabel.pack(fill = 'x', expand=True)

delimiterSequence = tk.StringVar()
delimiterSequenceEntry = ttk.Entry(configFrame, textvariable=delimiterSequence)
delimiterSequenceEntry.pack(fill = 'x', expand=True)

isFindNamesChecked = False
findNamesButton = ttk.Checkbutton(configFrame, text = "Find names", command = findNamesCheckChanged, variable = isFindNamesChecked, onvalue = True, offvalue = False)
findNamesButton.pack(fill = 'x', expand=True)


processButton = ttk.Button(root, text="Process", command=processButtonPressed)
processButton.pack(fill = 'x', expand=True, padx = 10, pady = 10)

root.mainloop()
