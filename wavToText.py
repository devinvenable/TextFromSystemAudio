from transformers import pipeline
import librosa
import soundfile as sf

transcriber = pipeline("automatic-speech-recognition",
                       model="facebook/wav2vec2-large-960h-lv60-self",
                       tokenizer="facebook/wav2vec2-large-960h-lv60-self")


def WavToText(input_file):

    # read the file
    speech, samplerate = sf.read(input_file)

    # make it 1-D
    if len(speech.shape) > 1:
        speech = speech[:, 0] + speech[:, 1]

    # Resample to 16khz
    if samplerate != 16000:
        speech = librosa.resample(speech, samplerate, 16000)

    return transcriber(speech)
