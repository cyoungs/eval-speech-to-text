import os
import speech_recognition as sr
from tqdm import tqdm
from multiprocessing.dummy import Pool
pool = Pool(8) # Number of concurrent threads


# Adapted heavily from https://github.com/akras14/speech-to-text
# https://github.com/akras14/speech-to-text/blob/master/fast.py


with open("api-key.json") as f:
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()

r = sr.Recognizer()
files = os.listdir('parts/')

def transcribe(data):
    idx, file = data
    name = "parts/" + file
    if file == ".DS_Store":
        return {
            "idx": "",
            "text": "DS Object"
        }
    print(name + " started")
    # Load audio file
    with sr.AudioFile(name) as source:
        audio = r.record(source)
    # Transcribe audio file
    try:
        text = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
        print(name + " done")
        return {
            "idx": file,
            "text": text
        }

    except sr.UnknownValueError:
        print(name + " didn't work")
        return {
            "idx": file,
            "text": "Google Speech didn't recognize this file"
        }

all_text = pool.map(transcribe, enumerate(files))
pool.close()
pool.join()

print("all files through cloud speech")

transcript = ""
try:
    for t in sorted(all_text, key=lambda x: x['idx']):
        # Format time as h:m:s - 30 seconds of text
        transcript = transcript + "{}: {}\n".format(t['idx'].split(".")[0], t['text'])
except TypeError:
    print(all_text)


print(transcript)

with open("transcript.txt", "w") as f:
    f.write(transcript)
