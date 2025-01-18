from google.cloud import speech

import base64


speech_client = speech.SpeechClient()


def speech_to_text(audio_base64):

    # decode the base64 audio
    audio_bytes = base64.b64decode(audio_base64)

    audio = speech.RecognitionAudio(content=audio_bytes)

    # configuration
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz = 16000,
        language_code= 'en-US'
    )

    # peforming speech recognition
    response = speech_client.recognize(config=config, audio=audio)

    # CHECK response is not empty
    if response.results:
        return response.results[0].alternatives[0].transcript
    

    return None



