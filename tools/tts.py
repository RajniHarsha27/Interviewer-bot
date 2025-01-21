from google.cloud import texttospeech
import typing
import base64

tts_client = texttospeech.TextToSpeechClient()

# Converts to speehc and return Base64-encoded
def text_to_speech(text):
    
    wave = texttospeech.SynthesisInput(text=text)

    # selecting voice
    voice = texttospeech.VoiceSelectionParams(
        language_code='en-US', ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    
    # configuration
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEnconding.MP3)

    # generate speech
    response = tts_client.synthesize_speech(
        input=wave, voice=voice, audio_config=audio_config
    )

    # convert to base64 encoder

    return base64.b64encode(response.audio_content).decode('utf-8')



    


    

    


