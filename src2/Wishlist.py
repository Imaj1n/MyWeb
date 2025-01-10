import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd


def app():
    st.title("Wishlist 🗓️")
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="BARU")    
    # Data awal
    # df0 = pd.DataFrame(
    #     [
    #         {"Kegiatan": "Belajar", "Prioritas": 8, "checklist": False},
    #     ]
    # )

    # # Menyimpan DataFrame di session state jika belum ada
    # if 'df' not in st.session_state:
    #     st.session_state.df = df0

    # Membuat dua kolom untuk input dan editor
    col1, col2 = st.columns(2)

    with col1:
        st.text("Ini tempay kita buat wishlist yang bakal kita pengen")
        st.session_state.df = df
        st.session_state.df['checklist'] = st.session_state.df['checklist'].replace({0: False, 1: True,"TRUE":True,"FALSE":False})
        # Menampilkan editor data dengan opsi untuk menambah baris baru
        edited_df = st.data_editor(st.session_state.df, num_rows="dynamic")

    with col2:
        # Input untuk menambah kegiatan baru
        input_kegiatan = st.text_input("Kegiatannya apa")
        prioritas = st.number_input('Prioritas:', min_value=0, max_value=10, step=1)
        Checkkbox =  st.selectbox(
            "Udah Belum?",
            (False,True),
            )   

        @st.cache_data
        def ubah_tabel(Mode):
            conn.update(worksheet="BARU", data=st.session_state.df)
            edited_df = st.data_editor(st.session_state.df, num_rows="dynamic")
            st.info(f"{Mode} Berhasil dilakukan")
        # Button untuk menambahkan baris baru
        kol1,kol2,kol3 = st.columns(3)
        with kol1:
            a =  st.button('Add')
        with kol2 : 
            b = st.button('Edit')
        with kol3:
            c = st.button('Delete')

        if a:
            # Menambahkan baris baru dengan data yang dimasukkan
            new_row = pd.DataFrame([{"Kegiatan": input_kegiatan, "Prioritas": prioritas, "checklist": Checkkbox}])
            st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)  
            conn.update(worksheet="BARU", data=st.session_state.df)
            # Memperbarui editor data dengan DataFrame yang telah diperbarui
            edited_df = st.data_editor(st.session_state.df, num_rows="dynamic")
            st.info("Edit Berhasil dilakukan")
        if b:
            if input_kegiatan in st.session_state.df['Kegiatan'].values:
                st.session_state.df.loc[st.session_state.df['Kegiatan'] == input_kegiatan, ['Prioritas', 'checklist']] = [prioritas, Checkkbox]
                ubah_tabel("Edit")
            else:
                st.error(f"Tidak ada namanya kegiatan {input_kegiatan}")
        if c:
            if input_kegiatan in st.session_state.df['Kegiatan'].values:
                st.session_state.df = st.session_state.df[st.session_state.df['Kegiatan'] != input_kegiatan]
                ubah_tabel("Delete")
            else:
                st.error(f"Tidak ada namanya kegiatan {input_kegiatan}")
    # Menentukan kegiatan dengan prioritas tertinggi
    favorite_command = edited_df.loc[edited_df["Prioritas"].idxmax()]["Kegiatan"]

    # Menampilkan hasil
    st.sidebar.info(f"Kegiatan yang mesti dilakuin terlebih dahulu **{favorite_command}** 🎈")
