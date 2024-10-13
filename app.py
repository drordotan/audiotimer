import sys
from PyQt5.QtWidgets import QApplication
from controller.controller import Controller
from model.model import Model
from view.view import View
from pydub import AudioSegment

import platform

if platform.system() == "Windows":
    AudioSegment.converter = "ffmpeg.exe"
    AudioSegment.ffprobe = "ffprobe.exe"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    view = View(controller=controller)
    model = Model()
    controller.set_vm(view=view, model=model)
    view.show()
    sys.exit(app.exec_())
