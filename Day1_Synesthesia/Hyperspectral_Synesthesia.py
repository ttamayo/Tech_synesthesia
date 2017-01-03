import sys, pygame
import matplotlib.image as mpimg
from pydub import AudioSegment
import numpy as np
import sys
import pickle as pkl
import time
import os

#Load the hyperspectral slices you want to hear: 
nm_list = [620,590,520,455]

nm_dict = {}
max_dict = {}
for nm in nm_list:
    file_name = os.path.join('image_dir', 'single_channel_' +str(nm)+ '_nm.pkl')
    channel = pkl.load( open(file_name, 'rb') )
    nm_dict[nm] = channel
    print nm, channel.shape
    max_dict[nm] = np.float(np.max(channel))

#Load the sounds that will be mapped to each channel-- 
# Using the pygame.mixer subclass. 
sound_files = ['double-bass_C2', 'cello_E4', 'mandolin_G4_very-long_piano_normal', 'violin_A4']
pygame.mixer.init()
sound_dict = {}
for i in range(len(nm_list)):
    nm = nm_list[i]
    sound_file = sound_files[i]
    sound_file_full = os.path.join('sound_dir', sound_file+'.ogg')
    sound_dict[nm] = pygame.mixer.Sound(sound_file_full)

#Load the background RGB image
image = pkl.load(open('image_dir/LEDs_4_RGB.pkl', 'rb')) # Do I really need this? 
#Get image dimensions -- 
width = image.shape[1]
height = image.shape[0]

size = width, height #= 1400, 600 
speed = [0, 0]
black = 0, 0, 0

print 'WIDTH, HEIGHT', width, height

pygame.init()

# Set the screen size to be the dimensions of the image. 
screen = pygame.display.set_mode(size)

#### PyGame commands to display the image on the screen 
image_background = pygame.image.load("image_dir/LEDs_4_RGB.png")
image_background_rect = image_background.get_rect() #what does this command do? 

while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            #Grab mouse click coordinate. 
            X,Y = pygame.mouse.get_pos()
            # Grab the intensity of each hyperspectral channel at coordinate X,Y. 
            # and convert to volume
            volume_dict = {}
            for nm in nm_list:
                volume_dict[nm] = nm_dict[nm][Y,X] / max_dict[nm]

            print X,Y, '\n'

            #These two commands in PyGame set the volume and play the sound. 
            for nm in nm_list:
                print 'Channel -- ', str(nm), str(volume_dict[nm])
                sound_dict[nm].set_volume( volume_dict[nm] )
                sound_dict[nm].play()
                time.sleep(1)
                #sound_dict[nm].stop()


        ## You can play around with mouse click / release.. 

        # if event.type == pygame.MOUSEBUTTONUP:
        #     sound_R.fadeout(1000)
        #     # sound_G.fadeout(1000)
        #     sound_B.fadeout(1000)


    screen.fill(black)
    screen.blit(image_background, image_background_rect)

    pygame.display.flip()

