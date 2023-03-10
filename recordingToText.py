import os, time
from datetime import datetime
from wavToText import WavToText
import threading

def run(recordingFilename, textFilename):
    # Get the current timestamp
    timestamp = datetime.now().strftime("%m-%d-%Y:%H")

    # Create a new directory with the timestamp as the name
    not os.path.exists(timestamp) and os.makedirs(timestamp)

    # Convert the audio file to text
    result = WavToText(recordingFilename)
    with open(textFilename, "a") as file:
        file.write(result['text'])
        file.write(', ')
        print(result['text'])


def toTextFile(recordingFilename, textFilename):
    # create a thread object
    thread = threading.Thread(target=run, args=(recordingFilename, textFilename))

    # start the thread
    thread.start()
    