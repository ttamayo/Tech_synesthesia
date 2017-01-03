import pygame
import matplotlib.image as mpimg
import numpy as np
import time


#initialize pygame
pygame.init()
sound_delay = 0.5

### Load an image file called Sample.jpg that's stored in the image_dir directory: 

###

### Store the height and width of the image: 

###

### Store each of the three channels (Red, Green, Blue) separately as different variables: 

###

### Get the maximum value of each channel. Store in separate variables:

###

pygame.mixer.init()

### Choose three different instrument-notes from the "sound_dir" directory. 
### Load them as sounds using the mixer.Sound() function, 
### and store them separately as soundRed, soundGreen, and soundBlue variables.

###

#some not-important pygame stuff. 
size = width, height
speed = [0, 0]
black = 0, 0, 0

# Set the screen size to be the dimensions of the image. 
screen = pygame.display.set_mode(size)

#PyGame commands to display the image on the screen 
image_background = pygame.image.load("image_dir/Sample.jpg")
image_background_rect = image_background.get_rect()

while 1: #An infinite while loop...

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  #if you click the "quit" button, exit the game
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN: #if you click the mouse button
            #Grab mouse click coordinate. 
            X,Y = pygame.mouse.get_pos()
            
            ### Grab the pixel intensity of each color in the X (column), Y (row) position.  
            
            ###
            
            ### Convert channel intensity to volume. Can be modified. 
            
            ###

            print X,Y, R_sig, R_vol_pix, B_sig, B_vol_pix
            
            ### Set the volume of the sound using the set_volume(my_volume) function. 
            ### Play each sound using the play() method.   
            ### Add a time delay between each sound.  
            
            ###

    #Other not-important pygame stuff
    screen.fill(black)
    screen.blit(image_background, image_background_rect)

    pygame.display.flip()

