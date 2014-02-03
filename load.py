import pyglet

WINDOW_SIZE_X = 1300
WINDOW_SIZE_Y = 1000

# Load the resources from the following folders,
# then re-index the file resource locations.
def load_resources():
    pyglet.resource.path = ["res",
                            "res/images",
                            "res/music",
                            "res/maps"]
    
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
