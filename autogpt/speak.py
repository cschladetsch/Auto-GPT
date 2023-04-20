import os

import requests
from playsound import playsound

from autogpt.config import Config

import threading
from threading import Lock, Semaphore

import gtts

cfg = Config()

mutex_lock = Lock()  # Ensure only one sound is played at a time
queue_semaphore = Semaphore(
    1
)  # The amount of sounds to queue before blocking the main thread


def brian_speech(text):
    """Speak text using Brian with the streamelements API"""
    tts_url = f"https://api.streamelements.com/kappa/v2/speech?voice=Brian&speed=1.2&text={text}"
    response = requests.get(tts_url)

    if response.status_code == 200:
        with mutex_lock:
            with open("speech.mp3", "wb") as f:
                f.write(response.content)
            playsound("speech.mp3")
            os.remove("speech.mp3")
        return True
    else:
        print("Request failed with status code:", response.status_code)
        print("Response content:", response.content)
        return False



def say_text(text, voice_index=0):
    def speak():
        success = brian_speech(text)
        queue_semaphore.release()

    queue_semaphore.acquire(True)
    thread = threading.Thread(target=speak)
    thread.start()
