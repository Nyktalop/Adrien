import tkinter as tk
from tkinter import filedialog, messagebox
from Modules.physics import Physics
from Modules.character import Character

def saveas() :
    global saved, file_name
    if not p.map.initialized :
        return

    file = filedialog.asksaveasfilename(initialdir='./Ressources/Maps', title='Select File')
    if file :
        saved = True
        file_name = file
        p.map.save_bin_level(file,True)
        messagebox.showinfo("Saved", "Map sauvegardée sous le nom : \n" + file_name)



def open():
    global saved, file_name

    if not saved :
        a = messagebox.askyesnocancel("Save ?", "Sauvegarder le niveau actuel ?\n(Il y a des changements non sauvegardés)")
        if a == None :
            return
        elif a == True :
            saveas()

    file = filedialog.askopenfilename(initialdir='./Ressources/Maps', title='Select File')
    if file :
        p.map.open_bin_level(file,True)
        saved = True
        pos = p.get_init_char_pos()
        move_cara_to(pos[0],pos[1])
        file_name = file

def save():
    global saved

    if not p.map.initialized :
        return

    if file_name == "New Map" :
        saveas()
    else :
        saved = True
        p.map.save_bin_level(file_name,absolute=True)
        messagebox.showinfo("Saved","Map sauvegardée sous le nom : \n" + file_name)

def new() :
    global file_name, saved

    if not saved:
        a = messagebox.askyesnocancel("Save ?",
                                      "Sauvegarder le niveau actuel ?\n(Il y a des changements non sauvegardés)")
        if a == None:
            return
        elif a == True:
            saveas()

    saved = True
    p.map.open_blank()
    file_name = "New Map"
    move_cara_to(-50,-50)


def move_cara_to(x,y) :
    Adrien.reset_to(16 * (x // 16) + 6, 16 * (y // 16))
    p.map.cara_pos = (16*(x//16),16*(y//16))

def motion(evt) :
    global x, y

    if not p.map.initialized :
        return

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
    global clicked1, saved

    if not p.map.initialized :
        return

    clicked1 = True
    if pointval == 65534 :
        move_cara_to(evt.x,evt.y)
    else :
        p.map.change_tile(evt.x, evt.y, pointval)

    saved = False

def click2(evt):
    global clicked2, saved

    if not p.map.initialized :
        return

    clicked2 = True

    p.map.change_tile(evt.x, evt.y, 0)
    saved = False

def labelclick(evt) :
    global i_select, pointval

    labels[i_select].config(relief=tk.FLAT)

    i_select = id_to_iselect[evt.widget.winfo_id()]

    pointval = vals[i_select]
    labels[i_select].config(relief=tk.GROOVE)

def select(evt):
    global i_select,pointval

    labels[i_select].config(relief=tk.FLAT)

    if evt.keysym == "Up" :
        i_select = (i_select - 5) % len(labels)
    elif evt.keysym == "Down" :
        i_select = (i_select + 5) % len(labels)
    elif evt.keysym == "Left" :
        i_select = (i_select - 1) % len(labels)
    elif evt.keysym == "Right" :
        i_select = (i_select + 1) % len(labels)

    pointval = vals[i_select]
    labels[i_select].config(relief=tk.GROOVE)


fen = tk.Tk()
fen.geometry("1220x643")
fen.title("  Level Create")
fen.iconphoto(False,tk.PhotoImage(file="Ressources/icon.png"))

canvas = tk.Canvas(fen, width=960, height=640, bg="#B0B0BB")
canvas.grid(row=0, column=0,rowspan=25)

sep_line = canvas.create_rectangle(2,2,961,641,width=2)

frame = tk.Frame(fen)
frame.grid(row=0,column=1,padx=25)

p = Physics(canvas)
# p.map.open_bin_level("bin0")
# pos = p.get_init_char_pos()
Adrien = Character(-50, -50, canvas, p)

file_name = "New Map"

labels = []
vals = []
id_to_iselect = {}

labels.append(tk.Label(frame,image=Adrien.animator.frames["idle_r_0"]))
vals.append(65534)
labels[-1].grid(row=0,column=0,padx=10,pady=10)
labels[-1].bind("<Button-1>", labelclick)
id_to_iselect[labels[-1].winfo_id()] = 0





for i,val in enumerate(p.map.img_dict) :
    x = (i+1) % 5
    y = (i+1) // 5
    labels.append(tk.Label(frame,image=p.map.img_dict[val],bd=5))
    vals.append(val)
    labels[-1].grid(row=y,column=x,padx=5,pady=5)
    labels[-1].bind("<Button-1>",labelclick)

    id_to_iselect[labels[-1].winfo_id()] = i+1


new_button = tk.Button(frame,text="New",command=new,width=10)
new_button.grid(row=25,column=0,pady=25,columnspan=3)

save_button = tk.Button(frame,text="Save",command=save,width=10)
save_button.grid(row=25,column=3,pady=25,columnspan=3)

open_button = tk.Button(frame,text="Open",command=open,width=10)
open_button.grid(row=26,column=0,pady=25,columnspan=3)

saveas_button = tk.Button(frame, text="Save As", command=saveas, width=10)
saveas_button.grid(row=26,column=3,pady=25,columnspan=3)

p.map.open_blank()



i_select = 0
labels[i_select].config(relief=tk.GROOVE)

x = 0
y = 0

pointval = 65534
clicked1 = False
clicked2 = False
saved = True




canvas.bind("<Motion>",motion)
canvas.bind("<Button-1>",click)
canvas.bind("<Button-3>",click2)
canvas.bind("<ButtonRelease-1>",unclick)
canvas.bind("<ButtonRelease-3>",unclick2)

fen.bind_all("<KeyPress>", select)
fen.mainloop()

