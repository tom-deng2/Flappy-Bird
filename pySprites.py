'''Author : Tom Deng

   Description : This module contains classes for the Flappy Bird game.
   
   Date : 29/05/2017
'''
import pygame,random

class Bird(pygame.sprite.Sprite):
    '''This class defines the sprite for the bird.'''
    def __init__(self):
        '''This initializer method has no parameters. It loads the images and
        sound files, and defines key variables.'''
        pygame.sprite.Sprite.__init__(self)
        self.__flap_sound = pygame.mixer.Sound("Sounds/sfx_wing.wav")
        self.__hit_sound = pygame.mixer.Sound("Sounds/sfx_hit.wav")
        self.__point_sound = pygame.mixer.Sound("Sounds/sfx_point.wav")
        self.__point_sound.set_volume(1)
        self.__hit_sound.set_volume(1)
        self.__fall_sound = pygame.mixer.Sound("Sounds/sfx_die.wav")
        self.__fall_sound.set_volume(1)
        self.__upflap = pygame.image.load("Sprites/bird_upflap.gif")
        self.__upflap.convert()
        self.__downflap = pygame.image.load("Sprites/bird_downflap.gif")
        self.__downflap.convert()
        self.__midflap = pygame.image.load("Sprites/bird_midflap.gif")
        self.__midflap.convert()
        self.__images = [self.__upflap,self.__midflap,self.__downflap]
        self.image = self.__midflap
        #copy of image, it will be used for rotating/animation purposes 
        self.__original = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (250,300)
        #jumping speed of the bird
        self.__dy = 0
        #default gravity value
        self.__gravity = 2
        self.__max_grav = 15
        #keeps track of height jumped by the bird
        self.__distance = 0
        self.__rot = 0
        self.__current_angle = 0
        self.__flap_index = -1
        self.__falling = False
        self.__jump_height = 9
        self.__dead = False
        self.__play_sound = True
        self.__tick_count = 0
        
    def rotate(self):
        '''This method rotates the bird depending on the angle given.'''
        #saves the position of the old image before rotation (for image quality purposes)
        oldCenter = self.rect.center
        self.image = pygame.transform.rotate(self.__original, self.__rot)
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(-5,0)
        self.rect.center = oldCenter
        
    def jump(self):
        '''This method makes the bird move upwards in the y-direction.'''
        if self.__dead == False:
            self.__flap_sound.play()
            self.__falling = False
            self.__dy = -6.1
            self.__distance = 0
            self.__gravity = 2
            self.rotate()
        
    def set_gravity(self):
        '''This method sets the multiplies the gravity attribute by 1.15.'''
        if self.__gravity < self.__max_grav:
            self.__gravity *= 1.15
            
    def hit_pipe(self):
        '''This method plays the sounds for when the bird collides with the pipe.'''
        #only play the hit sound once
        if self.__play_sound:        
            self.__hit_sound.play()
            self.__play_sound = False
        self.__dead = True
        self.__fall_sound.play()
        
    def hit_ground(self):
        '''This method plays the sound for when the bird collides with the ground.'''
        self.__dead = True
        if self.__play_sound:
            self.__hit_sound.play()

    def point_sound(self):
        '''This method plays the sound for when the player gets a point.'''
        self.__point_sound.play()
        
    def stop(self):
        '''This method sets the gravity attribute to 0.'''
        self.__gravity = 0
        
    def get_status(self):
        '''This method returns the dead attribute.'''
        return self.__dead
        
    def update(self):
        '''This method is called automatically to reposition the bird sprite.
        It also manages the animations, rotations, and if the bird is falling 
        or going upwards.'''
        if self.__dead == False:
            self.__flap_index += 1
            self.__tick_count += 1
            
            if self.__flap_index >= len(self.__images):
                self.__flap_index = -1
                
            elif self.__falling == False and self.__tick_count == 1:
                self.__original = self.__images[self.__flap_index]       
                
            elif self.__falling:
                self.__original = self.__midflap
                
            if self.__tick_count == 3:
                self.__tick_count = 0             
                
            if self.__distance < self.__jump_height:
                self.rect.top += self.__dy
                if self.__dy == -6.1:
                    self.__distance += 1
                    if self.__current_angle < 30:
                        self.__rot += 22
                        self.__current_angle += 22
                    
            elif self.__distance == self.__jump_height:
                if self.__current_angle > -90:
                    self.__rot += -5
                    self.__current_angle += -5
                #angle at which bird stops flapping
                if self.__current_angle < -40:
                    self.__falling = True
                    
                self.set_gravity()
                self.rect.top += self.__gravity

        else:
            if self.__current_angle > -90:
                self.__rot += -12
                self.__current_angle += -12
            self.set_gravity()
            self.rect.top += self.__gravity     
            
