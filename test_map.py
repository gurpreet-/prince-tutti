import pyglet
from random import randint
from math import floor
from ctypes import POINTER, c_ubyte, cast

## Important defines.
WINDOW_SIZE_X = 1300
WINDOW_SIZE_Y = 1000
MUMMY_SPEED = 2
MUMMY_DASH = 3
PLAYER_SPEED = 2.10
##

class Rect:
    '''Fast rectangular collision structure'''
    
    def __init__(self, x1, y1, x2, y2):
        '''Create a rectangle from a minimum and maximum point'''
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        
    def intersect(self, r):
        '''Compute the intersection of two rectangles'''
        n = Rect( max(self.x1, r.x1), max(self.y1, r.y1), min(self.x2, r.x2), min(self.y2, r.y2) )
        return n
        
    def collides(self, r):
        '''Determine whether two rectangles collide'''
        if self.x2 < r.x1 or self.y2 < r.y1 or self.x1 > r.x2 or self.y1 > r.y2:
            return False
        return True
    
    @property
    def width(self):
        return self.x2 - self.x1
    
    @property
    def height(self):
        return self.y2 - self.y1
    
    def __repr__(self):
        return '[%d %d %d %d]' % (self.x1, self.y1, self.x2, self.y2)
    
    @staticmethod
    def from_sprite(s):
        '''Create a rectangle matching the bounds of the given sprite'''
        i = (s._texture if not s._animation else s._animation.frames[s._frame_index].image)
        x = int(s.x - i.anchor_x)
        y = int(s.y - i.anchor_y)
        return Rect(x, y, x + s.width+2, y + s.height+2)
    
def get_rect(sprite):
    '''Returns the bounding rectangle for the sprite'''
    return Rect.from_sprite(sprite)

def get_image(sprite):
    '''Returns the (potentially cached) image data for the sprite'''
    image_data_cache = {}
    # if this is an animated sprite, grab the current frame
    if sprite._animation:
        i = sprite._animation.frames[sprite._frame_index].image
    # otherwise just grab the image
    else:
        i = sprite._texture
    
    # if the image is already cached, use the cached copy
    if i in image_data_cache:
        d = image_data_cache[i]
    # otherwise grab the image's alpha channel, and cache it
    else:
        d = i.get_image_data().get_data('A', i.width)
        image_data_cache[i] = d
    
    # return a tuple containing the image data, along with the width and height
    return d, i.width, i.height
 
def collide(lhs, rhs, offset2=None):
    '''Checks for collision between two sprites'''
    
    # first check if the bounds overlap, no need to go further if they don't
    r1, r2 = get_rect(lhs), get_rect(rhs)
    if offset2 is not None:
        r2.x1 += offset2[0]
        r2.x2 += offset2[0]
        r2.y1 += offset2[1]
        r2.y2 += offset2[1]
        
    if r1.collides(r2):
        # calculate the overlapping area
        ri = r1.intersect(r2)
        
        # figure out the offsets of the overlapping area in each sprite
        offx1, offy1 = int(ri.x1 - r1.x1), int(ri.y1 - r1.y1)
        offx2, offy2 = int(ri.x1 - r2.x1), int(ri.y1 - r2.y1)
        
        # grab the image data
        d1, d2 = get_image(lhs), get_image(rhs)
        
        # and cast it to something we can operate on (it starts as a string)
        p1 = cast(d1[0], POINTER(c_ubyte))
        p2 = cast(d2[0], POINTER(c_ubyte))
        
        # for each overlapping pixel, check for a collision
        for i in range(0, ri.width):
            for j in range(0, ri.height):
                c1 = p1[(offx1+i) + (j + offy1)*d1[1]]
                c2 = p2[(offx2+i) + (j + offy2)*d2[1]]
                
                # if both pixels are non-empty, we have a collision
                if c1 > 0 and c2 > 0:
                    return True
    # no collision found
    return False

# Load the resources from the following folders,
# then re-index the file resource locations.
def load_resources():
    pyglet.resource.path = ["res",
                            "res/images",
                            "res/videos",
                            "res/fonts",
                            "res/music",
                            "res/maps"]
    
    pyglet.resource.reindex()

# Set the anchor points to the center of the image.
def center_anchor(image):
    image.anchor_x = image.width//2
    image.anchor_y = image.height//2

