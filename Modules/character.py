from Modules.animator import Animator
from Modules.physics import Tile

import tkinter as tk


class Character:
    def __init__(self, x, y, width, height, canvas, physics):
        self.animator = Animator(canvas, x, y)
        self.physics = physics
        self.x = x
        self.y = y
        self.vit_dep_hor = 5
        self.vit_dep_vert = 10
        self.dx = 0
        self.dy = 0
        self.infos = self.physics.get_infos(self.x,self.y)

        self.state = "ground" # ground/jump/landing
        self.jump_timer = 0
        self.jump_start = 0



    def next_step(self, key_pressed, key_released):
        change = False

        if self.state == "jump":
            if self.dy < 10:
                if self.dy >= 0 :
                    if self.animator.state != "falling" :
                        self.animator.change_state("falling")
                        change = True
                self.dy += 1

        elif self.animator.state == "landing" :
            self.animator.change_state("running") if self.dx != 0 else self.animator.change_state("idle")
            change = True



        if "Right" in key_pressed and not "Right" in key_released:
            self.dx = self.vit_dep_hor
            self.animator.change_dir("r")
            if self.state == "ground" :
                self.animator.change_state("running")
            change = True

        elif "Left" in key_pressed and not "Left" in key_released:
            self.dx = -self.vit_dep_hor
            self.animator.change_dir("l")
            if self.state == "ground":
                self.animator.change_state("running")
            change = True

        elif ("Right" in key_released and self.animator.dir == "r") or (
                "Left" in key_released and self.animator.dir == "l"):
            self.dx = 0
            if self.state == "ground" :
                self.animator.change_state("idle")
                change = True



        if "Up" in key_pressed and self.state == "ground":
            self.dy = -self.vit_dep_vert
            self.jump_timer = 0
            self.jump_start = self.y
            self.state = "jump"

            self.animator.change_state("rising")
            change = True

        if "Up" in key_released and self.dy < -4 :
            self.dy = -4



        if not change:
            self.animator.next_frame()

        self.x += self.dx
        self.y += self.dy

        # for e in ["DownLeft"]:#self.infos :
        #     self.physics.canvas.itemconfig(self.infos[e].highlight,state=tk.HIDDEN)


        self.infos = self.physics.get_infos(self.x, self.y)

        # for e in ["DownLeft"]:#self.infos :
        #     self.physics.canvas.itemconfig(self.infos[e].highlight,state=tk.NORMAL)


        if self.state == "jump" and (self.infos["Down"].type == "Block" or (self.dx > 0 and self.infos["DownRight"] == "Block") or (self.dx < 0 and self.infos["DownLeft"] == "Block"))  :

            self.dy = 0
            self.state = "ground"
            self.y = self.infos["Down"].pos[1] - 16

            self.animator.change_state("landing")

        if self.dx < 0 and (self.infos["Left"].type == "Block" or self.infos["UpLeft"].type == "Block") :
            self.dx = 0
            self.x = self.infos["Left"].pos[0]+23

        if self.dx > 0 and (self.infos["Right"].type == "Block" or self.infos["UpRight"].type == "Block"):
            self.dx = 0
            self.x = self.infos["Right"].pos[0]-9

        self.animator.move_to(self.x, self.y)

