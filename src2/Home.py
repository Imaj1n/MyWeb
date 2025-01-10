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
    # Menambahkan CSS untuk menyesuaikan font hanya di sidebar
    st.markdown(
        """
        <style>
        .css-1d391kg {
            font-family: 'Courier New', Courier, monospace;
            font-size: 16px;
            color: #333333;
        }
        .css-1kyxreq {
            font-family: 'Arial', sans-serif;
            font-size: 18px;
            color: #4CAF50;
        }
        .css-1kv3btt {
            font-family: 'Verdana', sans-serif;
            font-size: 14px;
            color: #555555;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    cola,colb = st.columns(2)
    # Mendapatkan jam saat ini
    current_hour = datetime.datetime.now().hour
    # Menampilkan teks di konten utama
    if current_hour < 12:
        condition = "Pagii"
    elif 12 <= current_hour < 15:
        condition = "Siangg"
    elif 15 <= current_hour < 18:
        condition = "Soree"
    else:
        condition = "Malemm"

    icon = {
        "Love":"💖",
        "Smile":"🥰",
        "Rose":"🌹",
        "Cat":"🐱"
    }
    emoji = gif_url = random.choice(list(icon.values()))
    with cola:
        st.subheader(f"Mett {condition} Ayangg {emoji}")
        # Menampilkan input URL GIF
        url_gift = {
            '1':"https://media.giphy.com/media/1yld7nW3oQ2IyRubUm/giphy.gif",
            '2':"https://media.giphy.com/media/1yld7nW3oQ2IyRubUm/giphy.gif",
            '3':"https://media.giphy.com/media/1yld7nW3oQ2IyRubUm/giphy.gif",
        }
        # Menampilkan GIF animasi dari input
        gif_url = random.choice(list(url_gift.values()))
        url_ayang = "https://raw.githubusercontent.com/Imaj1n/MyWeb/main/src2/Bahan_Lain/Gif_Us/Gif_Ayang1.gif"
        #Gif_Ayang1.gif
        st.image(url_ayang,use_container_width=True)
    with colb:
        # Tampilkan judul aplikasi
        emoji1 = gif_url = random.choice(list(icon.values()))
        st.subheader(f'Gimana Harinya?{emoji1}')
        # Tautkan file audio (bisa berupa file lokal atau URL)
        # Ganti dengan URL gambar yang Anda dapatkan dari Internert
        image_url = 'https://i.pinimg.com/originals/4c/3d/d7/4c3dd72edde903f71cfaa05e20231f92.gif'
        # Menampilkan gambar
        st.image(image_url, use_container_width=True)
        # Memasukkan file audio lokal
        # Daftar musik
        audio = {
            "Kill Bill - SZA": "https://raw.githubusercontent.com/Imaj1n/MyWeb/main/src2/Bahan_Lain/Music/SZA%20-%20Kill%20Bill%20(Audio).mp3",
            "Bad - Wave to Earth": "https://raw.githubusercontent.com/Imaj1n/MyWeb/main/src2/Bahan_Lain/Music/wave%20to%20earth%20-%20bad%20(Official%20Lyric%20Video).mp3",
            "Blue - Yung Kai": "https://raw.githubusercontent.com/Imaj1n/MyWeb/main/src2/Bahan_Lain/Music/Yung%20Kai%20-%20Blue.mp3"
        }

        # Menampilkan pilihan musik di selectbox
        music_choice = st.selectbox("Mau Musik Apaa", list(audio.keys()), format_func=lambda x: f"{x}")

        # Mengambil file path berdasarkan pilihan pengguna
        selected_audio = audio[music_choice]
        # Memutar audio berdasarkan pilihan
        audio_file = open(selected_audio, "rb").read()
        st.audio(audio_file, format="audio/mp3")
        # Inisialisasi koneksi ke Google Sheets
        conn = st.connection("gsheets", type=GSheetsConnection)
        # Nama worksheet dan kolom
        worksheet_name = "Sheet3"
        column_name = "Pesan Ayang"
        # Membaca data yang ada di worksheet
        df = conn.read(worksheet=worksheet_name)

        # Jika kolom "Pesan Ayang" belum ada, buat kolom baru kosong
        if column_name not in df.columns:
            df[column_name] = pd.NA  # Gunakan pd.NA untuk NaN yang konsisten di seluruh baris
        # Input pesan baru dari pengguna
        new_message = st.text_input("Kmu mau ngomong apaa buat hari ini")
        if new_message:
            # Menambahkan pesan baru ke data
            new_row = pd.DataFrame({column_name: [new_message]})  # Membuat DataFrame dengan 1 baris
            
            # Menggabungkan data baru dengan DataFrame yang ada
            df = pd.concat([df, new_row], ignore_index=True)
            
            # Menyimpan kembali ke Google Sheets
            conn.update(worksheet=worksheet_name, data=df)
        # Tampilkan data yang sudah diperbarui
        d = (list((df.to_dict()).values()))[0]
    # Menampilkan waktu di sidebar
    st.sidebar.success(f"{datetime.datetime.now().strftime('%d %B %Y')}")
    st.sidebar.subheader("Catatan Kecil")
    st.divider()
    st.sidebar.info((list(d.values()))[-1])
    gif_for_conditions = {
        "1": "https://i.pinimg.com/originals/b0/9a/06/b09a0682c2cd4d291bf195d52870affd.gif",
        "2": "https://i.pinimg.com/originals/18/d7/13/18d713fbda6a28afc6ddf2cb87341a4c.gif",
        "3": "https://i.pinimg.com/originals/1a/01/c0/1a01c05651c84d12ca135a48b71ee138.gif",
    }

    # Memilih GIF secara acak dari daftar GIF
    selected_gif_url = random.choice(list(gif_for_conditions.values()))
    # Menampilkan GIF di sidebar
    st.sidebar.image(selected_gif_url,use_container_width=True)

    #-------------------------------------------------------------------------
    # Fungsi untuk memuat animasi Lottie
    def load_lottie_animation(file_path: str):
        with open(file_path, "r") as file:
            return json.load(file)

    # Tentukan tanggal ulang tahun dan ulang tahun jadian
    tanggal_ulang_tahun = datetime.date(2025, 1, 11)
    tanggal_ulang_jadian = datetime.date(2025, 1, 12)

    # Tentukan file animasi untuk ulang tahun dan ulang tahun jadian
    animasi_ulang_tahun = "https://raw.githubusercontent.com/Imaj1n/MyWeb/main/src2/Animasi/anim.json"
    animasi_ulang_jadian = "https://raw.githubusercontent.com/Imaj1n/MyWeb/main/src2/Animasi/anim2.json"

    # Fungsi untuk mengecek apakah hari ini adalah ulang tahun atau ulang tahun jadian
    def check_surprise_date():
        today = datetime.date.today()
        
        if today == tanggal_ulang_tahun:
            return "Mett Ulang tahun ayy 🎉!", animasi_ulang_tahun
        elif today == tanggal_ulang_jadian:
            return "Mett ulang tahun jadian kita 💫!", animasi_ulang_jadian
        else:
            return None, None

    # Fungsi untuk mengecek apakah saat ini adalah jam 12 malam
    def check_midnight():
        current_time = datetime.datetime.now()
        if current_time.hour == 0 and current_time.minute == 0:
            return True
        return False

    # Fungsi utama untuk menampilkan kejutan sepanjang hari
    def show_surprise():
        surprise_message, animation_file = check_surprise_date()
        
        if surprise_message and animation_file:
            # Memuat animasi berdasarkan file yang dipilih
            animation_json = load_lottie_animation(animation_file)
            
            st.title(surprise_message)
            
            # Menampilkan animasi dan audio sepanjang hari
            st_lottie(animation_json, speed=0.7, width=600, height=400, key="animation")
            
            # Tentukan file audio berdasarkan tanggal
            audio_file = 'https://raw.githubusercontent.com/Imaj1n/MyWeb/main/src2/Bahan_Lain/Music/LullabyThe%20Promised%20Neverland.mp3'
            st.audio(audio_file, format='audio/mp3', start_time=0)
            # Jika saat ini jam 12 malam, tampilkan Toast Notification dan efek salju
            today = datetime.date.today()
            if check_midnight():
                if today == tanggal_ulang_tahun:
                    st.toast(f"Selamat {surprise_message} 🎉")
                    time.sleep(2)
                    st.toast(f"Semoga tahun ini semakin banyak kebahagiaan dan kesuksesan untukmu! 🎂✨")
                    time.sleep(2)
                    st.toast(f"Semoga semua impianmu tercapai! Lov uuu 💖💖💖")
                elif today == tanggal_ulang_jadian:
                    st.toast(f"Selamat {surprise_message} 💖")
                    time.sleep(2)
                    st.toast(f"Terima kasih sudah menjadi bagian dari hidupku! 🥰")
                    time.sleep(2)
                    st.toast(f"Semoga kita terus bahagia bersama, lov uuu 💞💫")
                time.sleep(2)
                st.snow()  # Menampilkan salju di Streamlit
        else:
            pass

    # Panggil fungsi utama untuk mengecek dan menampilkan kejutan jika perlu
    show_surprise()






    
    # Mengambil file path berdasarkan pilihan pengguna
    # selected_audio = "https://raw.githubusercontent.com/Imaj1n/MyWeb/main/src2/Bahan_Lain/Music/SZA%20-%20Kill%20Bill%20(Audio).mp3"
    # Memutar audio berdasarkan pilihan
    # st.audio(selected_audio, format="audio/mpeg", loop=True)
