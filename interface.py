import pyglet

WINDOW_SIZE_X = 1300
WINDOW_SIZE_Y = 1000

# Use the interface class to manage the GUI elements
# on-screen. I have done it like this so that individual
# elements can be removed if necessary. 
class Interface:
    "This class controls the GUI of the game."
    def __init__(self, game, group_images, group_text, batch):
        self.batch = batch
        self.group_images = group_images
        self.group_text = group_text
        self.game = game
        
        self.scroll_handle_width = 20
        self.spacing = 1

        self.logo_image = pyglet.image.load("res/images/logo.png")
        self.logo = pyglet.sprite.Sprite(img=self.logo_image, x=self.spacing+20,
                                     y=WINDOW_SIZE_Y/1.17, batch=self.batch,
                                     group=self.group_images)
            
        self.score_image = pyglet.image.load("res/images/score_scroll.png")
        self.score_scroll = pyglet.sprite.Sprite(img=self.score_image, x=self.logo.width + self.spacing,
                                             y=WINDOW_SIZE_Y/1.17, batch=self.batch,
                                             group=self.group_images)
        
        # Gets the position where the lives, bonus, score container will start.
        # This is necessary because we may scale (or move) the scroll behind it at some point.
        # If we scale the scroll, then we lose the positioning.
        # The following code aims to stop the positioning of the messing up.
        # This code will position everything correctly even if you move the scroll.
        
        # First of all we need to find where the lives container will start.
        # And where it will end.
        self.livescontainer_start = self.score_scroll.x + self.scroll_handle_width
        self.livescontainer_end = self.livescontainer_start + self.score_scroll.width/4
    
        # The ending of the lives container is the start of the bonus container.
        self.bonuscontainer_start = self.livescontainer_end
        self.bonuscontainer_end = self.bonuscontainer_start + self.score_scroll.width/4
    
        # The ending of the bonus container is the start of the score container.
        self.scorecontainer_start = self.bonuscontainer_end
        self.scorecontainer_end = (self.scorecontainer_start - 
                                   self.scroll_handle_width + 
                                   self.score_scroll.width/2)
        
        # Initialise all the classes that control the GUI.
        self.score = Score(self.group_text, self.batch, self.scorecontainer_start,
                           self.score_scroll.y,
                           self.scorecontainer_end - self.scorecontainer_start,
                           self.score_scroll.height/1.5)
        
        self.lives = Lives(self.group_text, self.batch, self.livescontainer_start,
                           self.score_scroll.y,
                           self.livescontainer_end - self.livescontainer_start,
                           self.score_scroll.height/1.5)
        
        self.bonus = Bonus(self.group_text, self.batch, self.bonuscontainer_start,
                           self.score_scroll.y,
                           self.bonuscontainer_end - self.bonuscontainer_start,
                           self.score_scroll.height/1.5)
        
        # Create the remaining elements
        self.active_key_scroll = pyglet.resource.image("parchment.png")
        self.key_scroll = pyglet.resource.image("parchment_faded.png")
        self.key_scroll_sprite = pyglet.sprite.Sprite(img=self.key_scroll, 
                                                     x=self.logo.width + 
                                                     self.score_scroll.width + self.spacing*3,
                                                     y=WINDOW_SIZE_Y/1.17, batch=self.batch,
                                                     group=self.group_images)
        self.key_scroll_sprite.scale = 0.5
        
        self.level = Level(self.group_text, self.batch,
                           self.logo.width + self.score_scroll.width + 
                           self.key_scroll_sprite.width + self.spacing*35,
                           self.score_scroll.y,
                           self.game.return_level())
        
        self.level_im = pyglet.resource.image("level.png")
        self.level_im_sprite = pyglet.sprite.Sprite(img=self.level_im, 
                                                     x=self.logo.width + self.score_scroll.width + 
                                                     self.key_scroll_sprite.width + self.spacing*35,
                                                     y=WINDOW_SIZE_Y/1.17 + 80, batch=self.batch,
                                                     group=self.group_text)
        self.level_im_sprite.scale = 0.5

        self.level_num = pyglet.image.load("res/images/circle_frame.png")
        self.level_wide = self.logo.width + self.score_scroll.width + self.key_scroll_sprite.width + self.spacing*42
        self.level_num_sprite = pyglet.sprite.Sprite(img=self.level_num, 
                                                     x=self.level_wide,
                                                     y=WINDOW_SIZE_Y/1.17+4, batch=self.batch,
                                                     group=self.group_images)
        self.level_num_sprite.scale = 0.3
        
    # Call this whenever you need to update the score.
    def update_score_value(self):
        self.score.update_score()
        
    def update_bonus(self):
        self.bonus.update_bonus()
        
    def gotthe_key_scroll(self):
        self.key_scroll_sprite.image = self.active_key_scroll

    def notgotthe_key_scroll(self):
        self.key_scroll_sprite.image = self.key_scroll

    # Call this to return the score value.
    def get_score_value(self):
        return self.score.return_score()
        
    # Call this to return the bonus value.
    def get_bonus_value(self):
        return self.bonus.return_bonus()
        
    # Call this to revert all values.
    def revert_all_value(self):
        self.score.revert_score()
        self.bonus.revert_bonus()
        
    # Call this to revert the score value.
    def revert_score_value(self):
        self.score.revert_score()
        
    # Call this to revert the bonus value.
    def revert_bonus_value(self):
        self.bonus.revert_bonus_value()
    
    # New bonus value - update the old and new bonus now.
    def inject_bonus(self, the_new_bonus):
        self.bonus.new_bonus(the_new_bonus)
        
    # New score value - update the old and new score now.
    def inject_score(self, the_new_score):
        self.score.new_score(the_new_score)
        
    # Call this whenever you need to store the current values.
    def carry_all_value(self):
        self.score.update_old_score()
        self.bonus.update_old_bonus()

    # Call this whenever you need to carry score values forward to new level.
    def carry_score_value(self):
        self.score.update_old_score()
        
    # Call this whenever you need to carry score values forward to new level.
    def carry_bonus_value(self):
        self.bonus.update_old_bonus()
        
    # Call this to return the lives value
    def lost_life(self):
        self.lives.lose_life()
        
    # Call this to return the lives value
    def get_lives_value(self):
        return self.lives.return_lives()
        

