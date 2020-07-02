import tkinter as tk
from Modules.physics import Physics
from Modules.character import Character

def move_cara_to(x,y) :
    Adrien.move_to(16*(x//16)+6,16*(y//16))
    p.map.cara_pos = (16*(x//16),16*(y//16))

def motion(evt) :
    global x, y
    p.map.unhighlight_tile(x, y)

    x = evt.x
    y = evt.y

    p.map.highlight_tile(evt.x,evt.y)

    if clicked1 and pointval != 65534 :
        p.map.change_tile(evt.x,evt.y,pointval)

    elif clicked2 :
        p.map.change_tile(evt.x,evt.y,0)

def unclick(evt):
    global clicked1
    clicked1 = False

def unclick2(evt):
    global clicked2
    clicked2 = False

def click(evt) :
    global clicked1
    clicked1 = True
    if pointval == 65534 :
        move_cara_to(evt.x,evt.y)
    else :
        p.map.change_tile(evt.x, evt.y, pointval)

def click2(evt):
    global clicked2
    clicked2 = True

    p.map.change_tile(evt.x, evt.y, 0)

fen = tk.Tk()
fen.geometry("1260x640")
fen.title("  Level Create")
fen.iconphoto(False,tk.PhotoImage(file="Ressources/icon.png"))

canvas = tk.Canvas(fen, width=960, height=640, bg="#B0B0BB")
canvas.grid(row=0, column=0)

p = Physics(canvas)

p.map.open_bin_level("bin0")

x = 0
y = 0

pointval = 501
clicked1 = False
clicked2 = False

pos = p.get_init_char_pos()
Adrien = Character(pos[0]+6, pos[1], 14, 26, canvas, p)


canvas.bind("<Motion>",motion)
canvas.bind("<Button-1>",click)
canvas.bind("<Button-3>",click2)
canvas.bind("<ButtonRelease-1>",unclick)
canvas.bind("<ButtonRelease-3>",unclick2)
fen.mainloop()

p.map.save_bin_level("bin0")
print("oui")
