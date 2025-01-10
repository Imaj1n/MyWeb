import random
import streamlit as st
import datetime
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import time
from streamlit_lottie import st_lottie
import json

def app():
    audio = {
            "Kill Bill - SZA": "https://raw.githubusercontent.com/Imaj1n/MyWeb/main/src2/Bahan_Lain/Music/SZA%20-%20Kill%20Bill%20(Audio).mp3",
            "Bad - Wave to Earth": "https://raw.githubusercontent.com/Imaj1n/MyWeb/main/src2/Bahan_Lain/Music/wave%20to%20earth%20-%20bad%20(Official%20Lyric%20Video).mp3",
            "Blue - Yung Kai": "https://raw.githubusercontent.com/Imaj1n/MyWeb/main/src2/Bahan_Lain/Music/Yung%20Kai%20-%20Blue.mp3"
        }

        # Menampilkan pilihan musik di selectbox
    music_choice = st.selectbox("Mau Musik Apaa", list(audio.keys()), format_func=lambda x: f"{x}")

        # Mengambil file path berdasarkan pilihan pengguna
    selected_audio = "https://raw.githubusercontent.com/Imaj1n/MyWeb/main/src2/Bahan_Lain/Music/SZA%20-%20Kill%20Bill%20(Audio).mp3"
        # Memutar audio berdasarkan pilihan
    audio_file = open(selected_audio, "rb").read()
    st.audio(audio_file, format="audio/mp3")
  
