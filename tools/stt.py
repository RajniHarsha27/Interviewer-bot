import io
from google.oauth2 import service_account
from google.cloud import storage, speech

def upload_to_gcs(client_file: str, bucket_name: str, local_file: str, destination_blob_name: str):
    """
    Uploads a file to a Google Cloud Storage bucket.

    Args:
        client_file (str): Path to the service account JSON file.
        bucket_name (str): Name of the GCS bucket.
        local_file (str): Path to the local file to upload.
        destination_blob_name (str): The destination name for the file in GCS.

    Returns:
        str: The GCS URI of the uploaded file.
    """
    # Initialize Google Cloud Storage client
    credentials = service_account.Credentials.from_service_account_file(client_file)
    storage_client = storage.Client(credentials=credentials)

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload the file
    blob.upload_from_filename(local_file)

    # Generate GCS URI
    gcs_uri = f"gs://{bucket_name}/{destination_blob_name}"
    print(f"File uploaded to {gcs_uri}")
    return gcs_uri


def transcribe_audio(client_file: str, gcs_uri: str):
    """
    Transcribes long audio using Google Cloud Speech-to-Text API.

    Args:
        client_file (str): Path to the Google Cloud service account JSON file.
        gcs_uri (str): The GCS URI of the audio file.

    Returns:
        str: The transcribed text.
    """
    # Set up Google Cloud Speech-to-Text client
    credentials = service_account.Credentials.from_service_account_file(client_file)
    client = speech.SpeechClient(credentials=credentials)

    # Speech-to-Text API configuration
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Change if necessary
        sample_rate_hertz=44100,  # Adjust to match your audio file
        language_code="en-US",
    )

    audio = speech.RecognitionAudio(uri=gcs_uri)

    # Use LongRunningRecognize for audio longer than 1 minute
    operation = client.long_running_recognize(config=config, audio=audio)
    print("Waiting for operation to complete...")
    response = operation.result(timeout=300)  # Adjust timeout as needed

    # Process transcription results
    alternatives = [result.alternatives[0].transcript for result in response.results]
    return " ".join(alternatives)


# Example usage
if __name__ == "__main__":
    # Service account files
    client_file_s = 'sa_cloud_storage.json'
    client_file_t = 'sa_speech2text.json'
    audio_file = 'conversation.wav'
    bucket_name = 'audio_files_hubnex'
    destination_blob_name = 'uploaded_audio/conversation.wav'


    

    # Cloud
    gcs_uri = upload_to_gcs(client_file_s, bucket_name, audio_file, destination_blob_name)

#   Transcribe audio from GCS
    transcription = transcribe_audio(client_file_t, gcs_uri)
    print("Transcription:", transcription)