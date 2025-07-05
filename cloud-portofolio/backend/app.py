from flask import Flask, request, jsonify, render_template
import psycopg2
import os

app = Flask(__name__)

# DATABASE URL (langsung tempel dari Railway)
DATABASE_URL = "postgresql://postgres:zWbDFtVGonwIOAcCbyZZoYccNPGTFjRz@postgres.railway.internal:5432/railway"

# Koneksi ke database
def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"[ERROR] Gagal konek DB: {e}")
        return None

# Landing page (jika pakai render_template)
@app.route("/")
def index():
    return "API Backend aktif 🔥"

# Endpoint nerima POST dari frontend
@app.route("/contact", methods=["POST"])
def contact():
    email = request.form.get("email")
    message = request.form.get("message")

    if not email or not message:
        return jsonify({"error": "Data kosong!"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Koneksi DB gagal"}), 500

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    email TEXT NOT NULL,
                    message TEXT NOT NULL
                );
            """)
            conn.commit()

            cursor.execute("INSERT INTO messages (email, message) VALUES (%s, %s);", (email, message))
            conn.commit()

        return jsonify({"success": "Pesan berhasil disimpan ✅"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
