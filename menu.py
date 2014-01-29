import pyglet
import main2
import load, player, interface, map
from random import randint
from math import floor

WINDOW_SIZE_X = 1300
WINDOW_SIZE_Y = 1000


# This returns true if the cursor is within an area
# that is 'clickable'
def get_area(img, x, y):
        if img.x - img.width/2 < x < img.x + img.width/2 and img.y - img.height/2 < y < img.y + img.height/2:
            return True


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
        interface.interface_batch = pyglet.graphics.Batch()
        self.tile_batch = pyglet.graphics.Batch()
        
        self.text_group = pyglet.graphics.OrderedGroup(4)
        self.fg_group = pyglet.graphics.OrderedGroup(3)
        self.plank_group = pyglet.graphics.OrderedGroup(2)
        self.bg2_group = pyglet.graphics.OrderedGroup(1)
        self.bg_group = pyglet.graphics.OrderedGroup(0)
        
        self.interface = interface.Interface(self.fg_group, self.text_group, interface.interface_batch)
        self.wood_image = pyglet.image.load("res/images/woodenplank.png")
        self.plank = pyglet.sprite.Sprite(img=self.wood_image, x=0,
                                     y=WINDOW_SIZE_Y/1.17, batch=interface.interface_batch,
                                     group=self.plank_group)
        self.b_map = map.Maps(self.bg_group, self.tile_batch)
        self.f_map = map.Maps(self.bg2_group, self.tile_batch)
        self.f_map_pos = []
        self.list_of_pos = 0
        
        self.mummy = player.Player(65, 500, self.tile_batch, self.fg_group)
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
        interface.interface_batch.draw()
		
      
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
        
        self.logo = load.image_aligner("res/images/logo.png", self.window_half_x,
                                  WINDOW_SIZE_Y/2+300, self.batch, self.fg_group)
        
        self.pyramid = load.image_aligner("res/images/pyramids.png", self.window_half_x,
                                     WINDOW_SIZE_Y/3, self.batch, self.bg_group_3)
        
        self.sun = load.image_aligner("res/images/sun.jpg", self.window_half_x,
                                 WINDOW_SIZE_Y/1.9, self.batch, self.bg_group)
        
        self.sand = load.image_aligner("res/images/sandy.png", self.window_half_x,
                                 WINDOW_SIZE_Y/5, self.batch, self.bg_group_4)
        
        self.start_button = load.image_aligner("res/images/main_start.png", self.window_half_x,
                                          WINDOW_SIZE_Y/2+100, self.batch, self.fg_group)
        
        self.instr_button = load.image_aligner("res/images/main_help.png", self.window_half_x,
                                          WINDOW_SIZE_Y/2, self.batch, self.fg_group)

        self.settings_button = load.image_aligner("res/images/main_settings.png", self.window_half_x,
                                             WINDOW_SIZE_Y/2-100, self.batch, self.fg_group)

        self.cloud1 = load.image_aligner("res/images/cloud.png", self.cloud_start,
                                     WINDOW_SIZE_Y-300, self.batch, self.bg_group_2)
        
        self.cloud2 = load.image_aligner("res/images/cloud2.png", self.cloud_start,
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
        self.music = pyglet.resource.media("res/music/rumba.mp3")
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

