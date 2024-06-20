import sys
import os
from tkinter import *
from tkinter import ttk


def printOutput(text):
    output.insert(END, '\n'+str(text))
    print(text)

def printOutput_(text):
    output.insert(END, text)
    print(text, end='')

def saveFile():
    with open(f"factScripts/{scriptName}", "w") as file:
        file.write(editor.get(1.0, END).strip())

def savePExit():
    with open(f"factScripts/{scriptName}", "w") as file:
        file.write(editor.get(1.0, END).strip())
    sys.exit()


def codeInterpretation():

    output.delete(1.0, END)
    saveFile()

    lType = []
    lVal = []
    script = []
    inputVals = []

    with open(f"factScripts/{scriptName}", "r") as file:
        for line in file:
            if line[:1] == '#':
                continue
            if line[-2:] == '\n':
                if line.find(' ') != -1:
                    lType.append(1)
                    lVal.append(len(line[:-2].split()))
                    script.extend(line[:-2].split())
                else:
                    lType.append(0)
                    lVal.append(1)
                    script.append(line[:-2])
            else:
                if line.find(' ') != -1:
                    lType.append(1)
                    lVal.append(len(line.split()))
                    script.extend(line.split())
                else:
                    lType.append(0)
                    lVal.append(1)
                    script.append(line)

    with open("input.txt", 'r') as file:
        for line in file:
            if line[:1] == '#':
                continue
            if line[-2:] == '\n':
                inputVals.extend(line[:-2].split())
            else:
                inputVals.extend(line.split())

    for i in range(len(inputVals)):
        if inputVals[i] != '':
            try:
                inputVals[i] = int(inputVals[i], 2)
            finally:
                continue
        else:
            inputVals.pop(i)

    for i in range(len(script)):
        if script[i] != '':
            script[i] = int(script[i], 2)
        else:
            script.pop(i)

    #setup
    if script[0] != 0:
        printOutput("init error")
        sys.exit()

    printOutput("init complete")
    printOutput(f"Script: {script}")
    printOutput(f"Input: {inputVals}")
    printOutput("Starting code performance:" + '\n')


    stacks = []
    stack = []
    funcs = []
    curS = 0
    #curVal = 0
    #tempVStock = 0

    while curS < len(script):
        #print("Stack:", stack)
        #print("curS:", curS)
        #print("Command:", script[curS])


        if curS == 0:
            curS+=1
            continue

        match script[curS]:
            case 0:
                printOutput('\n')
                printOutput("Performance end")
                printOutput(f"Stacks: {stacks} Cur stack: {stack}")
                printOutput(f"Funcs: {funcs}")
                break
            case 1:
                stack.append(script[curS+1])
                curS+=2
                continue
            case 2:
                printOutput(stack.pop())
            case 3:
                stack.append(stack[-1])
            case 4:
                stack[-2] += stack[-1]
                stack.pop(-2)
            case 5:
                stack[-2] -= stack[-1]
                stack.pop(-1)
            case 6:
                stack[-2] *= stack[-1]
                stack.pop(-2)
            case 7:
                stack[-2] /= stack[-1]
                stack.pop(-1)
            case 8:
                tempS = []
                tempS.extend(stack)
                stack.pop()
                for i in range(script[curS-1]):
                    stack.append(tempS[-2])
                curS += 1
                continue
            case 9:
                stacks.append([])
                stacks[-1].extend(stack)
            case 10:
                tempV = stacks[stack[-1]]
                stack.pop()
                stack.extend(tempV)
            case 11:
                #print(stacks[stack[-1]][-1])
                stack.append(stacks[stack[-1]][-1])
                stack.pop(-2)
            case 12:
                stacks[stack[-1]] = []
                tempP = stack[-1]
                stack.pop()
                stacks[tempP].extend(stack)
            case 13:
                for i in stack:
                    stacks[stack[-1]].append(i)
                stacks[stack[-1]].pop()
                stack.pop()
            case 14:
                stack = []
            case 15:
                stack.pop()
            case 16:
                for i in range(stack[-1]+1):
                    stack.pop()
            case 17:
                stack.append(chr(stack[-1]))
                stack.pop(-2)
            case 18:
                funcs.append(script[curS+1:script.index(19,curS)])
                del script[curS+1:script.index(19,curS)]
            case 20:
                j = 0
                for i in funcs[stack[-1]]:
                    script.insert(curS + 1 + j, i)
                    j += 1
                stack.pop()
            case 21:
                for i in range(stack[-1]):
                    script.insert(curS + 1 + i, script[curS + 1])
                stack.pop()
            case 22:
                printOutput_(stack.pop())
            case 23:
                t = stack.pop()
                stack.append(stack[-1- t])
            case 24:
                stack[-1], stack[-2] = stack[-2], stack[-1]
            case 25:
                for i in range(stack[-1]):
                    script.pop(curS + 1)
                stack.pop()
            case 26:
                tmpComp = False
                match stack.pop():
                    case 0:
                        if stack[-2] == stack[-1]:
                            tmpComp = True
                    case 1:
                        if stack[-2] != stack[-1]:
                            tmpComp = True
                    case 2:
                        if stack[-2] > stack[-1]:
                            tmpComp = True
                    case 3:
                        if stack[-2] < stack[-1]:
                            tmpComp = True
                    case 4:
                        if stack[-2] >= stack[-1]:
                            tmpComp = True
                    case 5:
                        if stack[-2] <= stack[-1]:
                            tmpComp = True
                if tmpComp == True:
                    if 28 in script:
                        if script.index(28, curS) < script.index(27, curS):
                            del script[script.index(28, curS):script.index(27, curS)]
                elif 28 in script:
                    if script.index(28, curS) < script.index(27, curS):
                        del script[curS:script.index(28, curS)]
                    else:
                        del script[curS:script.index(27,curS)]
                else:
                    del script[curS:script.index(27, curS)]
                for i in range(2): stack.pop()
            case 29:
                for i in range(2): stack.append(stack[-2])
            case 30:
                stacks[stack[-1]].append(stack[-2])
                stack.pop()
            case 31:
                stack.append(inputVals.pop())


        curS += 1



