from moviepy.editor import *
from pytube import YouTube

import re
import os
import time

class video_object():
    def __init__(self, url):
        self.url = url


fileToRead = open("songs.txt", "r")

thislist = []

for link in fileToRead:
    thislist.append(video_object(link.strip("/n")))


while(len(thislist) > 0):

    for video in thislist:
        #This section gets the video from the link, and downloads a MP4 of it.
        try:
            print("\nLink processing: "+video.url)
            yVideo = YouTube(video.url)

            print("Title is: ", yVideo.title, "\nLength (Min):", "{:10.2f}".format(yVideo.length / 60) ,"\nViews: ", yVideo.views, "\nRatings: ", yVideo.rating)
            videoStream = yVideo.streams.get_highest_resolution()

            fileToBeRenamed = videoStream.download()


            #Reformats name and removes spacing from video title to use as file name
            newName = str(videoStream.title).replace('/',"")
            nameComponents = newName.split()
            for i in nameComponents:
                i = i.capitalize()
            seperator = ''
            newName = seperator.join(nameComponents)

           

            newName.replace(':',"-")

            print(newName)

            
            mp4_file = fileToBeRenamed
            mp3_file = 'finishedSongs/'+newName+'.mp3'

            videoclip = VideoFileClip(mp4_file)
            audioclip = videoclip.audio
            audioclip.write_audiofile(mp3_file)
            audioclip.close()
            videoclip.close()

            os.remove(fileToBeRenamed)


            thislist.remove(video)
            print("There is",len(thislist),"video(s) left in the que.")

        except Exception:
            print("\nException. Waiting ")
            time.sleep(5)

print("All done!")