# Using center_anchor() set the anchor in the center,
# then return the resulting sprite.
def image_aligner(img, x_pos, y_pos, batch, group):
    image_load = pyglet.image.load(img) # First load the image
    center_anchor(image_load) # Then center the anchor points
    image = pyglet.sprite.Sprite(image_load, x=x_pos, # Convert to sprite
                                           y=y_pos,
                                           batch=batch,
                                           group=group)
    return image

# This returns true if the cursor is within an area
# that is 'clickable'
def get_area(img, x, y):
        if img.x - img.width/2 < x < img.x + img.width/2 and img.y - img.height/2 < y < img.y + img.height/2:
            return True
        
def get_sarea(img, x, y):
        if img.x < x < img.x + img.width and img.y < y < img.y + img.height:
            return True
        return False

# Draws a rectangle using the in-built commands of
# OpenGL.
class Rectangle(object):
    '''Draws a rectangle into a batch.'''
    def __init__(self, x1, y1, x2, y2, group, batch):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, group,
            ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c4B', [0, 0, 0, 255] * 4))


# Defines the Mummy, is able to set the Mummy's
# speed and inform is if the mummy is speeding up.
class Player(pyglet.sprite.Sprite):
    def __init__(self, x, y, batch, group):
        self.x_pos = x
        self.y_pos = y
        self.player_image = pyglet.image.load("res/images/player.png")
        self.the_player = pyglet.sprite.Sprite(img=self.player_image,
                                              x=self.x_pos, y=self.y_pos,
                                              batch=batch, group=group)
        self.speed = PLAYER_SPEED
        self.allowed_down = True
        self.allowed_up = True
        self.allowed_left = True
        self.allowed_right = True
        self.reset_bools()
        self.going_nowhere = True
        
    def allow_bools(self):
        self.allowed_down = True
        self.allowed_up = True
        self.allowed_left = True
        self.allowed_right = True
        
    def reset_bools(self):
        self.going_left = False
        self.going_right = False
        self.going_up = False
        self.going_down = False
        self.going_nowhere = False
        
    # Use this method only for testing speed up.
#     def speed_up(self):
#         self.speed = MUMMY_DASH
    
    def reset_speed(self):
        self.speed = PLAYER_SPEED
        
    def no_down(self):
        self.allowed_down = False

    def no_left(self):
        self.allowed_left = False

    def no_right(self):
        self.allowed_right = False

    def no_up(self):
        self.allowed_up = False
        
    def yes_down(self):
        self.allowed_down = True

    def yes_left(self):
        self.allowed_left = True

    def yes_right(self):
        self.allowed_right = True

    def yes_up(self):
        self.allowed_up = True
            
    def get_speed(self):
        return self.speed
    
    # Unschedule all movement if the mummy is going any other
    # direction other than down.
    # Why would we do this? To prevent the mummy from going in
    # any other direction other than 90 degree angles.
    def move_down(self):
        if self.going_left:
            pyglet.clock.unschedule(self.move_player_left)
            
        if self.going_right:
            pyglet.clock.unschedule(self.move_player_right)

        if self.going_up:
            pyglet.clock.unschedule(self.move_player_up)
            self.reset_bools()
            self.going_nowhere = True
        
        elif not self.going_down or self.going_nowhere:
            pyglet.clock.schedule_interval(self.move_player_down, 1/120.0)
            self.reset_bools() # Reset the bools...
            self.going_down = True # Then set the going down variable to true.
        
    def move_up(self):
        if self.going_left:
            pyglet.clock.unschedule(self.move_player_left)
        if self.going_right:
            pyglet.clock.unschedule(self.move_player_right)
        if self.going_down:
            pyglet.clock.unschedule(self.move_player_down)
            self.reset_bools()
            self.going_nowhere = True
        elif not self.going_up or self.going_nowhere:
            pyglet.clock.schedule_interval(self.move_player_up, 1/120.0)
            self.reset_bools()
            self.going_up = True
    
    def move_left(self):
        if self.going_up:
            pyglet.clock.unschedule(self.move_player_up)
        if self.going_down:
            pyglet.clock.unschedule(self.move_player_down)
        if self.going_right:
            pyglet.clock.unschedule(self.move_player_right)
            self.reset_bools()
            self.going_nowhere = True
        elif not self.going_left or self.going_nowhere:
            pyglet.clock.schedule_interval(self.move_player_left, 1/120.0)
            self.reset_bools()
            self.going_left = True
        
    def move_right(self):
        if self.going_up:
            pyglet.clock.unschedule(self.move_player_up)
        if self.going_down:
            pyglet.clock.unschedule(self.move_player_down)
        if self.going_left:
            pyglet.clock.unschedule(self.move_player_left)
            self.reset_bools()
            self.going_nowhere = True
        elif not self.going_right or self.going_nowhere:
            pyglet.clock.schedule_interval(self.move_player_right, 1/120.0)
            self.reset_bools()
            self.going_right = True

    def reset_x(self):
        self.the_player.x = 0
        
    def reset_y(self):
        self.the_player.y = 0
        
    def move_player_down(self, dt):
        if self.allowed_down:
            #self.going_nowhere = True
            self.the_player.y -= self.speed
            
    def move_player_up(self, dt):
        if self.allowed_up:
            #self.going_nowhere = True
            self.the_player.y += self.speed

    def move_player_left(self, dt):
        if self.allowed_left:
            #self.going_nowhere = True
            self.the_player.x -= self.speed
            
    def move_player_right(self, dt):
        if self.allowed_right:
            #self.going_nowhere = True
            self.the_player.x += self.speed
        
    def player_stop(self):
        self.speed = 0
        
    def get_y(self):
        return self.the_player.y
    
    def get_x(self):
        return self.the_player.x
    
    def return_pos(self):
        return self.the_player.position


