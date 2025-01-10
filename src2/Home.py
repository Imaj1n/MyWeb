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
    # Mengambil file path berdasarkan pilihan pengguna
    selected_audio = "https://raw.githubusercontent.com/Imaj1n/MyWeb/main/src2/Bahan_Lain/Music/SZA%20-%20Kill%20Bill%20(Audio).mp3"
    # Memutar audio berdasarkan pilihan
    st.audio(selected_audio, format="audio/mpeg", loop=True)
