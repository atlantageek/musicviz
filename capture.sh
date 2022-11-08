ffmpeg -f pulse -ac 2 -i default -f x11grab -r 30 -framerate 25 -s 820x920  -i :0.0+100,50 -c:v libx264 bob2.mp4
#ffmpeg -f pulse -ac 2 -i default -f x11grab -framerate 25 \
#    $(xwininfo | gawk 'match($0, /-geometry ([0-9]+x[0-9]+).([0-9]+).([0-9]+)/, a)\
#      { print "-video_size " a[1] " -i +" a[2] "," a[3] }') \
#    $(date +%Y-%m-%d_%H-%M_%S).mp4
