#!/bin/sh

import sys
import re
import Tkinter as tk
from ScrolledText import ScrolledText
import subprocess
import time
import json

def convertToUserFriendly(line):
    line = line.replace("--- /dev/null", "[New file]")
    line = line.replace("diff --git a/", "File: ")
    return line + "\n"


def parseJson(text):
    return json.loads(text)

def prettifyJson(myJson):
    return json.dumps(myJson, indent=4, sort_keys=True)

class WaffleClipboard(tk.Tk):
    listOptions = None
    parsedDiff = None
    diffFilename = None
    currentFilename = None

    root = None
    textbox = None
    lb = None

    def __init__(self):
        #tk.Tk.__init__(self, *args, **kwargs)
        print "Loading WaffleClipboard"

        self.root = tk.Tk()
        lb = tk.Listbox(self.root)

        #lb.bind("<Double-Button-1>", self.OnDouble)
        #lb.bind("<<ListboxSelect>>", self.OnDouble)
        lb.pack(side="top", fill="both", expand=True)

        def reloadCallback():
            print "Reloading"
            newContent = parseJson(self.getMainText())
            newContent = prettifyJson(newContent);
            self.setMainText(newContent)

        b = tk.Button(self.root, text="JSON", command=reloadCallback)
        b.pack()

        text = ScrolledText(self.root, height=500, width=150, bg="white")

        text.tag_configure("normal", foreground="black")
        text.pack()

        self.lb = lb
        self.textbox = text

    def getMainText(self):
        return self.textbox.get("1.0", tk.END)

    def setMainText(self, textContent):
        self.textbox.delete('1.0', tk.END) # clear it
        self.textbox.insert(tk.END, textContent, ("normal"))
'''
    def OnDouble(self, event):
        widget = event.widget
        selection=widget.curselection()
        value = widget.get(selection[0])
        print "selection:", selection, ": '%s'" % value

        self.currentFilename = value
        self.loadFileIntoTextbox();
'''

#diffFile = sys.argv[1]

if __name__ == "__main__":
    app = WaffleClipboard()
    app.root.mainloop()