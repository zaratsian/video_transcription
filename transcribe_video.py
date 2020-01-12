

import subprocess



def extract_audio_from_video(video_file, audio_file):
    '''
        Inputs:
            video_file: Name of video file that contains the audio.
            audio_file: Name of the audio file that is generated.
    '''
    process = subprocess.Popen(['ffmpeg', '-i', video_file, audio_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
    
    stdout, stderr = process.communicate()
    print(stdout)
    return None


def copy_to_gcs(audio_file, gcs_bucket):
    process = subprocess.Popen(['gsutil', 'cp', audio_file, gcs_bucket],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
    
    stdout, stderr = process.communicate()
    print(stdout)
    return None


def sample_long_running_recognize(storage_uri):
    '''
    Transcribe long audio file from Cloud Storage using asynchronous speech
    recognition

    Args:
      storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
    
    # storage_uri = 'gs://cloud-samples-data/speech/brooklyn_bridge.raw'
    '''
    
    client = speech_v1.SpeechClient()
    
    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 16000

    # The language of the supplied audio
    language_code = "en-US"

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "sample_rate_hertz": sample_rate_hertz,
        "language_code": language_code,
        "encoding": encoding,
    }
    audio = {"uri": storage_uri}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()

    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))
