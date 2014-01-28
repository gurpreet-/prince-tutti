import pyglet
import load, main2, menu, interface, map

## Important defines.
MUMMY_SPEED = 2
MUMMY_DASH = 3
PLAYER_SPEED = 2.15
##

# Defines the Mummy, is able to set the Mummy's
# speed and inform is if the mummy is speeding up.
class Player(pyglet.sprite.Sprite):
    def __init__(self, x, y, batch, group):
        self.x_pos = x
        self.y_pos = y
        self.mummy_image = pyglet.image.load("res/images/player.png")
        self.the_mummy = pyglet.sprite.Sprite(img=self.mummy_image,
                                              x=self.x_pos, y=self.y_pos,
                                              batch=batch, group=group)
        self.speed = MUMMY_SPEED
        self.reset_bools()
        self.going_nowhere = True
        
    def reset_bools(self):
        self.going_left = False
        self.going_right = False
        self.going_up = False
        self.going_down = False
        self.going_nowhere = False
        
    def speed_up(self):
        self.speed = MUMMY_DASH
    
    def reset_speed(self):
        self.speed = MUMMY_SPEED
    
    def get_speed(self):
        return self.speed
    
    # This function is similar to the others. Basically, when you want the 
    # mummy to move down check if it's going left. If it is, then move the
    # mummy right. Why would we do this? To prevent the mummy from going in
    # any other direction other than 90 degree angles. Check if it's going
    # right for the same reason.
    def move_down(self):
        if self.going_left:
            pyglet.clock.unschedule(self.move_mummy_left)
            
        if self.going_right:
            pyglet.clock.unschedule(self.move_mummy_right)

        if self.going_up:
            pyglet.clock.unschedule(self.move_mummy_up)
            self.reset_bools()
            self.going_nowhere = True
            
        elif not self.going_down or self.going_nowhere:
            pyglet.clock.schedule_interval(self.move_mummy_down, 1/120.0)
            self.reset_bools() # Reset the bools and then set the going down
                                # bool to true.
            self.going_down = True
        
    def move_up(self):
        if self.going_left:
            pyglet.clock.unschedule(self.move_mummy_left)
        if self.going_right:
            pyglet.clock.unschedule(self.move_mummy_right)
        if self.going_down:
            pyglet.clock.unschedule(self.move_mummy_down)
            self.reset_bools()
            self.going_nowhere = True
        elif not self.going_up or self.going_nowhere:
            pyglet.clock.schedule_interval(self.move_mummy_up, 1/120.0)
            self.reset_bools()
            self.going_up = True
    
    def move_left(self):
        if self.going_up:
            pyglet.clock.unschedule(self.move_mummy_up)
        if self.going_down:
            pyglet.clock.unschedule(self.move_mummy_down)
        if self.going_right:
            pyglet.clock.unschedule(self.move_mummy_right)
            self.reset_bools()
            self.going_nowhere = True
        elif not self.going_left or self.going_nowhere:
            pyglet.clock.schedule_interval(self.move_mummy_left, 1/120.0)
            self.reset_bools()
            self.going_left = True
        
    def move_right(self):
        if self.going_up:
            pyglet.clock.unschedule(self.move_mummy_up)
        if self.going_down:
            pyglet.clock.unschedule(self.move_mummy_down)
        if self.going_left:
            pyglet.clock.unschedule(self.move_mummy_left)
            self.reset_bools()
            self.going_nowhere = True
        elif not self.going_right or self.going_nowhere:
            pyglet.clock.schedule_interval(self.move_mummy_right, 1/120.0)
            self.reset_bools()
            self.going_right = True

    def reset_x(self):
        self.the_mummy.x = 0
        
    def reset_y(self):
        self.the_mummy.y = 0
        
    def move_mummy_down(self, dt):
        self.the_mummy.y -= self.speed
            
    def move_mummy_up(self, dt):
        self.the_mummy.y += self.speed

    def move_mummy_left(self, dt):
        self.the_mummy.x -= self.speed
            
    def move_mummy_right(self, dt):
        self.the_mummy.x += self.speed
        
    def mummy_stop(self):
        self.speed = 0
        
    def get_y(self):
        return self.the_mummy.y
    
    def get_x(self):
        return self.the_mummy.x
    
    def return_pos(self):
        return self.the_mummy.position
