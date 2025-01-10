import streamlit as st
from streamlit_option_menu import option_menu
import Home, Timeline, Wishlist
# # import streamlit as st
# # from streamlit_gsheets import GSheetsConnection

# # st.title("Read Google Sheet as DataFrame")

# # conn = st.connection("gsheets", type=GSheetsConnection)
# # df = conn.read(worksheet="Sheet1")

# Set konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Web",
)

# Cek apakah session state sudah memiliki status login
if 'password_correct' not in st.session_state:
    st.session_state.password_correct = False

# Jika password benar, tampilkan aplikasi
if not st.session_state.password_correct:
    # Masukkan password untuk akses aplikasi
    password = st.text_input('Enter password', type='password')

    if password =="":
        pass
    # Jika password benar, set session state dan sembunyikan input password
    elif password == "1234":  # Ganti dengan password yang Anda inginkan
        st.session_state.password_correct = True
        st.rerun()  # Refresh aplikasi setelah login berhasil

    elif password != "1234":
        st.error("Incorrect password")  # Menampilkan pesan jika password salah
else:
    # Define kelas MultiApp
    class MultiApp:

        def __init__(self):
            self.apps = []

        def add_app(self, title, func):
            self.apps.append({
                "title": title,
                "function": func
            })

        def run(self):
            # Sidebar untuk memilih menu aplikasi
            with st.sidebar:
                app = option_menu(
                    menu_title='Mii-Chan',
                    options=["Timeline", "Home", "Wishlist"],
                    icons=['chat-fill','house-fill','person-circle'],#,'trophy-fill','info-circle-fill'
                    menu_icon='chat-text-fill',
                    default_index=1,
                    styles={
                        "container": {"padding": "5!important", "background-color": 'black'},
                        "icon": {"color": "white", "font-size": "23px"},
                        "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                        "nav-link-selected": {"background-color": "#02ab21"},
                    }
                )

            # Panggil aplikasi berdasarkan pilihan menu
            if app == "Timeline":
                Timeline.app()
            if app == "Home":
                Home.app()
            if app == "Wishlist":
                Wishlist.app()

    # Jalankan aplikasi
    app = MultiApp()
    app.run()
