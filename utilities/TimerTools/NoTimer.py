from tkinter import *
from tkinter.ttk import *
from classes import logger
import os

window = Tk()
window.title("No Timer")
window.geometry('350x200')

os.chdir('../../')

def submitCallBack():
   log = logger.logger()
   times = []
   for rb in radioButtonVaribales:
       times.append(float(rb.get()))

   log.logRace(times)



B = Button(window, text ="Submit", command = submitCallBack)
B.grid(column=0, row=5)


radioButtonVaribales = []
for i in range (0, 4):
    radioButtonVaribales.append(StringVar())
    w = Label(window, text='lane ' + str(i+1) + ':')
    rad1 = Radiobutton(window,text='First', variable = radioButtonVaribales[i], value=1)
    rad2 = Radiobutton(window,text='Second', variable = radioButtonVaribales[i], value=2)
    rad3 = Radiobutton(window,text='Third', variable = radioButtonVaribales[i], value=3)
    rad4 = Radiobutton(window,text='Fourth', variable = radioButtonVaribales[i], value=4)

    w.grid(column=0, row=i)
    rad1.grid(column=1, row=i)
    rad2.grid(column=2, row=i)
    rad3.grid(column=3, row=i)
    rad4.grid(column=4, row=i)

window.mainloop()