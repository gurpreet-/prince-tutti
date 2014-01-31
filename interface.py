import pyglet

WINDOW_SIZE_X = 1300
WINDOW_SIZE_Y = 1000

# Use the interface class to manage the GUI elements
# on-screen. I have done it like this so that individual
# elements can be removed if necessary. 
class Interface:
    '''This class controls the GUI of the game.'''
    def __init__(self, group_images, group_text, batch):
        self.batch = batch
        self.group_images = group_images
        self.group_text = group_text
        
        self.scroll_handle_width = 20
        self.spacing = 20

        self.logo_image = pyglet.image.load("res/images/logo.png")
        self.logo = pyglet.sprite.Sprite(img=self.logo_image, x=self.spacing,
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
        self.scorecontainer_end = self.scorecontainer_start - self.scroll_handle_width + self.score_scroll.width/2
        
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
        
    # Call this whenever you need to update the score.
    def update_score_value(self):
        self.score.update_score()
    
    # Call this to return the score value.
    def get_score_value(self):
        self.score.return_score()

# Updates the score.
class Score(Interface):
    def __init__(self, group_text, batch, x, y, width, height):
        self.group_text = group_text
        self.batch = batch
        self.x_loc = x
        self.y_loc = y
        self.width = width
        self.height = height
        self.score_num = 0
        
        self.score_heading = "Score\n"
        self.document = pyglet.text.document.FormattedDocument(self.score_heading)
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
        
    
    def return_score(self):
        return self.score_num
    
    def position(self, document, x, y):
        document.x = x
        document.y = y
    
    def update_score(self):
        self.score_num = str(43434)
        self.document.insert_text(len(self.document.text), self.score_num)

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
        
        self.lives_heading = "Lives\n"
        self.document = pyglet.text.document.FormattedDocument(self.lives_heading)
        self.document.set_style(0, len(self.document.text),
                                dict(color=(0, 0, 0, 255)))
         
         
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
    
    def position(self, document, x, y):
        document.x = x
        document.y = y
    
    def update_lives(self):
        self.lives_num = str(self.lives_num)
        self.document.insert_text(len(self.document.text), self.lives_num)

# Updates the bonus points.
class Bonus(Interface):
    def __init__(self, group_text, batch, x, y, width, height):
        self.group_text = group_text
        self.batch = batch
        self.x_loc = x
        self.y_loc = y
        self.width = width
        self.height = height
        self.bonus_num = 500
        
        self.bonus_heading = "Bonus\n"
        self.document = pyglet.text.document.FormattedDocument(self.bonus_heading)
        self.document.set_style(0, len(self.document.text),
                                dict(color=(0, 0, 0, 255)))
        self.document.set_paragraph_style(0, len(self.document.text), dict(align=("center")))
         
         
        self.layout = pyglet.text.layout.IncrementalTextLayout(self.document,
                                                                self.width,
                                                                self.height,
                                                                multiline=True,
                                                                batch=self.batch,
                                                                group=self.group_text)
        
        self.position(self.layout, self.x_loc + self.width/2, self.y_loc)
        self.update_bonus()
        
    
    def return_bonus(self):
        return self.bonus_num
    
    def position(self, document, x, y):
        document.x = x
        document.y = y
    
    def update_bonus(self):
        self.bonus_num = str(self.bonus_num)
        self.document.insert_text(len(self.document.text), self.bonus_num)
