import tkinter as tk
import wave
import os
from datetime import datetime
import threading
import pygame  # For playing audio (install pygame using pip if not installed)
import pyaudio  # For audio recording (install pyaudio using pip if not installed)
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import sec

class SpeechRecorderApp:
    def __init__(self, master):
        self.master = master
        master.title("Speech Recorder App")

        self.label = tk.Label(master, text="Press 'Start Recording' to begin recording.")
        self.label.pack()

        self.start_button = tk.Button(master, text="Start Recording", command=self.start_recording)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack()

        self.save_button = tk.Button(master, text="Save Audio", command=self.save_audio, state=tk.DISABLED)
        self.save_button.pack()

        self.text_output = tk.Text(master, height=10, width=50)
        self.text_output.pack()

        self.scrollbar = tk.Scrollbar(master, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(master, yscrollcommand=self.scrollbar.set, height=10, width=50)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.listbox.yview)

        self.load_saved_audio_files()

        self.recording_thread = None
        self.is_recording = False
        self.frames = []

        # Initialize Pygame for audio playback
        pygame.init()
        self.pygame_initialized = True

    def start_recording(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)
        self.label.config(text="Recording...")

        self.is_recording = True
        self.frames = []

        self.recording_thread = threading.Thread(target=self.record_audio)
        self.recording_thread.start()

    def stop_recording(self):
        self.is_recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.NORMAL)
        self.label.config(text="Press 'Start Recording' to begin recording.")

    def record_audio(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100

        audio = pyaudio.PyAudio()

        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        while self.is_recording:
            data = stream.read(CHUNK)
            self.frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

    def save_audio(self):
        directory = "./audio_saves"
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_name = generate_log_filename(directory)
        wav_filename = f"{directory}/{file_name}.wav"

        # Save recorded audio as a WAV file
        with wave.open(wav_filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))

        # Encrypt the audio file
        encrypted_filename = f"{directory}/{file_name}_encrypted.wav"
        sec.encrypt_audio_aes_gcm(wav_filename, encrypted_filename, b"your_password")

        self.update_text_output(f"Audio recorded and saved to {encrypted_filename}\n")
        self.load_saved_audio_files()  # Refresh list of saved audio files

    def load_saved_audio_files(self):
        self.listbox.delete(0, tk.END)  # Clear existing items

        directory = "./audio_saves"
        if not os.path.exists(directory):
            os.makedirs(directory)

        audio_files = sorted([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name)) and name.endswith("_encrypted.wav")])

        for idx, audio_file in enumerate(audio_files):
            button_frame = tk.Frame(self.listbox)
            button_frame.pack(fill=tk.X)

            label_text = f"Audio Log {idx + 1} - {get_date_from_filename(audio_file)}"
            label = tk.Label(button_frame, text=label_text, width=40)
            label.pack(side=tk.LEFT, padx=5)

            play_button = tk.Button(button_frame, text="Play", command=lambda file=directory + '/' + audio_file: self.play_audio(file))
            play_button.pack(side=tk.RIGHT, padx=5)

    def play_audio(self, audio_file):
        # Decrypt the audio file before playing
        decrypted_filename = audio_file.replace("_encrypted.wav", "_decrypted.wav")
        sec.decrypt_audio_aes_gcm(audio_file, decrypted_filename, b"your_password")

        if self.pygame_initialized:
            pygame.mixer.music.load(decrypted_filename)
            pygame.mixer.music.play()

    def update_text_output(self, text):
        self.text_output.insert(tk.END, text)
        self.text_output.see(tk.END)  # Scroll to the end

    def on_closing(self):
        if self.pygame_initialized:
            pygame.quit()
        self.master.destroy()

def generate_log_filename(directory):
    current_date = datetime.now().strftime("%d_%m_%Y")
    num_files = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
    filename = f"audio_log_{num_files:03d}_{current_date}"
    return filename

def get_date_from_filename(filename):
    try:
        date_str = "_".join(filename.split('_')[3:]).split(".")[0]  # Extract dd_mm_yyyy from filename
        date_obj = datetime.strptime(date_str, "%d_%m_%Y")
        return date_obj.strftime("%d/%m/%Y")
    except Exception as e:
        print(f"Error parsing filename: {e}")
        return "Unknown Date"

def main():
    root = tk.Tk()
    app = SpeechRecorderApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
