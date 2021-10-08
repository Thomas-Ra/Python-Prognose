from tkinter import *
import tkinter as tk

# DEF
def quit (event=None): 
    root.destroy()
    return

root = Tk()
root.geometry('+%d+%d'%(1300,300))

# EVENTS
root.bind("<Alt-q>", quit)

#LOGO
#logo = Image.open('')

# TITLE Bar
root.title("Market Prediction")
title_bar = Frame(bg='grey17', relief='raised')


# MENU 
menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
menu.add_cascade(label="Aktien", menu=filemenu)
filemenu.add_command(label="A", command="")
filemenu.add_command(label="B", command="")
filemenu.add_command(label="C", command="")
filemenu.add_command(label="Open...", command="")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

gachamenu = Menu(menu)
menu.add_cascade(label="Kurs", menu=gachamenu)
gachamenu.add_command(label="Bla", command="")

steammenu = Menu(menu)
menu.add_cascade(label="Moin", menu=steammenu)
steammenu.add_command(label="a", command="")

servermenu = Menu(menu)
menu.add_cascade(label="Hier Noch", menu=servermenu)
servermenu.add_command(label="asda", command="")

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="Keybinds", command="")
helpmenu.add_command(label="Resolution", command="")
helpmenu.add_command(label="About...", command="")
helpmenu.add_command(label="Quit", command=quit, accelerator="Alt+q")

# SCROLLBAR
scrollbar = Scrollbar(root, orient=VERTICAL)

# TOP AREA Sidebar - Title 
top_sidebar_part = Frame(root, width=250, height=600, bg="lightgrey")
top_sidebar_part.grid(row=0, column=0, rowspan=2)

# TOP AREA -  Script running 
header_part = Frame(root, width=700, height=200, bg="white")
header_part.grid(row=0, column=1, rowspan=1, columnspan=2)

# Main AREA - Script
main_part = Frame(root, width=700, height=400, bg="lightgrey")
main_part.grid(row=1, column=1, rowspan=1, columnspan=2)

# EXCECUTION AREA  
excecution_part = Frame(root, width=1000, height=50, bg="grey")
excecution_part.grid(row=2, column=0, columnspan=3)

# EXCECUTION AREA Buttons- Start / Stop 
start_button = Button(root, text="Button1", font=("shanti", 10), height=1, width=25, bg="#c8c8c8")
start_button.grid(row=2, column=0, rowspan=1)
stop_button = Button(root, text="stop", font=("shanti", 10), height=1, width=25, bg="#c8c8c8")
stop_button.grid(row=2, column=1, rowspan=1)
stop_all_button = Button(root, text="stop all", font=("shanti", 10), height=1, width=25, bg="#c8c8c8")
stop_all_button.grid(row=2, column=2, rowspan=1)

# FOOTER - Code Execution
footer_part = Frame(root, width=1000, height=50, bg="black")
footer_part.grid(row=3, rowspan=2, columnspan=3)

root.mainloop()
