import tkinter as tk

val_spe = {"endl" : 65535, "cara" : 65534}
char_val = {' ': 0, 'X': 1, 'R': 2, 'L': 5, 'o': 9, 'g': 3, 'd': 4, 'K': 6, '[': 7, ']': 8, '0': 11, '1': 12, '2': 13, '3': 10, 'A': 17, 'Z': 18, 'E': 19, 'Y': 20, 'H': 21, 'N': 22, '+': 27, '{': 24, '}': 23, 'v': 26, '^': 25, 'C': 14, 'B': 15, 'M': 16, 'I': 501}
val_char = dict((v, k) for k, v in char_val.items())

class Tile:
    def __init__(self, canvas, img, val, x, y):
        self.val = val
        self.pos = (x, y)
        self.type = self.det_type()
        if canvas:
            if self.val != 0:
                self.rep = canvas.create_image(x, y, image=img, anchor="nw")
            else :
                self.rep = None
            self.highlight_rect = canvas.create_rectangle(x, y, x + 16, y + 16, state=tk.HIDDEN, outline="white")


    def det_type(self):
        if self.val != 0 and self.val < 500:
            return "Block"

        elif self.val > 500 and self.val < 1000 :
            return "Rope"

        elif self.val > 1000 :
            return "Death"

        return "Air"


    def __repr__(self):
        return "Tile(Type : " + self.type + ", Char : " + self.val + ")"

class Map :
    def __init__(self,canvas):
        self.tiles = []
        self.cara_pos = (480, 320)
        self.canvas = canvas
        self.initialized = False
        self.img_dict = self.build_dict()


    def build_dict(self):
        dict = {}
        for i in range(1,500) :
            try :
                dict[i] = tk.PhotoImage(file="Ressources/Terrain/" + str(i) + ".gif")
            except :
                break

        for i in range(501,600) :
            try:
                dict[i] = tk.PhotoImage(file="Ressources/Terrain/" + str(i) + ".gif")
            except:
                break

        for i in range(1001,1100) :
            try:
                dict[i] = tk.PhotoImage(file="Ressources/Terrain/" + str(i) + ".gif")
            except:
                break

        return dict

    def clean_tiles(self):
        if self.tiles :
            for line in self.tiles :
                for tile in line :
                    if tile.rep :
                        self.canvas.delete(tile.rep)
                    self.canvas.delete(tile.highlight_rect)
                del(line)
            del(self.tiles)
            self.tiles = []

    def save_bin_level(self, file_name, absolute=False):
        with open("Ressources/Maps/" + file_name if not absolute else file_name, "wb") as file:
            for i, line in enumerate(self.tiles):
                for j, tile in enumerate(line):
                    if (j * 16, i * 16) == self.cara_pos:
                        print("char found write")
                        file.write(val_spe['cara'].to_bytes(2, "big"))
                    else:
                        file.write(tile.val.to_bytes(2, "big"))
                file.write(b'\xff\xff')


    def open_blank(self):
        self.clean_tiles()
        for i in range(40) :
            self.tiles.append([])
            for j in range(60) :
                self.tiles[-1].append(Tile(self.canvas, None, 0, j * 16, i * 16))

        self.initialized = True

        #print(len(self.tiles), len(self.tiles[-1]))

    def open_bin_level(self, file_name, absolute=False):
        self.clean_tiles()
        with open("Ressources/Maps/" + file_name if not absolute else file_name, "rb") as file:
            content = file.read()

        self.tiles.append([])
        nb_y = 0
        x = 0
        for i in range(0, len(content), 2):
            if nb_y > 39:
                break
            val = int.from_bytes(content[i:i + 2], "big")

            if x > 59 or val == val_spe["endl"]:
                for j in range(x + 1, 60):
                    self.tiles[-1].append(Tile(self.canvas, None, 0, j * 16, nb_y * 16))
                nb_y += 1
                if nb_y > 39:
                    break
                x = 0
                self.tiles.append([])

            elif val == val_spe["cara"]:
                print("char found bin")
                self.cara_pos = (x * 16, nb_y * 16)
                self.tiles[-1].append(Tile(self.canvas, None, 0, x * 16, nb_y * 16))
                x += 1

            elif val == 0 :
                self.tiles[-1].append(Tile(self.canvas, None, 0, x * 16, nb_y * 16))
                x += 1

            elif val in self.img_dict:
                self.tiles[-1].append(Tile(self.canvas, self.img_dict[val], val, x * 16, nb_y * 16))
                x += 1

        for j in range(nb_y + 1, 41):
            self.tiles.append([])
            for i in range(60):
                self.tiles[-1].append(Tile(self.canvas, None, 0, i * 16, j * 16))

        self.initialized = True


    def open_level(self, file_name, absolute=False):
        self.clean_tiles()
        with open("Ressources/Maps/" + file_name if not absolute else file_name) as file:
            line = file.readline()
            nb_y = 0
            while line:
                if nb_y > 39:
                    break
                nb_x = 0
                self.tiles.append([])
                for i, char in enumerate(line):
                    if i > 59:
                        break
                    nb_x = i
                    if not char in ['P']:
                        if (char in char_val) and char != ' ' :
                            self.tiles[-1].append(Tile(self.canvas, self.img_dict[char_val[char]], char_val[char], i * 16, nb_y * 16))
                        else :
                            self.tiles[-1].append(Tile(self.canvas, None, 0, i * 16, nb_y * 16))
                    else:
                        print("char found open")
                        self.cara_pos = (i * 16, nb_y * 16)
                        self.tiles[-1].append(Tile(self.canvas, None, 0, i * 16, nb_y * 16))
                for i in range(nb_x + 1, 60):
                    self.tiles[-1].append(Tile(self.canvas, None, 0, i * 16, nb_y * 16))

                nb_y += 1
                line = file.readline()
            for j in range(nb_y + 1, 41):
                self.tiles.append([])
                for i in range(60):
                    self.tiles[-1].append(Tile(self.canvas, 0, i * 16, j * 16))

            self.initialized = True

    def highlight_tile(self,x,y):
        if x < 0 or x >= 960 or y < 0 or y >= 640:
            return
        self.canvas.itemconfig(self.tiles[y//16][x//16].highlight_rect, state=tk.NORMAL)

    def unhighlight_tile(self,x,y):
        if x < 0 or x >= 960 or y < 0 or y >= 640:
            return
        self.canvas.itemconfig(self.tiles[y//16][x//16].highlight_rect, state=tk.HIDDEN)

    def change_tile(self,x,y,val):
        tile = self.tiles[y//16][x//16]
        if tile.rep :
            if val :
                self.canvas.itemconfig(self.tiles[y//16][x//16].rep, image = self.img_dict[val])
            else :
                self.canvas.delete(tile.rep)
                tile.rep = None
        else :
            tile.rep = self.canvas.create_image(tile.pos[0], tile.pos[1], image= self.img_dict[val] if val else None, anchor="nw")

        tile.val = val
