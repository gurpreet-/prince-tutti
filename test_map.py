import pyglet
from random import randint
from math import floor
from testclass import *
from ctypes import *

## Important defines.
WINDOW_SIZE_X = 1300
WINDOW_SIZE_Y = 1000
MUMMY_SPEED = 2
MUMMY_DASH = 3
PLAYER_SPEED = 2.1
##

collision_group = []
# needed to cast image data

 
def intersect(r1, r2):
    '''Compute the intersection of two rectangles'''
    n = Rect( max(r1.x1, r2.x1), max(r1.y1, r2.y1), min(r1.x2, r2.x2), min(r1.y2, r2.y2) )
    return n
 
def collides(r1, r2):
    '''Determine whether two rectangles collide'''
    if r1.x2 < r2.x1 or r1.y2 < r2.y1 or r1.x1 > r2.x2 or r1.y1 > r2.y2:
        return False
    return True
 
def from_sprite(s):
    '''Create a rectangle matching the bounds of the given sprite'''
    t = s.texture
    x = int(s.x - t.anchor_x)
    y = int(s.y - t.anchor_y)
    return Rect(x-t.width/2, y- t.height/2, x + t.width/2, y + t.height/2)
 
class Rect:
    '''Fast rectangular collision structure'''
 
    def __init__(self, x1, y1, x2, y2):
        '''Create a rectangle from a minimum and maximum point'''
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.height = self.y2 - self.y1
        self.width = self.x2 - self.x1
 
def get_mask(self):
    '''Returns the (potentially cached) image data for the sprite'''
 
    t = self.renderable.sprite.texture
    d = self.terrain.mask
    # return a tuple containing the image data, along with the width and height
    return d, t.width, t.height
 
def get_rect(s):
    '''Returns the bounding rectangle for the sprite'''
    return from_sprite(s)

def collide_with(ent1, ent2):
    pass

# Load the resources from the following folders,
# then re-index the file resource locations.
def load_resources():
    pyglet.resource.path = ["res", "res/images",
                            "res/videos", "res/fonts",
                            "res/music", "res/maps"]
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
class Mummy(pyglet.sprite.Sprite):
    def __init__(self, x, y, batch, group):
        self.x_pos = x
        self.y_pos = y
        self.mummy_image = pyglet.image.load("res/images/mummy.png")
        self.the_mummy = pyglet.sprite.Sprite(img=self.mummy_image,
                                              x=self.x_pos, y=self.y_pos,
                                              batch=batch, group=group)
        self.speed = MUMMY_SPEED
        self.reset_bools()
        
    def reset_bools(self):
        self.going_left = False
        self.going_right = False
        self.going_up = False
        self.going_down = False
        
    def speed_up(self):
        self.speed = MUMMY_DASH
    
    def reset_speed(self):
        self.speed = MUMMY_SPEED
    
    def get_speed(self):
        return self.speed
    
    # This function is similar to the others. Basically, when you want the 
    # mummy to move down check if it's going left. If it is, then move the
    # mummy right. Why would we do this? To prevent the mummy from going in
    # any other direction other than 90 degree angles. Check if it's going
    # right for the same reason.
    def move_down(self):
        if self.going_left:
            pyglet.clock.schedule_interval(self.move_mummy_right, 1/120.0)
        if self.going_right:
            pyglet.clock.schedule_interval(self.move_mummy_left, 1/120.0)
    # If it's going up and not already going down then allow the mummy to
    # reverse the speed at which it was going. Basically to stop.
    # Then, if it wasn't already going down, allow the mummy to go down.
        if self.going_up and not self.going_down:
            pyglet.clock.schedule_interval(self.move_mummy_down, 1/120.0)
        if not self.going_down:
            pyglet.clock.schedule_interval(self.move_mummy_down, 1/120.0)
            self.reset_bools() # Reset the bools and then set the going down
                                # bool to true.
            self.going_down = True
        
    def move_up(self):
        if self.going_left:
            pyglet.clock.schedule_interval(self.move_mummy_right, 1/120.0)
        if self.going_right:
            pyglet.clock.schedule_interval(self.move_mummy_left, 1/120.0)
        if self.going_down and not self.going_up:
            pyglet.clock.schedule_interval(self.move_mummy_up, 1/120.0)
        if not self.going_up:
            pyglet.clock.schedule_interval(self.move_mummy_up, 1/120.0)
            self.reset_bools()
            self.going_up = True
    
    def move_left(self):
        if self.going_up:
            pyglet.clock.schedule_interval(self.move_mummy_down, 1/120.0)
        if self.going_down:
            pyglet.clock.schedule_interval(self.move_mummy_up, 1/120.0)
        if self.going_right and not self.going_left:
            pyglet.clock.schedule_interval(self.move_mummy_left, 1/120.0)
        if not self.going_left:
            pyglet.clock.schedule_interval(self.move_mummy_left, 1/120.0)
            self.reset_bools()
            self.going_left = True
        
    def move_right(self):
        if self.going_up:
            pyglet.clock.schedule_interval(self.move_mummy_down, 1/120.0)
        if self.going_down:
            pyglet.clock.schedule_interval(self.move_mummy_up, 1/120.0)
        if self.going_left and not self.going_right:
            pyglet.clock.schedule_interval(self.move_mummy_right, 1/120.0)
        if not self.going_right:
            pyglet.clock.schedule_interval(self.move_mummy_right, 1/120.0)
            self.reset_bools()
            self.going_right = True

    def reset_x(self):
        self.the_mummy.x = 0
        
    def reset_y(self):
        self.the_mummy.y = 0
        
    def move_mummy_down(self, dt):
        self.the_mummy.y -= self.speed
            
    def move_mummy_up(self, dt):
        self.the_mummy.y += self.speed

    def move_mummy_left(self, dt):
        self.the_mummy.x -= self.speed
            
    def move_mummy_right(self, dt):
        self.the_mummy.x += self.speed
        
    def mummy_stop(self):
        self.speed = 0
        
    def get_y(self):
        return self.the_mummy.y
    
    def get_x(self):
        return self.the_mummy.x
    
    def return_pos(self):
        return self.the_mummy.position


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
        #pyglet.gl.glScalef(1, 1, 1) # Can be used to scale the game's contents.
        self.start_current_screen()
        pyglet.app.run()

