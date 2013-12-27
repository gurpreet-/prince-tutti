import pyglet
import math
#from maps import *

WINDOW_SIZE_X = 1200
WINDOW_SIZE_Y = 1000
MUMMY_SPEED = 50
MUMMY_DASH = 70
PLAYER_SPEED = 40

# Load the resources from the following folders,
# then re-index the file resource locations.
def load_resources():
    pyglet.resource.path = ["res", "res/images", "res/videos", "res/fonts"]
    pyglet.resource.reindex()
    
def center_anchor(image):
    image.anchor_x = image.width//2
    image.anchor_y = image.height//2

def get_area(img, x, y):
        if img.x - img.width/2 < x < img.x + img.width/2 and img.y - img.height/2 < y < img.y + img.height/2:
            return True


class Rectangle(object):
    '''Draws a rectangle into a batch.'''
    def __init__(self, x1, y1, x2, y2, group, batch):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, group,
            ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c4B', [0, 0, 0, 255] * 4))


class Mummy(pyglet.sprite.Sprite):
    def __init__(self, img, x=0, y=0):
        pyglet.sprite.Sprite.__init__(self, img, x, y)
        self.speed = MUMMY_SPEED
        
    def speed_up(self):
        self.speed = MUMMY_DASH
    
    def reset_speed(self):
        self.speed = MUMMY_SPEED
    
    def get_speed(self):
        return self.speed


class Game:
    def __init__(self):
        self.current_level = 0
        self.current_screen = Video(self)

    def load(self):
        "Load progress from disk"
        pass
    
    def load_actualgame(self):
        self.current_screen = ActualGame(self)
    
    def load_mainmenu(self):
        self.current_screen = MainMenu(self)

    def save(self):
        "Save progress to disk"
        pass

    def clear_current_screen(self):
        self.current_screen.clear()
        self.window.remove_handlers()

    def start_current_screen(self):
        self.window.set_handler("on_key_press", self.current_screen.on_key_press)
        self.window.set_handler("on_draw", self.current_screen.on_draw)
        self.window.set_handler("on_mouse_press", self.current_screen.on_mouse_press)
        self.window.set_handler("on_mouse_motion", self.current_screen.on_mouse_motion)
        self.current_screen.start()

    def goto_next_level(self):
        "called from within LevelPlayer when the player beats the level"
        self.clear_current_screen()
        self.current_level += 1
        self.current_screen = LevelPlayer(self, game, self.current_level)
        self.start_current_screen()

    def start_playing(self):
        "called by the main menu when the user selects an option"
        self.clear_current_screen()
        self.current_screen = LevelPlayer(self, game, self.current_level)
        self.start_current_screen()

    def execute(self):
        self.display = pyglet.canvas.Display().get_default_screen()
        self.window = pyglet.window.Window(caption="Prince Tutti",
                                           style='dialog',
                                           screen=self.display,
                                           #fullscreen=True,
                                           width=WINDOW_SIZE_X,
                                           height=WINDOW_SIZE_Y)
        #pyglet.gl.glScalef(0.9, 0.9, 0.9)
        self.start_current_screen()
        pyglet.app.run()


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

    def on_draw(self):
        pyglet.gl.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST) 
        pyglet.gl.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)


class LevelPlayer(Screen):
    "This class contains all your game logic. This is the class that enables the user to play through a level."
    def __init__(self, game, level_to_play):
        pass
    
    
class ActualGame(Screen):
    "This class presents the title screen and options for new game."
    def __init__(self, game):
        self.game = game
        self.mummy_image = pyglet.image.load("res/images/mummy.png") # Loads an arbitrary image for testing.
        self.mummy1 = Mummy(self.mummy_image, x=50, y=50) # Places the ball in the bottom left corner.
        
    def start(self):
        self.main_menu_keys = pyglet.window.key

    def handle_new_game(self):
        self.game.start_playing()
        
    def move_mummy_right(self, dt):
        self.mummy1.x += dt * self.mummy1.get_speed()

    def on_key_press(self, symbol, modifiers):
        if symbol == self.main_menu_keys.RIGHT:
            pyglet.clock.schedule_interval(self.move_mummy_right, 1/120)
            self.mummy1.speed_up()
            
        if symbol == self.main_menu_keys.ENTER: # When they press enter, maximise the window
            if window.fullscreen:
                window.set_fullscreen(False)
    
            elif not window.fullscreen: # Enable the toggling of window sizing. 
                window.set_fullscreen(True)

    def on_draw(self):
        self.game.window.clear()
        self.mummy1.draw()
        


