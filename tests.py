import tkinter as tk
from tkinter import ttk, messagebox

clicked = False
width = 1
x = None
y = None


fen = tk.Tk()
fen.geometry("600x600")
fen.title("Test")

canvas = tk.Canvas(fen, width=600, height=600, bg="white")
canvas.grid(column=0,row=0)

def unclick(evt) :
    global clicked,x,y
    clicked = False

def click(evt) :
    global clicked,x,y
    clicked = True
    x = evt.x
    y = evt.y

def motion(evt) :
    global x,y
    if clicked :
        canvas.create_line(x, y, evt.x, evt.y, fill="#000000",width=width)
        x = evt.x
        y =evt.y

def up(evt) :
    global width

    print(width)
    width += 1

def down(evt) :
    global width

    if width > 1 :
        width -= 1


canvas.bind("<Button-1>",click)
canvas.bind("<ButtonRelease-1>",unclick)
canvas.bind("<Motion>",motion)

fen.bind_all("<Up>",up)
fen.bind_all("<Down>",down)

fen.mainloop()