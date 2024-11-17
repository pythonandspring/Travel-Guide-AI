#PYTHON CODE FOR DATA VOICE CONTROLLER:
import speech_recognition as sr
def speech_to_text():
    recognizer = sr.Recognizer()

    # Use the microphone as the source of input
    with sr.Microphone() as source:
        print("Please speak...")
        # Adjust for ambient noise and listen to the input
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Convert the audio to text
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError:
        print("Could not request results; check your internet connection.")

# Call the function
speech_to_text()
