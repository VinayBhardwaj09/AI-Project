from gtts import gTTS
import os

# Text to speak
text = "Hello, how can I assist you today?"

# Set language and TLD (for accents like 'com.au' for Australian, 'co.uk' for British)
tts = gTTS(text=text, lang='en', tld='co.uk')  # British accent

# Save to a file
tts.save("output.mp3")

# Play the file (works in most systems)
os.system("start output.mp3")
