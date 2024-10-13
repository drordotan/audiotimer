import numpy as np
from pydub import AudioSegment

class SoundModel:

    def __init__(self,model) -> None:
        self.model = model
        self.audio_data = []

        self.red_line_positions = []

        self.current_chunk_index = 0
        self.time_total_str = None
        self.is_playing = False
        self.is_paused = False

        self.is_load = False

    def load_sound(self,path):
        audio = AudioSegment.from_mp3(path)
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(44100)

        self.audio_data = np.array(audio.get_array_of_samples(), dtype=np.int16)

        # Update the total time display
        total_time_sec = len(self.audio_data) / 44100
        minutes, seconds = divmod(total_time_sec, 60)
        hours, minutes = divmod(minutes, 60)
        milliseconds = int((total_time_sec % 1) * 1000)
        self.time_total_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{milliseconds:03}"

        self.is_load = True

    