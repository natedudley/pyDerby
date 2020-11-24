#requires pip install python-vlc
#does not work on mac
import tkinter as tk
import vlc
import time
import os
import datetime

class myframe(tk.Frame):
    def __init__(self, root, bd=5):
        super(myframe, self).__init__(root)
        self.grid()
        
        w = int(root.winfo_screenwidth() * .25)
        h = int(root.winfo_screenheight() * .25)
        self.frame = tk.Frame(self, width=w, height=h, bd=5)
        self.frame.configure(bg="black")
        self.frame.grid(row=0, column=0, columnspan=3, padx=8)
        self.play_button = tk.Button(self, text = 'Play', command = self.play)
        self.play_button.grid(row=1, column=0, padx=4)
        self.car_label = tk.Label(self, text='', font=("Helvetica", 16))
        self.car_label.grid(row=1, column=1, padx=4)
        self.next_button = tk.Button(self, text = 'Next', command = self.next)
        self.next_button.grid(row=1, column=2, padx=4)
        self.isPlaying = False
        self.gallery = []
        self.galleryIndex = 0
        self.countDownTime = datetime.datetime.now()
        self.curfileName= ''

    def update(self):
        if self.galleryIndex >= len(self.gallery):
            self.galleryIndex = 0

        totalSeconds = (datetime.datetime.now()- self.countDownTime ).total_seconds()
        print(str(totalSeconds)) 
            
        if self.isPlaying and (not self.player.is_playing() or (not '.mp4' in self.curfileName and totalSeconds > 5)):
            
            self.curfileName = self.gallery[self.galleryIndex]['file']
            self.curCarNum = self.gallery[self.galleryIndex]['carNum']
            self.galleryIndex += 1
            if len(self.curfileName) > 1:
                print('playing: ' + self.curfileName)
                self.player.set_mrl(self.curfileName)
                self.car_label['text'] = 'Car: ' + str(self.curCarNum)
                self.player.play()

                time.sleep(1)
                self.countDownTime = datetime.datetime.now()


        
        root.after(1000, self.update)

    def play(self):
        print('play')
        base = '../../static/'
        basePath = base + '/gallery/'
        dirs = os.listdir(basePath)
        for d in dirs:
            if os.path.isdir(basePath + d):
                carNum = d
                carPath = 'gallery/' + carNum + '/'
                files = os.listdir(base + carPath)
                images = []
                youtubeFile = ''
                for file in files:
                    if '.mp4' in file:
                        youtubeFile = base + carPath + file
                    elif ('.jpg' in file or '.png' in file):
                        images.append(base + carPath + file)
                if len(youtubeFile) > 0:
                    self.gallery.append({'carNum': carNum, 'file': youtubeFile})
                for f in images:
                    self.gallery.append({'carNum': carNum, 'file': f})

        
        i = vlc.Instance('--no-xlib --quiet')
        self.player = i.media_player_new()
        
        xid = self.frame.winfo_id()
        self.player.set_xwindow(xid)
        self.isPlaying = True

        
            


        
    def next(self):
        print('next')
        try:
            self.player.pause()
        except:
            pass

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Pinewood Derby")
    #root.attributes('-fullscreen', True)
    app = myframe(root)
    app.update()
    root.mainloop()
