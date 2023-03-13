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

## configure Pulse

  DEFAULT_OUTPUT=$(pacmd list-sinks | grep -A1 "* index" | grep -oP "<\K[^ 
  >]+")

  pactl load-module module-combine-sink sink_name=record-n-play slaves=$DEFAULT_OUTPUT sink_properties=device.description="Record-and-Play"

This command loads a module called module-combine-sink in PulseAudio and creates a new sink called record-n-play. The slaves option specifies that the new sink should combine the output from the $DEFAULT_OUTPUT sink (which is likely the default audio output device on your system) with itself, effectively creating a sink that can be used for recording and playback simultaneously. The sink_properties option sets the description of the new sink to "Record-and-Play".

This command will allow you to record audio output while simultaneously listening to it. By creating a combined sink, you can direct the output of an application to the new sink, which will then be available for recording while still being played back through the original output device.

## run
python main.py
