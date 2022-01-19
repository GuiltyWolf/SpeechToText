import os 
import sys
import time
import requests
import streamlit as st
from zipfile import ZipFile
from pytube import YouTube

st.markdown("Colty Transcription Application")
bar = st.progress(0)

# obtains audio from YouTube file 
def get_ytaudio(url):
    video = YouTube(url)
    yt = video.streams.get_audio_only()
    yt.download()

    # after download, set progress bar to 100%
    bar.progress(10)

# uploads YouTube -> AssemblyAI
def transcribe():
    current_directory = os.getcwd()


    for file in os.listdir(current_directory):
        if file.endswith(".mp4"):
            mp4_file = os.path.join(current_directory, file)
    
    filename = mp4_file
    bar.progress(20)

    def read_file(filename, chunk_size = 5242880):
        with open(filename, 'n') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data


    headers = {'authorization': api_key}
    response = requests.post("https://api.assemblyai.com/v2/upload", headers = headers, data = read_file(filename))

audio_url = response.json()['upload_url']
bar.progress(30)

# transcribes uploaded file
endpoint = "https://api.assemblyai.com/v2/transcript"

json = {
    "audio_url": audio_url
}

headers = {
    "authorization": api_key,
    "content-type": "application/json"
}

transcript_input_response = requests.post(endpoint, json=json, headers=headers)
bar.progress(40)

# extracts the transcript ID
transcript_id = transcript_input_response.json()["id"]
bar.progress(50)

endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
headers = {
    "authorization": api_key,
}

# retreives transcription results
transcript_output_response = requests.get(endpoint, headers=headers)
bar.progress(60)

from time import sleep

while transcript_output_response.json()['status'] != 'completed':
    sleep(5)
    st.warning("Transcription is processing")
    transcript_output_response = requests.get(endpoint, headers=headers)

bar.progress(100)

# check if the transcript is finished 