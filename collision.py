import pyglet

class Rect:
    '''Fast rectangular collision structure'''
    
    def __init__(self, x1, y1, x2, y2):
        '''Create a rectangle from a minimum and maximum point'''
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        
    def intersect(self, r):
        '''Compute the intersection of two rectangles'''
        n = Rect( max(self.x1, r.x1), max(self.y1, r.y1), min(self.x2, r.x2), min(self.y2, r.y2) )
        return n
        
    def collides(self, r):
        '''Determine whether two rectangles collide'''
        if self.x2 < r.x1 or self.y2 < r.y1 or self.x1 > r.x2 or self.y1 > r.y2:
            return False
        return True
    
    @property
    def width(self):
        return self.x2 - self.x1
    
    @property
    def height(self):
        return self.y2 - self.y1
    
    def __repr__(self):
        return '[%d %d %d %d]' % (self.x1, self.y1, self.x2, self.y2)
    
    @staticmethod
    def from_sprite(s):
        '''Create a rectangle matching the bounds of the given sprite'''
        i = (s._texture if not s._animation else s._animation.frames[s._frame_index].image)
        x = int(s.x - i.anchor_x)
        y = int(s.y - i.anchor_y)
        return Rect(x, y, x + s.width, y + s.height)
    
def get_rect(sprite):
    '''Returns the bounding rectangle for the sprite'''
    return Rect.from_sprite(sprite)

def get_image(sprite):
    '''Returns the (potentially cached) image data for the sprite'''
    image_data_cache = {}
    # if this is an animated sprite, grab the current frame
    if sprite._animation:
        i = sprite._animation.frames[sprite._frame_index].image
    # otherwise just grab the image
    else:
        i = sprite._texture
    
    # if the image is already cached, use the cached copy
    if i in image_data_cache:
        d = image_data_cache[i]
    # otherwise grab the image's alpha channel, and cache it
    else:
        d = i.get_image_data().get_data('A', i.width)
        image_data_cache[i] = d
    
    # return a tuple containing the image data, along with the width and height
    return d, i.width, i.height

# This returns true if the cursor is within an area
# that is 'clickable'
def get_area(img, x, y):
        if img.x - img.width/2 < x < img.x + img.width/2 and img.y - img.height/2 < y < img.y + img.height/2:
            return True
        
def get_sarea(img, x, y):
        if img.x < x < img.x + img.width and img.y < y < img.y + img.height:
            return True

# Draws a rectangle using the in-built commands of
# OpenGL.
class Rectangle(object):
    '''Draws a rectangle into a batch.'''
    def __init__(self, x1, y1, x2, y2, group, batch):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, group,
            ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c4B', [0, 0, 0, 255] * 4))
            
            
		

#b = utils.get_sprites_from_map(self)
#print(b)
