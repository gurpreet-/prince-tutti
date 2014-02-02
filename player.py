import pyglet

MUMMY_SPEED = 2
MUMMY_DASH = 3
PLAYER_SPEED = 2.5

# Defines the Mummy, is able to set the Mummy's
# speed and inform is if the mummy is speeding up.
class Player(pyglet.sprite.Sprite):
    def __init__(self, x, y, batch, group, img):
        self.x_pos = x
        self.y_pos = y
        
        
        self.the_player = pyglet.sprite.Sprite(img=pyglet.image.load("res/images/indy/man.png"),
                                              x=self.x_pos, y=self.y_pos,
                                              batch=batch, group=group)
                                             
        self.the_player.scale = 0.25
                                              
        self.speed = PLAYER_SPEED
        self.allowed_down = True
        self.allowed_up = True
        self.allowed_left = True
        self.allowed_right = True
        self.reset_bools()
        self.going_nowhere = True

    def down(self):
        self.the_player.image = pyglet.image.load("res/images/indy/man.png")
        return self

    def right(self):
        self.the_player.image = pyglet.image.load('res/images/indy/man_right.png')   
        return self
   
    def left(self):
        self.the_player.image = pyglet.image.load('res/images/indy/man_left.png')    
        return self
    
    def up(self):
        self.the_player.image = pyglet.image.load('res/images/indy/man_back.png')    
        return self  

        
    def allow_bools(self):
        self.allowed_down = True
        self.allowed_up = True
        self.allowed_left = True
        self.allowed_right = True
        
    def reset_bools(self):
        self.going_left = False
        self.going_right = False
        self.going_up = False
        self.going_down = False
        self.going_nowhere = False
        
    # Use this method only for testing speed up.
#     def speed_up(self):
#         self.speed = MUMMY_DASH
    
    def reset_speed(self):
        self.speed = PLAYER_SPEED
        
    def no_down(self):
        self.allowed_down = False

    def no_left(self):
        self.allowed_left = False

    def no_right(self):
        self.allowed_right = False

    def no_up(self):
        self.allowed_up = False
        
    def yes_down(self):
        self.allowed_down = True

    def yes_left(self):
        self.allowed_left = True

    def yes_right(self):
        self.allowed_right = True

    def yes_up(self):
        self.allowed_up = True
            
    def get_speed(self):
        return self.speed
    
    # Unschedule all movement if the mummy is going any other
    # direction other than down.
    # Why would we do this? To prevent the mummy from going in
    # any other direction other than 90 degree angles.
    def move_down(self):
        if self.going_left:
            pyglet.clock.unschedule(self.move_player_left)
            
        if self.going_right:
            pyglet.clock.unschedule(self.move_player_right)

        if self.going_up:
            pyglet.clock.unschedule(self.move_player_up)
            self.reset_bools()
            self.going_nowhere = True
        
        elif not self.going_down or self.going_nowhere:
            pyglet.clock.schedule_interval(self.move_player_down, 1/60.0)
            self.reset_bools() # Reset the bools...
            self.going_down = True # Then set the going down variable to true.
        
    def move_up(self):
        if self.going_left:
            pyglet.clock.unschedule(self.move_player_left)
        if self.going_right:
            pyglet.clock.unschedule(self.move_player_right)
        if self.going_down:
            pyglet.clock.unschedule(self.move_player_down)
            self.reset_bools()
            self.going_nowhere = True
        elif not self.going_up or self.going_nowhere:
            pyglet.clock.schedule_interval(self.move_player_up, 1/60.0)
            self.reset_bools()
            self.going_up = True
    
    def move_left(self):
        if self.going_up:
            pyglet.clock.unschedule(self.move_player_up)
        if self.going_down:
            pyglet.clock.unschedule(self.move_player_down)
        if self.going_right:
            pyglet.clock.unschedule(self.move_player_right)
            self.reset_bools()
            self.going_nowhere = True
        elif not self.going_left or self.going_nowhere:
            pyglet.clock.schedule_interval(self.move_player_left, 1/60.0)
            self.reset_bools()
            self.going_left = True
        
    def move_right(self):
        if self.going_up:
            pyglet.clock.unschedule(self.move_player_up)
        if self.going_down:
            pyglet.clock.unschedule(self.move_player_down)
        if self.going_left:
            pyglet.clock.unschedule(self.move_player_left)
            self.reset_bools()
            self.going_nowhere = True
        elif not self.going_right or self.going_nowhere:
            pyglet.clock.schedule_interval(self.move_player_right, 1/60.0)
            self.reset_bools()
            self.going_right = True

    def reset_x(self):
        self.the_player.x = 0
        
    def reset_y(self):
        self.the_player.y = 0
        
    def move_player_down(self, dt):
        if self.allowed_down:
            #self.going_nowhere = True
            self.the_player.y -= self.speed
            
    def move_player_up(self, dt):
        if self.allowed_up:
            #self.going_nowhere = True
            self.the_player.y += self.speed

    def move_player_left(self, dt):
        if self.allowed_left:
            #self.going_nowhere = True
            self.the_player.x -= self.speed
            
    def move_player_right(self, dt):
        if self.allowed_right:
            #self.going_nowhere = True
            self.the_player.x += self.speed
        
    def player_stop(self):
        self.speed = 0
        
    def get_y(self):
        return self.the_player.y
    
    def get_x(self):
        return self.the_player.x
    
    def return_pos(self):
        return self.the_player.position

    