def changeInt():
    if int1['text'] == '10':
        int1.config(text="2")
        int2.config(text="10")
    else:
        int1.config(text="10")
        int2.config(text="2")

def intConvert():
    entry2.delete(0, END)
    if int1['text'] == '10':
        entry2.insert(0, bin(int(entry1.get()))[2:])
    else:
        entry2.insert(0, int(entry1.get(), 2))

def charConvert():
    asciiInt.delete(0, END)
    asciiInt.insert(0, bin(ord(asciiChar.get()))[2:])

def textConvert():
    for i in range(len(convText.get())):
        editor.insert(END, '1 ' + bin(ord(convText.get()[len(convText.get()) - 1 -i]))[2:] + ' 10001' + '\n')
    convText.delete(0, END)

def changeFile(event):
    saveFile()
    global scriptName
    scriptName = fileSelect.get()
    editor.delete("1.0", END)
    with open(f"factScripts/{scriptName}", "r") as file:
        for i in file:
            editor.insert(END, i)

def newFileWin():

    def addNewFile():
        with open(f"factScripts/{newFileName.get()}.txt", "w") as file:
            file.close()
        global filesList
        global fileSelect
        filesList = os.listdir("factScripts/")
        fileSelect.config(values=filesList)
        curFiles.delete("1.0", END)
        for i in filesList:
            curFiles.insert(END, i + '\n')

    newFile = Tk()
    newFile.title("New file")
    newFile.geometry("300x400+500+300")
    newFile.resizable(False, False)

    newFileName = ttk.Entry(newFile)
    newFileName.place(x=0, y=40, anchor='w', width=200, height=25)
    newFileNameL = ttk.Label(newFile, text="File name (without .txt)")
    newFileNameL.place(x=0, y=15, anchor='w', width=150, height=25)
    newFileNameBtn = ttk.Button(newFile, text="Create new file", command=addNewFile)
    newFileNameBtn.place(x=200, y=40, anchor='w', width=100, height=25)

    curFilesL = ttk.Label(newFile, text="Curent files:")
    curFilesL.place(x=0, y=100, anchor='w', width=200, height=25)
    curFiles = Text(newFile, wrap="word")
    curFiles.place(x=0, y=260, anchor='w', width=300, height=300)

    ys1 = ttk.Scrollbar(master=curFiles, orient="vertical", command=curFiles.yview)
    ys1.pack(expand=True, anchor='e', fill=Y)
    curFiles["yscrollcommand"] = ys1.set

    for i in filesList:
        curFiles.insert(END, i + '\n')