# Updates the score.
class Score(Interface):
    def __init__(self, group_text, batch, x, y, width, height):
        self.group_text = group_text
        self.batch = batch
        self.x_loc = x
        self.y_loc = y
        self.width = width
        self.height = height
        self.score_num_old = 0
        self.score_num = 0
        
        self.scoreimage = pyglet.resource.image("score.png")
        self.simage = pyglet.sprite.Sprite(img=self.scoreimage, 
                      x=self.x_loc+71, y=self.y_loc+63.5, 
                      batch=batch, group=group_text)
        self.simage.scale = 0.46
        self.document = pyglet.text.document.FormattedDocument(" \n \n ")
        self.document.set_style(0, len(self.document.text),
                                dict(color=(0, 0, 0, 255)))
         
         
        self.layout = pyglet.text.layout.IncrementalTextLayout(self.document,
                                                                self.width,
                                                                self.height,
                                                                multiline=True,
                                                                batch=self.batch,
                                                                group=self.group_text)
        
        self.position(self.layout, self.x_loc + self.width/2, self.y_loc)
        self.update_score()
        
    def revert_score(self):
        self.score_num = self.score_num_old
        self.update_score()
    
    # Updates the old score value so that if we're going on next level
    # the score gets carried over.
    def update_old_score(self):
        self.score_num_old = self.score_num
        
    def new_score(self, score):
        self.score_num_old = score
        self.score_num = score
    
    def return_score(self):
        return self.score_num
    
    def position(self, document, x, y):
        document.x = x
        document.y = y
    
    def update_score(self):
        self.document.delete_text(0, len(self.document.text))
        self.score_num += 1
        self.document.insert_text(0, " \n \n " + str(self.score_num))

