from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QHBoxLayout, QLabel, QDialog
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QPen, QMouseEvent

class SoundView(QWidget):
    def __init__(self, view):
        super().__init__()
        self.view = view

        # Initialize attributes
        self.samples = None
        self.current_position = 0
        self.max_position = 0
        self.zoom_level = 1

        self.playback_position = 0
        self.samples_per_60_seconds = 44100 * 30  # Assuming a 44,100 Hz sample rate
        self.draw_is_word = False

        # Create the scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setWidget(self)

        # Set mouse tracking for tooltips
        self.setMouseTracking(True)

    def mousePressEvent(self, event: QMouseEvent):
        """Handle button-press event (equivalent to `button-press-event` in GTK)."""
        self.view.controller.soundController.on_click(event)

    def on_mouse_move(self, event):
        # Check if the mouse is near any red line
        for point in self.view.controller.model.soundModel.red_line_positions:
            if abs(event.x() - point.position * self.zoom_level) < 5:  # Adjust sensitivity as needed
                if point.name:
                    # Show the tooltip
                    self.setToolTip(f"{point}")
                else:
                    minutes, seconds = divmod(point.time, 60)
                    hours, minutes = divmod(minutes, 60)
                    milliseconds = int((point.time % 1) * 1000)
                    time_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{milliseconds:03}"
                    # Show the tooltip
                    self.setToolTip(f"Time: {time_str}")
                return

        # If not near any red line, clear the tooltip
        self.setToolTip(None)

    def paintEvent(self, event):
        painter = QPainter(self)

        if self.samples is None or len(self.samples) == 0:
            return

        width = self.width()
        height = self.height()

        # Draw waveform
        painter.setPen(QPen(QColor(0, 128, 255), 2))  # Blue color for waveform

        for x in range(0, self.current_position, 2048):
            if x >= len(self.samples):
                break

            y = self.samples[x]
            calc_x = (x / self.samples_per_60_seconds * 1000) * self.zoom_level

            # Ensure calc_x and y are integers
            painter.drawLine(int(calc_x), height // 2, int(calc_x), height // 2 - int(y * 0.005))
            painter.drawLine(int(calc_x), height // 2, int(calc_x), height // 2 + int(y * 0.005))

        # Draw red lines for markers
        painter.setPen(QPen(QColor(255, 0, 0), 1))  # Red color for markers
        for point in self.view.controller.model.soundModel.red_line_positions:
            painter.drawLine(int(point.position * self.zoom_level), 0, int(point.position * self.zoom_level), height)

        # Draw the playback position line
        painter.setPen(QPen(QColor(0, 255, 0), 2))  # Green color for playback position
        playback_x = (self.playback_position / self.samples_per_60_seconds * 1000) * self.zoom_level
        painter.drawLine(int(playback_x), 0, int(playback_x), height)

        # Auto-scroll to center the green line in the visible area
        self.auto_scroll_to_playback(playback_x)


    def auto_scroll_to_playback(self, playback_x):
        visible_area_start = self.scroll_area.horizontalScrollBar().value()
        visible_area_end = visible_area_start + self.scroll_area.viewport().width()

        # Scroll to keep playback line centered if near the edge
        if playback_x > visible_area_end - 20:
            new_scroll_value = playback_x - self.scroll_area.viewport().width() + 900
            self.scroll_area.horizontalScrollBar().setValue(new_scroll_value)

    def update_time_display(self, current_chunk_index):
        current_time_sec = current_chunk_index / 44100
        minutes, seconds = divmod(current_time_sec, 60)
        hours, minutes = divmod(minutes, 60)
        milliseconds = int((current_time_sec % 1) * 1000)
        time_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{milliseconds:03}"
        # Update the time display in a thread-safe way
        self.view.workView.current_time_entry.setText(time_str)

    def set_samples(self, samples):
        self.samples = samples
        self.max_position = len(samples)
        self.current_position = 0
        self.view.controller.model.soundModel.red_line_positions = []
        self.update_drawing_size()
        self.update()

        # Set up a timer to update the drawing incrementally
        QTimer.singleShot(0, self.update_drawing)

    def update_drawing_size(self):
        # Set the width to be slightly larger than the viewport, and let scrolling handle the rest
        viewport_width = self.scroll_area.viewport().width()
        calculated_width = max(1000, (len(self.samples) // self.samples_per_60_seconds + 1) * 100 * self.zoom_level)
        self.setFixedWidth(min(viewport_width * 3, calculated_width))  # Set a limit relative to viewport size


    def update_drawing(self):
        step = 600
        if self.current_position < self.max_position:
            self.current_position += step
            self.update()
            QTimer.singleShot(0, self.update_drawing)

    def set_playback_position(self, position):
        self.playback_position = position
        self.update()

    def process_audio(self, audio_data, time_total_str):
        QTimer.singleShot(0, lambda: self.set_samples(audio_data))
        QTimer.singleShot(0, lambda: self.view.workView.total_time_entry.setText(time_total_str))
        self.view.show()

    def seek_to_time(self, time_in_seconds):
        if self.samples is not None:
            new_chunk_index = int(time_in_seconds * 44100)  # Assuming a 44.1 kHz sample rate
            if 0 <= new_chunk_index < len(self.samples):
                self.playback_position = new_chunk_index
                self.update_time_display(new_chunk_index)
                self.update()

                # If audio playback is active, adjust the playback position
                if self.view.controller.soundController.stream and self.view.controller.soundController.stream.isActive():
                    self.view.controller.soundController.stream.stop()
                    self.view.controller.soundController.model.soundModel.current_chunk_index = new_chunk_index
                    self.view.controller.soundController.stream.start()
                else:
                    self.view.controller.soundController.model.soundModel.current_chunk_index = new_chunk_index

    def center_on_playback_position(self):
        playback_x = (self.playback_position / self.samples_per_60_seconds * 1000) * self.zoom_level

        # Access the horizontal scrollbar
        scroll_bar = self.scroll_area.horizontalScrollBar()
        visible_area = self.scroll_area.viewport().width()

        # Center the playback position in the visible area
        new_scroll_value = playback_x - (visible_area / 2)
        scroll_bar.setValue(max(0, new_scroll_value))

    def get_popup_geometry(self):
        """Calculate the popup geometry based on the main window's size."""
        popup_width = int(self.view.width() * 0.6)  # 60% of the main window's width
        popup_height = 100  # Fixed height for the popup
        popup_x = self.view.x() + (self.view.width() - popup_width) // 2  # Center the popup horizontally
        popup_y = self.view.y() + self.view.height() - popup_height - 20  # Position near the bottom
        return popup_x, popup_y, popup_width, popup_height

    def show_popup(self):
        # Create the popup window
        self.popup = QDialog(self.view)
        self.popup.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)

        # Get dynamic popup size and position
        popup_x, popup_y, popup_width, popup_height = self.get_popup_geometry()
        self.popup.setGeometry(popup_x, popup_y, popup_width, popup_height)

        # Add a label to the popup
        label = QLabel("Time copy!", self.popup)
        label.setAlignment(Qt.AlignCenter)  # Center the text

        # Style the popup with a transparent background and clearly visible text
        label.setStyleSheet("font-size: 16px; color: black; background-color: transparent; padding: 10px;")
        self.popup.setStyleSheet("background-color: rgba(255, 255, 255, 0.4); border-radius: 10px;")

        popup_layout = QVBoxLayout()
        popup_layout.addWidget(label)
        self.popup.setLayout(popup_layout)

        # Show the popup at the bottom of the main window
        self.popup.show()

        # Set a timer to close the popup after 2 seconds
        QTimer.singleShot(2000, self.popup.close)


def css():
        return """
        """