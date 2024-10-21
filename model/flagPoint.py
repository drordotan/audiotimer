

class FlagPoint:

    def __init__(self,position ,time,row_num=None, name = None) -> None:
        self.position = position
        self.time = time
        self.row_num = row_num
        self.name = name
        self.green_on_me = False

    def set_row_name(self,row_num,name):
        self.row_num = row_num
        self.name = name

    def __str__(self) -> str:
        return f"#{self.row_num} {self.name}"