# Updates the lives.
class Lives(Interface):
    def __init__(self, group_text, batch, x, y, width, height):
        self.group_text = group_text
        self.batch = batch
        self.x_loc = x
        self.y_loc = y
        self.width = width
        self.height = height
        self.lives_num = 3
        self.lives_array = []
        self.position_lives = self.x_loc
        
        self.livesimage = pyglet.resource.image("lives.png")
        self.heartimage = pyglet.resource.image("heart.png")
        self.limage = pyglet.sprite.Sprite(img=self.livesimage, 
                      x=self.x_loc+45, y=self.y_loc+67, 
                      batch=batch, group=group_text)
        self.limage.scale = 0.35
        self.document = pyglet.text.document.FormattedDocument("\n \n ")
        self.document.set_style(0, len(self.document.text), {'color':(0,0,0,1)})
         
        self.layout = pyglet.text.layout.IncrementalTextLayout(self.document,
                                                                self.width,
                                                                self.height,
                                                                multiline=True,
                                                                batch=self.batch,
                                                                group=self.group_text)
        
        self.position(self.layout, self.x_loc + self.width/2, self.y_loc)
        self.update_lives()
        
    
    def return_lives(self):
        return self.lives_num
    
    def lose_life(self):
        self.lives_num -= 1
        if len(self.lives_array) > 0:
            self.lives_array[-1].visible = False
            self.lives_array.pop()
    
    def position(self, document, x, y):
        document.x = x
        document.y = y
    
    def update_lives(self):
        if not(len(self.lives_array) >= self.lives_num):
            for lives in range(0, self.return_lives()):
                self.heart_sprite =  pyglet.sprite.Sprite(img=self.heartimage, 
                                                          x=self.position_lives+55, y=self.y_loc+37, 
                                                          batch=self.batch, group=self.group_text)
                self.lives_array.append(self.heart_sprite)
                self.position_lives += 23
# Updates the bonus points.
class Bonus(Interface):
    def __init__(self, group_text, batch, x, y, width, height):
        self.group_text = group_text
        self.batch = batch
        self.x_loc = x
        self.y_loc = y
        self.width = width
        self.height = height
        self.bonus_num_old = 0
        self.bonus_num = 0
        
        self.bonusimage = pyglet.resource.image("bonus.png")
        self.bimage = pyglet.sprite.Sprite(img=self.bonusimage, 
                      x=self.x_loc+56, y=self.y_loc+62, 
                      batch=batch, group=group_text)
        self.bimage.scale = 0.40
        
        self.document = pyglet.text.document.FormattedDocument(" \n \n ")
        self.document.set_style(0, len(self.document.text),
                                dict(color=(0, 0, 0, 255)))
        self.document.set_paragraph_style(0, len(self.document.text), dict(align=("center")))
        
         
         
        self.layout = pyglet.text.layout.IncrementalTextLayout(self.document,
                                                                self.width,
                                                                self.height,
                                                                multiline=True,
                                                                batch=self.batch,
                                                                group=self.group_text)
        
        self.position(self.layout, self.x_loc + self.width/2 -10, self.y_loc)
        self.update_bonus()
        
    def revert_bonus(self):
        self.bonus_num = self.bonus_num_old
        self.update_bonus()
    
    # Updates the old bonus value so that if we're going on next level
    # the bonus gets carried over.
    def update_old_bonus(self):
        self.bonus_num_old = self.bonus_num
        
    def new_bonus(self, bonus):
        self.bonus_num_old = bonus
        self.bonus_num = bonus
        
    def return_bonus(self):
        return self.bonus_num
    
    def position(self, document, x, y):
        document.x = x
        document.y = y
    
    def update_bonus(self):
        self.document.delete_text(0, len(self.document.text))
        self.bonus_num += 10
        self.document.insert_text(0, " \n \n " + str(self.bonus_num))
        
