import tkinter as tk
from Modules.character import Character
from Modules.evthandler import EvtHandler
from Modules.physics import Physics

class GameWindow :
    def __init__(self,width,height):
        self.fen = tk.Tk()
        self.fen.geometry("{}x{}".format(width,height))
        self.fen.title("  Adrien")
        self.fen.iconphoto(False, tk.PhotoImage(file="Ressources/icon.png"))

        self.canvas = tk.Canvas(self.fen, width=width, height=height, bg="#B0B0BB")
        self.canvas.grid(row=0, column=0)



class Game :
    def __init__(self):
        self.current_level = 2
        self.window = GameWindow(960, 640)
        self.physics = Physics(self.window.canvas)
        self.physics.map.open_bin_level(str(self.current_level))

        pos = self.physics.get_init_char_pos()
        self.char = Character(pos[0]+6, pos[1], self.window.canvas, self.physics)

        self.evt_handler = EvtHandler()
        self.evt_handler.add_subscriber(self.char)
        self.evt_handler.add_subscriber_list(self.physics.map.goal_tiles)

        self.window.fen.bind_all("<KeyPress>", self.evt_handler.evt_key_pressed)
        self.window.fen.bind_all("<KeyRelease>", self.evt_handler.evt_key_released)


    def load_level(self):
        self.physics.map.open_bin_level(str(self.current_level))
        self.evt_handler.reset()
        self.evt_handler.add_subscriber(self.char)
        self.evt_handler.add_subscriber_list(self.physics.map.goal_tiles)

        pos = self.physics.get_init_char_pos()
        self.char.reset_to(pos[0] + 6, pos[1])

    def run(self):
        self.loop()
        self.window.fen.mainloop()

    def after(self):
        self.window.fen.after(50,self.loop)


    def loop(self):
        self.evt_handler.publish()

        if self.char.command == "normal":
            self.window.fen.after_idle(self.after)

        elif self.char.command == "death":
            self.load_level()
            self.window.fen.after_idle(self.after)

        elif self.char.command == "win" :
            self.load_level()
            self.window.fen.after_idle(self.after)
