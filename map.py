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
        
        # Load all the necessary images for the maps.
        self.sand_load = pyglet.image.load("res/images/sand.jpg")
        self.brick_load = pyglet.image.load("res/images/brick.png")
        self.brickl_load = pyglet.image.load("res/images/brick-left.png")
        self.brick_sand = pyglet.image.load("res/images/brick-sand.jpg")
        self.stone_sand = pyglet.image.load("res/images/stone-sand.jpg")
        self.key = pyglet.image.load("res/images/key.png")
        self.coin = pyglet.image.load("res/images/coin.png")
        self.torch = pyglet.image.load("res/images/torch.png")
        self.gate = pyglet.image.load("res/images/gate.png")
        self.exit_gate = pyglet.image.load("res/images/chain2.png")
     
        
    ### Impliment Dictionaries in order to increase readability of code  
    def draw_map(self, mapfile):
        with open("res/maps/" + mapfile, "rt") as map_file:
            map_data = map_file.read()
            # Here is what each letter corresponds to:
            # s = sand (bg)
            # u = brick under sand (bg)
            # ; = stone under sand (bg)
            # b = brick
            # t = torch
            # l = brick shadow on left (main)
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

                elif letter == "e":
                    self.exit_sprite = pyglet.sprite.Sprite(self.exit_gate, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.exit_sprite) # See above

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
                    
                elif letter == "l":
                    self.brickl_sprite = pyglet.sprite.Sprite(self.brickl_load, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.brickl_sprite) # See above
                    
                elif letter == "k":
                    self.key_sprite = pyglet.sprite.Sprite(self.key, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.key_sprite) # See above

                elif letter == "c":
                    self.coin_sprite = pyglet.sprite.Sprite(self.coin, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.coin_sprite) # See above
                    
                elif letter == "t":
                    self.torch_sprite = pyglet.sprite.Sprite(self.torch, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.torch_sprite) # See above
                    
                elif letter == "g":
                    self.gate_sprite = pyglet.sprite.Sprite(self.gate, x=self.tile_x,
                                                       y=self.tile_y, batch=self.batch,
                                                       group=self.group)
                    self.sprites.append(self.gate_sprite) # See above
                 
                elif letter == "[":
                    self.tile_x = 0
                 
                elif letter == "]":
                    self.tile_y -= 32
                      
                self.tile_x += 32      
            #print(self.sprites)

    def list_set_sprites(self, mapfile):
        draw_map(self, mapfile)
        return(list(set(self.sprites)))
        
    def return_sprites(self):
        return set(self.sprites)

    def return_srectangles(self):
        self.rect_array = []
        for sprite in self.return_sprites():
            self.rect_array.append(Rect(sprite.x, sprite.y, 
                                          sprite.x + sprite.width, 
                                          sprite.y + sprite.height))
        return set(self.rect_array)      

