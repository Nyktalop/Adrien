import tkinter as tk


class Animator:
    def __init__(self, canvas, x=480, y=320):
        self.state = "idle"
        self.dir = "r"
        self.frame_num = 0
        self.frames = {}
        self.num_frames = {}

        self.build_frames()

        self.canvas = canvas
        self.img = canvas.create_image(x, y, image=self.frames["idle_r_0"])

        self.hitbox = canvas.create_rectangle(x - 7, y - 13, x + 7, y + 13,state=tk.HIDDEN)

    def build_frames(self):
        for dir in ['r', 'l']:
            for state in ["idle", "running", "rising", "falling", "landing"]:
                for index in range(20):
                    name = state + "_" + dir + "_" + str(index)
                    try:
                        self.frames[name] = tk.PhotoImage(file="Ressources/Adrien/" + name + ".gif")
                        self.num_frames[state] = index + 1
                    except:
                        break

    def next_frame(self):
        change = False
        if self.state in ["idle", "running"]:
            self.frame_num = (self.frame_num + 1) % self.num_frames[self.state]
            change = True

        elif self.state in ["rising", "falling","landing"] and self.frame_num < self.num_frames[self.state] - 1:
            self.frame_num += 1
            change = True

        if change:
            self.canvas.itemconfig(self.img, image=self.frames[self.state + "_" + self.dir + "_" + str(self.frame_num)])

    def change_state(self, state):
        if state in ["idle", "running", "landing", "rising", "falling"]:
            self.state = state
            self.frame_num = 0
            self.canvas.itemconfig(self.img, image=self.frames[self.state + "_" + self.dir + "_0"])

    def change_dir(self, dir):
        if dir in ["r", "l"]:
            self.dir = dir
            self.canvas.itemconfig(self.img, image=self.frames[self.state + "_" + self.dir + "_" + str(self.frame_num)])

    def move_to(self, x, y):
        self.canvas.coords(self.img, x, y)
        self.canvas.coords(self.hitbox, x-7, y-13,x+7,y+13)
