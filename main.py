#################### Imports ####################
import pyglet
# import bots # imports the bots, could be players
#################################################

################### Functions ###################
# Starts the game
def begin_game():
    pass


def load_resources():
    pyglet.resource.path = ["res", "res/images", "res/videos"]
    pyglet.resource.reindex()


def load_intro_video():
    pass
#################################################


load_resources() # Loads the resources from the resources folder.

# Following creates a window and makes the window white.
window = pyglet.window.Window(caption="Hello, world!", width=1000, height=900)
pyglet.gl.glClearColor(1, 1, 1, 1)


ball_image = pyglet.image.load("res/images/ball.png") # Loads an arbitrary image for testing.
ball = pyglet.sprite.Sprite(ball_image, x=50, y=50) # Places the ball in the bottom left corner.

# Get what keys are being pressed.
key = pyglet.window.key



video_path = "res/videos/intro_vid.wmv" # Where's the arbitrary video located?
player = pyglet.media.Player() # Load the video player
source = pyglet.media.StreamingSource() # Load the streaming device source
load_media = pyglet.media.load(video_path) # Actually load the video

player.queue(load_media) # Queue the video
player.play() # Play the video

@window.event
def on_draw():
    window.clear() # Clear the window before doing anything on it
    if player.source and player.source.video_format: # If we have the source of the video and the format of it..
        player.get_texture().blit(50, 20) #... Place the video at the following location.
    else:
        ball.draw() # Else if we don't have the video, draw the ball.

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE: # When the user presses space, change the caption!
        window.set_caption("Changed caption, skipped video")
        if player.playing:
            player.next()

    if symbol == key.ENTER: # When they press enter, maximise the window
        if window.fullscreen:
            window.set_fullscreen(False)

        elif not window.fullscreen: # Enable the toggling of window sizing. 
            window.set_fullscreen(True)

# Run the game!!
if __name__ == '__main__':
    pyglet.app.run()

