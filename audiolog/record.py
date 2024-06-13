import tkinter as tk
import speech_recognition as sr
import wave
import os
from datetime import datetime
import threading

class SpeechRecorderApp:
    def __init__(self, master):
        self.master = master
        master.title("Speech Recorder App")

        self.label = tk.Label(master, text="Press 'Start Recording' to begin recording.")
        self.label.pack()

        self.record_button = tk.Button(master, text="Start Recording", command=self.start_recording)
        self.record_button.pack()

        self.text_output = tk.Text(master, height=10, width=50)
        self.text_output.pack()

        self.recording_thread = None
        self.is_recording = False
        self.frames = []

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def start_recording(self):
        self.record_button.config(state=tk.DISABLED)
        self.label.config(text="Recording... Say 'end recording' to stop.")
        
        self.is_recording = True
        self.frames = []

        self.recording_thread = threading.Thread(target=self.record_audio)
        self.recording_thread.start()

        # Check periodically if the recording thread is still alive
        self.master.after(100, self.check_recording_status)

    def record_audio(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.is_recording:
                audio = self.recognizer.listen(source)
                self.frames.append(audio.get_wav_data())

                try:
                    speech_as_text = self.recognizer.recognize_google(audio)
                    # self.master.after(10, lambda: self.update_text_output(f"You said: {speech_as_text}\n"))

                    if "end recording" in speech_as_text.lower():
                        self.master.after(10, lambda: self.update_text_output("Recording ended.\n"))
                        self.is_recording = False  # Exit the recording loop
                except sr.UnknownValueError:
                    self.master.after(10, lambda: self.update_text_output("Google Speech Recognition could not understand audio.\n"))
                except sr.RequestError as e:
                    self.master.after(10, lambda: self.update_text_output(f"Could not request results from Google Speech Recognition service; {e}\n"))

        # After recording stops, save the audio
        self.save_audio()

    def update_text_output(self, text):
        self.text_output.insert(tk.END, text)
        self.text_output.see(tk.END)  # Scroll to the end

    def check_recording_status(self):
        if self.recording_thread.is_alive():
            self.master.after(100, self.check_recording_status)
        else:
            self.record_button.config(state=tk.NORMAL)
            self.label.config(text="Press 'Start Recording' to begin recording.")

    def save_audio(self):
        directory = "./audio_saves"
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_name = generate_log_filename(directory)
        wav_filename = f"{directory}/{file_name}.wav"
        with wave.open(wav_filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.microphone.SAMPLE_RATE)
            wf.writeframes(b''.join(self.frames))

        self.update_text_output(f"Audio recorded and saved to {wav_filename}\n")

def generate_log_filename(directory):
    current_date = datetime.now().strftime("%d_%m_%Y")
    num_files = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
    filename = f"audio_log_{num_files:03d}_{current_date}"
    return filename

def main():
    root = tk.Tk()
    app = SpeechRecorderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