# This class controls the overall mechanics of the game.
# It allows you to start screens which can be videos,
# main menu's or even levels. This is instantiated at
# the very beginning and is passed down to all screens.
class Game:
    def __init__(self):
        self.current_level = 0  # When we first create the game,
                                # the level is 0.
        self.current_screen = Video(self)

    def load(self):
        "Load progress from disk"
        pass
    
    def return_level(self):
        return self.current_level
    
    def load_actualgame(self):
        self.current_screen = ActualGame(game, self.current_level)
    
    def load_mainmenu(self):
        self.current_screen = MainMenu(self)

    def save(self):
        "Save progress to disk"
        pass

    def clear_current_screen(self):
        self.current_screen.clear()
        self.window.remove_handlers()

    # This is the method that handles the main events.
    # If the event is not here, then you can't use it.
    def start_current_screen(self):
        self.window.set_handler("on_key_press", self.current_screen.on_key_press)
        self.window.set_handler("on_draw", self.current_screen.on_draw)
        self.window.set_handler("on_mouse_press", self.current_screen.on_mouse_press)
        self.window.set_handler("on_mouse_motion", self.current_screen.on_mouse_motion)
        self.window.set_handler("on_eos", self.current_screen.on_eos)
        self.current_screen.start()

    def goto_next_level(self):
        "Called from within LevelPlayer when the player beats the level"
        self.clear_current_screen()
        self.current_level += 1
        self.current_screen = ActualGame(game, self.current_level)
        self.start_current_screen()
        
    def goto_bonus_level(self):
        "Called from within LevelPlayer when the player beats the level"
        self.clear_current_screen()
        self.bonus_level = str(self.current_level) + "bonus"
        self.current_screen = ActualGame(game, self.bonus_level)
        self.start_current_screen()

    def start_playing(self):
        "Called by the main menu when the user selects an option"
        self.clear_current_screen()
        self.current_screen = ActualGame(game, self.current_level)
        self.start_current_screen()

    # This method is called once: when the game starts.
    def execute(self):
        self.display = pyglet.canvas.Display().get_default_screen()
        self.window = pyglet.window.Window(caption="Prince Tutti",
                                           style='dialog',
                                           screen=self.display,
                                           #fullscreen=True,
                                           width=WINDOW_SIZE_X,
                                           height=WINDOW_SIZE_Y)
        # Try to set the window icon to the key.
        self.window.set_icon(pyglet.image.load("res/images/key.png"))
        #pyglet.gl.glScalef(1, 1, 1) # Can be used to scale the game's contents.
        self.start_current_screen()
        pyglet.app.run()

# This class is here so that you can make
# any large game-wide modifications to the screen.
class Screen:
    "Any pyglet methods not present here will not work anywhere."
    def __init__(self):
        pass
 
    def start(self):
        pass
 
    def clear(self):
        pass

    def on_key_press(self, key, modifiers):
        pass
    
    def on_mouse_press(self, x, y, button, modifiers):
        pass
    
    def on_mouse_motion(self, x, y, dx, dy):
        pass
    
    def on_eos(self):
        pass

    def on_draw(self):
        pass
    
