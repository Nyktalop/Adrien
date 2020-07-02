import tkinter as tk
from Modules.map import Map, Tile


class Physics:
    def __init__(self, canvas):
        self.map = Map(canvas)

    def get_tile_type(self, x, y):
        if x < 0 or x >= 960 or y < 0 or y >= 640:
            return "Block"

        return self.map.tiles[x // 16][y // 16].type

    def get_tile(self, x, y):
        if x < 0 or x >= 960 or y < 0 or y >= 640:
            return Tile(None, None, 1, 16 * (x // 16), 16 * (y // 16))

        return self.map.tiles[y // 16][x // 16]

    def get_init_char_pos(self):
        return self.map.cara_pos

    def get_infos(self, x, y):
        infos = {}
        infos["Self"] = self.get_tile(x,y)
        infos["Up"] = self.get_tile(x, y - 10)
        infos["UpLeft"] = self.get_tile(x - 8, y - 10)
        infos["UpRight"] = self.get_tile(x + 8, y - 10)
        infos["Down"] = self.get_tile(x, y + 20)
        infos["Left"] = self.get_tile(x - 8, y + 5)
        infos["Right"] = self.get_tile(x + 8, y + 5)

        return infos
