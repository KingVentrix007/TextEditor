from gtts import gTTS
import os

# Text to be spoken
text = "Stand By for recording to start"

# Language in which you want to convert
language = 'en'

# Create gTTS object
speech = gTTS(text=text, lang=language, slow=False, tld='com')

# Save the converted audio to a file
speech.save("./audiolog/audio/wait.mp3")

# Play the converted file (optional)
os.system("start ./audiolog/audio/wait.mp3")
