import streamlit as st
from google import genai
from google.genai import types
import time

# 1. Konfigurasi Halaman & Desain Visual Modern (Ramah Anak Kelas 3 MI)
st.set_page_config(
    page_title="Qiraahku - Belajar Maharah Qiraah",
    page_icon="📚",
    layout="centered"
)

# Custom CSS untuk mempercantik tampilan di tema gelap maupun terang
st.markdown("""
    <style>
    h1 {
        color: #1e6b7b;
        font-family: 'Poppins', sans-serif;
        text-align: center;
        font-weight: bold;
        margin-top: -30px;
    }
    .stButton>button {
        background-color: #ffb703 !important;
        color: #023047 !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 10px 24px !important;
    }
    .stButton>button:hover {
        background-color: #fb8500 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Inisialisasi Session State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_topic" not in st.session_state:
    st.session_state.current_topic = ""
if "current_teacher" not in st.session_state:
    st.session_state.current_teacher = ""

# 3. HALAMAN LOGIN
if not st.session_state.authenticated:
    st.title("📚 Qiraahku")
    st.subheader("Selamat Datang di Aplikasi Pembelajaran Maharah Qiraah!")
    st.write("Silakan masukkan nama dan API Key Google AI Studio Anda untuk memulai petualangan belajar.")
    
    with st.form("login_form"):
        username = st.text_input("Nama Pengguna (Username)", placeholder="Masukkan namamu...")
        api_key = st.text_input("Google AI Studio API Key", type="password", placeholder="AIzaSy...")
        submit_login = st.form_submit_button("Masuk Aplikasi")
        
        if submit_login:
            if username.strip() == "" or api_key.strip() == "":
                st.error("❌ Nama Pengguna dan API Key wajib diisi!")
            else:
                try:
                    # Validasi koneksi awal
                    client = genai.Client(api_key=api_key)
                    st.session_state.username = username
                    st.session_state.api_key = api_key
                    st.session_state.authenticated = True
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Gagal verifikasi API Key. Pastikan kunci benar. Detail: {e}")

# 4. HALAMAN UTAMA UTAMA (Setelah Login)
else:
    client = genai.Client(api_key=st.session_state.api_key)

    # Sidebar Navigasi
    with st.sidebar:
        st.header(f"👋 Halo, {st.session_state.username}!")
        st.markdown("---")
        
        teacher = st.radio(
            "Pilih Guru Pengajar:",
            ("Ustadz Rama", "Ustadzah Aisyah")
        )
        
        st.subheader("Pilihan Topik Pembelajaran")
        topic = st.selectbox(
            "Pilih materi di sekitar rumah:",
            (
                "Mengenal Hewan di Halaman Rumah (الْحَيَوَانَاتُ فِي الْفِنَاءِ)",
                "Hewan Peliharaan di Dalam Rumah (الْحَيَوَانَاتُ الْأَلِيفَةُ)",
                "Suara Hewan Pagi Hari di Sekitar Rumah (أَصْوَاتُ الْحَيَوَانَاتِ)"
            )
        )
        
        st.markdown("---")
        if st.button("🚪 Keluar dari Aplikasi", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    # Reset chat otomatis jika ganti topik atau guru
    if st.session_state.current_topic != topic or st.session_state.current_teacher != teacher:
        st.session_state.current_topic = topic
        st.session_state.current_teacher = teacher
        
        sifat = "tegas, interaktif, ramah, dan suka memuji anak" if teacher == "Ustadz Rama" else "sangat lembut, penuh kasih sayang, sabar, dan penuh senyuman"
        
        st.session_state.system_instruction = f"""
        Kamu adalah {teacher}, seorang guru bahasa Arab yang {sifat} untuk anak kelas 3 Madrasah Ibtidaiyah (MI).
        Fokus utama kamu adalah melatih Maharah Qiraah (membaca) teks bahasa Arab bertema "Asmaul Hayawanat" (Nama-nama Hewan) di sekitar rumah.
        
        Topik saat ini: {topic}.
        
        Aturan wajib:
        1. Gunakan bahasa Indonesia anak-anak yang ceria dan selipkan apresiasi Islami (Barakallah, Hebat, Pintar!).
        2. Setiap menuliskan kosakata/kalimat Arab, WAJIB diberi HARAKAT LENGKAP agar mudah dibaca anak kelas 3 MI, lalu berikan artinya.
        3. Berikan teks bacaan pendek secara bertahap (cukup 1 kalimat pendek per sesi) dan ajak siswa membaca ulang atau menebaknya.
        """
        
        greeting_msg = f"Assalamu'alaikum warahmatullah wabarakatuh, {st.session_state.username}! ✨ " \
                       f"Perkenalkan, saya {teacher}. Hari ini kita akan belajar Maharah Qiraah bersama-sama tentang " \
                       f"**{topic}**. Sudah siap membaca teks bahasa Arab bersamaku? Yuk, coba sebutkan satu hewan yang ada di rumahmu! 🐈🦆"
        
        st.session_state.messages = [{"role": "model", "text": greeting_msg}]

    # Tampilan Area Chat
    st.title("🦚 Aplikasi Qiraahku")
    st.markdown(f"<p style='text-align: center; color: #7f8c8d;'>Belajar Maharah Qiraah Kelas 3 MI bersama {teacher}</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Tampilkan History Chat
    for message in st.session_state.messages:
        avatar_icon = "🕌" if message["role"] == "model" else "👦"
        sender_name = teacher if message["role"] == "model" else st.session_state.username
        with st.chat_message(message["role"], avatar=avatar_icon):
            st.markdown(f"**{sender_name}**:\n{message['text']}")

    # Input User
    if user_input := st.chat_input("Tulis jawabanmu di sini..."):
        with st.chat_message("user", avatar="👦"):
            st.markdown(f"**{st.session_state.username}**:\n{user_input}")
        st.session_state.messages.append({"role": "user", "text": user_input})
        
        # Menyusun Format History Percakapan sesuai SDK Baru
        contents_history = []
        for msg in st.session_state.messages:
            contents_history.append(
                types.Content(
                    role=msg["role"],
                    parts=[types.Part.from_text(text=msg["text"])]
                )
            )
        
        # Eksekusi API dengan Mekanisme Anti-Error 503 (Retry & Backup Model)
        with st.spinner(f"✨ {teacher} sedang membaca jawabanmu..."):
            reply_text = ""
            models_to_try = ['gemini-2.5-flash', 'gemini-1.5-flash'] # Cadangan jika model utama sibuk
            
            for current_model in models_to_try:
                success = False
                for attempt in range(3): # Coba ulang hingga 3 kali jika server drop sementara
                    try:
                        response = client.models.generate_content(
                            model=current_model,
                            contents=contents_history,
                            config=types.GenerateContentConfig(
                                system_instruction=st.session_state.system_instruction,
                                temperature=0.6,
                            )
                        )
                        reply_text = response.text
                        success = True
                        break # Keluar dari loop attempt jika berhasil
                    except Exception as e:
                        if "503" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                            time.sleep(1.5) # Tunggu sebentar sebelum mencoba lagi
                            continue
                        else:
                            reply_text = f"Maaf ya, ada kendala sistem: {e}"
                            break
                
                if success:
                    break # Keluar dari loop model jika sudah berhasil dapat respon
            
            # Jika semua metode di atas gagal karena server Google down total
            if not reply_text:
                reply_text = "Wah, server Google Studio AI sedang sangat ramai sekali, shalih/shalihah. Mari coba kirim pesanmu sekali lagi ya! ✨"

            # Tampilkan respon akhir ke layar
            with st.chat_message("assistant", avatar="🕌"):
                st.markdown(f"**{teacher}**:\n{reply_text}")
            st.session_state.messages.append({"role": "model", "text": reply_text})