class TopPipe(pygame.sprite.Sprite):
    '''This class defines the sprite for the top pipe.'''
    def __init__(self,x_start):
        '''This initializer method has one parameter called x_start. Which should be
        a integer value for the x-position the top pipe should start at. This method
        also generates a random y position to start at.'''
        pygame.sprite.Sprite.__init__(self)    
        self.image = pygame.image.load("Sprites/top_green_pipe.gif")
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(-5,-15)
        self.__random_y = random.randint(-350, -90)
        self.rect.topleft = (x_start,self.__random_y)
        self.__dx = 0
        
    def reset(self):
        '''This method repositions the sprite back to the right side of the screen,
        and generates a random y position to start at.'''
        self.__random_y = random.randint(-350, -90)
        self.rect.topleft = (640,self.__random_y)
        
    def start(self):
        '''This method sets the dx attribute to -5, which will move the pipe
        to the left.'''
        self.__dx = -5
        
    def stop(self):
        '''This method sets the dx attribute to 0, which stops the pipe.'''
        self.__dx = 0
        
    def get_pixels(self):
        '''This method returns the amount of pixels the top pipe takes up on the screen.'''
        return 400 + self.__random_y
        
    def get_x_position(self):
        '''This method returns the top pipe's x-position.'''
        return self.rect.topleft[0] 
    
    def update(self):
        '''This method is called automatically to reposition the top pipe sprite.'''
        self.rect.left += self.__dx
        
class BottomPipe(pygame.sprite.Sprite):
    '''This class defines the sprite for the bottom pipe.'''
    def __init__(self,top_pipey,x_start):
        '''This initializer method has two parameters, top_pipey and x_start. top_pipey
        should be an integer value that is how much pixels the top pipe takes up.
        x_start should be an integer value for the x-position the bottom pipe should start
        at. This method also defines key variables.'''
        pygame.sprite.Sprite.__init__(self)
        #constant space in between the pipes
        self.__space = 100
        self.image = pygame.image.load("Sprites/bottom_green_pipe.gif")
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(-5,-25)
        self.rect.topleft = (x_start,top_pipey + self.__space)
        self.__dx = 0
        
    def start(self):
        '''This method sets the dx attribute to -5, which will move the pipe
        to the left.'''
        self.__dx = -5
        
    def stop(self):
        '''This method sets the dx attribute to 0, which stops the pipe.'''
        self.__dx = 0    
        
    def get_x_position(self):
        '''This method returns the bottom pipe's x-position.'''
        return self.rect.topleft[0]
    
    def reset(self,top_pipey):
        '''This method has a parameter called top_pipey, which should be an
        integer value for how many pixels the top pipe takes up on the screen. 
        This method sets the position of the bottom pipe back to the left side of 
        the screen, and the y-position based on the y-position of the top pipe.
        '''
        self.rect.topleft = (640,top_pipey + self.__space)
        
    def update(self):
        '''This method is called automatically to reposition the bottom pipe sprite.'''
        self.rect.left += self.__dx
        
class ScoreBoard(pygame.sprite.Sprite):
    '''This class defines a label sprite to display the score.'''
    def __init__(self):
        '''This initializer loads the custom font "FlappyFont", and
        sets the starting score to 0.'''        
        pygame.sprite.Sprite.__init__(self)
        self.__font = pygame.font.Font("FlappyFont.ttf", 30)
        self.__score = 0

    def score(self):
        '''This method adds one to the score attribute.'''
        self.__score += 1
    
    def update(self):
        '''This method will be called automatically to display the current 
        score at the top of the game window.'''        
        self.__message = str(self.__score) 
        self.image = self.__font.render(self.__message, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (320, 30)
        

class Ground(pygame.sprite.Sprite):
    '''This class defines the sprite for the ground.'''
    def __init__(self):
        '''This initialzer method sets key variables and loads the image for the
        ground.'''
        pygame.sprite.Sprite.__init__(self)    
        self.image = pygame.image.load("Sprites/base2.gif")
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,440)
        self.__dx = -5
        
    def stop(self):
        '''This method sets the dx attribute to 0, which stops the ground.'''
        self.__dx = 0
    
    def update(self):
        '''This method is called automatically to reposition the ground sprite.'''
        self.rect.left += self.__dx 
        if self.rect.left <= -640:
            self.rect.left = 0
            
class Instructions(pygame.sprite.Sprite):
    '''This class defines the sprite for the instructions.'''
    def __init__(self):
        '''This initialzer method sets key variables and loads the image for the
        instructions.'''        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Sprites/message.gif")
        self.image.convert_alpha()      
        self.rect = self.image.get_rect()
        self.rect.center = (320,220)
        self.__transparency = 255
        self.__start = False
        
    def start_fade(self):
        '''This method sets the start attribute to True.'''
        self.__start = True
        
    def update(self):
        '''This method is called automatically to show the instructions sprite,
        after the start attribute is set to True.'''
        if self.__start:
            self.__transparency -= 5
            self.image.set_alpha(self.__transparency)
            #removes the object after fading finishes
            if self.__transparency <= 0:
                self.kill()

class EndMessage(pygame.sprite.Sprite):
    '''This class defines the sprite for the end message.'''
    def __init__(self):
        '''This initializer method loads the images and sets key variables.'''
        pygame.sprite.Sprite.__init__(self)
        #used as a fully transparent image
        self.image = pygame.image.load("Sprites/blank.gif")
        self.__end_message = pygame.image.load("Sprites/end_screen.gif")
        self.__end_message.convert_alpha() 
        self.rect = self.image.get_rect()
        self.rect.topleft = (220,100)
        self.__transparency = 0
        self.__start = False
        
    def start_fade(self):
        '''This method sets the start attribute to True and changes the image to
        the end message.'''
        self.__start = True
        self.image = self.__end_message
        
    def update(self):
        '''This method is called automatically to show the end message sprite,
        after the start attribute is set to True.'''
        if self.__start:
            self.__transparency += 20
            self.image.set_alpha(self.__transparency)

        