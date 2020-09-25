Remote Image Viewer
===================

Shows images received from network in fullscreen.
Used in Houdinis Quest Adventure Game's


## Setup

Fedora:

    sudo dnf install python3-pyside2 python3-flask

Raspbian:

    sudo apt install python3-pyside2\* python3-flask


Then run it with

    ./main.py

It should open a webserver on localhost:5000

Or instead install it as a systemd service:

    sudo cp imageviewer.service /etc/systemd/system
