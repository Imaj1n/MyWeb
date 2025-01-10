# import streamlit as st
# import numpy as np
# import pandas as pd
# import plotly.graph_objects as go
# from datetime import datetime, timedelta
import plotly.express as px
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import time

def app():
    # Tambahkan konstanta untuk worksheet
    WORKSHEET_NAME = "Sheet2"  # Ganti dengan nama worksheet Anda
    # Koneksi tetap sama
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Fungsi load_data() dengan worksheet:
    def load_data():
        try:
            df = conn.read(worksheet=WORKSHEET_NAME)  # Menambahkan worksheet di sini
            if df.empty:
                return pd.DataFrame(columns=["Jadwal", "Start", "Finish", "Kegiatan", "Tanggal"])
            return df
        except Exception as e:
            st.error(f"Error reading from Google Sheets: {str(e)}")
            return pd.DataFrame(columns=["Jadwal", "Start", "Finish", "Kegiatan", "Tanggal"])

    # Fungsi save_data() dengan worksheet:
    def save_data(df):
        try:
            conn.update(data=df, worksheet=WORKSHEET_NAME)  # Menambahkan worksheet di sini
        except Exception as e:
            st.error(f"Error saving to Google Sheets: {str(e)}")

    # Membaca data kegiatan yang ada dan memastikan state session terupdate
    if 'kegiatan_list' not in st.session_state or len(st.session_state.kegiatan_list) == 0:
        df = load_data()
        st.session_state.kegiatan_list = df.to_dict(orient='records')

    # Judul aplikasi
    st.title("Timeline Kegiatan 📚")

    # Input untuk memilih tanggal yang ingin dilihat
    selected_date = st.date_input('Pilih Tanggal', value=pd.to_datetime('today').date())

    # Menyaring data kegiatan yang sesuai dengan tanggal yang dipilih
    filtered_df = [activity for activity in st.session_state.kegiatan_list if activity['Tanggal'] == str(selected_date)]

    # Input pengguna untuk kegiatan baru
    with st.form(key='input_form'):
        jadwal = st.selectbox("Pilih Jadwal", ['Aliffcuw', 'MiiChan'])
        # Menjadikan appointment slider untuk memilih rentang waktu
        appointment = st.slider(
            "Schedule your appointment:",
                min_value=time(0, 0),  # Waktu mulai dari 00:00
                max_value=time(23, 59),  # Waktu akhir hingga 23:59
                value=(time(12, 0), time(12, 30)),  # Default rentang waktu mulai dari 12:00 hingga 12:30
                format="HH:mm"
        )

        # Menentukan waktu mulai dan akhir berdasarkan slider appointment
        start_time = appointment[0]  # Waktu mulai dari slider
        end_time = appointment[1]    # Waktu akhir dari slider

        deskripsi = st.text_input('Deskripsi Kegiatan')
        submit_button = st.form_submit_button(label='Tambahkan Kegiatan')
        
        if submit_button:
            start_str = str(start_time)
            end_str = str(end_time)
            new_activity = {
                'Jadwal': jadwal,
                'Tanggal': str(selected_date),
                'Start': start_str,
                'Finish': end_str,
                'Kegiatan': deskripsi
            }
            st.session_state.kegiatan_list.append(new_activity)
            # Simpan ke Google Sheets setelah setiap input
            save_data(pd.DataFrame(st.session_state.kegiatan_list))
            # Langsung reload data untuk memastikan pembaruan
            st.rerun()

    # Menampilkan kegiatan yang sudah dimasukkan
    if filtered_df:
        # Mengubah data kegiatan menjadi DataFrame
        df_filtered = pd.DataFrame(filtered_df)
        
        # Mengonversi kolom Start dan Finish ke format datetime
        df_filtered['Start'] = pd.to_datetime('2025-01-01 ' + df_filtered['Start'])
        df_filtered['Finish'] = pd.to_datetime('2025-01-01 ' + df_filtered['Finish'])
        df_filtered['Tanggal'] = pd.to_datetime(df_filtered['Tanggal'])
        
        # Mengurutkan berdasarkan waktu mulai (Start)
        df_filtered = df_filtered.sort_values(by='Start')

        # Membuat Gantt chart
        fig = px.timeline(df_filtered, x_start="Start", x_end="Finish", y="Jadwal", 
                        color="Jadwal", title="Timeline Kegiatan")
        
        # Menyesuaikan format sumbu X
        fig.update_layout(
            xaxis=dict(
                tickformat="%H:%M",
                range=["2025-01-01 01:00:00", "2025-01-01 23:59:59"],
                tickmode='array',
                tickvals=pd.date_range("2025-01-01 01:00:00", "2025-01-01 23:00:00", freq="h")
            ),
            showlegend=True
        )
        
        # Menambahkan anotasi untuk setiap kegiatan
        for i, row in df_filtered.iterrows():
            # Garis vertikal
            fig.add_annotation(
                x=row['Start'] + (row['Finish'] - row['Start']) / 2,
                y=row['Jadwal'],
                ax=row['Start'] + (row['Finish'] - row['Start']) / 2,
                ay=-1,
                axref="x", ayref="y", xref="x", yref="y",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=1,
                arrowcolor="gray"
            )
            
            # Deskripsi kegiatan
            fig.add_annotation(
                x=row['Start'] + (row['Finish'] - row['Start']) / 2,
                y=row['Jadwal'],
                text=row['Kegiatan'],
                showarrow=False,
                font=dict(size=16, color="white"),
                align="center",
                valign="middle"
            )
        ##MEMBACA GSHEET
        # Menyambung ke Google Sheets
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(worksheet="Sheet2")

        # # Menampilkan DataFrame secara keseluruhan
        # st.write("Data Awal:")
        # st.dataframe(df)

        # Menggunakan waktu sekarang sebagai default untuk input tanggal
        tanggal_input = st.sidebar.date_input("Pilih tanggal", pd.to_datetime('now').date())

        # Mengonversi kolom 'Tanggal' yang bertipe object menjadi datetime
        df['Tanggal'] = pd.to_datetime(df['Tanggal'], errors='coerce')  # Mengonversi kolom Tanggal menjadi datetime

        # Memfilter baris berdasarkan tanggal yang dipilih
        filtered_df = df[df['Tanggal'].dt.date == tanggal_input]  # Memastikan hanya bagian tanggal yang dibandingkan

        # Menghapus kolom 'Tanggal' dari hasil filter
        filtered_df_a = filtered_df.drop(columns=['Tanggal'])

        # # Menampilkan hasil yang difilter dan kolom 'Tanggal' telah dihapus
        # if not filtered_df_a.empty:
        #     st.write(f"Data untuk tanggal {tanggal_input} (tanpa kolom Tanggal):")
        #     st.dataframe(filtered_df_a)
        # else:
        #     st.write(f"Tidak ada data untuk tanggal {tanggal_input}.")
        
        ### Overlap
        df = filtered_df
        # Mengonversi kolom Start dan Finish menjadi datetime
        df['Start'] = pd.to_datetime(df['Start'], errors='coerce')
        df['Finish'] = pd.to_datetime(df['Finish'], errors='coerce')

        # Filter data untuk Jadwal Aliffcuw dan MiiChan pada tanggal yang sama
        Aliffcuw_df = df[df['Jadwal'] == 'Aliffcuw']
        MiiChan_df = df[df['Jadwal'] == 'MiiChan']

        # Menyaring data berdasarkan tanggal yang sama
        merged_df = pd.merge(Aliffcuw_df, MiiChan_df, on='Tanggal', suffixes=('_Aliffcuw', '_MiiChan'))

        # Fungsi untuk memeriksa overlap waktu
        def check_time_overlap(start_Aliffcuw, finish_Aliffcuw, start_MiiChan, finish_MiiChan):
            # Cek apakah ada irisan waktu
            return max(start_Aliffcuw, start_MiiChan) < min(finish_Aliffcuw, finish_MiiChan)

        # Mencari irisan antara jadwal Aliffcuw dan MiiChan berdasarkan waktu
        overlap_dict = {}
        letter = 'a'  # Mulai dengan key 'a'
        for _, row in merged_df.iterrows():
            start_Aliffcuw = row['Start_Aliffcuw']
            finish_Aliffcuw = row['Finish_Aliffcuw']
            start_MiiChan = row['Start_MiiChan']
            finish_MiiChan = row['Finish_MiiChan']
            
            if check_time_overlap(start_Aliffcuw, finish_Aliffcuw, start_MiiChan, finish_MiiChan):
                # Jika ada irisan, simpan waktu irisan ke dalam dictionary dengan key yang sesuai
                overlap_start = max(start_Aliffcuw, start_MiiChan)
                overlap_end = min(finish_Aliffcuw, finish_MiiChan)
                overlap_dict[letter] = (overlap_start.time(), overlap_end.time())
                letter = chr(ord(letter) + 1)  # Menambah key berikutnya (misal 'a' -> 'b')

        # # Menampilkan hasil irisan waktu sebagai dictionary
        # if overlap_dict:
        #     st.write("Irisan Waktu (sebagai Dictionary):")
        #     st.write(overlap_dict)
        # else:
        #     st.write("Tidak ada irisan waktu antara jadwal Aliffcuw dan MiiChan.")
        

        #########################################
        st.plotly_chart(fig)
        # Menampilkan hasil yang difilter dan kolom 'Tanggal' telah dihapus
        if not filtered_df_a.empty:
            st.sidebar.write(f"Data untuk tanggal {tanggal_input}")
            st.sidebar.dataframe(filtered_df_a)
        else:
            st.write(f"Tidak ada data untuk tanggal {tanggal_input}.")
        # # Menampilkan hasil irisan waktu sebagai dictionary
        if overlap_dict:
            st.sidebar.info("Irisan Waktu (sebagai Dictionary):")
            st.sidebar.write(overlap_dict)
        else:
            st.sidebar.warning("Tidak ada irisan waktu antara jadwal Aliffcuw dan MiiChan.")
        

        # Membuat dua kolom untuk "Aliffcuw" dan "MiiChan"
        col1, col2 = st.columns(2)
        
        # Menampilkan kegiatan "Aliffcuw"
        with col1:
            st.header("Kegiatan Aliffcuw")
            for i, row in df_filtered[df_filtered['Jadwal'] == 'Aliffcuw'].iterrows():
                with st.expander(f"{row['Kegiatan']} (Start: {row['Start'].strftime('%H:%M')} - End: {row['Finish'].strftime('%H:%M')})"):
                    if st.button(f"Hapus Aliffcuw : {row['Kegiatan']}", key=f"hapus_{i}"):
                        st.session_state.kegiatan_list = [kegiatan for j, kegiatan in enumerate(st.session_state.kegiatan_list) if j != i]
                        save_data(pd.DataFrame(st.session_state.kegiatan_list))
                        st.rerun()
        
        # Menampilkan kegiatan "MiiChan"
        with col2:
            st.header("Kegiatan MiiChan")
            for i, row in df_filtered[df_filtered['Jadwal'] == 'MiiChan'].iterrows():
                with st.expander(f"{row['Kegiatan']} (Start: {row['Start'].strftime('%H:%M')} - End: {row['Finish'].strftime('%H:%M')})"):
                    if st.button(f"Hapus MiiChan : {row['Kegiatan']}", key=f"hapus_{i}"):
                        st.session_state.kegiatan_list = [kegiatan for j, kegiatan in enumerate(st.session_state.kegiatan_list) if j != i]
                        save_data(pd.DataFrame(st.session_state.kegiatan_list))
                        st.rerun()
    else:
        st.write("Belum ada kegiatan yang dimasukkan untuk tanggal ini.")