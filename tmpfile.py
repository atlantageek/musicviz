from PIL import Image,ImageDraw
import numpy as np
from moviepy.editor import *
from moviepy.video.io.bindings import mplfig_to_npimage

x = np.linspace(-2, 2, 200)

duration = 20


def make_frame(t):
    ax.clear()
    ax.plot(x, np.sinc(x**2) + np.sin(x + 2*np.pi/duration * t), lw=3)
    ax.set_ylim(-1.5, 2.5)
    return mplfig_to_npimage(fig)

def make_drawn_frame(t):
    im = Image.new("RGB", (600, 600), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    draw.line((t*600%600, 0) + im.size, fill=128)
    print(t)
    draw.polygon(((100, t), (300,t),(300,300+t),(100,300+t)), fill=128)
    return np.array(im)
    
audio=AudioFileClip("music/above-the-clouds.mp3").set_duration(duration)

#make_audio_frame = lambda t: 2*[ np.sin(440 * 2 * np.pi * t) ]
#audio = AudioClip(make_audio_frame, duration=12)
animation = VideoClip(make_drawn_frame, duration=duration).set_fps(20)
#animation.write_videofile('matplotlib.mp4', fps=20, codec='libx264',audio_codec='aac', temp_audiofile='music/above-the-clouds.mp3', remove_temp=True)
animation = animation.set_audio(audio)
animation.write_videofile('matplotlib4.mp4', fps=20)