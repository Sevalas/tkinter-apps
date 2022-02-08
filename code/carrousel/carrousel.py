from tkinter import *
from os import walk
from PIL import ImageTk, Image

root = Tk()
root.title('Carrousel')

imagesFileFormats = ['.tif', '.tiff', '.bmp', '.jpg', '.jpeg', '.gif', '.png', '.eps', '.raw', '.cr2', '.nef', '.orf', '.sr2']

def getListOfImgFromDirectory(NameOfdirectory):
    listOfImg = []
    for (dirpath, dirnames, filenames) in walk(NameOfdirectory):
        for name in filenames:
            if any(fileFormat in name for fileFormat in imagesFileFormats):
                image = Image.open(NameOfdirectory + '/' + name)
                image.thumbnail((800,600),Image.ANTIALIAS)
                listOfImg.append(ImageTk.PhotoImage(image))
    return listOfImg

imagesList = getListOfImgFromDirectory('carrousel')
imgIndex = 0

if len(imagesList) < 1:
    l = Label(root, text='Images not found, to use this image carrousel you must have images in a folder called "carrousel" in the same directory that this is running from.')
    l.grid(row=1,column=0,columnspan=3)

else:
    l = Label(root, image=imagesList[imgIndex])
    l.grid(row=1,column=0,columnspan=3)

    btnBack = Button(root, text='N/A', state=DISABLED)
    btnBack.grid(row=0,column=0)

    if(len(imagesList) > 1):
        btn_foward = Button(root, text='->', command=lambda: foward())
    else:
        btn_foward = Button(root, text='N/A', state=DISABLED)

    btn_foward.grid(row=0,column=2)

    def back():
        global imgIndex
        if imgIndex != 0:
            btn_foward.config(state=NORMAL,command=lambda: foward(),text='->')
            imgIndex -= 1
            l.config(image=imagesList[imgIndex])
            if imgIndex == 0:
                btnBack.config(text='N/A', state=DISABLED)

    def foward():
        global imgIndex
        if imgIndex + 1 < len(imagesList):
            btnBack.config(state=NORMAL,command=lambda: back(),text='<-')
            imgIndex += 1
            l.config(image=imagesList[imgIndex])
            if imgIndex == len(imagesList) - 1:
                btn_foward.config(text='N/A', state=DISABLED, command=None)

    root.bind('<Left>', lambda event=None: back())
    root.bind('<Right>', lambda event=None: foward())
    
root.mainloop()