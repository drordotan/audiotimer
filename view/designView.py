from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget

class DesignView:

    def __init__(self):
        pass

    def on_mouse_enter(self, widget, event):
        # Change the background color when mouse enters
        widget.setStyleSheet("background-color: rgba(52, 73, 94, 255);")  # Equivalent to (0.204, 0.286, 0.369) in RGBA

    def on_mouse_leave(self, widget, event):
        # Reset the background color when mouse leaves
        widget.setStyleSheet("background-color: rgba(62, 70, 85, 255);")  # Equivalent to (0.243, 0.278, 0.333) in RGBA
