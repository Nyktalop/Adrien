from Modules.animator import Animator


class Entity:
    def __init__(self, x, y, width, height, canvas):
        self.animator = Animator(canvas, x, y)
        self.x = x
        self.y = y
        self.vit_dep_hor = 5
        self.vit_dep_vert = 10
        self.dx = 0
        self.dy = 0

        self.state = "ground" # ground/jump/landing
        self.jump_timer = 0
        self.jump_start = 0


    def next_step(self, key_pressed, key_released):
        change = False



        if self.state == "jump":
            if self.y >= self.jump_start :
                self.dy = 0
                self.state = "ground"
                self.y = self.jump_start

                self.animator.change_state("landing")
                change = True

            elif self.dy < 10 :
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

        self.animator.move_to(self.x, self.y)
