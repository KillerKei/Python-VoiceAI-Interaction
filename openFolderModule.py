import speech_recognition as sr
import os
import re
import json
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

def load_cache():
    try:
        with open('cache.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_cache(cache):
    with open('cache.json', 'w') as f:
        json.dump(cache, f)

def openFolder():
    r = sr.Recognizer()
    root_dir_path = None
    cache = load_cache()
    
    with sr.Microphone() as source:
        speak("Say the name of the root directory to search in (or leave blank to search everywhere)")
        audio = r.listen(source)

    try:
        root_dir_name = r.recognize_google(audio).replace(" ", "")
        # Remove any extra spaces
        root_dir_name = root_dir_name.replace("underscore", "_")
    except sr.UnknownValueError:
        speak("Unable to recognize speech. Searching everywhere...")
        root_dir_name = None

    folder_path = None
    with sr.Microphone() as source:
        speak("Say the name of the folder you want to open")
        audio = r.listen(source)

    folder_name = r.recognize_google(audio).replace(" ", "")
    # Remove any extra spaces

    if root_dir_name is not None:
        if root_dir_name in cache:
            root_dir_path = cache[root_dir_name]
        else:
            for root, dirs, files in os.walk('/'):
                print(f"Searching in {root} for {root_dir_name}")
                for name in dirs:
                    m = re.search(r'\b{}\b'.format(re.escape(root_dir_name.lower())), name.lower(), re.IGNORECASE)
                    if m is not None:
                        root_dir_path = os.path.join(root, name)
                        cache[root_dir_name] = root_dir_path
                        break
                if root_dir_path is not None:
                    break

        if root_dir_path is None:
            speak("Root directory not found.")
        else:
            for root, dirs, files in os.walk(root_dir_path):
                print(f"Searching in {root}")
                for name in dirs:
                    m = re.search(r'\b{}\b'.format(re.escape(folder_name.lower())), name.lower(), re.IGNORECASE)
                    if m is not None:
                        folder_path = os.path.join(root, name)
                        break
                if folder_path is not None:
                    break
            if folder_path is None:
                speak("Folder not found.")
            else:
                speak(f"Opening folder {folder_name}...")
                os.system(f'start "" "{folder_path}"')
    else:
        for root, dirs, files in os.walk('/'):
            print(f"Searching in {root}")
            for name in dirs:
                m = re.search(r'\b{}\b'.format(re.escape(folder_name.lower())), name.lower(), re.IGNORECASE)
                if m is not None:
                    folder_path = os.path.join(root, name)
                    break
            if folder_path is not None:
                break

        if folder_path is None:
            speak("Folder not found.")
        else:
            speak(f"Opening folder {folder_name}...")
            os.system(f'start "" "{folder_path}"')

    save_cache(cache)