# This class represents the Actual Game. The GUI,
# the maps are all initialised here.
class ActualGame(Screen):
    "This class contains all your game logic. This is the class that enables the user to play through a level."
    def __init__(self, game, level_to_play):
        self.game = game
        self.level = level_to_play
        self.interface_batch = pyglet.graphics.Batch()
        self.tile_batch = pyglet.graphics.Batch()
        
        # Set up the groups so that they stack correctly.
        self.text_group = pyglet.graphics.OrderedGroup(4)
        self.fg_group = pyglet.graphics.OrderedGroup(3)
        self.plank_group = pyglet.graphics.OrderedGroup(2)
        self.bg2_group = pyglet.graphics.OrderedGroup(1)
        self.bg_group = pyglet.graphics.OrderedGroup(0)
        
        # Create the graphical user interface
        self.interface = Interface(self.fg_group, self.text_group, self.interface_batch)
        self.wood_image = pyglet.image.load("res/images/woodenplank.png")
        self.plank = pyglet.sprite.Sprite(img=self.wood_image, x=0,
                                     y=WINDOW_SIZE_Y/1.17, batch=self.interface_batch,
                                     group=self.plank_group)
        # Load the maps
        self.b_map = Maps(self.bg_group, self.tile_batch)
        self.f_map = Maps(self.bg2_group, self.tile_batch)
        
        # Create the sound manager
        self.soundplayer = pyglet.media.ManagedSoundPlayer() # Load the sound player
        self.soundplayer.push_handlers(on_eos=self.on_eos)
        self.source = pyglet.media.StreamingSource() # Load the streaming device source
        self.audio_path = "res/music/bonus.mp3" # First queue the bonus music
        self.load_media = pyglet.media.load(self.audio_path)
        self.on_to_next = False
        self.soundplayer.queue(self.load_media)
        self.soundplayer.queue(pyglet.media.load("res/music/main.mp3")) # Then the main music
        self.soundplayer.play()

        # Create the actual player who plays in the game
        self.player = Player(68, 480, self.tile_batch, self.fg_group)
        self.o_x = 0
        self.o_y = 0
        # Useful for collision detection
        pyglet.clock.schedule_interval(self.gen_rects, 1/4.0)
        pyglet.clock.schedule_interval(self.detect, 1/2.0)
        pyglet.clock.schedule_interval(self.collision, 1/4.0)
#         pyglet.clock.schedule_interval(self.timer, 1/2.0)
        self.rectl = 0
        self.rectr = 0
        self.rectu = 0
        self.rectd = 0
        self.collided = False
        
    def gen_rects(self, dt):
        self.rectl = Rect(self.player.the_player.x-5, 
                          self.player.the_player.y+5, 
                          self.player.the_player.x+4, 
                          self.player.the_player.y+10)
        self.rectr = Rect(self.player.the_player.x-2, 
                          self.player.the_player.y+1, 
                          self.player.the_player.x+1, 
                          self.player.the_player.y+5)
        self.rectu = Rect(self.player.the_player.x+2, 
                          self.player.the_player.y+10, 
                          self.player.the_player.x+15, 
                          self.player.the_player.y+40)
        self.rectd = Rect(self.player.the_player.x, 
                            self.player.the_player.y-20, 
                            self.player.the_player.x+1, 
                            self.player.the_player.y-10)
        
    def detect(self, dt):
        # Check where the player is
        if (self.player.the_player.x > WINDOW_SIZE_X or 
            self.player.the_player.x < 0 or 
            self.player.the_player.y > WINDOW_SIZE_Y or
            self.player.the_player.y < 0):
            print("out of bounds")
            
    def collision(self, dt):
        self.player.allow_bools()
        for rectangles in self.f_map.return_sprites():
            if get_rect(rectangles).collides(self.rectl):
                self.player.no_left()
 
            if get_rect(rectangles).collides(self.rectr):
                self.player.no_right()
             
            if get_rect(rectangles).collides(self.rectu):
                self.player.no_up()
             
            if get_rect(rectangles).collides(self.rectd):
                self.player.no_down()
                
    def collision2(self, dt):
        for rectangles in self.f_map.return_sprites():
            if get_rect(rectangles).collides(get_rect(self.player.the_player)):
                self.collided = True
                self.player.the_player.x = self.o_x
                self.player.the_player.y = self.o_y
        self.collided = False
                
    def timer(self, dt):
        if not self.collided:
            self.o_x = self.player.the_player.x
            self.o_y = self.player.the_player.y

    def on_key_press(self, key, modifiers):
        if key == self.actual_keys.DOWN:
            self.player.move_down() # Move the player down if user hits down key
                                    # See Player class for more information
        elif key == self.actual_keys.UP:
            self.player.move_up()
        elif key == self.actual_keys.LEFT:
            self.player.move_left()
        elif key == self.actual_keys.RIGHT:
            self.player.move_right()
    
    def launch_map(self):
        self.str_level = str(self.level) # Convert the current level to a string
        # Append the suffix for the background and the foreground respectively.
        self.b_map.draw_map(self.str_level + "b.txt")
        self.f_map.draw_map(self.str_level + "m.txt")
        # If the level name contains the string 'bonus' then load the
        # bonus music, otherwise don't.
        if "bonus" in self.str_level:
            self.soundplayer.next()
        elif not ("bonus" in self.str_level):
            self.soundplayer.next()

    def start(self):
        self.actual_keys = pyglet.window.key
        self.game.window.set_mouse_cursor(self.game.window.get_system_mouse_cursor(None))
        self.launch_map()

    def new_game(self):
        self.game.start_playing()

    def on_draw(self):
        self.game.window.clear()
        self.tile_batch.draw()
        self.interface_batch.draw()
    
    # This method is called whenever the player reaches end of source.
    def on_eos(self):
        self.soundplayer.next()
        self.soundplayer.next()

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
                
    # Returns the list of sprites as a set.
    # A set allows for much faster iteration than a list.
    # A set is like a list.
    def return_sprites(self):
        return set(self.sprites)

    def return_srectangles(self):
        self.rect_array = []
        for sprite in self.return_sprites():
            self.rect_array.append(Rect(sprite.x, sprite.y, 
                                          sprite.x + sprite.width, 
                                          sprite.y + sprite.height))
        return set(self.rect_array)
    
