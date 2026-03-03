<div align="center">

# 🧭 PathFinder

### AI Career Direction for Indonesian High School Students

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![GPT-4o](https://img.shields.io/badge/AI-GPT--4o-10a37f?style=flat-square&logo=openai&logoColor=white)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)]()

**Banyak anak SMA/SMK bingung mau pilih jurusan apa. PathFinder hadir untuk jawab itu — dengan AI.**

[Fitur](#-fitur) · [Instalasi](#-instalasi) · [Cara Pakai](#-cara-pakai) · [Tech Stack](#-tech-stack)

</div>

---

## 🎯 Tentang PathFinder

PathFinder adalah web app berbasis AI yang membantu pelajar SMA/SMK Indonesia menemukan jurusan kuliah yang paling sesuai dengan minat dan kepribadian mereka.

Bukan sekadar kuis biasa — PathFinder menggunakan GPT-4o untuk menganalisis pola jawaban dan memberikan rekomendasi yang personal, lengkap dengan data prospek kerja, estimasi gaji, dan roadmap karir nyata.

---

## ✨ Fitur

### 🎯 Tes Minat & Kepribadian
- 8 pertanyaan yang dirancang khusus untuk profiling karir
- Auto-advance setelah memilih jawaban — smooth kayak Duolingo
- Bisa kembali ke soal sebelumnya
- Progress bar animasi real-time

### 📊 Rekomendasi Jurusan AI
- Top 3 jurusan berdasarkan analisis skor
- Analisis kepribadian personal dari GPT-4o
- Motivasi dan peringatan yang relevan
- Match score per jurusan dalam persentase

### 💼 Info Karir Lengkap (per Jurusan)
- Prospek kerja dengan estimasi gaji junior & senior
- Tingkat demand di industri
- Roadmap karir step-by-step dari tahun 1 hingga setelah lulus
- Skill utama yang perlu dikuasai
- Universitas top di Indonesia

### 🔍 Explore Semua Jurusan
- Grid 6 jurusan dengan growth & happiness score
- Modal detail lengkap per jurusan
- Bar chart animasi

### 💬 Chat Konsultan AI
- Tanya apapun soal jurusan, kampus, atau karir
- Konteks otomatis dari hasil quiz
- Quick chips untuk pertanyaan populer

---

## 📚 Jurusan yang Tersedia

| Jurusan | Gaji Awal | Growth Score |
|---------|-----------|--------------|
| 💻 Teknik Informatika | ~Rp 11 jt | 95/100 |
| 🎨 Desain Komunikasi Visual | ~Rp 9 jt | 80/100 |
| 🧠 Psikologi | ~Rp 8 jt | 75/100 |
| 📈 Manajemen Bisnis | ~Rp 9 jt | 82/100 |
| ⚕️ Kedokteran | ~Rp 14 jt | 90/100 |
| ⚖️ Ilmu Hukum | ~Rp 9 jt | 72/100 |

---

## 🚀 Instalasi

### Prerequisites
- Python 3.8+
- API Key LiteLLM atau OpenAI

### Setup

```bash
# 1. Clone repository
git clone https://github.com/username/pathfinder.git
cd pathfinder

# 2. Install dependencies
pip install -r requirements.txt

# 3. Buat file .env
echo "LITELLM_API_KEY=api-key-kamu" > .env

# 4. Jalankan server
python app.py
```

Buka browser: **http://localhost:5003**

### Windows (PowerShell)

```powershell
cd "C:\path\to\pathfinder"
pip install -r requirements.txt
python app.py
```

---

## 📁 Struktur Project

```
pathfinder/
├── app.py                  # Flask server & semua API endpoint
├── requirements.txt        # Dependencies
├── .env                    # API key (jangan di-commit!)
├── data/
│   └── career.json         # Database jurusan, quiz, prospek kerja
└── templates/
    └── index.html          # Single-page app (full animated)
```

---

## 🔌 API Endpoints

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `GET` | `/` | Landing page |
| `POST` | `/api/quiz-result` | Proses hasil quiz & rekomendasi AI |
| `GET` | `/api/jurusan/<key>` | Detail jurusan spesifik |
| `POST` | `/api/chat` | Chat dengan konsultan AI |

### Contoh Request `/api/quiz-result`

```json
{
  "nama": "Budi",
  "jawaban": [
    { "pertanyaan_id": 1, "opsi_index": 0 },
    { "pertanyaan_id": 2, "opsi_index": 2 }
  ]
}
```

---

## 🛠 Tech Stack

- **Backend** — Python Flask
- **AI** — GPT-4o via LiteLLM
- **Frontend** — Vanilla HTML/CSS/JS (no framework)
- **Font** — Bricolage Grotesque + DM Sans
- **Data** — JSON (career.json)

---

## 🎨 Design Highlights

- Clean & modern — terinspirasi Notion/Linear
- Floating card animations di hero section
- Auto-advance quiz dengan smooth transition
- Card expand/collapse untuk detail jurusan
- Responsive untuk mobile

---

## 📝 License

[MIT](LICENSE) — bebas dipakai dan dimodifikasi.

---

<div align="center">

Dibuat untuk pelajar Indonesia yang masih bingung mau jadi apa 🇮🇩

**[⬆ Kembali ke atas](#-pathfinder)**

</div>
