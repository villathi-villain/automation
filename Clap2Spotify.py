import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pyaudio
import numpy as np

# Spotify API credentials
CLIENT_ID = 'XXX'
CLIENT_SECRET = 'XXX' 
REDIRECT_URI = 'http://localhost:8888/callback'  # Replace with your redirect URI
SCOPE = 'user-modify-playback-state user-read-playback-state user-read-currently-playing'

# Initialize Spotipy with OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

# Parameters for clap detection
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
CLAP_THRESHOLD = 5000  # Adjust this threshold based on your microphone sensitivity
SONG_URI = 'spotify:track:6FahmzZYKH0zb2f9hrVsvw'  # Replace with the URI of the song you want to play

audio = pyaudio.PyAudio()

# Start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
print("Listening for claps...")

def play_song(song_uri):
    devices = sp.devices()
    if devices and devices['devices']:
        device_id = devices['devices'][0]['id']
        print(f"Playing on device: {device_id}")
        sp.start_playback(device_id=device_id, uris=[song_uri])
    else:
        print("No active device found. Please open Spotify on one of your devices and try again.")

try:
    while True:
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        peak = np.abs(data).max()
        if peak > CLAP_THRESHOLD:
            print(f"Clap detected! Peak value: {peak}")
            play_song(SONG_URI)
            break  # Exit after playing the song
except KeyboardInterrupt:
    print("Stopped listening.")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()