from pydub import AudioSegment
from pydub.playback import play
import random
import sounddevice as sd
import soundfile as sf
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
