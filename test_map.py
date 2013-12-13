#################### Imports ####################
import pyglet
import bots # bots could be players
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

def move_player(dt):
    ball.x += dt * 50
#################################################


load_resources() # Loads the resources from the resources folder.


window = pyglet.window.Window(caption="Hello, world!", width=1000, height=900)
#pyglet.gl.glClearColor(1, 1, 1, 1)


ball_image = pyglet.image.load("res/images/ball.png") # Loads an arbitrary image for testing.
ball = pyglet.sprite.Sprite(ball_image, x=50, y=50) # Places the ball in the bottom left corner.

# Get what keys are being pressed.
key = pyglet.window.key

@window.event
def on_draw():
    window.clear() # Clear the window before doing anything on it
    ball.draw() # Else if we don't have the video, draw the ball.

@window.event
def on_key_press(symbol, modifiers):
#     if symbol == key.SPACE: # When the user presses space, change the caption!
#         window.set_caption("Changed caption, skipped video")
#         if player.playing:
#             player.next()
    
    if symbol == key.RIGHT:
        pyglet.clock.schedule_interval(move_player, 1/60)
        

    if symbol == key.ENTER: # When they press enter, maximise the window
        if window.fullscreen:
            window.set_fullscreen(False)

        elif not window.fullscreen: # Enable the toggling of window sizing. 
            window.set_fullscreen(True)

# Run the game!!
if __name__ == '__main__':
    pyglet.app.run()

