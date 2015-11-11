#!/bin/python

import sys
import re
import Tkinter as tk
from ScrolledText import ScrolledText
import subprocess
import time

def convertToUserFriendly(line):
    line = line.replace("--- /dev/null", "[New file]")
    line = line.replace("diff --git a/", "File: ")
    return line + "\n"

def parseDiffText(diffText):
    filenameParseRegex = "diff --git (.*)"
#
    lineArray = diffText.split("\n");
#    for line in diffText.split("\r"):
 #       lineArray.append(line)

    print("Parsed diff to line array of size ", len(lineArray))

    diffFileData = {}

    currentLinesString = ""
    currentFilename = ""

    lineCount = 0
    linesTotal = len(lineArray)
    for line in lineArray:

        lineCount+=1

        isFilenameLine = re.search(filenameParseRegex, line)
        isLastLineInFile = lineCount == linesTotal
        if(isFilenameLine):
            print line
            
            filenames = isFilenameLine.group(1)
            # this is the "next" filename
            if(currentFilename == ""):
                header = currentLinesString
            else:
                diffFileData[currentFilename] = currentLinesString

            filenameA = filenames.split(" ")[0]
            filenameA = filenameA.replace("a/", "")
            currentFilename = filenameA

            
            currentLinesString = ""

        currentLinesString += convertToUserFriendly(line)

        # The "Save lines" code above will not trigger in the case
        # that we are at the end of file. Explicitly save.
        if(isLastLineInFile):
            diffFileData[currentFilename] = currentLinesString


    return diffFileData

def parseDiff(diffFile):
    print "Using file " + diffFile
    with diffText as myfile:
        file = open (myfile, "r")
    parseDiffText(file)

class ThreesDiff(tk.Tk):
    listOptions = None
    parsedDiff = None
    diffFilename = None
    currentFilename = None

    root = None
    textbox = None
    lb = None



    def __init__(self, diffFilename):
        self.diffFilename = diffFilename

        #tk.Tk.__init__(self, *args, **kwargs)
        print "Loading diff tool"

        self.loadData()

        self.root = tk.Tk()
        lb = tk.Listbox(self.root)

        lb.bind("<Double-Button-1>", self.OnDouble)
        lb.bind("<<ListboxSelect>>", self.OnDouble)
        lb.pack(side="top", fill="both", expand=True)

        def reloadCallback():
            numOptions = len(self.listOptions)
            self.lb.delete(0, last = numOptions)
            print "Reloading"
            self.loadData()
            self.loadGui()
            self.loadFileIntoTextbox() # Reload the currently displayed file

        b = tk.Button(self.root, text="Reload", command=reloadCallback)
        b.pack()

        text = ScrolledText(self.root, height=500, width=150, bg="black")
        text.tag_configure("minus", foreground="red")
        text.tag_configure("plus", foreground="green")
        text.tag_configure("normal", foreground="grey")
        text.pack()

        self.lb = lb
        self.textbox = text

        self.loadGui()

    def doDiff(self):
        out = subprocess.check_output(["git", "diff"])
        print "Output type: ", type(out)
        print out
        return out

    def loadGui(self):
        self.listOptions = self.parsedDiff.keys()
        for option in self.listOptions:
           self.lb.insert("end", option)

    def loadData(self):
        print "Parsing diffs from " + self.diffFilename
        diffText = self.doDiff()
        self.parsedDiff = parseDiffText(diffText)

    def getDiffContentsForFile(self):
        print "Getting contents for " + self.currentFilename
        return self.parsedDiff[self.currentFilename]

    def loadFileIntoTextbox(self):
        textContent = self.getDiffContentsForFile()

        self.textbox.delete('1.0', tk.END) # clear it

        splitContent = textContent.split("\n")

        for line in splitContent:
            line = line + "\n"
            if line.startswith("+"):
                self.textbox.insert(tk.END, line, ("plus"))
            elif line.startswith("-"):
                self.textbox.insert(tk.END, line, ("minus"))    
            else:
                self.textbox.insert(tk.END, line, ("normal"))

    def OnDouble(self, event):
        widget = event.widget
        selection=widget.curselection()
        value = widget.get(selection[0])
        print "selection:", selection, ": '%s'" % value

        self.currentFilename = value
        self.loadFileIntoTextbox();


diffFile = sys.argv[1]

if __name__ == "__main__":
    app = ThreesDiff(diffFile)
    app.root.mainloop()