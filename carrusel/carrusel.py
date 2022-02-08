from tkinter import *
from os import walk
from PIL import ImageTk, Image

root = Tk()
root.title('Carrusel')

def getListOfImgFromDirectory(NameOfdirectory):
    listOfImg = []
    print(walk('carrusel'))
    for (dirpath, dirnames, filenames) in walk(NameOfdirectory):
        for names in filenames:
            image = Image.open(NameOfdirectory + '/' + names)
            image.thumbnail((800,600),Image.ANTIALIAS)
            listOfImg.append(ImageTk.PhotoImage(image))
    return listOfImg

imagesList = getListOfImgFromDirectory('carrusel')
imgIndex = 0

if len(imagesList) < 1:
    l = Label(root, text='No images found, To use this Image Carousel you must have images in a folder called carousel in the same directory that this is running from')
    l.grid(row=1,column=0,columnspan=3)

else:
    l = Label(root, image=imagesList[imgIndex])
    l.grid(row=1,column=0,columnspan=3)

    btnBack = Button(root, text='N/A', state=DISABLED)
    btnBack.grid(row=0,column=0)
    btn_foward = Button(root, text='->', command=lambda: foward())
    btn_foward.grid(row=0,column=2)

    def back():
        global imgIndex
        btn_foward.config(state=NORMAL,command=lambda: foward(),text='->')
        if imgIndex != 0:
            imgIndex -= 1
            l.config(image=imagesList[imgIndex])
            if imgIndex == 0:
                btnBack.config(text='N/A', state=DISABLED)

    def foward():
        global imgIndex
        btnBack.config(state=NORMAL,command=lambda: back(),text='<-')
        if imgIndex + 1 < len(imagesList):
            imgIndex += 1
            l.config(image=imagesList[imgIndex])
            if imgIndex == len(imagesList) - 1:
                btn_foward.config(text='N/A', state=DISABLED, command=None)

    root.bind('<Left>', lambda event=None: back())
    root.bind('<Right>', lambda event=None: foward())
    
root.mainloop()