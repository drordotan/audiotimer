from controller.menuBarController import MenuBarController
from controller.openWorkController import OpenWorkController
from controller.soundController import SoundController
from controller.tableController import TableController


class Controller:

    def __init__(self) -> None:
        self.view = None 
        self.model = None

        self.menuBarController = MenuBarController(self)
        self.openWorkController = OpenWorkController(self)
        self.soundController = SoundController(self)
        self.tableController = TableController(self)
        

    def set_vm(self,view,model):
        self.view = view 
        self.model = model
        self.openWorkController.set_vm(view,model)
        self.soundController.set_vm(view,model)
        self.tableController.set_vm(view,model)
        self.menuBarController.set_vm(view,model)
