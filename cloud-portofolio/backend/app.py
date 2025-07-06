from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Gunakan variabel env atau fallback default
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:zWbDFtVGonwIOAcCbyZZoYccNPGTFjRz@shortline.proxy.rlwy.net:46773/railway")

try:
    conn = psycopg2.connect(DATABASE_URL)
except Exception as e:
    print("❌ Gagal konek DB:", e)
    conn = None

@app.route("/")
def home():
    return jsonify({"message": "🔥 Backend Flask is running!"})

@app.route("/contact", methods=["POST"])
def contact():
    if not conn:
        return jsonify({"error": "DB connection error"}), 500

    email = request.form.get("email")
    message = request.form.get("message")

    if not email or not message:
        return jsonify({"error": "Email dan pesan wajib diisi"}), 400

    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                email TEXT,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cur.execute("INSERT INTO messages (email, message) VALUES (%s, %s)", (email, message))
        conn.commit()
        cur.close()
        return jsonify({"success": True, "message": "Pesan berhasil dikirim!"})
    except Exception as e:
        print("❌ Error insert:", e)
        return jsonify({"error": "Gagal menyimpan pesan"}), 500

@app.route("/messages", methods=["GET"])
def get_messages():
    try:
        cur = conn.cursor()
        cur.execute("SELECT email, message, created_at FROM messages ORDER BY created_at DESC")
        rows = cur.fetchall()
        cur.close()
        return jsonify([
            {"email": row[0], "message": row[1], "created_at": row[2].isoformat()}
            for row in rows
        ])
    except Exception as e:
        print("❌ Error fetch:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return jsonify({"success": True, "message": "File uploaded!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/files", methods=["GET"])
def list_files():
    try:
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        valid_files = []

        for f in files:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f)
            if os.path.isfile(file_path):
                valid_files.append(f)

        return jsonify(valid_files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
