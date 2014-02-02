import pyglet


WINDOW_SIZE_X = 1300
WINDOW_SIZE_Y = 1000

# Loads maps from res/maps.
class Maps:
    def __init__(self, group, batch):
        # Make sure the maps are in the correct group and batch.
        self.group = group
        self.batch = batch
        # The starting position for the tile is -32 because
        # the width and height is 32x32
        self.tile_x = -32
        # Same goes for the placement of the tile's y value.
        self.tile_y = WINDOW_SIZE_Y-32
        self.sprites = []
        self.objects = []
        self.coins = []
        self.kgate = []
        self.egate = []
        self.keys = []
        self.torches = []
        
        # Load all the necessary images for the maps.
        self.sand_load = pyglet.image.load("res/images/sand.jpg")
        self.brick_load = pyglet.image.load("res/images/brick.png")
        self.brick_1x38 = pyglet.image.load("res/images/brick-1x38.png")
        self.brick_3x12 = pyglet.image.load("res/images/brick-3x12.png")
        self.brick_13x1 = pyglet.image.load("res/images/brick-13x1.png")
        self.brick_27x1 = pyglet.image.load("res/images/brick-27x1.png")
        self.brick_3x1 = pyglet.image.load("res/images/brick-3x1.png")
        self.brick_1x3 = pyglet.image.load("res/images/brick-1x3.png")
        self.brick_1x6 = pyglet.image.load("res/images/brick-1x6.png")
        self.brick_1x22 = pyglet.image.load("res/images/brick-1x22.png")
        
        self.brick_sand = pyglet.image.load("res/images/brick-sand.jpg")
        self.stone_sand = pyglet.image.load("res/images/stone-sand.jpg")
        self.key = pyglet.image.load("res/images/key.png")
        self.coin = pyglet.image.load("res/images/coin.png")
        self.torch = pyglet.image.load("res/images/torch.png")
        self.gate = pyglet.image.load("res/images/gate.png")
        self.exit_gate = pyglet.image.load("res/images/chain2.png")
        self.gray_stone = pyglet.image.load("res/images/gray_stone.png")
        self.gray_sand_stone = pyglet.image.load("res/images/gray_brick.png")
        self.wooden = pyglet.image.load("res/images/walk.png")
     
        
    ### Impliment Dictionaries in order to increase readability of code  
    def draw_map(self, mapfile):
        with open("res/maps/" + mapfile, "rt") as map_file:
            map_data = map_file.read()
            # Here is what each letter corresponds to:
            # s = sand (bg)
            # 3 = brick 1x38
            # 1 = brick 1x3
            # 3 = brick 3x12
            # 2 = 27x1
            # 4 = 3x1
            # 5 = 1x22
            # 6 = 1x6
            # 9 = 13x1
            # 7 = 27x1
            # u = brick under sand (bg)
            # ; = stone under sand (bg)
            # / = gray patterned sand (bg)
            # ? = gray patterned stone (bg)
            # b = brick
            # t = torch
            # k = key
            # c = coin
            # g = gate for key
            # e = gate for exit
            for letter in map_data:
                if letter == "s":
                    self.sand_sprite = pyglet.sprite.Sprite(self.sand_load, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    # Keep appending the sprites to the list.
                    # If we have a list of all the sprites perhaps
                    # we can iterate through them and see if they
                    # get hit by the player.
                    self.sprites.append(self.sand_sprite)
                     
                elif letter == "b":
                    self.brick_sprite = pyglet.sprite.Sprite(self.brick_load, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.brick_sprite) # See above
                    
                elif letter == "1":
                    self.b1x3 = pyglet.sprite.Sprite(self.brick_1x3, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.b1x3) # See above
                    
                elif letter == "3":
                    self.b1x38 = pyglet.sprite.Sprite(self.brick_1x38, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.b1x38) # See above
                    
                elif letter == "9":
                    self.b13x1 = pyglet.sprite.Sprite(self.brick_13x1, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.b13x1) # See above

                elif letter == "4":
                    self.b3x1 = pyglet.sprite.Sprite(self.brick_3x1, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.b3x1) # See above
                    
                elif letter == "5":
                    self.b1x22 = pyglet.sprite.Sprite(self.brick_1x22, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.b1x22) # See above
                    
                elif letter == "6":
                    self.b1x6 = pyglet.sprite.Sprite(self.brick_1x6, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.b1x6) # See above
                    
                elif letter == "7":
                    self.b27x1 = pyglet.sprite.Sprite(self.brick_27x1, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.b27x1) # See above

                elif letter == "e":
                    self.exit_sprite = pyglet.sprite.Sprite(self.exit_gate, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.exit_sprite) # See above
                    self.egate.append(self.exit_sprite)

                elif letter == "u":
                    self.bricksand_sprite = pyglet.sprite.Sprite(self.brick_sand, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.bricksand_sprite) # See above

                elif letter == ";":
                    self.stonesand_sprite = pyglet.sprite.Sprite(self.stone_sand, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.stonesand_sprite) # See above

                elif letter == "?":
                    self.graystone_sprite = pyglet.sprite.Sprite(self.gray_stone, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.graystone_sprite) # See above

                elif letter == "/":
                    self.graystonesand_sprite = pyglet.sprite.Sprite(self.gray_sand_stone, 
                                                                     x=self.tile_x, 
                                                                     y=self.tile_y, 
                                                                     batch=self.batch, 
                                                                     group=self.group)
                    self.sprites.append(self.graystonesand_sprite) # See above

                elif letter == "w":
                    self.wooden_sprite = pyglet.sprite.Sprite(self.wooden, 
                                                                     x=self.tile_x, 
                                                                     y=self.tile_y, 
                                                                     batch=self.batch, 
                                                                     group=self.group)
                    self.sprites.append(self.wooden_sprite) # See above
                    
                elif letter == "k":
                    self.key_sprite = pyglet.sprite.Sprite(self.key, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.keys.append(self.key_sprite) # See above

                elif letter == "c":
                    self.coin_sprite = pyglet.sprite.Sprite(self.coin, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.coins.append(self.coin_sprite) # See above
                    
                elif letter == "t":
                    self.torch_sprite = pyglet.sprite.Sprite(self.torch, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.torches.append(self.torch_sprite) # See above
                    
                elif letter == "g":
                    self.gate_sprite = pyglet.sprite.Sprite(self.gate, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.kgate.append(self.gate_sprite) # See above
                    self.sprites.append(self.gate_sprite)
                 
                elif letter == "[":
                    self.tile_x = 0
                 
                elif letter == "]":
                    self.tile_y -= 32
                      
                self.tile_x += 32      
            #print(self.sprites)

    def list_set_sprites(self, mapfile):
        return self.sprites
        
    def return_sprites(self):
        return set(self.sprites)
    
    def return_objects(self):
        return set(self.objects)
    
    def return_keys(self):
        return self.keys
    
    def return_torches(self):
        return set(self.torches)
    
    def return_keygate(self):
        return set(self.kgate)
    
    def return_exitgate(self):
        return set(self.egate)
        
    def return_coins(self):
        return set(self.coins)

#     def return_srectangles(self):
#         self.rect_array = []
#         for sprite in self.return_sprites():
#             self.rect_array.append(collision.Rect(sprite.x, sprite.y, 
#                                           sprite.x + sprite.width, 
#                                           sprite.y + sprite.height))
#         return set(self.rect_array)      

