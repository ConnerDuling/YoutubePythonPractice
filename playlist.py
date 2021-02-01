from pytube import YouTube
from pytube import Playlist

p = Playlist('https://www.youtube.com/watch?v=SI76wS6tlKs&list=PLfR6C-Jk1bWtftxu684TTFha_CrH0XqDt&index=1&ab_channel=Grey')
counter = 0

for url in p.video_urls:
    counter = counter + 1
    vidyea = YouTube(url)
    print("URL "+str(counter)+" is: "+vidyea.title)