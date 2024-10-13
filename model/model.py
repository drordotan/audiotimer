from model.exportModel import ExportModel
from model.readModel import ReadModel
from model.soundModel import SoundModel


class Model:

    def __init__(self) -> None:

        self.red_line_positions = [] 

        self.soundModel = SoundModel(model=self)
        self.readModel = ReadModel()
        self.exportModel = ExportModel()
