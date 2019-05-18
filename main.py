'''Author : Tom Deng

   Date : 2017/05/09
   
   Description : This is a flappy bird game.
'''

# I - Import and Initialize
import pygame,pySprites
pygame.init()
pygame.mixer.init()

def main():
    '''This function defines the 'mainline logic' for our game.'''
     
    # Display
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Basic Sprite Demo")

    # Entities
    background = pygame.image.load("Sprites/background.gif")
    background = background.convert()
    screen.blit(background, (0,0))
    
    pygame.mixer.music.load("Music.mp3")
    pygame.mixer.music.set_volume(0)
    pygame.mixer.music.play(-1)
    
    # create a Box sprite object
    bird = pySprites.Bird()
    top_pipe = pySprites.TopPipe(840)
    bottom_pipe = pySprites.BottomPipe(top_pipe.get_pixels(),840)
    
    top_pipe2 = pySprites.TopPipe(1065)
    bottom_pipe2 = pySprites.BottomPipe(top_pipe2.get_pixels(),1065)
    
    top_pipe3 = pySprites.TopPipe(1290)
    bottom_pipe3 = pySprites.BottomPipe(top_pipe3.get_pixels(),1290)
    
    top_pipes = [top_pipe, top_pipe2,top_pipe3]
    bottom_pipes = [bottom_pipe, bottom_pipe2,bottom_pipe3]
    
    pipes = pygame.sprite.Group(top_pipe,bottom_pipe,top_pipe2,bottom_pipe2,top_pipe3,bottom_pipe3)
    
    score_board = pySprites.ScoreBoard()
    
    ground = pySprites.Ground()
    ground_group = pygame.sprite.Group(ground)
    
    instructions = pySprites.Instructions()
    
    end_message = pySprites.EndMessage()
    
    allSprites = pygame.sprite.OrderedUpdates(pipes,bird,score_board,ground_group,instructions,end_message)
     
    # ACTION
     
    # Assign 
    
    clock = pygame.time.Clock()
    keepGoing = True
    started = False
    end = False

    # Loop
    while keepGoing:

        # Time
        clock.tick(30)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    bird.jump()
                    if started == False:
                        instructions.start_fade()
                        for pipe in pipes:
                            pipe.start()
                #when the user presses "ok" after gameover screen pops up, it will restart the game.
                if event.button == 1 and end == True and pygame.mouse.get_pos()[0] > 279 and pygame.mouse.get_pos()[0] < 354 and pygame.mouse.get_pos()[1] > 310 and pygame.mouse.get_pos()[1] < 332:
                    main()
                    keepGoing = False
                    
        stop_index = -1
        #collision detection for ground and the bird
        if pygame.sprite.spritecollide(bird, ground_group,False):
            for x in pygame.sprite.spritecollide(bird, ground_group,False):
                pipes.empty()
                ground_group.empty()
                bird.hit_ground()
                bird.stop()  
                ground.stop()
                for pipe in top_pipes:
                    stop_index += 1
                    pipe.stop()
                    bottom_pipes[stop_index].stop()
                
        #bird and pipe collision detection
        if pygame.sprite.spritecollide(bird, pipes,False):
            bird.hit_pipe()
            pipes.empty()
            ground.stop()
            #stops all the pipes after death  
            for pipe in top_pipes:
                stop_index += 1
                pipe.stop()
                bottom_pipes[stop_index].stop()
        
        #if bird goes over the top of the screen
        elif bird.rect.top <= -20:
            bird.hit_pipe()
            pipes.empty()
            ground.stop()            
            for pipe in top_pipes:
                stop_index += 1
                pipe.stop()
                bottom_pipes[stop_index].stop()            
                
        #resets the pipes
        pipe_index = -1
        for pipe in top_pipes:
            pipe_index += 1
            if pipe.get_x_position() <= -45:
                pipe.reset()
                bottom_pipes[pipe_index].reset(pipe.get_pixels())
            #adds a point after bird passes pipe
            if pipe.get_x_position() == 250:
                score_board.score()            
                bird.point_sound()
                
        #constantly rotates the bird
        bird.rotate()
        
        #when the game ends the gameover message appears
        if bird.get_status() and end == False:
            end = True
            end_message.start_fade()

        # Refresh screen
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
     
        pygame.display.flip()
    
main()
pygame.quit()