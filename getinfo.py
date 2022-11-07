import eyed3
import os




t=eyed3.load("./music/purrple-cat-bird-bath.mp3")
print(t.tag)
print(t.tag.artist)
print(t.tag.album)
print(t.tag.title)
