from Modules.animator import Animator
from Modules.physics import Tile

import tkinter as tk


class Character:
    def __init__(self, x, y, canvas, physics):
        self.animator = Animator(canvas, x, y)
        self.physics = physics
        self.x = x
        self.y = y
        self.vit_dep_hor = 5
        self.vit_dep_vert = 10
        self.dx = 0
        self.dy = 0
        self.infos = physics.get_infos(x,y)

        self.state = "ground"  # ground/jump/rope
        self.command = "normal" # normal/death/reset
        self.lrintent = "None"
        self.udintent = "None"
        self.update = False

        self.num_goal = 0

    def reset_to(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.state = "ground"
        self.command = "normal"
        self.lrintent = "None"
        self.udintent = "None"
        self.update = False
        self.animator.change_state("idle")
        self.animator.change_dir("r")
        self.animator.move_to(x,y)
        self.num_goal = 0

    def next_step(self, key_pressed, key_released):
        change = False
        self.update = not self.update

        if self.state == "jump":
            if self.dy < 16:
                if self.dy >= 0:
                    if self.animator.state != "falling":
                        self.animator.change_state("falling")
                        self.dy += 2
                        change = True

                self.dy += 1

        elif self.animator.state == "landing":
            self.animator.change_state("running") if self.dx != 0 else self.animator.change_state("idle")
            change = True

        if "Right" in key_pressed and not "Right" in key_released:
            print("go right")
            self.dx = self.vit_dep_hor
            self.animator.change_dir("r")
            self.lrintent = "Right"
            change = True

        elif "Left" in key_pressed and not "Left" in key_released:
            print("go left")
            self.dx = -self.vit_dep_hor
            self.animator.change_dir("l")
            self.lrintent = "Left"
            change = True

        elif ("Right" in key_released and self.animator.dir == "r") or (
                "Left" in key_released and self.animator.dir == "l"):
            print("stop")
            self.dx = 0
            self.lrintent = "None"
            if self.state == "ground":
                self.animator.change_state("idle")
                change = True

        if "Up" in key_pressed:
            self.udintent = "Up"
            if self.state == "ground":
                print("jump")
                self.dy = -self.vit_dep_vert
                self.state = "jump"

                self.animator.change_state("rising")
                change = True

            if self.state == "rope":
                print("climb")
                self.dy = -(self.vit_dep_vert // 3)

        if "Up" in key_released:
            self.udintent = "None"
            if self.state == "jump" and self.dy < -4:
                self.dy = -4
            elif self.state == "rope":
                self.dy = 0

        if "Down" in key_pressed:
            self.udintent = "Down"
            if self.state == "rope":
                self.dy = self.vit_dep_vert // 3

        if "Down" in key_released:
            self.udintent = "None"
            if self.state == "rope":
                self.dy = 0

        if self.dx != 0 and self.state == "ground" and self.animator.state != "running":
            self.animator.change_state("running")


        self.x += self.dx
        self.y += self.dy

        # for e in ["Self","Right","Left"] :
        #     self.physics.map.canvas.itemconfig(self.infos[e].highlight_rect,state=tk.HIDDEN)

        self.infos = self.physics.get_infos(self.x, self.y)

        # for e in ["Self","Right","Left"]:
        #     self.physics.map.canvas.itemconfig(self.infos[e].highlight_rect,state=tk.NORMAL)

        if self.infos["Self"].type == "Rope" and self.state != "rope":
            print("Rope")
            self.state = "rope"
            self.dy = 0
            self.animator.change_state("climbing")
            change = True

        if self.dy < 0 and self.infos["Up"].type == "Block":
            print("bump up")
            if self.state != "rope" :
                self.animator.change_state("falling")
                self.state = "jump"
                self.dy = 2
                self.y += 10
            else :
                self.y += -self.dy




            self.infos = self.physics.get_infos(self.x, self.y)

        if self.dx < 0 and (self.infos["Left"].type == "Block" or self.infos["UpLeft"].type == "Block"):
            print("bump left")
            self.dx = 0
            self.x = self.infos["Left"].pos[0] + 23
            self.infos = self.physics.get_infos(self.x, self.y)


        elif self.dx > 0 and (self.infos["Right"].type == "Block" or self.infos["UpRight"].type == "Block"):
            print("bump right")
            self.dx = 0
            self.x = self.infos["Right"].pos[0] - 8
            self.infos = self.physics.get_infos(self.x, self.y)

        elif self.lrintent != "None" and self.dx == 0:
            if self.infos[self.lrintent].type != "Block" and self.infos["Up" + self.lrintent].type != "Block":
                print("intent : ", self.lrintent)
                self.dx = self.vit_dep_hor if self.lrintent == "Right" else -self.vit_dep_hor
                if self.state == "ground":
                    self.animator.change_state("running")

        if self.udintent != "None" and self.dy == 0:
            if self.state == "rope" and self.udintent == "Up" and self.infos["Up"].type != "Block":
                print("udintent :", self.udintent)
                self.dy = -self.vit_dep_vert // 3
            elif self.udintent == "Down" and self.infos["Down"].type == "Rope":
                print("udintent :", self.udintent)
                self.dy = self.vit_dep_vert // 3
                self.state = "rope"
                self.animator.change_state("climbing")
                change = True

        if (self.state == "jump" and (self.infos["Down"].type == "Block" or self.infos["Down"].type == "Rope")) or (
            self.state == "rope" and self.infos["Down"].type == "Block"):
            print("land : ", self.infos["Self"].type)
            self.dy = 0
            self.state = "ground"
            self.y = self.infos["Down"].pos[1] - 16

            if self.infos["Self"].type != "Rope" :
                self.animator.change_state("landing")
            change = True

        elif self.infos["Down"].type != "Block" and self.state != "jump" and self.infos["Self"].type != "Rope":
            print("fall")
            self.state = "jump"
            self.animator.change_state("falling")
            change = True
            self.y += 5
            self.dy = 3


        self.animator.move_to(self.x, self.y)
        if not change and self.update:
            self.animator.next_frame(self.dx != 0 or self.dy != 0)

        if self.infos["Left"].type == "Death" or self.infos["Right"].type == "Death" or "r" in key_pressed or "R" in key_pressed:
            self.command = "death"

        if self.infos["Left"].type == "Goal" or self.infos["Right"].type == "Goal" or self.infos["UpLeft"].type == "Goal" or self.infos["UpRight"].type == "Goal" :
            self.num_goal += 1
            print("Goal",self.num_goal)

            if self.infos["UpRight"].type == "Goal":
                self.infos["UpRight"].clear()

            elif self.infos["UpLeft"].type == "Goal":
                self.infos["UpLeft"].clear()

            elif self.infos["Right"].type == "Goal" :
                self.infos["Right"].clear()

            elif self.infos["Left"].type == "Goal" :
                self.infos["Left"].clear()

            if self.num_goal == len(self.physics.map.goal_tiles) :
                self.command = "win"



        # print(self.infos,"\n---- Next Frame ----")
        return True
