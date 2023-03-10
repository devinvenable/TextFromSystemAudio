# TextFromSystemAudio
Using Pulse Audio, capture system sound and convert human speech to text.

## Overview
This is a small program I put together to capture audio from a team that liked to work verbally.
During online meetings, I would turn this on to capture audio notes. It uses HuggingFace's transformers
library to access a pre-trained automatic-speech-recognition model. 

Since I work on a Linux box, I found that capturing Pulse audio was the quickest and simplest way to capture 
audio playing through my speakers, regardless of source, like a conference call or something like YouTube.

I made some small effort to detect pauses in speech for a natural breaking point between recorded phases. 
To avoid a long pause between capture and transcription, I used the threading library, so that recording can 
continue while processing of the last phrase is underway.

## installation
pip install -r requirements.txt

## run
python main.py
