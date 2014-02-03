import pyglet

MUMMY_SPEED = 2
MUMMY_DASH = 2.5
PLAYER_SPEED = 3

# Defines the Mummy, is able to set the Mummy's
# speed and inform is if the mummy is speeding up.
class Player(pyglet.sprite.Sprite):
    def __init__(self, x, y, batch, group, img):
        self.x_pos = x
        self.y_pos = y
        
        self.stand_still = pyglet.image.load("res/images/indy/man.png")
        
        self.front1 = pyglet.image.load("res/images/indy/front_left.png")
        self.front2 = pyglet.image.load("res/images/indy/front_right.png")
        
        self.left1 = pyglet.image.load("res/images/indy/left_left.png")
        self.left2 = pyglet.image.load("res/images/indy/left_right.png")
        
        self.up1 = pyglet.image.load("res/images/indy/up_left.png")
        self.up2 = pyglet.image.load("res/images/indy/up_right.png")
        
        self.right1 = pyglet.image.load("res/images/indy/right_right.png")
        self.right2 = pyglet.image.load("res/images/indy/right_left.png")
     
        
         
         
        
        
        self.anim_front = pyglet.image.Animation.from_image_sequence([self.front1, self.front2], 0.5, True)  # 0.5 is the number in seconds between frames
        self.anim_left = pyglet.image.Animation.from_image_sequence([self.left1, self.left2], 0.5, True)    # True means to keep looping (We can always stop it later)
        self.anim_up = pyglet.image.Animation.from_image_sequence([self.up1, self.up2], 0.5, True)
        self.anim_right = pyglet.image.Animation.from_image_sequence([self.right1, self.right2], 0.5, True)
        
        self.idle = pyglet.image.load("res/images/indy/man.png")
        
        
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
        self.o_x = self.the_player.x
        self.o_y = self.the_player.y
        pyglet.clock.schedule_interval(self.updatepos, 1/60.0)
        pyglet.clock.schedule_interval(self.is_moving, 1/70.0)

#     def down(self):
#         self.the_player.image = self.anim_front
#         return self
#  
#     def right(self):
#         self.the_player.image = self.anim_right      
#         return self
#     
#     def left(self):
#         self.the_player.image = self.anim_left   
#         return self
#      
#     def up(self):
#         self.the_player.image = self.anim_up    
#         return self  

        
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
            self.the_player.image = self.anim_front
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
            self.the_player.image = self.anim_up 
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
            self.the_player.image = self.anim_left 
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
            self.the_player.image = self.anim_right
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
        else:
            self.the_player.image = self.idle

        

    def move_player_up(self, dt):
        if self.allowed_up:
            #self.going_nowhere = True
            self.the_player.y += self.speed
        else:
            self.the_player.image = self.idle


    def move_player_left(self, dt):
        if self.allowed_left:
            #self.going_nowhere = True
            self.the_player.x -= self.speed
        else:
            self.the_player.image = self.idle


    def move_player_right(self, dt):
        if self.allowed_right:
            #self.going_nowhere = True
            self.the_player.x += self.speed
        else:
            self.the_player.image = self.idle
            
    def is_moving(self, dt):
        if not (self.the_player.x == self.o_x and self.the_player.y == self.o_y):
            return True
        else:
            return False
        
    def updatepos(self, dt):
        self.o_x = self.the_player.x
        self.o_y = self.the_player.y
        
    def player_stop(self):
        self.speed = 0
        
    def get_y(self):
        return self.the_player.y
    
    def get_x(self):
        return self.the_player.x
    
    def return_pos(self):
        return self.the_player.position
    