# This class is here so that you can make
# any large game-wide modifications to the screen.
class Screen:
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
        pyglet.gl.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST) 
        pyglet.gl.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    
# This class represents the Actual Game. The GUI,
# the maps are all initialised here.
class ActualGame(Screen):
    "This class contains all your game logic. This is the class that enables the user to play through a level."
    def __init__(self, game, level_to_play):
        self.game = game
        self.level = level_to_play
        self.interface_batch = pyglet.graphics.Batch()
        self.tile_batch = pyglet.graphics.Batch()
        
        self.text_group = pyglet.graphics.OrderedGroup(4)
        self.fg_group = pyglet.graphics.OrderedGroup(3)
        self.plank_group = pyglet.graphics.OrderedGroup(2)
        self.bg2_group = pyglet.graphics.OrderedGroup(1)
        self.bg_group = pyglet.graphics.OrderedGroup(0)
        
        self.interface = Interface(self.fg_group, self.text_group, self.interface_batch)
        self.wood_image = pyglet.image.load("res/images/woodenplank.png")
        self.plank = pyglet.sprite.Sprite(img=self.wood_image, x=0,
                                     y=WINDOW_SIZE_Y/1.17, batch=self.interface_batch,
                                     group=self.plank_group)
        self.b_map = Maps(self.bg_group, self.tile_batch)
        self.f_map = Maps(self.bg2_group, self.tile_batch)
        self.f_map_pos = []
        self.list_of_pos = 0
        
        self.mummy = Mummy(65, 500, self.tile_batch, self.fg_group)
        pyglet.clock.schedule_interval(self.detect, 1/240.0)
        
    def detect(self, dt):
        pass
#         for num in self.list_of_pos:
#             if num[0]-1 <= self.mummy.return_pos()[0] <= num[0]+1 and num[1]-1 <= self.mummy.return_pos()[1] <= num[1]+1:
#                 self.mummy.mummy_stop()
#                 print("stop")
#             else:
#                 self.mummy.reset_speed()
                
    def on_key_press(self, key, modifiers):
        if key == self.actual_keys.DOWN:
            self.mummy.move_down()
        elif key == self.actual_keys.UP:
            self.mummy.move_up()
        elif key == self.actual_keys.LEFT:
            self.mummy.move_left()
        elif key == self.actual_keys.RIGHT:
            self.mummy.move_right()
    
    def launch_map(self):
        self.b_map.draw_map(str(self.level) + "b.txt")
        self.f_map.draw_map(str(self.level) + "m.txt")

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

# Loads maps from res/maps.
class Maps:
    def __init__(self, group, batch):
        self.group = group
        self.batch = batch
        self.tile_x = -32
        self.tile_y = WINDOW_SIZE_Y-32
        self.sprites = collision_group
        
        self.sand_load = pyglet.image.load("res/images/sand.jpg")
        self.brick_load = pyglet.image.load("res/images/brick.PNG")
        
    def draw_map(self, mapfile):
        with open("res/maps/" + mapfile, "rt") as map_file:
            map_data = map_file.read()
             
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

