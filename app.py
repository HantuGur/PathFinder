"""
PathFinder — AI Career Direction for SMA/SMK Students
======================================================
Flask app dengan fitur:
- Quiz minat & kepribadian (8 pertanyaan)
- Rekomendasi jurusan berdasarkan skor
- Info prospek kerja & gaji
- Roadmap karir step-by-step
- Chat konsultan karir AI
"""

from flask import Flask, render_template, request, jsonify
import os, json, requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_BASE_URL  = "https://litellm.koboi2026.biz.id/v1"
CHAT_ENDPOINT = f"{API_BASE_URL}/chat/completions"
MODEL_NAME    = "gpt-4o"


def get_api_key():
    key = os.environ.get("LITELLM_API_KEY")
    if not key:
        raise Exception("LITELLM_API_KEY tidak ditemukan di .env")
    return key


def load_career_data():
    path = os.path.join(os.path.dirname(__file__), "data", "career.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def call_ai(messages, max_tokens=1500):
    resp = requests.post(
        CHAT_ENDPOINT,
        headers={"Authorization": f"Bearer {get_api_key()}", "Content-Type": "application/json"},
        json={"model": MODEL_NAME, "max_tokens": max_tokens, "messages": messages},
        timeout=45
    )
    if resp.status_code != 200:
        raise Exception(f"API Error {resp.status_code}: {resp.text[:200]}")
    return resp.json()["choices"][0]["message"]["content"]


def clean_json(raw):
    c = raw.strip()
    if "```" in c:
        parts = c.split("```")
        c = parts[1] if len(parts) > 1 else parts[0]
        if c.startswith("json"):
            c = c[4:]
    return c.strip()


# ── ROUTES ──────────────────────────────

@app.route("/")
def index():
    data = load_career_data()
    return render_template("index.html", pertanyaan=data["pertanyaan_quiz"])


# ── API: PROSES HASIL QUIZ ───────────────

@app.route("/api/quiz-result", methods=["POST"])
def quiz_result():
    """Hitung skor quiz dan kembalikan top 3 jurusan rekomendasi"""
    body   = request.get_json()
    jawaban = body.get("jawaban", [])  # list of {pertanyaan_id, opsi_index}
    nama   = body.get("nama", "Kamu")

    data   = load_career_data()
    soal   = data["pertanyaan_quiz"]
    jurusan_db = data["jurusan"]

    # Hitung total skor per jurusan
    skor_total = {k: 0 for k in jurusan_db.keys()}

    for jawab in jawaban:
        pid  = jawab.get("pertanyaan_id")
        oidx = jawab.get("opsi_index")
        q    = next((s for s in soal if s["id"] == pid), None)
        if not q or oidx is None or oidx >= len(q["opsi"]):
            continue
        opsi_skor = q["opsi"][oidx].get("skor", {})
        for key, val in opsi_skor.items():
            if key in skor_total:
                skor_total[key] += val

    # Sort dan ambil top 3
    ranked = sorted(skor_total.items(), key=lambda x: x[1], reverse=True)
    top3   = [k for k, v in ranked[:3] if v > 0]

    if not top3:
        top3 = list(jurusan_db.keys())[:3]

    hasil = []
    for key in top3:
        j = jurusan_db[key]
        hasil.append({
            "key": key,
            "nama": j["nama"],
            "emoji": j["emoji"],
            "warna": j["warna"],
            "fakultas": j["fakultas"],
            "deskripsi": j["deskripsi"],
            "cocok_untuk": j["cocok_untuk"],
            "prospek_kerja": j["prospek_kerja"][:3],
            "universitas_top": j["universitas_top"],
            "roadmap": j["roadmap"],
            "skill_utama": j["skill_utama"],
            "rata_gaji_awal": j["rata_gaji_awal"],
            "growth_score": j["growth_score"],
            "happiness_score": j["happiness_score"],
            "skor": skor_total[key],
            "skor_persen": min(100, int(skor_total[key] / 24 * 100)),
        })

    # AI analisis personal
    try:
        jurusan_str = ", ".join([h["nama"] for h in hasil])
        system = """Kamu adalah konselor karir terbaik untuk pelajar SMA/SMK Indonesia.
Beri analisis singkat dan MOTIVASI yang personal berdasarkan hasil quiz.
Gaya bicara: ramah, supportif, seperti kakak senior yang paham dunia kerja.
Gunakan Bahasa Indonesia yang gaul tapi tetap informatif.

Balas dengan JSON:
{
  "analisis": "2-3 kalimat analisis kepribadian berdasarkan pilihan quiz",
  "motivasi": "1 kalimat motivasi yang personal dan powerful",
  "warning": "1 hal yang perlu diperhatikan dari kombinasi jurusan ini"
}"""

        user_msg = f"""Nama: {nama}
Rekomendasi jurusan (urutan prioritas): {jurusan_str}
Skor masing-masing: {', '.join([f"{h['nama']} ({h['skor']} poin)" for h in hasil])}"""

        raw = call_ai([{"role":"system","content":system},{"role":"user","content":user_msg}])
        ai  = json.loads(clean_json(raw))
    except Exception:
        ai = {
            "analisis": f"Berdasarkan pilihanmu, {nama} memiliki kombinasi minat yang unik dan multi-talented!",
            "motivasi": "Jurusan terbaik adalah yang kamu jalani dengan passion penuh.",
            "warning": "Pastikan kamu riset lebih dalam sebelum memutuskan."
        }

    return jsonify({"success": True, "hasil": hasil, "ai": ai, "nama": nama})


# ── API: DETAIL JURUSAN ──────────────────

@app.route("/api/jurusan/<key>", methods=["GET"])
def detail_jurusan(key):
    data = load_career_data()
    j    = data["jurusan"].get(key)
    if not j:
        return jsonify({"error": "Jurusan tidak ditemukan"}), 404
    return jsonify({"success": True, "data": j, "key": key})


# ── API: CHAT KONSULTAN ──────────────────

@app.route("/api/chat", methods=["POST"])
def chat():
    body    = request.get_json()
    history = body.get("history", [])
    pesan   = body.get("pesan", "")
    konteks = body.get("konteks", "")
    nama    = body.get("nama", "")

    system = f"""Kamu adalah PathFinder AI — konselor karir dan jurusan kuliah untuk pelajar SMA/SMK Indonesia.

Profil user: {nama} {('— ' + konteks) if konteks else ''}

Gaya bicara:
- Seperti kakak senior yang peduli dan supportif
- Bahasa Indonesia, bisa campur sedikit English kalau relevan
- Berikan info KONKRET: nama jurusan, nama universitas, estimasi gaji, nama profesi
- Selalu encourage dan positif, tapi jujur tentang tantangan
- Kalau ditanya hal di luar karir/pendidikan, arahkan kembali ke topik

Fokus area: jurusan kuliah, karir, skill yang perlu dipelajari, universitas Indonesia, beasiswa."""

    msgs = [{"role":"system","content":system}] + history[-10:] + [{"role":"user","content":pesan}]

    try:
        reply = call_ai(msgs, max_tokens=700)
        return jsonify({"success": True, "reply": reply})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    print("=" * 55)
    print("  🧭 PathFinder — AI Career Direction")
    print("  Buka browser: http://localhost:5003")
    print("=" * 55)
    app.run(debug=True, port=5003)
