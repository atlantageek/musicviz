from PIL import Image,ImageDraw
import numpy as np
from moviepy.editor import *
from moviepy.video.io.bindings import mplfig_to_npimage
import librosa
import math

x = np.linspace(-2, 2, 200)
mp3="music/above-the-clouds.mp3"
math.radians(40)
#preprocess-mp3
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
BLACK = (0,0,0)
BACKGROUND=(255,200,50)
FOREGROUND=(0,0,0)
SCREEN_WIDTH=854
SCREEN_HEIGHT=580
CENTER_X=SCREEN_WIDTH/2
CENTER_Y=SCREEN_HEIGHT/2

ANG_STEP=2
COLOR_LIST=[ (32,32,192),(128,0,128),(128,128,0),(0,128,0),(0,64,0),(0,128,128),(0,64,64)]
#initialize mp4
#generate shapes at right intervals
#attach audio file
#done



class SongProcessor:
    def __init__(self,filename):
        self.filename=filename
        #self.x=x
        self.time_series, self.sample_rate = librosa.load(self.filename)  # getting information from the file

        # getting a matrix which contains amplitude values according to frequency and time indexes
        stft = librosa.stft(self.time_series, hop_length=128, n_fft=512*4)
        self.magnitude,phase=librosa.magphase(stft)
        
        self.duration=librosa.get_duration(y=self.time_series, sr=self.sample_rate)#y=self.time_series, sr=self.sample_rate)
   
        self.spectrogram = librosa.amplitude_to_db(stft, ref=np.max)  # converting the matrix to decibel matrix
        
        self.frequencies = librosa.core.fft_frequencies()  # getting an array of frequencies


        # getting an array of time periodic
        self.times = librosa.core.frames_to_time(np.arange(self.spectrogram.shape[1]), sr=self.sample_rate, hop_length=128, n_fft=512*4)

        self.time_index_ratio = len(self.times)/self.times[len(self.times) - 1]

        self.frequencies_index_ratio = len(self.frequencies)/self.frequencies[len(self.frequencies)-1]
        print(self.time_series.shape)
        print(stft.shape)
        print(self.times.shape)
        print(self.frequencies.shape)
        print(self.spectrogram.shape)
        # print(self.time_index_ratio)
        # print(self.frequencies_index_ratio)
        # print(self.stft[1024,0])
        max_val = np.amax(self.magnitude)
        self.multiplier=3#250.0/max_val
        print(self.duration)
        
        print(self.times)
        print(self.get_index_for_time(33))
     
        print("Finish Analyzing")

    
    def get_index_for_time(self,t):
        difference_array=np.absolute(self.times-t)
        index=difference_array.argmin()
        return index


    def get_levels(self,target_time):
        idx=self.get_index_for_time(target_time)
        return self.spectrogram[:,idx]+80


    def play_song(self,width,x):
        
        x=0
        width=15#2880/len(self.frequencies)
        #print("Play song", width,x,len(self.frequencies))
        # for c in self.frequencies:
        #     bars.append(AudioBar(x, 300, c, background_color, max_height=400, ang_width=width))
        #     x += ang_width

sp=SongProcessor(mp3)

def draw_level(ang,level,idx,draw):
    pt1=(CENTER_X,CENTER_Y)
    mod_ang= ang % 360

    theta1=math.radians(mod_ang)
    theta2=math.radians((ang + ANG_STEP)%360)
    bs=math.sin(theta1)
    pt2=(math.cos(theta1) *level * sp.multiplier + CENTER_X , math.sin(theta1) * level * sp.multiplier + CENTER_Y)
    pt3=(math.cos(theta2) *level * sp.multiplier + CENTER_X, math.sin(theta2) * level * sp.multiplier + CENTER_Y)
    #print(math.cos(math.radians(theta1)) *level)
    #if (idx % 100 == 34):
    #print(level,idx,theta1,mod_ang,bs)
    color_idx=int(ang/360)
    color=COLOR_LIST[color_idx]
    draw.polygon((pt1,pt2,pt3,pt1),fill=color)

def make_frame(t):
    im=Image.new("RGB",(854,580),BACKGROUND)
    draw=ImageDraw.Draw(im)
    levels=sp.get_levels(t)
    #print(np.amax(levels))

    ang=0
    for idx,level in enumerate(levels):
        draw_level(ang,level,idx,draw)
        ang=ang+ANG_STEP
    return np.array(im)




# def make_drawn_frame(t):
#     im = Image.new("RGB", (600, 600), (255, 255, 255))
#     draw = ImageDraw.Draw(im)
#     draw.line((t*600%600, 0) + im.size, fill=128)
#     print(t)
#     draw.polygon(((100, t), (300,t),(300,300+t),(100,300+t)), fill=128)
#     return np.array(im)
    
audio=AudioFileClip(mp3).set_duration(sp.duration)
print(sp.times)
# #make_audio_frame = lambda t: 2*[ np.sin(440 * 2 * np.pi * t) ]
# #audio = AudioClip(make_audio_frame, duration=12)
animation = VideoClip(make_frame, duration=sp.duration).set_fps(20)
# #animation.write_videofile('matplotlib.mp4', fps=20, codec='libx264',audio_codec='aac', temp_audiofile='music/above-the-clouds.mp3', remove_temp=True)
animation = animation.set_audio(audio)
animation.write_videofile('above-the-clouds.mp4', fps=20)