import sys
import re
import Tkinter as tk
from ScrolledText import ScrolledText

def convertToUserFriendly(line):
    line = line.replace("--- /dev/null", "[New file]")
    line = line.replace("diff --git a/", "File: ")
    return line

def parseDiff(diffFile):
    filenameParseRegex = "diff --git (.*)"


    print "Using file " + diffFile

    lineArray = [];
    with open (diffFile, "r") as myfile:
        for line in myfile:
            lineArray.append(line)

    diffFileData = {}

    currentLinesString = ""
    currentFilename = ""

    lineCount = 0
    for line in lineArray:

        lineCount+=1
        if("diff" in line):
            m = re.search(filenameParseRegex, line)
            filenames = m.group(1)
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

    return diffFileData

diffFile = sys.argv[1]
parsedDiff = parseDiff(diffFile)

class ThreesDiff(tk.Tk):
    listOptions = None
    diffData = {}

    root = None
    textbox = None



    def __init__(self, diffData):
        self.diffData = diffData
        self.listOptions = diffData.keys()
        #tk.Tk.__init__(self, *args, **kwargs)
        self.root = tk.Tk()
        lb = tk.Listbox(self.root)

        for option in self.listOptions:
           lb.insert("end", option)

        lb.bind("<Double-Button-1>", self.OnDouble)
        lb.bind("<<ListboxSelect>>", self.OnDouble)
        lb.pack(side="top", fill="both", expand=True)

        text = ScrolledText(self.root, height=500, width=150, bg="black")
        text.tag_configure("minus", foreground="red")
        text.tag_configure("plus", foreground="green")
        text.tag_configure("normal", foreground="grey")
        text.pack()

        self.textbox = text

    def OnDouble(self, event):
        widget = event.widget
        selection=widget.curselection()
        value = widget.get(selection[0])
        print "selection:", selection, ": '%s'" % value

        textContent = self.diffData[value]

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


if __name__ == "__main__":
    app = ThreesDiff(parsedDiff)
    app.root.mainloop()