# Use the interface class to manage the GUI elements
# on-screen. I have done it like this so that individual
# elements can be removed if necessary. 
class Interface:
    '''This class controls the GUI of the game.'''
    def __init__(self, group_images, group_text, batch):
        self.batch = batch
        self.group_images = group_images
        self.group_text = group_text
        
        self.scroll_handle_width = 20
        self.spacing = 20

        self.logo_image = pyglet.image.load("res/images/logo.png")
        self.logo = pyglet.sprite.Sprite(img=self.logo_image, x=self.spacing,
                                     y=WINDOW_SIZE_Y/1.17, batch=self.batch,
                                     group=self.group_images)
            
        self.score_image = pyglet.image.load("res/images/score_scroll.png")
        self.score_scroll = pyglet.sprite.Sprite(img=self.score_image, x=self.logo.width + self.spacing,
                                             y=WINDOW_SIZE_Y/1.17, batch=self.batch,
                                             group=self.group_images)
        
        # Gets the position where the lives, bonus, score container will start.
        # This is necessary because we may scale (or move) the scroll behind it at some point.
        # If we scale the scroll, then we lose the positioning.
        # The following code aims to stop the positioning of the messing up.
        # This code will position everything correctly even if you move the scroll.
        
        # First of all we need to find where the lives container will start.
        # And where it will end.
        self.livescontainer_start = self.score_scroll.x + self.scroll_handle_width
        self.livescontainer_end = self.livescontainer_start + self.score_scroll.width/4
    
        # The ending of the lives container is the start of the bonus container.
        self.bonuscontainer_start = self.livescontainer_end
        self.bonuscontainer_end = self.bonuscontainer_start + self.score_scroll.width/4
    
        # The ending of the bonus container is the start of the score container.
        self.scorecontainer_start = self.bonuscontainer_end
        self.scorecontainer_end = self.scorecontainer_start - self.scroll_handle_width + self.score_scroll.width/2
        
        # Initialise all the classes that control the GUI.
        self.score = Score(self.group_text, self.batch, self.scorecontainer_start,
                           self.score_scroll.y,
                           self.scorecontainer_end - self.scorecontainer_start,
                           self.score_scroll.height/1.5)
        
        self.lives = Lives(self.group_text, self.batch, self.livescontainer_start,
                           self.score_scroll.y,
                           self.livescontainer_end - self.livescontainer_start,
                           self.score_scroll.height/1.5)
        
        self.bonus = Bonus(self.group_text, self.batch, self.bonuscontainer_start,
                           self.score_scroll.y,
                           self.bonuscontainer_end - self.bonuscontainer_start,
                           self.score_scroll.height/1.5)
        
    # Call this whenever you need to update the score.
    def update_score_value(self):
        self.score.update_score()
    
    # Call this to return the score value.
    def get_score_value(self):
        self.score.return_score()

