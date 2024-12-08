import pyperclip
from PyQt5.QtWidgets import QTableWidgetItem

class TableController:

    def __init__(self, controller):
        self.controller = controller
        self.view = None
        self.model = None

        self.point = None

    def set_vm(self, view, model):
        self.view = view
        self.model = model

    def edit_flag(self, row, name_col):
        if self.point:
            self.point.set_row_name(row, name_col)

    def set_flag(self, point):
        self.point = point
        str_time = self.get_flag(clear=False)
        if str_time:
            pyperclip.copy(str_time)

    def get_flag(self,clear=True):
        if self.point:
            minutes, seconds = divmod(self.point.time, 60)
            hours, minutes = divmod(minutes, 60)
            milliseconds = int((self.point.time % 1) * 1000)
            if clear:
                self.point = None
            return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{milliseconds:03}"

    def get_entries(self):
        rows_data = []

        # Iterate over all rows in the QTableWidget, starting from 0 (row index)
        for row in range(self.view.tableView.table.rowCount()):
            row_data = {}
            # Iterate over each column in the row
            for col in range(self.view.tableView.table.columnCount()):
                item = self.view.tableView.table.item(row, col)
                if item is not None:
                    header = self.view.tableView.headers[col]  # Match the header with the column index
                    row_data[header] = item.text()

            rows_data.append(row_data)

        return rows_data
