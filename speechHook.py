import openFolderModule
import openFileModule
import speech_recognition as sr
import os
import re
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

r = sr.Recognizer()

with sr.Microphone() as source:
    speak("Hey boss, what would you like me to do")
    audio = r.listen(source)

try:
    wordSaid = r.recognize_google(audio).lower()
    # check if wordSaid contains open file
    print(wordSaid)
    if "open folder" in wordSaid:
        openFolderModule.openFolder()
    elif "open file" in wordSaid:
        openFileModule.openFile()
except sr.UnknownValueError:
    speak("I didn't catch that")