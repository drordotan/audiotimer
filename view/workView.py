from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel,
    QLineEdit, QSlider, QSizePolicy
)
from PyQt5.QtCore import Qt

class WorkView(QWidget):
    def __init__(self, view):
        super().__init__()

        self.view = view

        self.setFocusPolicy(Qt.StrongFocus)

        # Main layout for the entire row
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        # Play and Stop button layout
        self.play_stop_layout = QHBoxLayout()
        self.main_layout.addLayout(self.play_stop_layout)

        # Play/Pause Button
        self.play_pause_button = QPushButton("Play")
        # Remove fixed size or increase it
        self.play_pause_button.setFixedSize(120, 40)  # Or simply remove this line
        self.play_pause_button.clicked.connect(self.view.controller.soundController.click_play_pause)
        self.play_stop_layout.addWidget(self.play_pause_button)

        # Stop Button
        self.stop_button = QPushButton("Stop")
        # Remove fixed size or increase it
        self.stop_button.setFixedSize(120, 40)  # Or simply remove this line
        self.stop_button.clicked.connect(self.view.controller.soundController.stop_audio)
        self.play_stop_layout.addWidget(self.stop_button)


        # Time control container layout
        self.time_control_layout = QVBoxLayout()
        self.main_layout.addLayout(self.time_control_layout)

        # Time entry layout
        self.time_entries_layout = QHBoxLayout()
        self.time_control_layout.addLayout(self.time_entries_layout)

        # Current time and total time text fields
        self.current_time_entry = QLineEdit("00:00:00.000")
        self.current_time_entry.setAlignment(Qt.AlignCenter)
        self.current_time_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.total_time_entry = QLineEdit("00:00:00.000")
        self.total_time_entry.setAlignment(Qt.AlignCenter)
        self.total_time_entry.setReadOnly(True)
        self.total_time_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Add entries to time entries layout
        self.time_entries_layout.addWidget(self.current_time_entry)
        self.time_entries_layout.addWidget(QLabel("-"))
        self.time_entries_layout.addWidget(self.total_time_entry)

        # Time control button layout
        self.time_buttons_layout = QHBoxLayout()
        self.time_control_layout.addLayout(self.time_buttons_layout)

        # Add time control buttons
        self.add_time_button("-10M", self.view.controller.soundController.on_jump_forward_clicked, -600)
        self.add_time_button("-5M", self.view.controller.soundController.on_jump_forward_clicked, -300)
        self.add_time_button("-1M", self.view.controller.soundController.on_jump_forward_clicked, -60)
        self.add_time_button("-10S", self.view.controller.soundController.on_jump_forward_clicked, -10)
        self.add_time_button("-5S", self.view.controller.soundController.on_jump_forward_clicked, -5)
        self.add_time_button("-1S", self.view.controller.soundController.on_jump_forward_clicked, -1)
        self.add_time_button("+1S", self.view.controller.soundController.on_jump_forward_clicked, 1)
        self.add_time_button("+5S", self.view.controller.soundController.on_jump_forward_clicked, 5)
        self.add_time_button("+10S", self.view.controller.soundController.on_jump_forward_clicked, 10)
        self.add_time_button("+1M", self.view.controller.soundController.on_jump_forward_clicked, 60)
        self.add_time_button("+5M", self.view.controller.soundController.on_jump_forward_clicked, 300)
        self.add_time_button("+10M", self.view.controller.soundController.on_jump_forward_clicked, 600)

        # Zoom slider
        self.zoom_slider = QSlider(Qt.Vertical)
        self.zoom_slider.setRange(10, 20)  # Equivalent to zoom levels 1.0 to 2.0
        self.zoom_slider.setValue(10)  # Default value (1x)
        self.zoom_slider.valueChanged.connect(self.on_zoom_slider_changed)
        self.main_layout.addWidget(self.zoom_slider)

    def add_time_button(self, label, callback, time_offset):
        button = QPushButton(label)
        # Increase the size to make sure text fits well
        button.setFixedSize(80, 30)  # Try a larger size
        button.clicked.connect(lambda: callback(time_offset))
        self.time_buttons_layout.addWidget(button)


    def on_zoom_slider_changed(self):
        zoom_level = self.zoom_slider.value() / 10.0  # Convert to a float between 1.0 and 2.0
        self.view.soundView.zoom_level = zoom_level
        self.view.soundView.update_drawing_size()
        self.view.soundView.center_on_playback_position()
        self.view.soundView.update()



def css():
        return """
            /* QPushButton {
                background-color: #3E4755;
                color: #FFFFFF;
                padding: 10px;
                border-radius: 5px;
                font-size: 15px;
            }

            QPushButton:hover {
                background-color: #586075;
            } */
        """

