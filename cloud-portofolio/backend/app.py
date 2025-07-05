from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Backend Flask Aktif! 🚀"

@app.route("/contact", methods=["POST"])
def contact():
    try:
        data = request.form  # Ambil data dari form
        print("Isi form:", dict(data), flush=True)

        email = data.get("email", "[no email]")
        message = data.get("message", "[no message]")

        print(f"Pesan masuk dari: {email} - {message}", flush=True)

        return "Pesan berhasil dikirim!"
    except Exception as e:
        print("Error:", str(e), flush=True)
        return "Terjadi kesalahan pada server.", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)