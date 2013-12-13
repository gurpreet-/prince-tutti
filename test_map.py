import pyglet
#from maps import *


MUMMY_SPEED = 50
MUMMY_DASH = 70
PLAYER_SPEED = 40

# Load the resources from the following folders,
# then re-index the file resource locations.
def load_resources():
    pyglet.resource.path = ["res", "res/images", "res/videos"]
    pyglet.resource.reindex()


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
        self.current_screen = MainMenu(self)

    def load(self):
        "Load progress from disk"
        pass

    def save(self):
        "Save progress to disk"
        pass

    def clear_current_screen(self):
        self.current_screen.clear()
        self.window.remove_handlers()

    def start_current_screen(self):
        self.window.set_handler("on_key_press", self.current_screen.on_key_press)
        self.window.set_handler("on_draw", self.current_screen.on_draw)
        # etc

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
        # Get what keys are being pressed.
        self.window = pyglet.window.Window(caption="Hello, world!", width=1200, height=1000)
        self.start_current_screen()
        pyglet.app.run()


class Screen:
    def __init__(self):
        pass

    def start():
        pass

    def clear():
        "delete all graphical objects on screen, batches, groups, etc. Clear all state in pyglet."
        pass

    def on_key_press(self, key, modifiers):
        pass

    def on_draw(self):
        pass


class LevelPlayer(Screen):
    "This class contains all your game logic. This is the class that enables the user to play through a level."
    def __init__(self, game, level_to_play):
        pass


class MainMenu(Screen):
    "This class presents the title screen and options for new game."
    def __init__(self, game):
        self.game = game
        
    def start(self):
        #pyglet.clock.schedule_interval(move_mummy, 1/120)
        pass

    def handle_new_game(self):
        self.game.start_playing()
        
    def move_mummy(self, dt):
        mummy1.x += dt * mummy1.get_speed()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.RIGHT:
            pyglet.clock.schedule_interval(self.move_mummy, 1/120)
            mummy1.speed_up()
            
        if symbol == key.ENTER: # When they press enter, maximise the window
            if window.fullscreen:
                window.set_fullscreen(False)
    
            elif not window.fullscreen: # Enable the toggling of window sizing. 
                window.set_fullscreen(True)

    def on_draw(self):
        mummy1.draw()
        
    # be sure to implement methods from Screen



def load_intro_video():
    pass



key = pyglet.window.key
mummy_image = pyglet.image.load("res/images/mummy.png") # Loads an arbitrary image for testing.
mummy1 = Mummy(mummy_image, x=50, y=50) # Places the ball in the bottom left corner.

load_resources() # Loads the resources from the resources folder.


# Run the game!!
if __name__ == '__main__':
    game = Game()
    game.execute()

