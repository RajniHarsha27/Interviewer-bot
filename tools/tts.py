from google.cloud import texttospeech
import os
import pyaudio
import time

def synthesize_and_play_audio(client_file: str, text: str, language_code: str = 'en-US', voice_name: str = 'en-US-Studio-O', speaking_rate: float = 1.0, pitch: float = 1.0):
    """
    Converts text to speech and plays the audio in real-time using Google Cloud Text-to-Speech.
    
    Args:
        client_file (str): Path to the Google Cloud service account JSON file.
        text (str): The text to be converted to speech.
        language_code (str): Language code for the voice. Default is 'en-US'.
        voice_name (str): Name of the voice. Default is 'en-US-Studio-O'.
        speaking_rate (float): Speaking rate for the voice. Default is 1.0.
        pitch (float): Pitch adjustment for the voice. Default is 1.0.
    """
    # Set up Google Cloud credentials
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = client_file
    client = texttospeech.TextToSpeechClient()
    

    # response = client.synthesize_speech(
    #     input = synthesis_input,
    #     voice = voice,
    #     audio_config = audio_config
    # )

    # with open('output.mp3', 'wb') as output:
    #     output.write(response.audio_content)
    #     print('Audio content written tot file "output.mp3"')
        # PyAudio configuration for streaming playback


    
    p = pyaudio.PyAudio()
    stream = p.open(rate=24000, channels=1, format=pyaudio.paInt16, output=True)
    
    def play_audio(response):
        """Streams audio content to the speaker."""
        stream.write(response.audio_content)
    
    # Split text into sentences and synthesize each one
    sentences = text.split('.')
    for sentence in sentences:
        if sentence.strip():  # Skip empty sentences
            synthesis_input = texttospeech.SynthesisInput(text=sentence.strip() + '.')
            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                name=voice_name
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                speaking_rate=speaking_rate,
                pitch=pitch
            )
            
            # Synthesize the speech and play it
            response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
            play_audio(response)
            time.sleep(0.2)  # Pause between sentences for natural flow
            print(f"Played sentence: {sentence.strip()}")
    
    # Clean up
    stream.stop_stream()
    stream.close()
    p.terminate()

# Example usage
if __name__ == "__main__":
    client_file = 'sa_text2speech.json'
    text_block = 'Your CV highlights experience with various LLMs and NLP tasks. Can you describe a project where you had to fine-tune a large language model for a specific application, detailing the challenges you faced and how you overcame them?'
    synthesize_and_play_audio(client_file, text_block)