import io
from google.oauth2 import service_account
from google.cloud import speech
import pyaudio

def transcribe_audio(client_file: str, duration: int = 5, rate: int = 16000, chunk: int = 1024):
    """
    Captures audio from the microphone and transcribes it using Google Cloud Speech-to-Text API.
    
    Args:
        client_file (str): Path to the Google Cloud service account JSON file.
        duration (int): Duration in seconds to record audio. Default is 5 seconds.
        rate (int): Audio sample rate in Hz. Default is 16000 Hz.
        chunk (int): Buffer size for capturing audio. Default is 1024 bytes.
    
    Returns:
        str: The transcribed text.
    """
    # Set up Google Cloud Speech-to-Text client
    credentials = service_account.Credentials.from_service_account_file(client_file)
    client = speech.SpeechClient(credentials=credentials)
    
    # PyAudio configuration
    format_ = pyaudio.paInt16
    channels = 1


    


    p = pyaudio.PyAudio()
    stream = p.open(format=format_,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)
    
    print("Recording...")
    audio_content = []
    
    # Record audio for the specified duration
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        audio_content.append(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # Combine recorded audio into a single byte string
    audio_data = b''.join(audio_content)
    audio = speech.RecognitionAudio(content=audio_data)
    
    # Speech-to-Text API configuration
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=rate,
        language_code="en-US"
    )

     # audio_file  = 'mono_audio.wav'


    # with io.open(audio_file, 'rb') as f:
    #     content = f.read()
    #     audio = speech.RecognitionAudio(content=content)

    # Transcribe audio
    response = client.recognize(config=config, audio=audio)
    alternatives = [alternative.transcript for result in response.results for alternative in result.alternatives]
    
    # Return the transcribed text
    return " ".join(alternatives)

# Example usage
if __name__ == "__main__":
    client_file = 'sa_speech2text.json'
    transcription = transcribe_audio(client_file)
    print("Transcription:", transcription)