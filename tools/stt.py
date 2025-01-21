import io
from google.oauth2 import service_account
from google.cloud import speech
import pyaudio

client_file = 'sa_speech2text.json'
credentials = service_account.Credentials.from_service_account_file(client_file)
client = speech.SpeechClient(credentials=credentials)

# from mic

RATE = 16000
CHUNK = 1024
FORMAT= pyaudio.paInt16
CHANNELS = 1



p = pyaudio.PyAudio()


stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)


print('Recoding...')


audio_content = []
# 5 second
for _ in range(0, int(RATE/CHUNK * 5)):
    data = stream.read(CHUNK)
    audio_content.append(data)



stream.stop_stream()
stream.close()
p.terminate()


audio_data = b''.join(audio_content)





audio = speech.RecognitionAudio(content=audio_data)


# audio_file  = 'mono_audio.wav'


# with io.open(audio_file, 'rb') as f:
#     content = f.read()
#     audio = speech.RecognitionAudio(content=content)



config = speech.RecognitionConfig(
    encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
    # sample_rate_hertz = 44100,
    sample_rate_hertz = RATE,
    language_code="en-US"
)


response = client.recognize(config=config, audio=audio)

alternatives = [alternative.transcript for result in response.results for alternative in result.alternatives]
print(" ".join(alternatives))
