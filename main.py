#!/usr/bin/env python3

import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import Slot, Qt, QSize

# based on https://stackoverflow.com/a/22618496
class ImageWidget(QLabel):
    def __init__(self):
        QLabel.__init__(self)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setMinimumSize(320, 240)
        self.img = None

        self.setAlignment(Qt.AlignCenter) # THIS IS KEY!

        self.setScaledContents(False)

    def setPixmap(self, pixmap):
        self.img = pixmap
        QLabel.setPixmap(self, self.scaledPixmap())

    def scaledPixmap(self):
        return self.img.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def resizeEvent(self, event):
        if self.img:
            QLabel.setPixmap(self, self.scaledPixmap())


class ImageViewer(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.image = ImageWidget()
        self.loadImage("testimg.jpg")

        self.setCentralWidget(self.image)

        self.setStyleSheet("background: black")

        # Connecting the signal
        #self.button.clicked.connect(self.magic)

    def loadImage(self, filename):
        reader = QImageReader(filename)
        reader.setAutoTransform(True)
        new_img = reader.read()
        if new_img:
            self.image.setPixmap(QPixmap.fromImage(new_img))

    @Slot()
    def magic(self):
        self.image.setText("foo bar")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = ImageViewer()
    widget.showFullScreen()
    #widget.show()

    sys.exit(app.exec_())
