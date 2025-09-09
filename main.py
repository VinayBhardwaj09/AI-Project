import speech_recognition as sr
import wikipediaapi 
import pyttsx3
import speedtest
import webbrowser
import musiclibrary
import requests
import threading
import datetime

def speak(text):
    engine.say(text)
    engine.runAndWait()

recognizer = sr.Recognizer()
engine = pyttsx3.init()
# Set a natural speech rate
engine.setProperty('rate', 170)
engine.setProperty('volume', 0.9) 
newsapi = "ebe2fe982228436e83cdc1dd7376dc4a"  

def test_speed():
    speak("Testing your internet speed, please wait.")
    st = speedtest.Speedtest()
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000      # Convert to Mbps
    ping = st.results.ping
    print(f"Your download speed is {download_speed:.2f} megabits per second.")
    print(f"Your upload speed is {upload_speed:.2f} megabits per second.")
    print(f"Your ping is {ping} milliseconds.")
    speak(f"Your download speed is {download_speed:.2f} megabits per second.")
    speak(f"Your upload speed is {upload_speed:.2f} megabits per second.")
    speak(f"Your ping is {ping} milliseconds.")

def fetch_wikipedia_summary(query):
    wiki_wiki = wikipediaapi.Wikipedia('ind')  # Create an instance for English Wikipedia
    page = wiki_wiki.page(query)  # Search for the page
    
    if page.exists():
        summary = page.summary[:500]  # Limit to 500 characters
        return summary
    else:
        return "Sorry, I could not find any information on that topic."
def get_current_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")  # e.g., 03:45 PM
    return current_time

def get_current_date():
    today = datetime.datetime.today()
    current_date = today.strftime("%B %d, %Y")  # e.g., October 03, 2024
    return current_date
def processCommand(command):
    # Process the command and perform tasks without looping forever
    if "open google" in command.lower():
        webbrowser.open("https://google.com")
        speak("Opening Google")
    elif "open youtube" in command.lower():
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
    elif "open facebook" in command.lower():
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook")
    elif "search wikipedia for" in command.lower():
        topic = command.lower().replace("search wikipedia for", "").strip()
        speak(f"Searching Wikipedia for {topic}")
        summary = fetch_wikipedia_summary(topic)
        speak(summary)
    elif "what time is it" in command.lower():
        current_time = get_current_time()
        speak(f"The current time is {current_time}")
        print(f"The current time is {current_time}")
    elif "what is the date" in command.lower() or "what's today's date" in command.lower():
        current_date = get_current_date()
        speak(f"Today's date is {current_date}")
        print(f"Today's date is {current_date}")
    elif command.lower().startswith("play"):
        song = command.lower().split(" ")[1]
        link = musiclibrary.music.get(song, None)
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find the song.")
    elif "news" in command.lower(): 
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}") 
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles:
                speak(article['title'])
        else:
            speak("Sorry, I couldn't retrieve the news.")
    elif "internet speed" in command.lower():
        test_speed()
        return "exit"  # return 'exit' to break out of the main loop
    else:
        speak("Sorry, I did not understand the command.")

if __name__ == "__main__":
    speak("Initializing Hermes....")
    while True:
        # Listen for the wake word
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Listening for the wake word...(hello)")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            word = recognizer.recognize_google(audio)
            if word.lower() == "hello":
                speak("Yes, how may I help you?")
                # Listen for command
                with sr.Microphone() as source:
                    print("Hermes Active...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    if processCommand(command) == "exit":
                        break  # break out of the loop when the user says "hermes bye"
        except sr.UnknownValueError:
            print("Didn't catch that.")
        except sr.RequestError as e:
            print(f"Request error: {e}")
        except Exception as e:
            print(f"Error: {e}")
