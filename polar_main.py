import librosa
import numpy as np
import pygame
import math
import random
import eyed3
from os import listdir
from os.path import isfile, join


musicfiles = ['./music/' + f for f in listdir('./music') if isfile(join('./music', f))]
random.shuffle(musicfiles)
#musicfiles=['./music/above-the-clouds.mp3']

print(musicfiles)
MUSIC_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(MUSIC_END)

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0,0,0)
background_color=(255,200,50)
foreground_color=(0,0,0)





def clamp(min_value, max_value, value):

    if value < min_value:
        return min_value

    if value > max_value:
        return max_value

    return value


class AudioBar:

    def __init__(self, ang_pos, y, freq, color, ang_width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        #print(x,y)
        self.ang_pos, self.y, self.freq = ang_pos, y, freq

        self.color = color
        self.color_list=[
            (32,32,192),(128,0,128),(128,128,0),(0,128,0),(0,64,0),(0,128,128),(0,64,64)
        ]

        self.ang_width, self.min_height, self.max_height = ang_width, min_height, max_height

        self.height = min_height

        self.min_decibel, self.max_decibel = min_decibel, max_decibel

        self.__decibel_height_ratio = (self.max_height - self.min_height)/(self.max_decibel - self.min_decibel)

    def update(self, dt, decibel):

        desired_height = decibel * self.__decibel_height_ratio + self.max_height
        speed = (desired_height - self.height)/0.1

        self.height =decibel*7
        #self.height = clamp(self.min_height, self.max_height, self.height)

    def render(self, screen,offset):
        center_y=self.max_height+50
        center_x=600
        radius=self.height+50
        if (self.height < 10):
            return
        radius=clamp(50,400,radius)
        theta1=((self.ang_pos + offset)*math.pi/180)%360
        theta2=((self.ang_pos+ang_width + offset)*math.pi/180)%360
        start_x1=20 * math.cos(theta1) + center_x
        start_y1=20 * math.sin(theta1) + center_y
        end_x1=radius * math.cos(theta1) + center_x
        end_y1=radius * math.sin(theta1) + center_y
        start_x2=20 * math.cos(theta2) + center_x
        start_y2=20 * math.sin(theta2) + center_y
        end_x2=radius * math.cos(theta2) + center_x
        end_y2=radius * math.sin(theta2) + center_y
        color_idx=int((self.ang_pos/360)%len(self.color_list))
        curr_color = self.color_list[color_idx]
        pygame.draw.polygon(screen,curr_color,((start_x1,start_y1),(end_x1,end_y1),(end_x2,end_y2),(start_x2,start_y2)),0)
        


class SongProcessor:
    def __init__(self,filename):
        self.filename=filename
        #self.x=x
        time_series, sample_rate = librosa.load(self.filename)  # getting information from the file

        # getting a matrix which contains amplitude values according to frequency and time indexes
        stft = np.abs(librosa.stft(time_series, hop_length=128, n_fft=512*4))
   
        self.spectrogram = librosa.amplitude_to_db(stft, ref=np.max)  # converting the matrix to decibel matrix
        
        self.frequencies = librosa.core.fft_frequencies(n_fft=512*4)  # getting an array of frequencies


        # getting an array of time periodic
        self.times = librosa.core.frames_to_time(np.arange(self.spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4)

        self.time_index_ratio = len(self.times)/self.times[len(self.times) - 1]

        self.frequencies_index_ratio = len(self.frequencies)/self.frequencies[len(self.frequencies)-1]
        print("Finish Analyzing")
        t=eyed3.load(self.filename)

        if (t.tag == None or (t.tag.artist == None and t.tag.title == None)):
            self.caption=filename
        elif (t.tag.artist == None):
            self.caption = t.tag.title
        elif (t.tag.title == None):
            self.caption = t.tag.artist
        else:
            self.caption=t.tag.title + " by " + t.tag.artist

     

    def get_decibel(self,target_time, freq):
        freq_idx=min(int(freq * self.frequencies_index_ratio),self.spectrogram.shape[0]-1)
        #print(freq, self.spectrogram[freq_idx][int(target_time * self.time_index_ratio)])
        return self.spectrogram[freq_idx][int(target_time * self.time_index_ratio)]


    def play_song(self,width,x):
        
        x=0
        width=15#2880/len(self.frequencies)
        print("Play song", width,x,len(self.frequencies))
        for c in self.frequencies:
            bars.append(AudioBar(x, 300, c, background_color, max_height=400, ang_width=width))
            x += ang_width
        pygame.mixer.music.load(self.filename)
        pygame.mixer.music.play(0)
def reset():
    bars = []
    frequencies = np.arange(100, 7300, 100)
    r = len(frequencies)
    screen.fill(foreground_color)




t = pygame.time.get_ticks()
getTicksLastFrame = t

pygame.init()


infoObject = pygame.display.Info()

screen_w = 1200
screen_h = 900

# Set up the drawing window
screen = pygame.display.set_mode([screen_w, screen_h])


bars = []


frequencies = np.arange(100, 7300, 100)

r = len(frequencies)


font = pygame.font.Font('freesansbold.ttf', 32)




width = screen_w/r
ang_width = 360/len(frequencies)

sp=SongProcessor(musicfiles.pop())
x = (screen_w - width*r)/2
ang=width*r
sp.play_song(ang_width,ang)

text = font.render(sp.caption, True, background_color, foreground_color)
textRect = text.get_rect()
textRect.center = (screen_w // 2,screen_h -26)


# Run until the user asks to quit
running = True
offset=0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == MUSIC_END:
            print('music end event')
            reset()
            sp=SongProcessor(musicfiles.pop())
            sp.play_song(ang_width,x)
            text = font.render(sp.caption, True, background_color, foreground_color)


        #if event.type == pygame.MOUSEBUTTONDOWN:
            # play again

            #pygame.mixer.music.play()

    t = pygame.time.get_ticks()
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill(foreground_color)
    
    for b in bars:
        #print(sp.get_decibel(pygame.mixer.music.get_pos()/1000.0,b.freq))
        offset += 0.0001
        b.update(deltaTime, sp.get_decibel(pygame.mixer.music.get_pos()/1000.0, b.freq)+80)
        b.render(screen,offset)
    screen.blit(text, textRect)
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
