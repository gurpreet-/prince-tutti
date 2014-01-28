
 
def intersect(r1, r2):
    '''Compute the intersection of two rectangles'''
    n = Rect( max(r1.x1, r2.x1), max(r1.y1, r2.y1), min(r1.x2, r2.x2), min(r1.y2, r2.y2) )
    return n
 
def collides(r1, r2):
    '''Determine whether two rectangles collide'''
    if r1.x2 < r2.x1 or r1.y2 < r2.y1 or r1.x1 > r2.x2 or r1.y1 > r2.y2:
        return False
    return True
 
def from_sprite(s):
    '''Create a rectangle matching the bounds of the given sprite'''
    t = s.texture
    x = int(s.x - t.anchor_x)
    y = int(s.y - t.anchor_y)
    return Rect(x-t.width/2, y- t.height/2, x + t.width/2, y + t.height/2)
 
class Rect:
    '''Fast rectangular collision structure'''
 
    def __init__(self, x1, y1, x2, y2):
        '''Create a rectangle from a minimum and maximum point'''
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.height = self.y2 - self.y1
        self.width = self.x2 - self.x1
 
def get_mask(self):
    '''Returns the (potentially cached) image data for the sprite'''
 
    t = self.renderable.sprite.texture
    d = self.terrain.mask
    # return a tuple containing the image data, along with the width and height
    return d, t.width, t.height
 
def get_rect(s):
    '''Returns the bounding rectangle for the sprite'''
    return from_sprite(s)

def collide_with(ent1, ent2):
    pass


# Draws a rectangle using the in-built commands of
# OpenGL.
class Rectangle(object):
    '''Draws a rectangle into a batch.'''
    def __init__(self, x1, y1, x2, y2, group, batch):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, group,
            ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c4B', [0, 0, 0, 255] * 4))

