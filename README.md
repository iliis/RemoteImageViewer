Remote Image Viewer
===================

Shows images received from network in fullscreen.
Used in Houdinis Quest Adventure Game's


## Setup

Fedora:

    sudo dnf install python3-flask pyqt5\* xdotool

Raspbian:

    sudo apt install python3-flask pyqt5\* xdotool

Then run it with

    ./main.py

It should open a webserver on localhost:5000

Or instead install it as a systemd service:

    sudo cp imageviewer.service /etc/systemd/system


To rotate the screen on a Raspberry, add the following to /boot/config.txt

    display_rotate=3

(0: no rotation, 1: 90 deg, etc.)


## Test / Usage

Simply do a PUT request, for example:

    curl 192.168.0.42:5000/show --upload-file myimage.jpeg


Supported image types: BMP, JPEG, PNG, GIF (and some others)

See https://doc.qt.io/qt-5/qpixmap.html#reading-and-writing-image-files
