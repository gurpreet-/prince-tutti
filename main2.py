import pyglet
from math import floor
from ctypes import *
import load, player, menu, interface, map




# needed to cast image data

# First of all load the resources.
#load_resources()


# This class controls the overall mechanics of the game.
# It allows you to start screens which can be videos,
# main menu's or even levels. This is instantiated at
# the very beginning and is passed down to all screens.
class Game:
    def __init__(self):
        self.current_level = 0  # When we first create the game,
                                # the level is 0.
        self.current_screen = menu.Video(self)

    def load(self):
        "Load progress from disk"
        pass
    
    def return_level(self):
        return self.current_level
    
    def load_actualgame(self):
        self.current_screen = menu.ActualGame(game, self.current_level)
    
    def load_mainmenu(self):
        self.current_screen = menu.MainMenu(self)

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
        self.current_screen = menu.ActualGame(game, self.current_level)
        self.start_current_screen()

    def start_playing(self):
        "Called by the main menu when the user selects an option"
        self.clear_current_screen()
        self.current_screen = menu.ActualGame(game, self.current_level)
        self.start_current_screen()

    # This method is called once: when the game starts.
    def execute(self):
        self.display = pyglet.canvas.Display().get_default_screen()
        self.window = pyglet.window.Window(caption="Prince Tutti",
                                           style='dialog',
                                           screen=self.display,
                                           #fullscreen=True,
                                           width=menu.WINDOW_SIZE_X,
                                           height=menu.WINDOW_SIZE_Y)
        self.window.set_icon(pyglet.image.load("res/images/key.png"))
        #pyglet.gl.glScalef(1, 1, 1) # Can be used to scale the game's contents.
        self.start_current_screen()
        pyglet.app.run()
		
		
# Run the game!!
if __name__ == '__main__':
    game = Game()
    game.execute()
