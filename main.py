#################### Imports ####################
import pyglet
# import bots # imports the bots, could be players
#################################################

################### Functions ###################
# Starts the game
def begin_game():
    pass


def load_resources():
    pyglet.resource.path = ["res", "res/images"]
    pyglet.resource.reindex()


def load_intro_video():
    pass
#################################################

load_resources()

window = pyglet.window.Window(caption="Hello, world!", width=1000, height=900)
window.set_exclusive_mouse()
pyglet.gl.glClearColor(1, 1, 1, 1)

ball_image = pyglet.image.load("res/images/ball.png")
ball = pyglet.sprite.Sprite(ball_image, x=50, y=50)


key = pyglet.window.key


video_path = "res/videos/intro_vid.wmv"
player = pyglet.media.Player()
source = pyglet.media.StreamingSource()
load_media = pyglet.media.load(video_path)

player.queue(load_media)
player.play()

@window.event
def on_draw():
    window.clear()
    if player.source and player.source.video_format:
        player.get_texture().blit(50, 20)
    else:
        ball.draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        window.set_caption("Changed caption, skipped video")
        if player.playing:
            player.next()

    if symbol == key.ENTER:
        if window.fullscreen:
            window.set_fullscreen(False)

        elif not window.fullscreen:
            window.set_fullscreen(True)


if __name__ == '__main__':
    pyglet.app.run()