# Updates the score.
class Score(Interface):
    def __init__(self, group_text, batch, x, y, width, height):
        self.group_text = group_text
        self.batch = batch
        self.x_loc = x
        self.y_loc = y
        self.width = width
        self.height = height
        self.score_num = 0
        
        self.score_heading = "Score\n"
        self.document = pyglet.text.document.FormattedDocument(self.score_heading)
        self.document.set_style(0, len(self.document.text),
                                dict(color=(0, 0, 0, 255)))
         
         
        self.layout = pyglet.text.layout.IncrementalTextLayout(self.document,
                                                                self.width,
                                                                self.height,
                                                                multiline=True,
                                                                batch=self.batch,
                                                                group=self.group_text)
        
        self.position(self.layout, self.x_loc + self.width/2, self.y_loc)
        self.update_score()
        
    
    def return_score(self):
        return self.score_num
    
    def position(self, document, x, y):
        document.x = x
        document.y = y
    
    def update_score(self):
        self.score_num = str(43434)
        self.document.insert_text(len(self.document.text), self.score_num)

# Updates the lives.
class Lives(Interface):
    def __init__(self, group_text, batch, x, y, width, height):
        self.group_text = group_text
        self.batch = batch
        self.x_loc = x
        self.y_loc = y
        self.width = width
        self.height = height
        self.lives_num = 3
        
        self.lives_heading = "Lives\n"
        self.document = pyglet.text.document.FormattedDocument(self.lives_heading)
        self.document.set_style(0, len(self.document.text),
                                dict(color=(0, 0, 0, 255)))
         
         
        self.layout = pyglet.text.layout.IncrementalTextLayout(self.document,
                                                                self.width,
                                                                self.height,
                                                                multiline=True,
                                                                batch=self.batch,
                                                                group=self.group_text)
        
        self.position(self.layout, self.x_loc + self.width/2, self.y_loc)
        self.update_lives()
        
    
    def return_lives(self):
        return self.lives_num
    
    def position(self, document, x, y):
        document.x = x
        document.y = y
    
    def update_lives(self):
        self.lives_num = str(self.lives_num)
        self.document.insert_text(len(self.document.text), self.lives_num)

# Updates the bonus points.
class Bonus(Interface):
    def __init__(self, group_text, batch, x, y, width, height):
        self.group_text = group_text
        self.batch = batch
        self.x_loc = x
        self.y_loc = y
        self.width = width
        self.height = height
        self.bonus_num = 500
        
        self.bonus_heading = "Bonus\n"
        self.document = pyglet.text.document.FormattedDocument(self.bonus_heading)
        self.document.set_style(0, len(self.document.text),
                                dict(color=(0, 0, 0, 255)))
        self.document.set_paragraph_style(0, len(self.document.text), dict(align=("center")))
         
         
        self.layout = pyglet.text.layout.IncrementalTextLayout(self.document,
                                                                self.width,
                                                                self.height,
                                                                multiline=True,
                                                                batch=self.batch,
                                                                group=self.group_text)
        
        self.position(self.layout, self.x_loc + self.width/2, self.y_loc)
        self.update_bonus()
        
    
    def return_bonus(self):
        return self.bonus_num
    
    def position(self, document, x, y):
        document.x = x
        document.y = y
    
    def update_bonus(self):
        self.bonus_num = str(self.bonus_num)
        self.document.insert_text(len(self.document.text), self.bonus_num)
        
