import tkinter as tk
from Modules.entity import Entity
from Modules.evthandler import EvtHandler

fen = tk.Tk()
fen.geometry("960x640")

canvas = tk.Canvas(fen, width=960, height=640, bg="#a9ebf2")
canvas.grid(row=0, column=0)

tile = tk.PhotoImage(file="Ressources/Terrain/X.gif")
for i in range(60):
    canvas.create_image(i*16+8,344,image=tile)



Adrien = Entity(480, 320, 32, 32, canvas)
evt_handler = EvtHandler()
evt_handler.add_subscriber(Adrien)


def loop():
    evt_handler.publish()

    fen.after(75, loop)


loop()

fen.bind_all("<KeyPress>", evt_handler.evt_key_pressed)
fen.bind_all("<KeyRelease>", evt_handler.evt_key_released)
fen.mainloop()
