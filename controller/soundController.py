import pyaudio
import pyperclip
from PyQt5.QtCore import Qt, QTimer, QEvent
from PyQt5.QtWidgets import QFileDialog
import threading
from model.flagPoint import FlagPoint

class SoundController:

    def __init__(self, controller):
        self.controller = controller
        self.stream = None
        self.pyaudio_instance = None
        self.stop_flag = False
        
    
    def set_vm(self, view, model):
        self.model = model
        self.view = view
        self.soundModel = model.soundModel

    def stop_flag_func(self):
        while True:
            if self.stop_flag:
                self.stream.stop_stream()
                return

    def click_play_pause(self):
        if self.soundModel.is_playing:
            if self.soundModel.is_paused:
                if self.stream.is_stopped():
                    self.stream.start_stream()
                self.soundModel.is_paused = False
                self.stop_flag = False
                threading.Thread(target=self.stop_flag_func).start()
                self.view.workView.play_pause_button.setText("Pause")
            else:
                if self.stream.is_active():
                    self.stream.stop_stream()
                self.soundModel.is_paused = True
                self.stop_flag = True
                self.view.workView.play_pause_button.setText("Play")
        else:
            threading.Thread(target=self.stop_flag_func).start()
            self.play_audio()
            self.soundModel.is_playing = True
            self.view.workView.play_pause_button.setText("Pause")

    def play_audio(self):
        self.pyaudio_instance = pyaudio.PyAudio()

        self.stream = self.pyaudio_instance.open(format=pyaudio.paInt16,
                                                 channels=1,
                                                 rate=44100,
                                                 output=True,
                                                 frames_per_buffer=1024,
                                                 stream_callback=self.callback)

        self.stream.start_stream()
    
    def stop_audio(self):
        if self.stream is not None:
            if self.stream.is_active():
                self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        if self.pyaudio_instance is not None:
            self.pyaudio_instance.terminate()

        self.soundModel.current_chunk_index = 0
        self.soundModel.is_playing = False
        self.soundModel.is_paused = False
        self.view.workView.play_pause_button.setText("Play")

        # Update the playback position in the drawing area
        self.view.soundView.set_playback_position(self.soundModel.current_chunk_index)

        # Update the time display
        self.view.soundView.update_time_display(self.soundModel.current_chunk_index)

    def callback(self, in_data, frame_count, time_info, status):
        if self.soundModel.current_chunk_index < len(self.soundModel.audio_data):
            chunk_data = self.soundModel.audio_data[self.soundModel.current_chunk_index:self.soundModel.current_chunk_index + frame_count]

            # Check if the playback position intersects a red line
            for point in self.model.soundModel.red_line_positions:
  
                if point.green_on_me:
                    point.green_on_me = False
                    break

                position_in_samples = int(point.time * 44100)
                if self.soundModel.current_chunk_index <= position_in_samples < self.soundModel.current_chunk_index + frame_count:
                    self.soundModel.is_paused = True
                    point.green_on_me = True
                    self.view.workView.play_pause_button.setText("Play")
                    self.stop_flag = True
                    return (chunk_data.tobytes(), pyaudio.paContinue)
            
            self.soundModel.current_chunk_index += frame_count

            self.view.soundView.set_playback_position(self.soundModel.current_chunk_index)

            self.view.soundView.update_time_display(self.soundModel.current_chunk_index)

            return (chunk_data.tobytes(), pyaudio.paContinue)
        else:
            return (None, pyaudio.paComplete)

    def on_jump_forward_clicked(self, time_offset):
        new_position = self.soundModel.current_chunk_index + time_offset * 44100  # time seconds * 44100 samples per second

        # Ensure the new position does not exceed the length of the audio
        if new_position < len(self.soundModel.audio_data):
            self.soundModel.current_chunk_index = new_position
            self.view.soundView.set_playback_position(self.soundModel.current_chunk_index)
            if self.stream and self.stream.is_active():
                self.stream.stop_stream()
                self.stream.start_stream()
            self.view.soundView.update_time_display(self.soundModel.current_chunk_index)
        else:
            print("Cannot jump forward, end of the audio reached.")

    def create_str_time(self,point_time):
        minutes, seconds = divmod(point_time, 60)
        hours, minutes = divmod(minutes, 60)
        milliseconds = int((point_time % 1) * 1000)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{milliseconds:03}"

    def on_click(self, event):
        # Define a tolerance for detecting clicks near a red line
        tolerance = 5

        # Calculate the time corresponding to the clicked position
        time_in_seconds = (event.x() / (1000 * self.view.soundView.zoom_level)) * (self.view.soundView.samples_per_60_seconds / 44100)
        new_position = int(time_in_seconds * 44100)  # Convert time to sample index


        # Detect double-click event

        if event.type() == QEvent.MouseButtonDblClick:

            # Check if the click is near an existing red line
            for point in self.model.soundModel.red_line_positions:
                if abs(point.position - (event.x() / self.view.soundView.zoom_level)) < tolerance:
                    # If close to a red line, remove it
                    self.model.soundModel.red_line_positions.remove(point)
                    self.view.soundView.update()
                    return

            # If a double-click, add a red line at the clicked position
            flagPoint = FlagPoint(event.x() / self.view.soundView.zoom_level, time_in_seconds)
            
            self.controller.tableController.set_flag(flagPoint)
            self.model.soundModel.red_line_positions.append(flagPoint)
            self.view.soundView.update()
        else:

            # Check if the click is near an existing red line
            for point in self.model.soundModel.red_line_positions:
                if abs(point.position - (event.x() / self.view.soundView.zoom_level)) < tolerance:
                    
                    flagPoint = FlagPoint(point.position, point.time)
                    self.controller.tableController.set_flag(flagPoint)
                    self.view.soundView.show_popup()
                    pyperclip.copy(self.create_str_time(point.time))
                    return


            pyperclip.copy(self.create_str_time(time_in_seconds))
            # Ensure the new position does not exceed the length of the audio
            if new_position < len(self.soundModel.audio_data):
                self.soundModel.current_chunk_index = new_position
                self.view.soundView.set_playback_position(self.soundModel.current_chunk_index)

                if self.stream and self.stream.is_active():
                    self.stream.stop_stream()
                    self.stream.start_stream()

                self.view.soundView.update_time_display(self.soundModel.current_chunk_index)
            else:
                print("Cannot jump forward, end of the audio reached.")

    def move_to_next_red_line(self):
        current_time = self.soundModel.current_chunk_index
        red_lines_after_current = [point for point in self.model.soundModel.red_line_positions if int(point.time * 44100) > current_time]
        if red_lines_after_current:
            next_red_line = min(red_lines_after_current, key=lambda point: point.time)
            self.view.soundView.seek_to_time(next_red_line.time)

    def move_to_previous_red_line(self):
        current_time = self.soundModel.current_chunk_index
        red_lines_before_current = [point for point in self.model.soundModel.red_line_positions if int(point.time * 44100) < current_time - 1500]
        if red_lines_before_current:
            previous_red_line = max(red_lines_before_current, key=lambda point: point.time)
            previous_red_line.green_on_me = True
            self.view.soundView.seek_to_time(previous_red_line.time)
