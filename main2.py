from __future__ import print_function
import requests
import random
import pyttsx
import math
import wave

artists_to_songs =	{
  "David Bowie": "Heroes",
  "Coldplay": "Yellow",
  "Cranberries": "Linger",
  "Nena": "99 Red Balloons",
  "Psy": "Gangnam style",
  "Netta": "toy"
}

BASE_API_URL = "https://api.lyrics.ovh/v1/"

def get_lyrics():
    lyrics_list = []
    for artist in artists_to_songs:
        song_url = BASE_API_URL + artist + "/" + artists_to_songs[artist]
        response = requests.get(song_url)
        response_json = response.json()
        lyrics_list.append(response_json["lyrics"])
    return lyrics_list

def extract_lyrics_lines(lyrics_list):
    all_lyrics_list = []
    for lyrics in lyrics_list:
        all_lyrics_list = all_lyrics_list + [line for line in lyrics.split('\n') if line]
    return all_lyrics_list

def get_random_lyrics(lyrics):
    string = ''
    for i in range(20):
        index = random.randint(1,len(lyrics)-1)
        string = string + lyrics[index]
    return string

def sing(song):
    engine = pyttsx.init()
    engine.say(song)
    engine.runAndWait()

def main():
    lyrics_list = get_lyrics()
    all_lyrics_lines = extract_lyrics_lines(lyrics_list)
    random.shuffle(all_lyrics_lines)
    lyrics_string = get_random_lyrics(all_lyrics_lines)
    print(lyrics_string)
    # sing(lyrics_string)
    return lyrics_string

def append_silence(duration_milliseconds=500):
    """
    Adding silence is easy - we add zeros to the end of our array
    """
    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)): 
        audio.append(0.0)

    return


def append_sinewave(
        freq=440.0, 
        duration_milliseconds=500, 
        volume=1.0):
    """
    The sine wave generated here is the standard beep.  If you want something
    more aggresive you could try a square or saw tooth waveform.   Though there
    are some rather complicated issues with making high quality square and
    sawtooth waves... which we won't address here :) 
    """ 

    global audio # using global variables isn't cool.

    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)):
        audio.append(volume * math.sin(2 * math.pi * freq * ( x / sample_rate )))

    return


def save_wav(file_name):
    # Open up a wav file
    wav_file=wave.open(file_name,"w")

    # wav params
    nchannels = 1

    sampwidth = 2

    # 44100 is the industry standard sample rate - CD quality.  If you need to
    # save on file size you can adjust it downwards. The stanard for low quality
    # is 8000 or 8kHz.
    nframes = len(audio)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

    # WAV files here are using short, 16 bit, signed integers for the 
    # sample size.  So we multiply the floating point data we have by 32767, the
    # maximum value for a short integer.  NOTE: It is theortically possible to
    # use the floating point -1.0 to 1.0 data directly in a WAV file but not
    # obvious how to do that using the wave module in python.
    for sample in audio:
        wav_file.writeframes(struct.pack('h', int( sample * 32767.0 )))

    wav_file.close()

    return

C_major_f = [261.6256, 293.6648, 329.6276, 349.2282, 391.9954, 440, 493.8833]

def sound_1():
    i = 0
    f = 0
    dir = 1
    while i < 30:

        append_sinewave(C_major_f[f], 500, 1.0)
        append_silence(500)
        if random.randint(0,4) == 0:
            dir *= -1
        f += dir
        if f < 0:
            f = len(C_major_f) - 1
        elif f >= len(C_major_f):
            f = 0
        i += 1
        print("i = %d, f = %d"%(i, f))

def random_key(word):
    
    key_index = random.randint(0,len(C_major_f)-1)
    append_sinewave(C_major_f[key_index], len(word) * 100, 1.0)
    append_silence(500)

def random_key_accounting_length(word):

    index = len(word) % len(C_major_f) 
    append_sinewave(C_major_f[index], 500, 1.0)
    append_silence()
    print("Doing stuff.")

if __name__== "__main__":
    words = main()
    audio = []
    sample_rate = 44100.0
    words = words.split(' ')

    for word in words:
        random_key_accounting_length(word)

    save_wav("output3.wav")
