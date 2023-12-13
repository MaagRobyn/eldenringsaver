# C:\Users\maagm\AppData\Roaming\EldenRing

import shutil, errno, os, time
import tkinter as tk

dir = os.path.join(os.getenv("APPDATA"), "EldenRing") + "\\"
existingFiles = os.listdir(dir)
saveFolders = []
for f in existingFiles:
    if f.isdigit():
        saveFolders.append(f)

window = tk.Tk()
window.title("Elden Ring Save State Manager")
saveNames = []

def refreshLists():
    global saveNames
    saves = os.listdir(dir)
    listbox.delete(0,tk.END)
    saveNames = []
    for save in saves:
        if "-" in save:
            if(save.index("-") <= len(save) and removeFolderPrefix(save) not in saveNames):
                listbox.insert(tk.END, removeFolderPrefix(save))
                saveNames.insert(len(saveNames), removeFolderPrefix(save))

def save():
    print("Saving " + name.get())
    for folder in saveFolders:
        copyanything(dir + folder, dir + folder + "-" + name.get())
    name.delete(0, tk.END)
    refreshLists()

def load():
    selections = listbox.curselection()
    if(len(selections) == 1):
        i = int(selections[0])
        fileName = saveNames[i]
        print("Loading " + fileName)
        for folder in saveFolders:
            shutil.rmtree(dir + folder)
            copyanything(dir + folder + "-" + fileName, dir + folder)
    refreshLists()

def delete():
    selections = listbox.curselection()
    if(len(selections) == 1):
        i = int(selections[0])
        fileName = saveNames[i]
        print("Deleting " + fileName)
        for folder in saveFolders:
            shutil.rmtree(dir + folder + "-" + fileName)
    refreshLists()

def saveAndLoad():
    save()
    load()

def copyanything(src, dst):
    if(os.path.isdir(src)):
        shutil.copytree(src,dst)
    else:
        shutil.copy(src,dst)

def getName(saveName):
    i = 0
    name = saveName
    while addFirstFolderPrefix(name) in existingFiles:
        i += 1
        name = saveName + str(i)
    return name

def removeFolderPrefix(fullFolderName):
    return fullFolderName[fullFolderName.index("-") + 1:]

def addFirstFolderPrefix(saveName):
    return saveFolders[0] + "-" + saveName

savetitle = tk.Label(text="Enter the name of the save you want to create:")
name = tk.Entry()


name.insert(0,getName("backup"))

savebutton = tk.Button(command=save, text="Save")

loadtitle = tk.Label(text="Which do you want to load:")
listbox = tk.Listbox()

loadbutton = tk.Button(command=load, text="Load")
saveAndLoadbutton = tk.Button(command=saveAndLoad, text="Save & Load")
refreshListsButton = tk.Button(command=refreshLists, text="Refresh Lists")
deleteButton = tk.Button(command=delete, text="Delete Save")

def packAll():
    savetitle.pack()
    name.pack()
    savebutton.pack()
    loadtitle.pack()
    listbox.pack()
    loadbutton.pack()
    saveAndLoadbutton.pack()
    refreshListsButton.pack()
    deleteButton.pack()

packAll()
refreshLists()
window.mainloop()
