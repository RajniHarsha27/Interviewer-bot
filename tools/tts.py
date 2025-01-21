from google.cloud import texttospeech
import os
import pyaudio 
import time

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'sa_text2speech.json'

client = texttospeech.TextToSpeechClient()

text_block = 'hello i am hubnex. How can I assist you?'

synthesis_input = texttospeech.SynthesisInput(text=text_block)

voice = texttospeech.VoiceSelectionParams(
    language_code='en-US',
    name='en-US-Studio-O'
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.LINEAR16,  # Use LINEAR16 for streaming
    speaking_rate=1,
    pitch=1
)



# response = client.synthesize_speech(
#     input = synthesis_input,
#     voice = voice,
#     audio_config = audio_config
# )

# with open('output.mp3', 'wb') as output:
#     output.write(response.audio_content)
#     print('Audio content written tot file "output.mp3"')

# Streaming setup
p = pyaudio.PyAudio()
stream = p.open(rate=24000, channels=1, format=pyaudio.paInt16, output=True)

def play_audio(response):
    stream.write(response.audio_content)

sentences = text_block.split('.')

for sentence in sentences:
    synthesis_input.text = sentence.strip() + '.'
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    play_audio(response)
    time.sleep(0.5)  
    print(f"Played sentence: {sentence.strip()}")

stream.stop_stream()
stream.close()
p.terminate()