class Mummy(pyglet.sprite.Sprite):
    def __init__(self, x, y, batch, group, img):
        self.x_pos = x
        self.y_pos = y
        
        self.idle = pyglet.image.load("res/images/mummy/mummy.png")
        
        self.front1 = pyglet.image.load("res/images/mummy/front_left.png")
        self.front2 = pyglet.image.load("res/images/mummy/front_right.png")
        
        self.left1 = pyglet.image.load("res/images/mummy/left_left.png")
        self.left2 = pyglet.image.load("res/images/mummy/left_right.png")
        
        self.up1 = pyglet.image.load("res/images/mummy/up_left.png")
        self.up2 = pyglet.image.load("res/images/mummy/up_right.png")
        
        self.right1 = pyglet.image.load("res/images/mummy/right_right.png")
        self.right2 = pyglet.image.load("res/images/mummy/right_left.png")
     
        
         
        pyglet.clock.schedule_interval(self.move_mummy_down, 1/60.0)
        pyglet.clock.schedule_interval(self.move_mummy_up, 1/60.0)
        pyglet.clock.schedule_interval(self.move_mummy_right, 1/60.0)
        pyglet.clock.schedule_interval(self.move_mummy_left, 1/60.0)
        
        
        self.anim_front = pyglet.image.Animation.from_image_sequence([self.front1, self.front2], 0.5, True)  # 0.5 is the number in seconds between frames
        self.anim_left = pyglet.image.Animation.from_image_sequence([self.left1, self.left2], 0.5, True)    # True means to keep looping (We can always stop it later)
        self.anim_up = pyglet.image.Animation.from_image_sequence([self.up1, self.up2], 0.5, True)
        self.anim_right = pyglet.image.Animation.from_image_sequence([self.right1, self.right2], 0.5, True)
        
        
        
        self.the_mummy = pyglet.sprite.Sprite(img=pyglet.image.load("res/images/mummy/mummy.png"),
                                              x=self.x_pos, y=self.y_pos,
                                              batch=batch, group=group)                                     
        self.the_mummy.scale = 0.25

                                              
        self.speed = MUMMY_SPEED
        self.allowed_down = True
        self.allowed_up = True
        self.allowed_left = True
        self.allowed_right = True
        self.reset_bools()
        self.going_nowhere = True
        self.o_x = self.the_mummy.x
        self.o_y = self.the_mummy.y
        pyglet.clock.schedule_interval(self.updatepos, 1/60.0)
        pyglet.clock.schedule_interval(self.is_moving, 1/70.0)

#     def down(self):
#         self.the_mummy.image = self.anim_front
#         return self
#  
#     def right(self):
#         self.the_mummy.image = self.anim_right      
#         return self
#     
#     def left(self):
#         self.the_mummy.image = self.anim_left   
#         return self
#      
#     def up(self):
#         self.the_mummy.image = self.anim_up    
#         return self  

        
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
        self.speed = MUMMY_SPEED
        
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
    
    def speed_up(self):
        self.speed = MUMMY_DASH
    
    # Unschedule all movement if the mummy is going any other
    # direction other than down.
    # Why would we do this? To prevent the mummy from going in
    # any other direction other than 90 degree angles.
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
            self.the_mummy.image = self.anim_front
            pyglet.clock.schedule_interval(self.move_mummy_down, 1/60.0)
            self.reset_bools() # Reset the bools...
            self.going_down = True # Then set the going down variable to true.
        
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
            self.the_mummy.image = self.anim_up 
            pyglet.clock.schedule_interval(self.move_mummy_up, 1/60.0)
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
            self.the_mummy.image = self.anim_left 
            pyglet.clock.schedule_interval(self.move_mummy_left, 1/60.0)
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
            self.the_mummy.image = self.anim_right
            pyglet.clock.schedule_interval(self.move_mummy_right, 1/60.0)
            self.reset_bools()
            self.going_right = True

    def reset_x(self):
        self.the_mummy.x = 0
        
    def reset_y(self):
        self.the_mummy.y = 0
        

    def move_mummy_down(self, dt):
        if self.allowed_down:
            #self.going_nowhere = True
            self.the_mummy.y -= self.speed
        else:
            self.the_mummy.image = self.idle

        

    def move_mummy_up(self, dt):
        if self.allowed_up:
            #self.going_nowhere = True
            self.the_mummy.y += self.speed
        else:
            self.the_mummy.image = self.idle


    def move_mummy_left(self, dt):
        if self.allowed_left:
            #self.going_nowhere = True
            self.the_mummy.x -= self.speed
        else:
            self.the_mummy.image = self.idle


    def move_mummy_right(self, dt):
        if self.allowed_right:
            #self.going_nowhere = True
            self.the_mummy.x += self.speed
        else:
            self.the_mummy.image = self.idle
            
    def is_moving(self, dt):
        if not (self.the_mummy.x == self.o_x and self.the_mummy.y == self.o_y):
            return True
        else:
            return False
        
    def updatepos(self, dt):
        self.o_x = self.the_mummy.x
        self.o_y = self.the_mummy.y
        
    def mummy_stop(self):
        self.speed = 0
        
    def get_y(self):
        return self.the_mummy.y
    
    def get_x(self):
        return self.the_mummy.x
    
    def return_pos(self):
        return self.the_mummy.position