def inputSetWin():

    def inputSave():
        with open("input.txt", "w") as file:
            file.write(inputSetText.get(1.0, END).strip())

    inputSet = Tk()
    inputSet.title("Input")
    inputSet.geometry("300x400+500+300")

    inputSetText = Text(inputSet, wrap="word")
    inputSetText.place(relx=0.5, y=50, anchor='n', relwidth=1, relheight=0.9)

    with open("input.txt", "r") as file:
        inputSetText.insert(END, file.read())

    inputSetSaveBtn = ttk.Button(inputSet, text="Save", command=inputSave)
    inputSetSaveBtn.place(x=0, y=25, anchor='w', width=50, height=50)

def instrOpen():

    instrWin = Tk()
    instrWin.title("Instruction")
    instrWin.geometry("800x600+550+350")

    instrText = Text(instrWin, wrap="word")
    instrText.place(relx=0, rely=0, anchor='nw', relwidth=1, relheight=1)

    with open("instruction.txt", "r") as file:
        instrText.insert(END, file.read())

root = Tk()
root.title("Fact IDE 1.0")
root.geometry("700x800+400+200")
root.minsize(700,700)
icon = PhotoImage(file = "icon1.png")
root.iconphoto(True, icon)

runBtn = ttk.Button(text = "Run", command=codeInterpretation)
runBtn.place(relx=1, anchor="ne", width=70, height=70)

editor = Text(wrap="word")
editor.place(rely=0.2, relwidth=1, relheight=0.6)
ys = ttk.Scrollbar(master=editor, orient = "vertical", command = editor.yview)
ys.pack(expand=True, anchor='e', fill=Y)
editor["yscrollcommand"] = ys.set

output = Text(wrap='word')
output.place(rely=0.8, relwidth=1, relheight=0.2)

int1 = ttk.Label(text="10")
int2 = ttk.Label(text="2")
entry1 = ttk.Entry()
entry2 = ttk.Entry()
entry1.place(x=0, y=40, anchor='w', width=105, height=25)
entry2.place(x=175, y=40, anchor='w', width=105, height=25)
int1.place(x=45, y=15, anchor='w', width=30, height=25)
int2.place(x=220, y=15, anchor='w', width=30, height=25)

intChangeBtn = ttk.Button(text="Swap", command=changeInt)
intChangeBtn.place(x=115, y=15, anchor='w', width=50, height=25)

convIntBtn = ttk.Button(text="Convert", command=intConvert)
convIntBtn.place(x=105, y=40, anchor='w', width=70, height=25)

asciiChar = ttk.Entry()
asciiInt = ttk.Entry()
asciiChar.place(x=315, y=40, anchor='w', width=105, height=25)
asciiInt.place(x=490, y=40, anchor='w', width=105, height=25)

convCharBtn = ttk.Button(text="Convert", command=charConvert)
convCharBtn.place(x=420, y=40, anchor='w', width=70, height=25)
convCLab1 = ttk.Label(text="Char")
convCLab2 = ttk.Label(text="ASCII")
convCLab1.place(x=315, y=15, anchor='w', width=50, height=20)
convCLab2.place(x=490, y=15, anchor='w', width=50, height=20)

convText = ttk.Entry()
convText.place(x=315, y=100, anchor='w', width=280, height=25)
convTextL = ttk.Label(text="Text")
convTextL.place(x=315, y=75, anchor='w', width=35, height=25)
convTextBtn = ttk.Button(text="Convert into code", command=textConvert)
convTextBtn.place(x=455, y=75, anchor='w', width=140, height=25)

filesList = os.listdir("factScripts/")
scriptName = filesList[0]
fileSelect = ttk.Combobox(values=filesList, state="readonly")
fileSelect.current(0)
fileSelect.bind("<<ComboboxSelected>>", changeFile)
fileSelect.place(x=0, y=100, anchor='w', width=200, height=25)
selFile = ttk.Label(text="Selected script:")
selFile.place(x=0, y=75, anchor='w', width=200, height=25)

root.option_add("*tearOff", FALSE)

main_menu = Menu()

file_menu = Menu()
file_menu.add_command(label="New", command=newFileWin)
file_menu.add_command(label="Save", command=saveFile)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=savePExit)

main_menu.add_cascade(label="File", menu=file_menu)
main_menu.add_cascade(label="Insruction", command=instrOpen)
#main_menu.add_cascade(label="View")

root.config(menu=main_menu)

inputSetWinBtn = ttk.Button(text="Input", command=inputSetWin)
inputSetWinBtn.place(relx=1, y=70, anchor="ne", width=70, height=70)

with open(f"factScripts/{scriptName}", "r") as file:
    for rewr in file:
        editor.insert(END, rewr)

root.mainloop()