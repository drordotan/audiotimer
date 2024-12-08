

import threading


class OpenWorkController:

    def __init__(self,controller) -> None:
        self.controller = controller
        self.view = None
        self.model = None

        self.audioPath = None
        self.xlsxPath = None

    def set_vm(self,view, model):
        self.view = view
        self.model = model

    def reset_files(self):
        self.audioPath = None
        self.xlsxPath = None

    def on_open(self, widget):
        self.view.loading()
        self.filePath = self.view.menuBarView.on_open()
        self.start_processing_visualization_thread()

    def setAudioPath(self,path):
        self.audioPath = path

    def setXslxPath(self,path):
        self.xlsxPath = path
    
    def start(self):
        if self.audioPath:
            self.start_thread()
            #thread = threading.Thread(target=self.start_thread)
            #thread.daemon = True
            #thread.start()

    def start_thread(self):
        data = None

        # Remove all widgets in button_box
        while self.view.button_box.count():
            child = self.view.button_box.takeAt(0)
            if child.widget():
                child.widget().setParent(None)  # Detach the widget from its parent

        # Continue with the remaining logic
        self.controller.menuBarController.on_new()

        if self.xlsxPath:
            data = self.model.readModel.read(self.xlsxPath)

        self.model.soundModel.load_sound(self.audioPath)
        self.view.start_work(data)
        self.view.soundView.process_audio(self.model.soundModel.audio_data, self.model.soundModel.time_total_str)


