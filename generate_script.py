from tkinter import TOP, Entry, Label, Button, StringVar
from tkinterdnd2 import *

root = TkinterDnD.Tk()
root.geometry("500x900")
root.title("Get file path")

monitor_number = 4#TODO: detect automatically

#nameVar = StringVar()

titles = []
paths = []
path_str = []
widgets = []
labels = []

def generate():
    if name_field.get().strip()=="":
        return
    for entry in path_str:
        if entry.strip()=="":
            return
    content="#!/usr/bin/env bash\n\n"
    content+="#"+name_field.get()+"\n\n"
    content+="flatpak run org.gabmus.hydrapaper -c"
    for entry in path_str:
        content+=" \""+entry+"\""
    content+="\n"
    file = open(name_field.get()+".sh", "w")  # write mode
    file.write(content)
    file.close()

def unlock_generate_button():
    for entry in path_str:
        if entry.strip()=="":
            return
    #button.state(['!disabled'])

def get_path(event,index):
    path = str(event.data).replace("{","").replace("}","").strip()
    paths[index].configure(text = path)
    path_str[index]= path
    #unlock_generate_button()

static_label = Label(root, text="Name:")
static_label.pack(side=TOP)

name_field = Entry(root)
name_field.pack(side=TOP)

for i in range(0,monitor_number):
    path_str.append("")

    labels.append(Label(root, text="Monitor #"+str(i)))
    labels[i].pack(side=TOP)

    widgets.append(Entry(root))
    widgets[i].pack(side=TOP, padx=5, pady=5, ipadx=500,ipady=50)

    paths.append(Label(root, text="Drag and drop file in the entry box"))
    paths[i].pack(side=TOP)

    widgets[i].drop_target_register(DND_ALL)
    widgets[i].dnd_bind("<<Drop>>", lambda event, index=i: get_path(event, index))

button = Button(
    root,
    text='Generate',
    command=lambda: generate()
)
button.pack(side=TOP)
exit = Button(
    root,
    text='Exit',
    command=lambda: root.quit()
)
exit.pack(side=TOP)
#button.state(['disabled'])

root.mainloop()
