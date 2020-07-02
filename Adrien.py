import tkinter as tk
from Modules.character import Character
from Modules.evthandler import EvtHandler
from Modules.physics import Physics

fen = tk.Tk()
fen.geometry("960x640")
fen.title("  Adrien")
fen.iconphoto(False,tk.PhotoImage(file="Ressources/icon.png"))

canvas = tk.Canvas(fen, width=960, height=640, bg="#B0B0BB")
canvas.grid(row=0, column=0)

p = Physics(canvas)
p.map.open_bin_level("3")

pos = p.get_init_char_pos()
Adrien = Character(pos[0]+6, pos[1], 14, 26, canvas, p)


evt_handler = EvtHandler()
evt_handler.add_subscriber(Adrien)


def loop():
    evt_handler.publish()

    fen.after(50, loop)


loop()

fen.bind_all("<KeyPress>", evt_handler.evt_key_pressed)
fen.bind_all("<KeyRelease>", evt_handler.evt_key_released)
fen.mainloop()
