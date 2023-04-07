import speech_recognition as sr
import os
import re
import json
import openFolderModule
import subprocess
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

def openFile():
    r = sr.Recognizer()
    root_dir_path = None
    cache = openFolderModule.load_cache()

    with sr.Microphone() as source:
        speak("Say the name of the root directory to search in (or leave blank to search everywhere)")
        audio = r.listen(source)

    try:
        root_dir_name = r.recognize_google(audio).replace(" ", "")
        # Remove any extra spaces
        root_dir_name = root_dir_name.replace("underscore", "_")
        root_dir_name = root_dir_name.replace("dot", ".")
        root_dir_name = root_dir_name.replace("left square bracket", "[")
        root_dir_name = root_dir_name.replace("right square bracket", "]")
        print(root_dir_name)
    except sr.UnknownValueError:
        speak("Unable to recognize speech. Searching everywhere...")
        root_dir_name = None

    file_path = None
    with sr.Microphone() as source:
        speak("Say the name of the file you want to open")
        audio = r.listen(source)

    file_name = r.recognize_google(audio).replace(" ", "")
    file_name = file_name.replace("underscore", "_")
    file_name = file_name.replace("dot", ".")
    file_name = file_name.replace("left square bracket", "[")
    file_name = file_name.replace("right square bracket", "]")

    if root_dir_name is not None:
        if root_dir_name in cache:
            root_dir_path = cache[root_dir_name]

            for root, dirs, files in os.walk(root_dir_path):
                print(f"Searching in {root} for {root_dir_name}")
                for name in files:
                    print(file_name.lower(), name.lower())
                    m = re.search(r'\b{}\b'.format(re.escape(file_name.lower())), name.lower(), re.IGNORECASE)
                    if m is not None:
                        file_path = os.path.join(root, name)
                        break
                if file_path is not None:
                    break

            if file_path is None:
                speak("File not found.")
            else:
                if file_path.endswith('.bat'):
                    with open(file_path, 'r') as f:
                        args = f.read().strip().split()
                    os.chdir(os.path.dirname(file_path))
                    subprocess.Popen(args, cwd=os.path.dirname(file_path))
                else:
                    subprocess.Popen(file_path, shell=True)
        else:
            for root, dirs, files in os.walk('/'):
                print(f"Searching in {root} for {root_dir_name}")
                for name in files:
                    m = re.search(r'\b{}\b'.format(re.escape(root_dir_name.lower())), name.lower(), re.IGNORECASE)
                    if m is not None:
                        file_path = os.path.join(root, name)
                        cache[root_dir_name] = file_path
                        break
                if file_path is not None:
                    break
            if file_path is None:
                speak("File not found.")
            else:
                if file_path.endswith('.bat'):
                    with open(file_path, 'r') as f:
                        args = f.read().strip().split()
                    os.chdir(os.path.dirname(file_path))
                    subprocess.Popen(args, cwd=os.path.dirname(file_path))
                else:
                    subprocess.Popen(file_path, shell=True)
    else:
        for root, dirs, files in os.walk('/'):
            print(f"Searching in {root} for {file_name}")
            for name in files:
                m = re.search(r'\b{}\b'.format(re.escape(file_name.lower())), name.lower(), re.IGNORECASE)
                if m is not None:
                    file_path = os.path.join(root, name)
                    break
            if file_path is not None:
                break
        if file_path is None:
            speak("File not found.")
        else:
            os.system(f'start "" "{file_path}"')