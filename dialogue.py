#!/usr/bin/env python3
import json
from datetime import datetime

import speech_recognition as sr
import pyttsx3

from gtts import gTTS
from playsound import playsound

import nltk


class Dialogue:
    def __init__(self, microphone_device_index=0):
        self.recognizer = sr.Recognizer()
        self.setMicrophone(microphone_device_index)
        self.speechCache = {}
        self.load_speech_cache()

    def adjust_for_ambient_noise(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

    def setMicrophone(self, device_index=0):
        self.microphone = sr.Microphone(device_index=device_index)
        self.adjust_for_ambient_noise()

    def listen(self):
        with self.microphone as source:
            audio = self.recognizer.listen(source)
        try:
            # TODO try offline first to recognize for keywords?
            # TODO try online and fallback to offline if not available?
            # recognize speech using Google Speech Recognition
            value = self.recognizer.recognize_google(audio)
            return value
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
            return ""
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}", e)
            return ""

    def load_speech_cache(self):
        with open("speech_cache.json") as fp:
            self.speechCache = json.loads(fp.read())

    def save_speech_cache(self):
        with open("speech_cache.json", "w") as fp:
            fp.write(json.dumps(self.speechCache))

    def say(self, words):
        # speak text
        # engine = pyttsx3.init()
        # engine.say(value)
        # engine.runAndWait()

        # TODO try online and fall back to offline

        if not words:
            # nothing to say
            return

        currentTime = datetime.now().isoformat()  # used for caching

        words = words.lower()

        # split into sentences and say one after the other to improve cache collision
        # and enable precaching
        sentences = nltk.sent_tokenize(words)

        if len(sentences) > 1:
            for sentence in sentences:
                self.say(sentence)
            return
        else:
            words = words.strip(". ")

        # TODO precache sentences while playing

        if words in self.speechCache.keys():
            # try speaking from cache
            playsound(self.speechCache[words]["filePath"])

            # update cache
            self.speechCache[words]["timesUsed"] += 1
            self.speechCache[words]["lastUsed"] = currentTime
            self.save_speech_cache()
        else:
            # save to cache and play from it
            self.precache(words, currentTime)
            self.say(words)


    def precache(self, words, currentTime=datetime.now().isoformat()):
        tts = gTTS(text=words, lang='en', slow=False)
        filePath = "speech_cache/" + currentTime + ".mp3"
        tts.save(filePath)

        # remember cache
        self.speechCache[words] = {
            "filePath": filePath,
            "timeSaved": currentTime,
            "timesUsed": 1,
            "lastUsed": currentTime
        }
        self.save_speech_cache()
