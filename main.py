import wave
import os, time
from datetime import datetime
import pasimple
import numpy as np
from recordingToText import toTextFile
import argparse
import select
import sys

# Ignore warnings for now
import warnings

warnings.filterwarnings("ignore")

def scaleArray (data):
    return (data - data.min()) / (data.max() - data.min())

def foundSilence(data, threshold):
    checkData = scaleArray(data)
    m = np.median(checkData)
    if m < (threshold ) or np.isnan(m):
        return True

def foundAudio(data, threshold):
    # scale array
    checkData = scaleArray(data) 
    m = np.median(checkData)
    if not np.isnan(m) and m > threshold:
        return True

parser = argparse.ArgumentParser(description='Audio Capture From System')
parser.add_argument('--stream',
                    help='Give a name for the stream.',
                    default="yo")
parser.add_argument(
    '--threshold',
    help='Stop recording when the amplitude is below this threshold.',
    default=0.5)
parser.add_argument('--device_name',
                    help='Record from this device',
                    default="record-n-play.monitor")
args = parser.parse_args()

# Audio attributes for the recording
FORMAT = pasimple.PA_SAMPLE_S32LE
SAMPLE_WIDTH = pasimple.format2width(FORMAT)
CHANNELS = 1
SAMPLE_RATE = 16000
seconds_of_audio = 2
threshold = float(args.threshold)


if __name__ == '__main__':

    while True:
        stop_recording = False  # Flag to control the recording loop

        # Start the recording loop
        while not stop_recording:
            
            # Initialize the recording
            recording = []  # List to store the recorded audio chunks

            try:

                with pasimple.PaSimple(
                        pasimple.PA_STREAM_RECORD,
                        FORMAT,
                        CHANNELS,
                        SAMPLE_RATE,
                        app_name=args.stream,
                        stream_name=args.stream,
                        #device_name=args.device_name,
                ) as pa:
                    audio_data = pa.read(CHANNELS * SAMPLE_RATE *
                                            SAMPLE_WIDTH * seconds_of_audio)

                    # Convert the audio data into a numpy array
                    audio_data_array = np.frombuffer(audio_data,
                                                        dtype=np.int32)

                    # Reshape the array to a 2D array with one column
                    audio_data_array = audio_data_array.reshape(-1, 1)

                    # Append the recorded chunk to the list
                    recording.append(audio_data_array)

                    # Check if a pause was detected in the recorded chunk
                    if foundSilence(audio_data_array, threshold):
                        stop_recording = True  # Stop the recording loop

            except KeyboardInterrupt:
                stop_recording = True

            # Concatenate the recorded chunks into a single array
            recording = np.concatenate(recording)

            if np.mean(recording) == 0:
                print('no audio...')
                continue

            # Get the current timestamp
            timestamp = datetime.now().strftime("%m-%d-%Y:%H")

            # Create a new directories with the timestamp as the name
            not os.path.exists(timestamp) and os.makedirs(timestamp)
            not os.path.exists(f"{timestamp}/text") and os.makedirs(
                f"{timestamp}/text")
            not os.path.exists(f"{timestamp}/audio") and os.makedirs(
                f"{timestamp}/audio")

            textFileName = f"{timestamp}/text/{time.time()}.txt"
            audioFileName = f"{timestamp}/audio/{time.time()}.wav"

            # Save audio to a file
            with wave.open(audioFileName, 'wb') as wave_file:
                wave_file.setsampwidth(SAMPLE_WIDTH)
                wave_file.setnchannels(CHANNELS)
                wave_file.setframerate(SAMPLE_RATE)
                wave_file.writeframes(recording.tobytes())

            toTextFile(audioFileName, textFileName)