class MainMenu(Screen):
    "This class presents the title screen and options for new game."
    def __init__(self, game):
        self.game = game
        pyglet.font.add_directory("res/fonts")
        self.text1 = "Start. \n"
        
        self.batch = pyglet.graphics.Batch()
        self.fg_group = pyglet.graphics.OrderedGroup(4)
        self.bg_group_4 = pyglet.graphics.OrderedGroup(3)
        self.bg_group_3 = pyglet.graphics.OrderedGroup(2)
        self.bg_group_2 = pyglet.graphics.OrderedGroup(1)
        self.bg_group = pyglet.graphics.OrderedGroup(0)
        
        self.logo_image = pyglet.image.load("res/images/logo.png")
        center_anchor(self.logo_image)
        self.logo = pyglet.sprite.Sprite(img=self.logo_image, x=WINDOW_SIZE_X/2,
                                         y=WINDOW_SIZE_Y/2+300, batch=self.batch,
                                         group=self.fg_group)
        
        self.pyramid_image = pyglet.image.load("res/images/pyramids.png")
        center_anchor(self.pyramid_image)
        self.pyramid = pyglet.sprite.Sprite(self.pyramid_image, x=WINDOW_SIZE_X/2,
                                               y=WINDOW_SIZE_Y/3,
                                               batch=self.batch,
                                               group=self.bg_group_3)
        
        self.sun_image = pyglet.image.load("res/images/sun.jpg")
        center_anchor(self.sun_image)
        self.sun = pyglet.sprite.Sprite(self.sun_image, x=WINDOW_SIZE_X/2,
                                               y=WINDOW_SIZE_Y/1.9,
                                               batch=self.batch,
                                               group=self.bg_group)
        
        self.sand_image = pyglet.image.load("res/images/sandy.png")
        center_anchor(self.sand_image)
        self.sand = pyglet.sprite.Sprite(self.sand_image, x=WINDOW_SIZE_X/2,
                                               y=WINDOW_SIZE_Y/5,
                                               batch=self.batch,
                                               group=self.bg_group_4)
        
        self.start_image = pyglet.image.load("res/images/main_start.png")
        center_anchor(self.start_image)
        self.start_button = pyglet.sprite.Sprite(self.start_image, x=WINDOW_SIZE_X/2,
                                               y=WINDOW_SIZE_Y/2+100,
                                               batch=self.batch,
                                               group=self.fg_group)
        
        self.instructions_image = pyglet.image.load("res/images/main_help.png")
        center_anchor(self.instructions_image)
        self.instr_button = pyglet.sprite.Sprite(self.instructions_image, x=WINDOW_SIZE_X/2,
                                               y=WINDOW_SIZE_Y/2,
                                               batch=self.batch,
                                               group=self.fg_group)
        
        self.settings_image = pyglet.image.load("res/images/main_settings.png")
        center_anchor(self.settings_image)
        self.settings_button = pyglet.sprite.Sprite(self.settings_image, x=WINDOW_SIZE_X/2,
                                               y=WINDOW_SIZE_Y/2-100,
                                               batch=self.batch,
                                               group=self.fg_group)
        
        self.cloud_image1 = pyglet.image.load("res/images/cloud.png")
        center_anchor(self.cloud_image1)
        self.cloud1 = pyglet.sprite.Sprite(self.cloud_image1, x=-WINDOW_SIZE_X/10,
                                               y=WINDOW_SIZE_Y-300,
                                               batch=self.batch,
                                               group=self.bg_group_2)

        
        self.cloud1.scale = 0.3
        self.start_button.scale = 0.13
        self.instr_button.scale = 0.13
        self.settings_button.scale = 0.13
        self.sun.scale = 0.92
        self.sand.scale = 0.86
        self.pyramid.scale = 1.3
        
        
#         self.document = pyglet.text.document.FormattedDocument(self.text1)
#         self.document.set_style(0, len(self.document.text),
#                                 dict(color=(255, 255, 255, 255)))
#         
#         
#         self.layout = pyglet.text.layout.IncrementalTextLayout(self.document,
#                                                                 500,
#                                                                 300,
#                                                                 multiline=True,
#                                                                 batch=self.batch,
#                                                                 group=self.fg_group)
        
#         self.layout.x = WINDOW_SIZE_X/2
#         self.layout.y = WINDOW_SIZE_Y/3

        self.count = 0
        self.reset_count = 160
        self.lower_count = self.reset_count/4
        self.middle_count = self.lower_count*2
        self.upper_count = self.reset_count-self.lower_count
        pyglet.clock.schedule_interval(self.move_logo, 1/120.0)
        pyglet.clock.schedule_interval(self.counter, 1/120.0)
        pyglet.clock.schedule_interval(self.move_clouds, 1/120.0)
        
        self.in_upper = False
        self.is_hand = False
        
        
         
        #self.text2 = "yoyo"
        #self.document.insert_text(len(self.document.text), self.text2, dict(color=(255, 255, 255, 255)))
        
    def counter(self, dt):
        self.count += 1
        if self.count > self.reset_count:
            self.count = 0
            
    def move_logo(self, dt):
        if self.upper_count > self.count > self.middle_count:
            self.logo.y -= 12 * dt
            
        elif self.count >= self.upper_count:
            self.logo.y -= 6 * dt

        elif self.lower_count < self.count <= self.middle_count:
            self.logo.y += 6 * dt
            
        elif self.count <= self.lower_count:
            self.logo.y += 12 * dt
            
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
            if self.is_hand:
                self.game.clear_current_screen()
                self.game.load_actualgame()
                self.game.start_current_screen()
            
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
            self.is_hand = True
        elif not get_area(self.start_button, x, y):
            self.game.window.set_mouse_cursor(self.game.window.get_system_mouse_cursor(None))
            self.is_hand = False
        
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
        self.cloud1.x += 50 * dt

    def on_draw(self):
        self.game.window.clear()
        self.batch.draw()
        

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



load_resources()

# Run the game!!
if __name__ == '__main__':
    game = Game()
    game.execute()

