import tkinter as tk
from PIL import ImageTk, Image, ExifTags, ImageOps
import PIL

import os


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #self.path = '/Users/jennifedudley/Google Drive/Cub scouts/Pinewood Derby/Scouts' Choice (File responses)/Pictures (File responses)'
        self.path = '/Users/jennifedudley/Google Drive/Cub scouts/Pinewood Derby/Scouts\' Choice (File responses)/Pictures (File responses)/'
        self.destPath = '/Users/jennifedudley/Google Drive/Cub scouts/Pinewood Derby/Scouts\' Choice (File responses)/Pictures (File responses)/res/'
        self.aspectRatio = 4/3
        self.maxWidth = int(1080)
        self.maxHeight = int(self.maxWidth/self.aspectRatio)

        self.buttonframe = tk.Frame(self)
        self.buttonframe.grid(row=1,column=0)
        self.BNext = tk.Button(self.buttonframe, text ="next", command = self.nextCallback)
        self.BNext.pack(side='right')
        self.BPrev = tk.Button(self.buttonframe, text ="prev", command = self.prevCallback)
        self.BPrev.pack(side='right')
        self.BSave = tk.Button(self.buttonframe, text ="save", command = self.saveCallback)
        self.BSave.pack(side='right')
        self.BOrig = tk.Button(self.buttonframe, text ="orig", command = self.origCallback)
        self.BOrig.pack(side='right')

        self.textInfo = tk.Label(self, text="")
        self.textInfo.config(font=("Courier", 14))
        self.textInfo.bind_all('<Key>', self.keyCallback)
        self.textInfo.grid(row=0,column=0)

        self.outputName = tk.StringVar()
        self.EoutputName = tk.Entry(self.buttonframe, width = 15, textvariable = self.outputName)
        self.EoutputName.pack(side='left')

        ld = os.listdir(self.path)
        self.resizedImages = []
        self.resizedImageTitles = []

        for f in ld:
            if os.path.isfile(self.path + '/' + f)  and ('.jpeg' in f.lower() or '.jpg' in f.lower() or '.png' in f.lower()):
                img = Image.open(self.path+f)
                img = ImageOps.exif_transpose(img)
                (w, h) = img.size

                if w > self.maxWidth or h > self.maxHeight:
                    if w > self.maxWidth:
                        h = int(h * self.maxWidth/w)
                        w = self.maxWidth
                    if h > self.maxHeight:
                        w = int (w * self.maxHeight/h)
                        h = self.maxHeight

                    img = img.resize((w,h))
                    print('aspect ratio is ' + str(w/h))

                    if not w/h == self.aspectRatio:
                        pngImg = None
                        if w/h > self.aspectRatio:
                            pngImg = Image.new('RGBA', (w, int(w/self.aspectRatio)), (0, 0, 0, 0))
                            pngImg.paste(img, (0,int(((w/self.aspectRatio)-h)/2)))
                        if w/h < self.aspectRatio:
                            pngImg = Image.new('RGBA', (int(h*self.aspectRatio), h), (0, 0, 0, 0))
                            pngImg.paste(img, (int(((h*self.aspectRatio)-w)/2),0))
                        img = pngImg
                        

                self.resizedImages.append(img)
                self.resizedImageTitles.append(f)

        self.origCallback()
    
    def keyCallback(self, event):
        if event.keycode == 32: #spaace bar
            self.saveCallback()
        if event.keycode == 39: #right arrow
            self.nextCallback()
        if event.keycode == 37: #left arrow
            self.prevCallback()


    def origCallback(self):
        self.currentIndex = 0
        self.currentPhotoImage = ImageTk.PhotoImage(self.resizedImages[self.currentIndex])
        self.imageLabel = tk.Label(self, image= self.currentPhotoImage, height=self.maxHeight, width=self.maxWidth)
        self.imageLabel.grid(row=2,column=0)
        self.textInfo.configure(text=self.resizedImageTitles[self.currentIndex])
        return

    def nextCallback(self):
        self.currentIndex +=1
        if self.currentIndex >= len(self.resizedImages):
            self.currentIndex = len(self.resizedImages) - 1

        self.currentPhotoImage = ImageTk.PhotoImage(self.resizedImages[self.currentIndex])
        self.imageLabel = tk.Label(self, image= self.currentPhotoImage)
        self.imageLabel.grid(row=2,column=0)
        self.textInfo.configure(text=self.resizedImageTitles[self.currentIndex])
        return

    def prevCallback(self):
        self.currentIndex -=1
        if self.currentIndex < 0:
            self.currentIndex = 0

        self.currentPhotoImage = ImageTk.PhotoImage(self.resizedImages[self.currentIndex])
        self.imageLabel = tk.Label(self, image= self.currentPhotoImage)
        self.imageLabel.grid(row=2,column=0)
        self.textInfo.configure(text=self.resizedImageTitles[self.currentIndex])
        return

    def saveCallback(self):
        #self.detPath = 'C:/Users/B1050767/Pictures/res'
        outputName = self.outputName.get()
        if not os.path.isdir(self.destPath + '/' + outputName):
            os.makedirs(self.destPath + '/' + outputName)

        ld = os.listdir(self.destPath + '/' + outputName)
        count = 1
        for file in ld:
            if '.jpeg' in file.lower() or '.jpg' in file.lower() or 'png' in file.lower():
                count += 1

        self.resizedImages[self.currentIndex].save(self.destPath + '/' + outputName +'/image_' + outputName + '-' + str(count) + '.png')



        return

if __name__== "__main__":
    app = SampleApp()
    app.mainloop()
   