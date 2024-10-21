from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QFileDialog, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from view import workView
from view import tableView
from view.soundView import SoundView
from view.tableView import TableView
from view.workView import WorkView
from .menuBarView import MenuBarView
from view import menuBarView  # Import your MenuBarView

class View(QMainWindow):

    WIDTH = 1000
    HEIGHT = 600

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Time Tagging in Speech Recordings")
        self.setGeometry(100, 100, self.WIDTH, self.HEIGHT)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Initialize the menu bar
        self.menuBarView = MenuBarView(self)
        self.setMenuBar(self.menuBarView)

        # Ensure menu bar is shown explicitly (in case it is hidden)
        self.menuBarView.show()

        # For macOS: ensure the menu bar is shown within the window
        self.menuBarView.setNativeMenuBar(False)

        # Initialize UI elements
        self.init_ui()


    def init_ui(self):
        # Create a vertical spacer to push the button box to the bottom
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)

        # Create button box for file selection and start buttons
        self.button_box = QHBoxLayout()
        self.main_layout.addLayout(self.button_box)

        # Choose Audio File button
        self.audio_button = QPushButton("Select Audio", self)
        self.audio_button.clicked.connect(self.on_choose_audio_file)
        self.button_box.addWidget(self.audio_button)

        # Choose XLSX File button
        self.xlsx_button = QPushButton("Select XLSX", self)
        self.xlsx_button.clicked.connect(self.on_choose_xlsx_file)
        self.button_box.addWidget(self.xlsx_button)

        # Start button
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.controller.openWorkController.start)
        self.button_box.addWidget(self.start_button)

        # Apply stylesheet (optional)
        self.apply_css()


    def on_choose_audio_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.wav *.mp3)", options=options)
        if file_name:
            self.controller.openWorkController.audioPath = file_name
            self.audio_button.setText(file_name.split('/')[-1])

    def on_choose_xlsx_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select XLSX File", "", "XLSX Files (*.xlsx)", options=options)
        if file_name:
            self.controller.openWorkController.xlsxPath = file_name
            self.xlsx_button.setText(file_name.split('/')[-1])

    def start_work(self, data=None):
        self.workView = WorkView(view=self)
        self.soundView = SoundView(view=self)
        self.tableView = TableView(view=self, data=data)

        # Add the views to the main layout in the correct order
        self.main_layout.addWidget(self.workView)  # Add WorkView first
        self.main_layout.addWidget(self.soundView.scroll_area)  # Add the scroll area containing SoundView
        self.main_layout.addWidget(self.tableView)  # Add TableView last

    def keyPressEvent(self, event):

        if self.controller.model.soundModel.is_load:
            # Check if the space key was pressed

            if event.key() == Qt.Key_Space:
                self.controller.soundController.click_play_pause()
            elif event.key() == Qt.Key_Right:
                self.controller.soundController.move_to_next_red_line()
            elif event.key() == Qt.Key_Left:
                self.controller.soundController.move_to_previous_red_line()


    def apply_css(self):
        # Apply some basic styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #323232;
            }

            QPushButton {
                background-color: #3E4755;
                color: #FFFFFF;
                padding: 10px;
                border-radius: 5px;
                font-size: 15px;
            }

            QPushButton:hover {
                background-color: #586075;
            }
        """ + workView.css() + tableView.css() + menuBarView.css() )
