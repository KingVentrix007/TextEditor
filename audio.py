from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import pyaudio
import wave
import speech_recognition as sr
def encrypt_audio_aes_gcm(input_file, output_file, password):
    with open(input_file, 'rb') as f:
        audio_data = f.read()

    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password)

    cipher = Cipher(algorithms.AES(key), modes.GCM(salt), backend=default_backend())
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(audio_data) + encryptor.finalize()

    with open(output_file, 'wb') as f:
        f.write(salt + ciphertext + encryptor.tag)

def decrypt_audio_aes_gcm(input_file, output_file, password):
    with open(input_file, 'rb') as f:
        encrypted_data = f.read()

    salt = encrypted_data[:16]
    ciphertext = encrypted_data[16:-16]
    tag = encrypted_data[-16:]

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password)

    cipher = Cipher(algorithms.AES(key), modes.GCM(salt, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    with open(output_file, 'wb') as f:
        f.write(decrypted_data)




def record_audio(file_name, duration=5, sample_rate=44100, channels=2, chunk=1024):
    audio = pyaudio.PyAudio()

    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk)

    print("Recording...")
    frames = []

    recognizer = sr.Recognizer()

    while True:
        data = stream.read(chunk)
        frames.append(data)

        # Convert the last chunk of audio to text
        audio_chunk = sr.AudioData(data, sample_rate=sample_rate, sample_width=audio.get_sample_size(pyaudio.paInt16))
        try:
            text = recognizer.recognize_google(data)
            print("Recognized:", text)
            if "end recording" in text.lower() or "end transmission" in text.lower():
                print("Recording stopped.")
                break
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wave_file = wave.open(file_name, 'wb')
    wave_file.setnchannels(channels)
    wave_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wave_file.setframerate(sample_rate)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()
# Example usage
# output_file = 'recorded_audio.wav'
# record_audio(output_file, duration=10)  # Record for 10 seconds
# Example usage
if __name__ == "__main__":
    input_file = 'recorded_audio.wav'
    record_audio(input_file)  
    output_file = 'encrypted_audio_aes_gcm.wav'
    password = b'my_super_secret_password'
    encrypt_audio_aes_gcm(input_file, output_file, password)
    input_file = 'encrypted_audio_aes_gcm.wav'
    output_file = 'decrypted_audio.wav'
    password = b'my_super_secret_password'

    decrypt_audio_aes_gcm(input_file, output_file, password)