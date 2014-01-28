import pyglet
import menu
import load, player, menu, interface, main2

collision_group = []

# Loads maps from res/maps.
class Maps:
    def __init__(self, group, batch):
        self.group = group
        self.batch = batch
        self.tile_x = -32
        self.tile_y = menu.WINDOW_SIZE_Y-32
        self.sprites = collision_group
        
        self.sand_load = pyglet.image.load("res/images/sand.jpg")
        self.brick_load = pyglet.image.load("res/images/brick.png")
        self.brickl_load = pyglet.image.load("res/images/brick-left.png")
        self.brick_sand = pyglet.image.load("res/images/brick-sand.jpg")
        self.stone_sand = pyglet.image.load("res/images/stone-sand.jpg")
        self.key = pyglet.image.load("res/images/key.png")
        self.coin = pyglet.image.load("res/images/coin.png")
        self.torch = pyglet.image.load("res/images/torch.png")
        
    def draw_map(self, mapfile):
        with open("res/maps/" + mapfile, "rt") as map_file:
            map_data = map_file.read()
            
            # s = sand (bg)
            # u = brick under sand (bg)
            # ; = stone under stand (bg)
            # b = brick
            # t = torch
            # l = main brick shadow on left
            # k = key
            # c = coin
            for letter in map_data:
                if letter == "s":
                    self.sand_sprite = pyglet.sprite.Sprite(self.sand_load, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.sand_sprite)
                     
                elif letter == "b":
                    self.brick_sprite = pyglet.sprite.Sprite(self.brick_load, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.brick_sprite)

                elif letter == "u":
                    self.bricksand_sprite = pyglet.sprite.Sprite(self.brick_sand, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.bricksand_sprite)

                elif letter == ";":
                    self.stonesand_sprite = pyglet.sprite.Sprite(self.stone_sand, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.stonesand_sprite)
                    
                elif letter == "l":
                    self.brickl_sprite = pyglet.sprite.Sprite(self.brickl_load, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.brickl_sprite)
                    
                elif letter == "k":
                    self.key_sprite = pyglet.sprite.Sprite(self.key, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.key_sprite)

                elif letter == "c":
                    self.coin_sprite = pyglet.sprite.Sprite(self.coin, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.coin_sprite)
                    
                elif letter == "t":
                    self.torch_sprite = pyglet.sprite.Sprite(self.torch, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.torch_sprite)
                 
                elif letter == "[":
                    self.tile_x = 0
                 
                elif letter == "]":
                    self.tile_y -= 32
                      
                self.tile_x += 32
                
    def return_sprites(self):
        return set(self.sprites)

#     def return_sprites_x(self):
#         for objects in self.return_sprites():
#             self.sprites_x.append(objects.x)
#         return self.sprites_x