# This is the Main Menu screen which is loaded on game start.
# It includes all the methods necessary for the movement of
# elements.
class MainMenu(Screen):
    "This class presents the title screen and options for new game."
    def __init__(self, game):
        self.game = game
        pyglet.font.add_directory("res/fonts")
        # This is where the cloud starts
        self.cloud_start = -WINDOW_SIZE_X/10
        self.cloud_end = WINDOW_SIZE_X + WINDOW_SIZE_X/10
        self.window_half_x = WINDOW_SIZE_X/2
        
        self.batch = pyglet.graphics.Batch()
        self.fg_group = pyglet.graphics.OrderedGroup(4)
        self.bg_group_4 = pyglet.graphics.OrderedGroup(3)
        self.bg_group_3 = pyglet.graphics.OrderedGroup(2)
        self.bg_group_2 = pyglet.graphics.OrderedGroup(1)
        self.bg_group = pyglet.graphics.OrderedGroup(0)
        
        #self.rectangle = Rectangle(50, 50, 100, 100, self.fg_group, self.batch)
        
        # Whenever we create an image, we want to set its anchor point to its center.
        # We do this using image_aligner()
        # This is so that we don't have weirdly aligned images.
        self.logo = image_aligner("res/images/logo.png", self.window_half_x,
                                  WINDOW_SIZE_Y/2+300, self.batch, self.fg_group)
        
        self.pyramid = image_aligner("res/images/pyramids.png", self.window_half_x,
                                     WINDOW_SIZE_Y/3, self.batch, self.bg_group_3)
        
        self.sun = image_aligner("res/images/sun.jpg", self.window_half_x,
                                 WINDOW_SIZE_Y/1.9, self.batch, self.bg_group)
        
        self.sand = image_aligner("res/images/sandy.png", self.window_half_x,
                                 WINDOW_SIZE_Y/5, self.batch, self.bg_group_4)
        
        self.start_button = image_aligner("res/images/main_start.png", self.window_half_x,
                                          WINDOW_SIZE_Y/2+100, self.batch, self.fg_group)
        
        self.instr_button = image_aligner("res/images/main_help.png", self.window_half_x,
                                          WINDOW_SIZE_Y/2, self.batch, self.fg_group)

        self.settings_button = image_aligner("res/images/main_settings.png", self.window_half_x,
                                             WINDOW_SIZE_Y/2-100, self.batch, self.fg_group)

        self.cloud1 = image_aligner("res/images/cloud.png", self.cloud_start,
                                     WINDOW_SIZE_Y-300, self.batch, self.bg_group_2)
        
        self.cloud2 = image_aligner("res/images/cloud2.png", self.cloud_start,
                                     WINDOW_SIZE_Y-100, self.batch, self.bg_group_2)
        
        self.clouds = [self.cloud1, self.cloud2]

        # We scale everything so that it does not mess up
        # the position of the images when the user goes into
        # or out of fullscreen mode.
        self.cloud1.scale = 0.3
        self.cloud2.scale = 0.3
        self.start_button.scale = 0.13
        self.instr_button.scale = 0.13
        self.settings_button.scale = 0.13
        self.sun.scale = 0.92
        self.sand.scale = 0.86
        self.pyramid.scale = 1.3
        
        self.count = 0
        self.reset_count = 160
        self.lower_count = self.reset_count/4
        self.middle_count = self.lower_count*2
        self.upper_count = self.lower_count*3
        self.highest_y = self.logo.y
        pyglet.clock.schedule_interval(self.move_logo, 1/120.0)
        pyglet.clock.schedule_interval(self.counter, 1/120.0)
        pyglet.clock.schedule_interval(self.move_clouds, 1/120.0)
        
        # Load the player to play some music!
        self.player = pyglet.media.Player()
        self.music = pyglet.resource.media("rumba.mp3")
        self.player.queue(self.music)
        self.player.play()
        self.stop_playing = False
        
        self.in_upper = False
        # Bools to check where the mouse is
        self.is_on_start = False
        self.is_on_help = False
        self.is_on_settings = False
        
    def counter(self, dt):
        if self.count >= self.reset_count:
            self.count = 0
        self.count += 1
            
    # This method is called every 120th of a second.
    # It basically gives a cool floating effect to the logo.
    def move_logo(self, dt):
        # If the count is less than 120 but greater than 80
        # Move the logo down 12 pixels.
        # The count is set by counter().
        if self.upper_count > self.count >= self.middle_count:
            self.logo.y -= 12 * dt
        
        # If the count is greater than 120
        elif self.count >= self.upper_count:
            self.logo.y -= 6 * dt

        # If the count is greater than 40 but less than 80
        elif self.lower_count <= self.count <= self.middle_count:
            self.logo.y += 12 * dt
            
        # If the count is less than 40
        elif self.count <= self.lower_count:
            self.logo.y += 6 * dt
            
    def start(self):
        self.main_menu_keys = pyglet.window.key
        self.mouse = pyglet.window.mouse
        self.hand = self.game.window.get_system_mouse_cursor('hand')
        self.i = 0

    def handle_new_game(self):
        self.game.start_playing()

    def on_key_press(self, symbol, modifiers):
        if symbol == self.main_menu_keys.DOWN:
            pass
    
    def on_mouse_press(self, x, y, button, modifiers):
        if button == self.mouse.LEFT:
            if self.is_on_start:
                self.player.pause()
                self.game.start_playing()
            
    def on_mouse_motion(self, x, y, dx, dy):
        self.x = x
        self.y = y
