from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)  # Aktifkan CORS biar frontend Netlify bisa akses backend ini

# URL DB dari Railway
DATABASE_URL = "postgresql://postgres:zWbDFtVGonwIOAcCbyZZoYccNPGTFjRz@postgres.railway.internal:5432/railway"

# Fungsi konek DB
def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"[ERROR] Gagal konek DB: {e}")
        return None

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "🔥 Backend Flask is running!"})

# Endpoint POST buat form
@app.route("/contact", methods=["POST"])
def contact():
    email = request.form.get("email")
    message = request.form.get("message")

    if not email or not message:
        return jsonify({"error": "Email dan pesan wajib diisi"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Gagal konek ke database"}), 500

    try:
        with conn.cursor() as cur:
            # Buat tabel kalau belum ada
            cur.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    email TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)
            conn.commit()

            # Simpan data
            cur.execute("INSERT INTO messages (email, message) VALUES (%s, %s);", (email, message))
            conn.commit()

        return jsonify({"success": True, "message": "Pesan berhasil disimpan!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
