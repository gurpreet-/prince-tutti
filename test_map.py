
#################### Imports ####################
import pyglet
#################################################

################### Functions ###################
# Starts the game
def begin_game():
    pass

# Load the resources from the following folders,
# then re-index the file resource locations.
def load_resources():
    pyglet.resource.path = ["res", "res/images", "res/videos"]
    pyglet.resource.reindex()


def load_intro_video():
    pass

def move_mummy(dt):
    mummy1.x += dt * mummy1.get_speed()
    
    
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
#################################################

MUMMY_SPEED = 50
MUMMY_DASH = 70
PLAYER_SPEED = 40

load_resources() # Loads the resources from the resources folder.


window = pyglet.window.Window(caption="Hello, world!", width=1000, height=900)


ball_image = pyglet.image.load("res/images/player.png") # Loads an arbitrary image for testing.
mummy1 = Mummy(ball_image, x=50, y=50) # Places the ball in the bottom left corner.

# Get what keys are being pressed.
key = pyglet.window.key

@window.event
def on_draw():
    window.clear() # Clear the window before doing anything on it
    mummy1.draw() 

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.RIGHT:
        pyglet.clock.schedule_interval(move_mummy, 1/120)
        mummy1.speed_up()
        

    if symbol == key.ENTER: # When they press enter, maximise the window
        if window.fullscreen:
            window.set_fullscreen(False)

        elif not window.fullscreen: # Enable the toggling of window sizing. 
            window.set_fullscreen(True)

# Run the game!!
if __name__ == '__main__':
    pyglet.app.run()