# Use the interface class to manage the GUI elements
# on-screen. I have done it like this so that individual
# elements can be removed if necessary. 
class Interface:
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
            
        self.livescontainer_start = self.score_scroll.x + self.scroll_handle_width
        self.livescontainer_end = self.livescontainer_start + self.score_scroll.width/4
    

        self.bonuscontainer_start = self.livescontainer_end
        self.bonuscontainer_end = self.bonuscontainer_start + self.score_scroll.width/4
    
        self.scorecontainer_start = self.bonuscontainer_end
        self.scorecontainer_end = self.scorecontainer_start - self.scroll_handle_width + self.score_scroll.width/2
        
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
        
    def update_score_value(self):
        self.score.update_score()
        
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
        self.text1 = "Start. \n"
        self.cloud_start = -WINDOW_SIZE_X/10
        self.cloud_end = WINDOW_SIZE_X + WINDOW_SIZE_X/10
        self.window_half_x = WINDOW_SIZE_X/2
        
        self.batch = pyglet.graphics.Batch()
        self.fg_group = pyglet.graphics.OrderedGroup(4)
        self.bg_group_4 = pyglet.graphics.OrderedGroup(3)
        self.bg_group_3 = pyglet.graphics.OrderedGroup(2)
        self.bg_group_2 = pyglet.graphics.OrderedGroup(1)
        self.bg_group = pyglet.graphics.OrderedGroup(0)
        
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
        
        self.player = pyglet.media.Player()
        self.music = pyglet.resource.media("rumba.mp3")
        self.player.queue(self.music)
        self.player.play()
        self.stop_playing = False
        
        self.in_upper = False
        self.is_on_start = False
        
    def counter(self, dt):
        if self.count >= self.reset_count:
            self.count = 0
        self.count += 1
            
    def move_logo(self, dt):
        # If the count is less than 120 but greater than 80
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
            
    def on_eos(self):
        pass
            
    def start(self):
        self.main_menu_keys = pyglet.window.key
        self.mouse = pyglet.window.mouse
        self.i = 0

    def handle_new_game(self):
        self.game.start_playing()

    def on_key_press(self, symbol, modifiers):
        if symbol == self.main_menu_keys.DOWN:
            pass
    
    def on_mouse_press(self, x, y, button, modifiers):
        if button == self.mouse.LEFT:
            if self.is_on_start:
                self.game.start_playing()
            
    def on_mouse_motion(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dy = dy
        pyglet.clock.schedule_interval(self.move_elements, 1/120.0)
        if WINDOW_SIZE_Y/2 < self.y:
            self.in_upper = True
            
        elif WINDOW_SIZE_Y/2 >= self.y:
            self.in_upper = False
            
        if get_area(self.start_button, x, y):
            self.hand = self.game.window.get_system_mouse_cursor('hand')
            self.game.window.set_mouse_cursor(self.hand)
            self.is_on_start = True
        elif not get_area(self.start_button, x, y):
            self.game.window.set_mouse_cursor(self.game.window.get_system_mouse_cursor(None))
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
    "This class presents the title screen and options for new game."
    def __init__(self, game):
        self.game = game
        self.video_path = "res/videos/intro_vid.wmv" # Where's the arbitrary video located?
        self.player = pyglet.media.Player() # Load the video player
        self.source = pyglet.media.StreamingSource() # Load the streaming device source
        self.load_media = pyglet.media.load(self.video_path) # Actually load the video
    
    def start(self):
        self.video_keys = pyglet.window.key
        self.player.queue(self.load_media) # Queue the video
        self.player.play() # Play the video

    def on_key_press(self, symbol, modifiers):
        if symbol == self.video_keys.SPACE or symbol == self.video_keys.ENTER:
            #self.game.window.set_fullscreen(True)
            self.game.clear_current_screen()
            self.game.load_mainmenu()
            self.game.start_current_screen()
            
    def on_mouse_press(self, x, y, button, modifiers):
         pass
            
    def clear(self):
        self.game.window.clear()
            
    def on_draw(self):
        if self.player.source and self.player.source.video_format: # If we have the source of the video and the format of it..
            self.player.get_texture().blit(WINDOW_SIZE_X/2, WINDOW_SIZE_Y/2) #... Place the video at the following location.


# First of all load the resources.
load_resources()

# Run the game!!
if __name__ == '__main__':
    hell = testthing
    game = Game()
    game.execute()

