from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
    QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QHeaderView
)
from PyQt5.QtCore import Qt


class TableView(QWidget):
    headers = [
        "#", "subject", "trail_num", "n1", "n2", "result",
        "start", "end", "1 start", "1 end", "2 start", "2 end",
        "final start", "final end"
    ]

    def __init__(self, view, data=None):
        super().__init__()

        self.view = view
        self.data = data

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Table for holding rows of data
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Add rows to the table (initialize with data or default)
        if self.data:
            for i, row_data in enumerate(self.data):
                self.add_row(i + 1, data=row_data)
        else:
            for i in range(10):  # Example with 5 empty rows
                self.add_row(i + 1, *["" for _ in range(len(self.headers) - 1)])

        # Scroll area for the table
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.table)
        self.layout.addWidget(self.scroll_area)

        # Button to add a new row
        add_row_button = QPushButton("Add Row")
        add_row_button.clicked.connect(self.on_add_row_clicked)
        self.layout.addWidget(add_row_button)

        # Connect cell click signal to slot
        self.table.cellClicked.connect(self.on_cell_clicked)

    def add_row(self, counter, *texts, data=None):
        # Determine the new row index
        row_index = self.table.rowCount()
        self.table.insertRow(row_index)

        # Set the counter in the first column
        counter_item = QTableWidgetItem(str(counter))
        counter_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)  # Make counter non-editable
        self.table.setItem(row_index, 0, counter_item)

        # Populate the row with either data or texts
        to_row = [data.get(header, "") for header in self.headers[1:]] if data else texts

        for col_index, text in enumerate(to_row, start=1):
            item = QTableWidgetItem(str(text))
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
            self.table.setItem(row_index, col_index, item)

    def on_add_row_clicked(self):
        # Add a new row with default empty text fields
        new_counter = self.table.rowCount() + 1
        self.add_row(new_counter, *["" for _ in range(len(self.headers) - 1)])

    def on_cell_clicked(self, row, column):
        self.view.controller.tableController.edit_flag(row, self.headers[column])
        text = self.view.controller.tableController.get_flag()
        if text:
            entry = self.table.item(row, column)

            if entry.text().replace(" ","") == '':
                entry.setText(text)

def css():
    return """
        QTableWidget {
            background-color: #323232;  /* Set table background color to white */
        }
        QTableWidget::item {
            color: white;
            background-color: black;  /* Ensure individual items are also white */
        }
        """
