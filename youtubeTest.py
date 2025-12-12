from moviepy.editor import *
from pytubefix import YouTube # New library using fix for pytube
from pytubefix import Playlist
import requests

import re
import os
import shutil
import time

# # Temp fix for 400 error # 
# from pytubefix. innertube import _default_clients

# _default_clients[ "ANDROID"][ "context"]["client"]["clientVersion"] = "19.08.35"
# _default_clients["IOS"]["context"]["client"]["clientVersion"] = "19.08.35"
# _default_clients[ "ANDROID_EMBED"][ "context"][ "client"]["clientVersion"] = "19.08.35"
# _default_clients[ "IOS_EMBED"][ "context"]["client"]["clientVersion"] = "19.08.35"
# _default_clients["IOS_MUSIC"][ "context"]["client"]["clientVersion"] = "6.41"
# _default_clients[ "ANDROID_MUSIC"] = _default_clients[ "ANDROID_CREATOR" ]

# Sometime, the pypi release becomes slightly outdated. To install from the source with pip:

# $ python -m pip install git+https://github.com/pytube/pytube

class video_object():
    def __init__(self, url):
        self.url = url


fileToRead = open("songs.txt", "r")

thislist = []

for line in fileToRead:
    lineArgs = line.split()
    link = lineArgs[0]
    isMP3 = (lineArgs[1].upper() == "MP3")
    link = link.strip("/n")
    # If the string  "playlist" is in the link, will add each url in the playlist to thisList
    if "playlist" in link:
        pList = Playlist(link)
        for url in pList:
            thislist.append({
                "videoObject": video_object(url),
                "isMP3": isMP3
                })
    # Else, treats URL as normal video URL
    else:
        thislist.append({
            "videoObject": video_object(link),
            "isMP3": isMP3
            })

fileToRead.close()

fileOfError = open("errors.txt", "w")
errorCount = 0
listCounter = len(thislist)

for videoConfig in thislist:
    try:
        isMp3 = videoConfig["isMP3"]
        video = videoConfig["videoObject"]
        #This section gets the video from the link, and downloads a MP4 of it.
        print("\nLink processing: "+video.url)
        yVideo = YouTube(video.url)

        print("Title:\t", yVideo.title,
            "\nLength (Min):\t", "{:10.2f}".format(yVideo.length / 60) ,
            "\nViews:\t", yVideo.views)
        videoStream = yVideo.streams.get_highest_resolution()

        fileToBeRenamed = videoStream.download(filename='tempfile')

        #Reformats name and removes spacing from video title to use as file name
        newName = str(videoStream.title).replace('/',"")
        string_encode = newName.encode("ascii", "ignore")
        newName = string_encode.decode()

        nameComponents = newName.split()
        for i in nameComponents:
            i = i.capitalize()
        seperator = ''
        newName = seperator.join(nameComponents)           
        # illegal characters to avoid in finished filenames
        bad_chars = [';','|','.','\'', ':','?', '!', '*','\\','/','"','#','&','%','#','{','}','>','<',' ',';','@',')','(']
        
        # using filter() to remove bad_chars
        newName = ''.join((filter(lambda i: i not in bad_chars, newName)))
        
        mp4_file = fileToBeRenamed

        if isMp3: # If not MP3 there is no need to make MP3 version nor delete original MP4
           
            mp3_file = 'finishedSongs/'+newName+'.mp3'

            videoclip = VideoFileClip(mp4_file)
            audioclip = videoclip.audio
            audioclip.write_audiofile(mp3_file)
            audioclip.close()
            videoclip.close()
            os.remove(fileToBeRenamed)
        else:
            shutil.move(mp4_file, 'finishedSongs/'+newName+'.mp4')

    except Exception as e:
        print("\nException occured. Logging bad video.\n"+str(e))

        fileOfError.write(YouTube(video.url).title+" had an error\n"+
        str(e)+"\n----------\n")

    listCounter -= 1
    if listCounter == 0:
        print("List completed.")
    else:
        print("There is", listCounter, "video(s) left in the queue.")
        time.sleep(5)

fileOfError.close()
print("Process Completed.")