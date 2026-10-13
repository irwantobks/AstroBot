import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="AstroBot AI", page_icon="🤖", layout="wide")

# --- UI styling ---
st.markdown("""
<style>
.stApp { background: #f4f8ff; }
[data-testid="stSidebar"] { background: linear-gradient(180deg,#063b80,#0757ad); }
[data-testid="stSidebar"] * { color: white !important; }
.hero {
  background: linear-gradient(120deg,#0757ad,#65b8ff);
  color: white; padding: 24px; border-radius: 18px; margin-bottom: 18px;
}
.info-card {
  background: white; border: 1px solid #d7e7ff; border-radius: 15px;
  padding: 16px; margin-bottom: 12px;
}
.small-muted { color: #55708f; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("# 🤖 AstroBot")
    st.markdown("### AI Assistant")
    st.write("Solusi cepat untuk masalah internet dan WiFi Anda.")
    page = st.radio("Menu", ["Chat", "Panduan", "Paket Internet", "Troubleshooting", "Tentang"])
    st.markdown("---")
    st.markdown("### Astro.Net")
    st.caption("Internet untuk Masa Depan")

st.markdown("""
<div class="hero">
  <h1>🤖 AstroBot</h1>
  <p>Asisten AI layanan internet dan WiFi</p>
  <strong>Ajukan pertanyaan dengan bahasa sehari-hari.</strong>
</div>
""", unsafe_allow_html=True)

SYSTEM_PROMPT = """
Anda adalah AstroBot, asisten layanan internet dan WiFi.
Jawablah dalam bahasa Indonesia yang sopan, jelas, ramah, dan mudah dipahami.
Bantu pengguna memahami gangguan internet, WiFi, router, dan troubleshooting dasar.
Jangan mengarang paket, tagihan, status jaringan, atau data pelanggan.
Jika informasi tidak tersedia, jelaskan keterbatasan dan sarankan menghubungi petugas.
Untuk tindakan teknis berisiko, sarankan bantuan teknisi.
"""

MODEL_NAME = "gemini-2.5-flash"
TEMPERATURE = 0.4
MAX_OUTPUT_TOKENS = 700

def get_client():
    key = st.secrets.get("GEMINI_API_KEY", "")
    if not key:
        return None
    return genai.Client(api_key=key)

if page == "Chat":
    left, right = st.columns([2.2, 1])
    with left:
        st.subheader("💬 Chat dengan AstroBot")
        st.caption("Contoh: Kenapa WiFi tersambung tetapi tidak ada internet?")
        if "messages" not in st.session_state:
            st.session_state.messages = []
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
                st.markdown(msg["content"])

        prompt = st.chat_input("Tanyakan sesuatu kepada AstroBot...")
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)
            client = get_client()
            with st.chat_message("assistant", avatar="🤖"):
                if client is None:
                    answer = ("API key belum diatur. Buat file "
                              "`.streamlit/secrets.toml` dan isi `GEMINI_API_KEY` "
                              "sesuai petunjuk README.md.")
                    st.info(answer)
                else:
                    history = []
                    for item in st.session_state.messages[-12:]:
                        history.append({
                            "role": "user" if item["role"] == "user" else "model",
                            "parts": [{"text": item["content"]}]
                        })
                    try:
                        with st.spinner("AstroBot sedang berpikir..."):
                            response = client.models.generate_content(
                                model=MODEL_NAME,
                                contents=history,
                                config=types.GenerateContentConfig(
                                    system_instruction=SYSTEM_PROMPT,
                                    temperature=TEMPERATURE,
                                    max_output_tokens=MAX_OUTPUT_TOKENS
                                )
                            )
                        answer = response.text or "Maaf, model belum menghasilkan jawaban."
                        st.markdown(answer)
                    except Exception as exc:
                        answer = "Maaf, AI belum dapat menjawab. Periksa koneksi, API key, nama model, dan kuota API."
                        st.error(answer)
                        st.caption(f"Detail teknis: {exc}")
                st.session_state.messages.append({"role": "assistant", "content": answer})

    with right:
        st.markdown('<div class="info-card"><h3>👋 Hai, saya AstroBot!</h3><p>Asisten untuk pertanyaan internet, WiFi, dan troubleshooting dasar.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="info-card"><h4>💡 Contoh pertanyaan</h4></div>', unsafe_allow_html=True)
        suggestions = [
            "Kenapa WiFi tersambung tetapi tidak ada internet?",
            "Apa perbedaan modem, router, dan access point?",
            "Apa yang dilakukan jika lampu LOS merah?",
            "Bagaimana memperkuat sinyal WiFi?"
        ]
        for suggestion in suggestions:
            if st.button(suggestion, use_container_width=True):
                st.session_state.pending_question = suggestion
                st.info("Silakan salin pertanyaan ini ke kolom chat di bawah.")
        st.markdown('<div class="info-card"><h4>⚙️ Konfigurasi AI</h4><p>Model: Gemini 2.5 Flash<br>Temperature: 0.4<br>Max output tokens: 700</p></div>', unsafe_allow_html=True)
        st.caption("AstroBot tidak terhubung ke data pelanggan atau status jaringan real-time.")

elif page == "Panduan":
    st.subheader("📘 Panduan dasar")
    st.markdown("""
    - Periksa apakah modem/router mendapat daya.
    - Perhatikan lampu indikator PON dan LOS.
    - Coba matikan router selama 30–60 detik, lalu hidupkan kembali.
    - Uji dengan perangkat lain.
    - Jika LOS merah atau gangguan tetap terjadi, hubungi teknisi.
    """)
elif page == "Paket Internet":
    st.subheader("📶 Informasi paket internet")
    st.info("Daftar paket dan harga resmi belum dihubungkan ke database. Hubungi petugas Astro.Net untuk informasi terbaru.")
elif page == "Troubleshooting":
    st.subheader("🛠️ Troubleshooting")
    with st.expander("WiFi tersambung, tetapi tidak ada internet"):
        st.write("Periksa lampu modem, coba perangkat lain, restart router, dan hubungi penyedia layanan jika tetap bermasalah.")
    with st.expander("Lampu LOS menyala merah"):
        st.write("Kemungkinan ada gangguan jalur fiber optik. Jangan melihat langsung ke ujung kabel fiber. Hubungi teknisi.")
    with st.expander("Sinyal WiFi lemah"):
        st.write("Letakkan router di tempat terbuka, agak tinggi, dan jauh dari penghalang atau perangkat yang menimbulkan interferensi.")
else:
    st.subheader("ℹ️ Tentang AstroBot")
    st.write("AstroBot adalah prototipe chatbot berbasis Large Language Model (LLM) untuk membantu pertanyaan umum tentang internet dan WiFi.")
    st.write("Model AI digunakan untuk memproses bahasa alami dan menghasilkan jawaban kontekstual.")
    st.warning("Jawaban AI dapat keliru. Jangan gunakan chatbot ini sebagai sumber status jaringan atau tagihan pelanggan tanpa integrasi data resmi.")
