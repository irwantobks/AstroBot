# AstroBot AI

AstroBot adalah prototipe chatbot AI untuk pertanyaan umum tentang layanan internet, WiFi, dan troubleshooting dasar. Antarmuka dibangun dengan Streamlit dan jawaban dibuat oleh model LLM melalui Google Gen AI API.

## Fitur
- UI web berwarna biru dengan menu Chat, Panduan, Paket Internet, Troubleshooting, dan Tentang.
- Percakapan berbahasa Indonesia dengan riwayat chat selama sesi.
- Konfigurasi `temperature`, `max_output_tokens`, dan system instruction.
- Pesan kesalahan jika API tidak dapat diakses.
- Tidak menyimpan API key di source code.

## Menjalankan di Windows
1. Instal Python 3.10 atau lebih baru.
2. Buka Command Prompt di folder proyek.
3. Buat dan aktifkan virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
4. Instal dependensi:
   ```bash
   pip install -r requirements.txt
   ```
5. Buat file `.streamlit/secrets.toml` dan isi:
   ```toml
   GEMINI_API_KEY = "API_KEY_ANDA"
   ```
6. Jalankan:
   ```bash
   streamlit run app.py
   ```
7. Buka alamat lokal yang muncul, biasanya `http://localhost:8501`.

Dapatkan API key melalui Google AI Studio: https://aistudio.google.com/
Periksa ketersediaan model, kuota, dan ketentuan API pada akun Anda. Jangan pernah mengunggah `secrets.toml` yang berisi API key ke GitHub.

## Konfigurasi parameter
- `MODEL_NAME`: nama model yang digunakan. Ubah jika model contoh tidak tersedia di akun.
- `TEMPERATURE = 0.4`: nilai relatif rendah untuk jawaban yang lebih terarah.
- `MAX_OUTPUT_TOKENS = 700`: batas panjang keluaran.
- `SYSTEM_PROMPT`: peran dan batasan jawaban AstroBot.

## Mengunggah ke GitHub
1. Buat akun di https://github.com/ jika belum ada.
2. Buat repository baru bernama `AstroBot`.
3. Pastikan `secrets.toml` tidak ikut diunggah. File tersebut sudah dimasukkan ke `.gitignore`.
4. Unggah `app.py`, `requirements.txt`, `README.md`, `.gitignore`, dan `secrets.toml.example` melalui tombol **Add file → Upload files**, lalu **Commit changes**.
5. Salin URL repository, misalnya `https://github.com/USERNAME/AstroBot`, dan kirimkan kepada pengajar. Ganti `USERNAME` dengan nama akun GitHub Anda.

## Batasan
AstroBot adalah prototipe edukasi. Ia tidak terhubung ke data pelanggan, tagihan, paket resmi, atau pemantauan jaringan real-time. Harga dan status layanan tidak boleh dianggap sebagai data resmi. Model AI dapat memberikan jawaban yang keliru, sehingga respons perlu diuji.
