import speech_recognition as sr 
import webbrowser
import pyttsx3

recognizer = sr.Recognizer()  # Instantiate the recognizer correctly
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    speak("Initializing Hermes...")
    
    while True:
        r = sr.Recognizer()  # Re-instantiate the recognizer
        with sr.Microphone() as source:
            print("Listening... ")
            r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = r.listen(source, timeout=2)
        
        print("Recognizing...")
        try:
            command = r.recognize_google(audio)
            print(f"You said: {command}")
            
            # Implement your logic for handling recognized commands here
            # e.g., if "open google" in command.lower():
            #           webbrowser.open("https://google.com")
            #           speak("Opening Google")

        except sr.UnknownValueError:
            print("Sorry, I could not understand the command.")
            speak("Sorry, I could not understand the command.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            speak("There was an error with the speech service.")
