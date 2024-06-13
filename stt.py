import speech_recognition as sr
import wave

def recognize_and_record_speech_from_mic():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening... Say 'end recording' to stop.")
        
        frames = []
        is_recording = True
        sample_rate = source.SAMPLE_RATE
        
        while is_recording:
            audio = recognizer.listen(source)
            frames.append(audio.get_wav_data())

            try:
                # Recognize speech using Google Web Speech API
                speech_as_text = recognizer.recognize_google(audio)
                print(f"You said: {speech_as_text}")
                
                if "end recording" in speech_as_text.lower():
                    print("Ending recording.")
                    is_recording = False
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand the audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
        
        # Save the audio to a WAV file
        wav_filename = "recorded_audio.wav"
        with wave.open(wav_filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # Set sample width to 2 bytes (16 bits)
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))
        
        print(f"Audio recorded and saved to {wav_filename}")

def main():
    print("Welcome to the Speech-to-Text and Text-to-Speech app!")
    while True:
        print("Please speak something...")
        recognize_and_record_speech_from_mic()
        
        # Ask if user wants to continue or exit
        user_input = input("Do you want to continue? (yes/no): ").strip().lower()
        if user_input == 'no':
            break

if __name__ == "__main__":
    main()
