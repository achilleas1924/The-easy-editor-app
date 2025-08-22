import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog,
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt # needs a Qt.KeepAspectRatio constant to resize while maintaining proportions
from PyQt5.QtGui import QPixmap # screen-optimised

from PIL import Image
#from PIL.ImageQt import ImageQt # to import the graphics from Pillow to Qt 
from PIL import ImageFilter
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)

app = QApplication([])

win = QWidget()
win.setWindowTitle("Easy Editor")
win.resize(700,500)

btn_dir = QPushButton("Folder")
btn_left = QPushButton("Left")
btn_right = QPushButton("Right")
btn_flip = QPushButton("Mirror")
btn_sharp = QPushButton("Sharpness")
btn_bw = QPushButton("B&W")

lw_files = QListWidget()
lb_image = QLabel("Image")


col1 = QVBoxLayout()
col2 = QVBoxLayout()
row = QHBoxLayout()
row_tools = QHBoxLayout()

col1.addWidget(btn_dir)
col1.addWidget(lw_files)
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addWidget(lb_image)
col2.addLayout(row_tools)
row.addLayout(col1,20)
row.addLayout(col2,80)

win.setLayout(row)


workdir=''

def filter(filenames, extensions):
    result = []
    for filename in filenames:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    
    return result

def showFilenamesList():
    global workdir
    ext = [".jpg",".jpeg",".png",".gif", ".bmp"]
    workdir = QFileDialog.getExistingDirectory() # c:\Users\ipanatsia\Desktop\algorithmics
    filenames = os.listdir(workdir) #["robotics_article.doc","turtles game.py","vacation2020.jpg","crazy_cat.gif"]
    filenames = filter(filenames,ext)
    lw_files.clear()
    for file in filenames:
        lw_files.addItem(file)

btn_dir.clicked.connect(showFilenamesList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None #'puppy.ng'
        self.save_dir = "Modified/"
        
    def loadImage(self, filename):
        self.filename = filename
        fullname = os.path.join(workdir, self.filename)
        self.image = Image.open(fullname)


    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()

    def saveImage(self):
        path = os.path.join(workdir,self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path,self.filename)
        self.image.save(fullname)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        path = os.path.join(workdir,self.save_dir,self.filename)
        self.showImage(path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        path = os.path.join(workdir,self.save_dir,self.filename)
        self.showImage(path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)




workimage = ImageProcessor()

def showChosenImage():
    if lw_files.currentRow()>=0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(filename)
        workimage.showImage(os.path.join(workdir, workimage.filename))

lw_files.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_flip.clicked.connect(workimage.do_flip)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)

win.show()
app.exec()