# Updates the bonus points.
class Level(Interface):
    def __init__(self, group_text, batch, x, y, level):
        self.group_text = group_text
        self.batch = batch
        self.x_loc = x
        self.y_loc = y
        self.level_number = level
        self.txt_lvl = str(self.return_level())
        self.sprite_array = []
        
        self.n0 = pyglet.resource.image("0.png") 
        self.n1 = pyglet.resource.image("1.png")
        self.n2 = pyglet.resource.image("2.png")
        self.n3 = pyglet.resource.image("3.png")
        self.n4 = pyglet.resource.image("4.png")
        self.n5 = pyglet.resource.image("5.png")
        self.n6 = pyglet.resource.image("6.png")
        self.n7 = pyglet.resource.image("7.png")
        self.n8 = pyglet.resource.image("8.png")
        self.n9 = pyglet.resource.image("9.png")
        self.update_level()
        
    
    def return_level(self):
        return self.level_number + 1
    
    def update_level(self):
        if len(self.txt_lvl) == 1:
            self.x_loc += 20
        for letter in self.txt_lvl:
                if letter == "0":
                    self.sn0 = pyglet.sprite.Sprite(img=self.n0, x=self.x_loc+22, 
                                         y=self.y_loc+30, batch=self.batch, group=self.group_text)
                    self.sprite_array.append(self.sn0)
                    
                elif letter == "1":
                    self.sn1 = pyglet.sprite.Sprite(img=self.n1, x=self.x_loc+22, 
                                         y=self.y_loc+30, batch=self.batch, group=self.group_text)
                    self.sprite_array.append(self.sn1)
                    
                elif letter == "2":
                    self.sn2 = pyglet.sprite.Sprite(img=self.n2, x=self.x_loc+22, 
                                         y=self.y_loc+30, batch=self.batch, group=self.group_text)
                    self.sprite_array.append(self.sn2)
                    
                elif letter == "3":
                    self.sn3 = pyglet.sprite.Sprite(img=self.n3, x=self.x_loc+22, 
                                         y=self.y_loc+30, batch=self.batch, group=self.group_text)
                    self.sprite_array.append(self.sn3)
                    
                elif letter == "4":
                    self.sn4 = pyglet.sprite.Sprite(img=self.n4, x=self.x_loc+22, 
                                         y=self.y_loc+30, batch=self.batch, group=self.group_text)
                    self.sprite_array.append(self.sn4)
                    
                elif letter == "5":
                    self.sn5 = pyglet.sprite.Sprite(img=self.n5, x=self.x_loc+22, 
                                         y=self.y_loc+30, batch=self.batch, group=self.group_text)
                    self.sprite_array.append(self.sn5)
                    
                elif letter == "6":
                    self.sn6 = pyglet.sprite.Sprite(img=self.n6, x=self.x_loc+22, 
                                         y=self.y_loc+30, batch=self.batch, group=self.group_text)
                    self.sprite_array.append(self.sn6)
                    
                elif letter == "7":
                    self.sn7 = pyglet.sprite.Sprite(img=self.n7, x=self.x_loc+22, 
                                         y=self.y_loc+30, batch=self.batch, group=self.group_text)
                    self.sprite_array.append(self.sn7)
                    
                elif letter == "8":
                    self.sn8 = pyglet.sprite.Sprite(img=self.n8, x=self.x_loc+22, 
                                         y=self.y_loc+30, batch=self.batch, group=self.group_text)
                    self.sprite_array.append(self.sn8)
                    
                elif letter == "9":
                    self.sn9 = pyglet.sprite.Sprite(img=self.n9, x=self.x_loc+22, 
                                         y=self.y_loc+30, batch=self.batch, group=self.group_text)
                    self.sprite_array.append(self.sn9)
                    
                self.x_loc += 40
                
        for sprite in self.sprite_array:
            sprite.scale = 0.6
                    
