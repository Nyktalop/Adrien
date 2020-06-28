import tkinter as tk

class Tile :
    def __init__(self,canvas,char,x,y):
        self.type = self.det_type(char)
        self.char = char
        self.pos = (x,y)
        if canvas :
            if self.type != "Air" :
                self.img = tk.PhotoImage(file="Ressources/Terrain/" + char + ".gif")
                self.rep = canvas.create_image(x,y,image=self.img,anchor="nw")
            self.highlight = canvas.create_rectangle(x, y, x + 16, y + 16, state=tk.HIDDEN, outline="white")

    @staticmethod
    def det_type(char):
        if char in ['X','R','L','o','g','d','K','[',']'] :
            return "Block"

        return "Air"



class Physics :
    def __init__(self, canvas):
        self.canvas = canvas
        self.tiles = []
        self.char_pos = (480, 320)

    def open_level(self, file_name):
        with open("Ressources/Maps/" + file_name) as file :
            line = file.readline()
            nb_y = 0
            while line :
                if nb_y > 39 :
                    break
                nb_x = 0
                self.tiles.append([])
                for i, char in enumerate(line) :
                    if i > 59 :
                        break
                    nb_x = i
                    if not char in ['P'] :
                        self.tiles[-1].append(Tile(self.canvas, char, i * 16, nb_y * 16))
                    else :
                        self.char_pos = (i * 16, nb_y * 16)
                        self.tiles[-1].append(Tile(self.canvas, " ", i * 16, nb_y * 16))
                for i in range(nb_x+1,60) :
                    self.tiles[-1].append(Tile(self.canvas, " ", i * 16, nb_y * 16))

                nb_y += 1
                line = file.readline()
            for j in range(nb_y+1,41) :
                self.tiles.append([])
                for i in range(60):
                    self.tiles[-1].append(Tile(self.canvas, " ", i * 16, j * 16))



    def get_tile_type(self,x,y):
        if x < 0 or x >= 960 or y < 0 or y >= 640 :
            return "Block"

        return self.tiles[y//16][x//16].type

    def get_tile(self,x,y):
        if x < 0 or x >= 960 or y < 0 or y >= 640 :
            return Tile(None,"X",16*(x//16),16*(y//16))

        return self.tiles[y//16][x//16]

    def get_init_char_pos(self):
        return self.char_pos

    def get_infos(self,x,y):
        infos = {}
        infos["Up"] = self.get_tile(x,y-14)
        infos["UpLeft"] = self.get_tile(x-8,y-14)
        infos["UpRight"] = self.get_tile(x+8,y-14)
        infos["Down"] = self.get_tile(x,y+20)
        infos["DownLeft"] = self.get_tile(x-8,y+20)
        infos["DownRight"] = self.get_tile(x+8,y+20)
        infos["Left"] = self.get_tile(x-8,y+5)
        infos["Right"] = self.get_tile(x+8,y+5)

        return infos
