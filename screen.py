import pyglet
from pyglet.gl import *
import load, interface, map, player
from collision import get_rect, get_area, get_sarea, Rect
from random import randint
from math import floor

WINDOW_SIZE_X = 1300
WINDOW_SIZE_Y = 1000

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
        self.interface = interface.Interface(self.game, self.fg_group, self.text_group, self.interface_batch)
        self.wood_image = pyglet.image.load("res/images/woodenplank.png")
        self.plank = pyglet.sprite.Sprite(img=self.wood_image, x=0,
                                     y=WINDOW_SIZE_Y/1.17, batch=self.interface_batch,
                                     group=self.plank_group)
        # Load the maps
        self.b_map = map.Maps(self.bg_group, self.tile_batch)
        self.f_map = map.Maps(self.bg2_group, self.tile_batch)
        
        # Create the sound effects manager
        self.effects = pyglet.media.ManagedSoundPlayer() # Load the sound player
        self.source2 = pyglet.media.StreamingSource() # Load the streaming device source
        
        # Create the music manager
        self.soundplayer = pyglet.media.ManagedSoundPlayer() # Load the sound player
        self.soundplayer.push_handlers(on_eos=self.on_eos)
        self.source = pyglet.media.StreamingSource() # Load the streaming device source
        self.audio_path = "res/music/scare.mp3" # First queue the bonus music
        self.load_media = pyglet.media.load(self.audio_path)
        self.on_to_next = False
        self.soundplayer.queue(self.load_media)
        self.soundplayer.queue(pyglet.media.load("res/music/main.mp3")) # Then the main music
        self.soundplayer.play()

        # Create the actual player who plays in the game
        self.player = player.Player(68, 480, self.tile_batch, self.fg_group, img = pyglet.image.load('res/images/indy/man.png')) 
        # Useful for collision detection
        self.lights = []
        self.rectang = []
        
        self.time = 0
        pyglet.clock.schedule_interval(self.gen_rects, 1/60.0)
        pyglet.clock.schedule_interval(self.gen_rects2, 1/60.0)
        pyglet.clock.schedule_interval(self.detect, 1/2.0)
        pyglet.clock.schedule_interval(self.collision, 1/60.0)
        pyglet.clock.schedule_interval(self.collision_coins, 1/15.0)
        pyglet.clock.schedule_interval(self.collision_key, 1/15.0)
        pyglet.clock.schedule_interval(self.update_score, 2.0)
        pyglet.clock.schedule_once(self.make_light, 2.0)
        self.invisible_box = pyglet.image.load("res/images/collision.png")
        self.invisible_box2 = pyglet.image.load("res/images/collision2.png")
        self.invis1 = pyglet.sprite.Sprite(img=self.invisible_box, x=self.player.the_player.x + 
                                           self.player.the_player.width,
                                     y=self.player.the_player.y, batch=self.interface_batch,
                                     group=self.bg2_group)
        self.invis2 = pyglet.sprite.Sprite(img=self.invisible_box, x=self.player.the_player.x,
                                     y=self.player.the_player.y, batch=self.interface_batch,
                                     group=self.bg2_group)
        self.invis3 = pyglet.sprite.Sprite(img=self.invisible_box2, x=self.player.the_player.x,
                                     y=self.player.the_player.y + self.player.the_player.height, 
                                     batch=self.interface_batch,
                                     group=self.bg2_group)
        self.invis4 = pyglet.sprite.Sprite(img=self.invisible_box2, x=self.player.the_player.x,
                                     y=self.player.the_player.y, 
                                     batch=self.interface_batch,
                                     group=self.bg2_group)
        self.rectang.append(self.invis1)
        self.rectang.append(self.invis2)
        self.rectang.append(self.invis3)
        self.rectang.append(self.invis4)
        
        self.circle = pyglet.resource.image("spot1.png")
        self.volume_num = 1
        self.unlock()
    
    # 0 = right
    # 1 = left
    # 2 = top
    # 3 = bottom
    def gen_rects(self, dt):
        self.rectang[0].x = self.player.the_player.x + self.player.the_player.width + 5
        self.rectang[0].y = self.player.the_player.y
        self.rectang[1].x = self.player.the_player.x - 5
        self.rectang[1].y = self.player.the_player.y - 2
        
    def gen_rects2(self, dt):
        self.rectang[2].x = self.player.the_player.x + 1
        self.rectang[2].y = self.player.the_player.y + self.player.the_player.height + 5
        self.rectang[3].x = self.player.the_player.x
        self.rectang[3].y = self.player.the_player.y - 5
        
    def make_light(self, dt):
        for torch in self.f_map.return_torches():
            self.torch_sprite = pyglet.sprite.Sprite(self.circle, x=torch.x-10,
                                                       y=torch.y-10, batch=self.interface_batch,
                                                       group=self.fg_group)
            self.torch_sprite.opacity = randint(50, 120)
            self.lights.append(self.torch_sprite)
        return set(self.lights)
        
    def detect(self, dt):
        # Check where the player is
        if (self.player.the_player.x > WINDOW_SIZE_X or 
            self.player.the_player.x < 0 or 
            self.player.the_player.y > WINDOW_SIZE_Y or
            self.player.the_player.y < 0):
            print("out of bounds")
        self.time += 1
        if self.time >= 100:
            self.time = 0
        for sprite in self.lights:
            if self.time >= 50 and sprite.opacity < 120:
                sprite.opacity += 1
            if self.time < 50 and sprite.opacity > 20:
                sprite.opacity -= 1
                
            
    def collision(self, dt):
        self.player.allow_bools()
        for rectangles in self.f_map.return_sprites():
            if get_sarea(rectangles, self.rectang[0].x, self.rectang[0].y):
                self.player.no_right()
 
            if get_sarea(rectangles, self.rectang[1].x, self.rectang[1].y):
                self.player.no_left()
              
            if get_sarea(rectangles, self.rectang[2].x, self.rectang[2].y):
                self.player.no_up()
              
            if get_sarea(rectangles, self.rectang[3].x, self.rectang[3].y):
                self.player.no_down()

    def collision_coins(self, dt):
        for coin in self.f_map.return_coins():
            if get_rect(coin).collides(get_rect(self.player.the_player)):
                if coin.visible == True:
                    self.interface.update_bonus()
                    coin.visible = False
                    
    def collision_key(self, dt):
        for key in self.f_map.return_keys():
            if get_rect(key).collides(get_rect(self.player.the_player)):
                if key.visible == True:
                    self.interface.update_key_scroll()
                    pyglet.clock.schedule_once(self.unlock_exit_gate, 0.1)
                    pyglet.clock.schedule_interval(self.volume_decrease, 1/10)
                    key.visible = False
    
    def volume_decrease(self, dt):
        if self.volume_num <= 0.2:
            pyglet.clock.unschedule(self.volume_decrease)
            self.soundplayer.pause()
            self.soundplayer.queue(pyglet.resource.media("scare.mp3"))
            self.soundplayer.next()
            self.soundplayer.play()
            self.on_to_next = True
            pyglet.clock.schedule_interval(self.volume_increase, 1.0)
        self.soundplayer.volume = self.volume_num
        self.volume_num -= 0.05
        
    def volume_increase(self, dt):
        if self.volume_num > 1:
            pyglet.clock.unschedule(self.volume_increase)
        self.soundplayer.volume = self.volume_num
        self.volume_num += 0.1
                    
    def update_score(self, dt):
        self.interface.update_score_value()
        
    def unlock(self):
        if self.level == 0:
            pyglet.clock.schedule_once(self.unlock_key_gate, 10.0)
        if self.level == 1:
            pyglet.clock.schedule_once(self.unlock_key_gate, 32.0)
        
    def unlock_key_gate(self, dt):
        for obj in self.f_map.return_keygate():
            for i in range(10, 0, -1):
                obj.scale = i/10
                obj.y += i/2
            self.load_effect = pyglet.resource.media("chain_gate.mp3")
            self.effects.queue(self.load_effect)
            self.effects.play()
            
    def unlock_exit_gate(self, dt):
        for obj in self.f_map.return_exitgate():
            for i in range(10, 0, -1):
                obj.scale = i/10
                obj.y += i/2
            self.load_effect = pyglet.resource.media("chain_gate.mp3")
            self.effects.queue(self.load_effect)
            self.effects.play()

    def on_key_press(self, key, modifiers):
        if key == self.actual_keys.DOWN:
            self.player.move_down()                                  # Move the player down if user hits down key
            self.player = self.player.down()                         # See Player class for more information
        elif key == self.actual_keys.UP:
            self.player.move_up()
            self.player = self.player.up()
        elif key == self.actual_keys.LEFT:
            self.player.move_left()
            self.player = self.player.left()
        elif key == self.actual_keys.RIGHT:
            self.player.move_right()
            self.player = self.player.right()
    
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
        self.soundplayer.pause()
        if not self.on_to_next:
            self.soundplayer.queue(pyglet.media.load("res/music/main.mp3"))
            self.soundplayer.next()
            self.soundplayer.play()
        if self.on_to_next:
            self.soundplayer.queue(pyglet.media.load("res/music/scare.mp3"))
            self.soundplayer.next()
            self.soundplayer.play()
             
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
        self.soundplayer = pyglet.media.ManagedSoundPlayer() # Load the sound player
        self.soundplayer.push_handlers(on_eos=self.on_eos)
        self.source = pyglet.media.StreamingSource() # Load the streaming device source
        self.audio_path = "res/music/rumba.mp3" # First queue the bonus music
        self.load_media = pyglet.media.load(self.audio_path)
        self.soundplayer.queue(self.load_media)
        self.soundplayer.play()
        self.i = 0

    def handle_new_game(self):
        self.game.start_playing()

    def on_key_press(self, symbol, modifiers):
        if symbol == self.main_menu_keys.DOWN:
            pass
    
    def on_mouse_press(self, x, y, button, modifiers):
        if button == self.mouse.LEFT:
            if self.is_on_start:
                self.soundplayer.pause()
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
        
    def on_eos(self):
        self.soundplayer.play()
        
# The video class. Plays a video.
class Video(Screen):
    "This class presents the video."
    def __init__(self, game):
        self.game = game
        self.video_path = "res/videos/intro_vid.wmv" # Where's the arbitrary video located?
        self.player = pyglet.media.Player() # Load the video player
        self.player.push_handlers(on_eos=self.on_eos)
        self.source = pyglet.media.StreamingSource() # Load the streaming device source
        #self.load_media = pyglet.media.load(self.video_path) # Actually load the video
        self.on_to_next = False
        #self.player.queue(self.load_media) # Queue the video
        #self.player.play() # Play the video
    
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
