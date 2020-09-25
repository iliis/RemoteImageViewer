#!/usr/bin/env python3

import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from flask import Flask, json, request
from base64 import b64decode

class RemoteInterface(QThread):

    show_img = Signal(bytes)

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        app = Flask("ImageDisplay")
        app.use_reloader = False
        app.debug = False

        @app.route('/status')
        def status():
            return "OK"

        @app.route('/show', methods=['PUT', 'POST'])
        def show():
            if request.method == 'PUT':
                print("request (PUT):", len(request.data), "bytes")
                self.show_img.emit(request.data)
                #print("data:", request.data)
                #with open('tmp.jpg', 'wb') as f:
                    #f.write(request.stream.read())
            else:
                if 'image' in request.form:
                    print("request (POST):", len(request.form['image']), "bytes")
                    print("type:", type(request.form['image']))
                    self.show_img.emit(b64decode(request.form['image']))
            return "OK"

        app.run(host = '0.0.0.0')

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

    @Slot(bytes)
    def showRawData(self, data):
        if not data:
            print("no data received :(")
            return
        else:
            print("got", len(data), "bytes")

        img = QPixmap()
        if img.loadFromData(data):
            self.image.setPixmap(img)
        else:
            print("failed to parse image data")

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

    viewer = ImageViewer()
    viewer.showFullScreen()
    #viewer.show()

    api = RemoteInterface()

    api.show_img.connect(viewer.showRawData)

    api.start()
    sys.exit(app.exec_())
