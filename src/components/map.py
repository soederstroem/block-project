import pygame
from pathlib import Path
from components.tile import Tile, tiles
from modules.toggle_module import ToggleModule

class Map:

    def __init__(self, id="test"):
        self.file = Path(__file__).resolve().parent.parent.parent/"assets"/"maps"/f"{id}.map"
        self.tiles = {}
        self.plr_spawn_pos = pygame.math.Vector2(0, 0)
        self.offset = pygame.math.Vector2(0, 300)
        self.bkg = Path(__file__).resolve().parent.parent.parent/"assets"/"img"/f"test_bkg.webp"

        self.load_tiles()

    def load_tiles(self):
        self.tiles.clear()
        self.tile_data = []

        tiles_loaded = False
        with open(self.file) as f:
            for line in [l.rstrip() for l in f]:
                if line == '_':
                    tiles_loaded = True
                if not tiles_loaded:
                    self.tile_data.append(line.split(','))
                elif tiles_loaded and line != '_':
                    print(line)
                else: continue

        for y, line in enumerate(self.tile_data):
            for x,col in enumerate(line):
                coord = (x*50 + self.offset.x, y*50 + self.offset.y)
                match col:
                    case '':
                        pass
                    case '1':
                        tile = Tile(coord)
                        self.tiles[(x,y)] = tile
                    case 'p':
                        self.plr_spawn_pos = coord
                    case 't':
                        tile = Tile(coord, ToggleModule(role="t"))
                        tile.image.fill("green")
                    case 'T':
                        tile = Tile(coord, ToggleModule(role="s"))
                        tile.image.fill("green")

        for (gx,gy), tile in self.tiles.items():
            tile.neighbors["up"] = self.tiles.get((gx, gy-1))
            tile.neighbors["down"] = self.tiles.get((gx, gy+1))
            tile.neighbors["left"] = self.tiles.get((gx-1, gy))
            tile.neighbors["right"] = self.tiles.get((gx+1, gy))

    def load(self, plr):
        plr.set_pos(self.plr_spawn_pos)


