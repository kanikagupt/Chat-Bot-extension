import speech_recognition as sr

def transcribe_audio_to_text(audio_file_path):
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(audio_file_path) as source:
        # Record the audio
        audio_data = recognizer.record(source)

    try:
        # Recognize the speech using Google's free service
        text = recognizer.recognize_google(audio_data)
        print("Transcription: " + text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# Example usage
if __name__ == "__main__":
    audio_file_path = "path/to/your/audio/file.wav"  # Change this to your audio file path
    transcribe_audio_to_text(audio_file_path)
