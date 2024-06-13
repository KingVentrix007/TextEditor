from pydub import AudioSegment
from pydub.playback import play
import random
import sounddevice as sd
import soundfile as sf

def record_audio(output_file, duration, sample_rate=44100):
    print("Recording audio...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
    sd.wait()
    sf.write(output_file, recording, sample_rate)
    print("Audio recording saved to:", output_file)

def scramble_audio(input_file, output_file, key):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Split the audio into small chunks (e.g., 50 milliseconds)
    chunk_size = 50  # milliseconds
    chunks = [audio[i:i+chunk_size] for i in range(0, len(audio), chunk_size)]

    # Use the key to seed the random number generator
    random.seed(key)

    # Randomly shuffle the chunks
    random.shuffle(chunks)

    # Concatenate the shuffled chunks back into a new audio file
    scrambled_audio = chunks[0]
    for chunk in chunks[1:]:
        scrambled_audio += chunk

    # Export the scrambled audio to a new file
    scrambled_audio.export(output_file, format="wav")

def descramble_audio(scrambled_file, output_file, key):
    # Load the scrambled audio file
    audio = AudioSegment.from_file(scrambled_file)

    # Split the audio into small chunks (e.g., 50 milliseconds)
    chunk_size = 50  # milliseconds
    chunks = [audio[i:i+chunk_size] for i in range(0, len(audio), chunk_size)]

    # Use the key to seed the random number generator
    random.seed(key)

    # Create an index list and shuffle it
    indices = list(range(len(chunks)))
    random.shuffle(indices)

    # Create a list to hold the descrambled chunks
    descrambled_chunks = [None] * len(chunks)

    # Place each chunk back to its original position
    for original_index, scrambled_index in enumerate(indices):
        descrambled_chunks[scrambled_index] = chunks[original_index]

    # Concatenate the descrambled chunks back into a new audio file
    descrambled_audio = descrambled_chunks[0]
    for chunk in descrambled_chunks[1:]:
        descrambled_audio += chunk

    # Export the descrambled audio to a new file
    descrambled_audio.export(output_file, format="wav")

# Example usage:
input_file = "recorded_audio.wav"
scrambled_file = "scrambled_audio.wav"
output_file = "descrambled_audio.wav"
key = 123  # Example key, you can change this
duration = 5  # Duration of recording in seconds

# Record audio
record_audio(input_file, duration)

# Scramble audio
scramble_audio(input_file, scrambled_file, key)

# Play scrambled audio
scrambled_audio = AudioSegment.from_wav(scrambled_file)
print("Playing scrambled audio...",scrambled_file)
play(scrambled_audio)
print("Scrambled audio playback finished.")

# Descramble audio
descramble_audio(scrambled_file, output_file, key)

# Play descrambled audio
descrambled_audio = AudioSegment.from_wav(output_file)
print("Playing descrambled audio...",output_file)
play(descrambled_audio)
print("Descrambled audio playback finished.")