#         self.dy = dy
#         pyglet.clock.schedule_interval(self.move_elements, 1/120.0)
#         if WINDOW_SIZE_Y/2 < self.y:
#             self.in_upper = True
#             
#         elif WINDOW_SIZE_Y/2 >= self.y:
#             self.in_upper = False
            
        if get_area(self.start_button, x, y):
            self.game.window.set_mouse_cursor(self.hand)
            self.is_on_start = True
            
        elif get_area(self.instr_button, x, y):
            self.game.window.set_mouse_cursor(self.hand)
            self.is_on_help = True
            
        elif get_area(self.settings_button, x, y):
            self.game.window.set_mouse_cursor(self.hand)
            self.is_on_settings = True
        
        elif not (get_area(self.start_button, x, y) and 
                  get_area(self.instr_button, x, y) and 
                  get_area(self.settings_button, x, y)):
            self.game.window.set_mouse_cursor(self.game.window.get_system_mouse_cursor(None))
            self.is_on_settings = False
            self.is_on_help = False
            self.is_on_start = False
        
    def move_elements(self, dt):
        self.factor = 6
            
        if self.in_upper:
            if self.i < 40:
                self.i = self.i + dt
                self.pyramid.y += 0.002 * self.factor
                self.sand.y += 0.003 * self.factor
            elif 40 <= self.i < 90:
                self.i = self.i + dt
                self.pyramid.y += 0.001 * self.factor
                self.sand.y += 0.002 * self.factor
            
        elif not self.in_upper:
            if self.i > 90:
                self.i = 90
            elif 40 < self.i <= 90:
                self.i = self.i - dt
                self.pyramid.y -= 0.001 * self.factor
                self.sand.y -= 0.002 * self.factor
            elif 0 < self.i <= 40:
                self.i = self.i - dt
                self.pyramid.y -= 0.002 * self.factor
                self.sand.y -= 0.003 * self.factor
                
    def move_clouds(self, dt):
        for obj in self.clouds:
            if obj.x > self.cloud_end:
                obj.x = self.cloud_start
                self.random_num = randint(floor(WINDOW_SIZE_Y/3), WINDOW_SIZE_Y)
                obj.y = self.random_num
                if WINDOW_SIZE_Y/3 < self.random_num < WINDOW_SIZE_Y/2:
                    obj.scale = 0.13
            obj.x += randint(2, 50) * dt

    def on_draw(self):
        self.game.window.clear()
        self.batch.draw()
        
# The video class. Plays a video.
class Video(Screen):
    "This class presents the video."
    def __init__(self, game):
        self.game = game
        self.video_path = "res/videos/intro_vid.wmv" # Where's the arbitrary video located?
        self.player = pyglet.media.Player() # Load the video player
        self.player.push_handlers(on_eos=self.on_eos)
        self.source = pyglet.media.StreamingSource() # Load the streaming device source
        self.load_media = pyglet.media.load(self.video_path) # Actually load the video
        self.on_to_next = False
        self.player.queue(self.load_media) # Queue the video
        self.player.play() # Play the video
    
    def start(self):
        self.video_keys = pyglet.window.key

    def on_key_press(self, symbol, modifiers):
        if symbol == self.video_keys.SPACE or symbol == self.video_keys.ENTER:
            #self.game.window.set_fullscreen(True)
            self.next_screen_now()
            self.on_to_next = True
            
    def on_mouse_press(self, x, y, button, modifiers):
        self.next_screen_now()
        self.on_to_next = True
     
    def on_eos(self): # If the video has stopped playing and...
        if not self.on_to_next: # if we haven't already gone onto the next screen...
            self.next_screen_now() # stop the video playing.
    
    # Stops the video from playing. Goes onto the main menu.        
    def next_screen_now(self):
        self.player.volume = 0 # Stops the video from making anymore annoying sounds.
        self.game.clear_current_screen()
        self.game.load_mainmenu()
        self.game.start_current_screen()

    def clear(self):
        self.game.window.clear()
            
    def on_draw(self):
        if self.player.source and self.player.source.video_format: # If we have the source of the video and the format of it..
            self.player.get_texture().blit(WINDOW_SIZE_X/4, WINDOW_SIZE_Y/4) # place the video at the following location.


load_resources() # First of all load the resources.
if __name__ == '__main__': # Run the game!!
    game = Game() # Load game class
    game.execute() # Then execute it

