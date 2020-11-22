#pip install pafy
#pycharm does not handle installing youtube-dl well. Open Terminal, "View->Tool Window->Terminal. run pip install youtube-dl

import pafy
import os

base = '../../'
basePath = '../../static/gallery/'
dirs = os.listdir(basePath)
for d in dirs:
    if(os.path.isdir(basePath + d)):
        carNum = d
        carPath = 'gallery/' + carNum + '/'
        files = os.listdir(base + 'static/' + carPath)
        youTubeId = ''
        for file in files:
            if '.id' in file:
                f = open(base + "static/" +carPath+file, "r")
                youTubeId = f.readline()
                url = "https://www.youtube.com/watch?v=" + youTubeId
                video = pafy.new(url)
                best = video.getbest()
                mp4FileName = base + 'static/' + carPath + 'car' + str(carNum) + '.mp4'
                best.download(mp4FileName)


