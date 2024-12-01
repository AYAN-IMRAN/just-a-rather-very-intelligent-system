import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import musiclibrary  # Assuming you have music data in a separate file or dictionary
import google.generativeai as genai
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "<Your NewsAPI Key Here>"

# Music library with song names as keys and YouTube links as values
music = {
    "Guman": "https://www.youtube.com/watch?v=ega13BleRJc",
    "Agency": "https://www.youtube.com/watch?v=DnLaJA75NRw",
    "skyfall": "https://www.youtube.com/watch?v=DeumyOzKqgI&pp=ygUHc2t5ZmFsbA%3D%3D",
    "wolf": "https://www.youtube.com/watch?v=ThCH0U6aJpU&list=PLnrGi_-oOR6wm0Vi-1OsiLiV5ePSPs9oF&index=21"
}





# Function to speak text using gTTS and Pygame
def speak(text):
    tts = gTTS(text)
    tts.save('Voice.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('Voice.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("Voice.mp3")

# Function to process AI content based on a command
def aiProcess(command):
    try:
        # Configure Gemini with your API key
        genai.configure(api_key="<Your Gemini Api Key Here>")
        # Initialize the model
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        # Generate content
        response = model.generate_content(command)
        return response.text
    except Exception as e:
        return "Sorry, I couldn't process that request."

# Function to process recognized commands
import webbrowser
import musiclibrary  # Ensure this is correctly imported

def processCommand(c):
    # Handle predefined commands
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com/AYAN-IMRAN")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        # Extract song name by splitting the command after "play"
        song_name = " ".join(c.lower().split()[1:]).strip()  # Get everything after "play"
        
        # Normalize song name to match the library (case insensitive)
        song_name = song_name.capitalize()

        # Check if the song exists in the music library
        if song_name in musiclibrary.music:
            link = musiclibrary.music[song_name]
            webbrowser.open(link)  # Open the song link
        else:
            # Handle the case when the song is not in the library
            print(f"Song '{song_name}' not found in the library.")
            speak(f"Sorry, I couldn't find the song {song_name}.")  # Assuming you have a speak function

        
    
    elif "news" in c.lower():
        # Fetch news using the NewsAPI
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])
                for article in articles:
                    speak(article['title'])
            else:
                speak("Sorry, I couldn't fetch the news at the moment.")
        except Exception as e:
            speak("There was an error fetching the news.")
    else:
        # Process unknown commands with AI
        output = aiProcess(c)
        speak(output)

# Main function to listen for commands
def main():
    speak("Hello, Sir! Jarvis at your service.....")
    while True:
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source)
                print("Listening for wake word 'Jarvis'...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=1)
            
            word = recognizer.recognize_google(audio)
            print(f"Word recognized: {word.lower()}")

            if word.lower() == "jarvis":
                speak("Yes, Sir")
                # Listen for a command after the wake word
                with sr.Microphone() as source:
                    print("Jarvis Active... Listening for command...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    print(f"Command recognized: {command}")
                    processCommand(command)

        except sr.UnknownValueError:
            print("Could not understand the audio. Please try again.")
        except sr.RequestError:
            print("Network error. Please check your connection.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
