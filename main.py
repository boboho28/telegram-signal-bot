import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Ambil token dan ID dari Environment Variables di Render
BOT_TOKEN = os.environ.get("7782307572:AAGDHOqlEHgU6T56ug0S1TAFLRrHDuH7TrU")
CHAT_ID = os.environ.get("-4830639173")

@app.route("/webhook", methods=["POST"])
def webhook():
    if not BOT_TOKEN or not CHAT_ID:
        return jsonify({"status": "error", "message": "BOT_TOKEN and CHAT_ID must be set"}), 500

    try:
        data = request.get_json()
        print("Received data:", data) # Untuk debugging di log Render

        # Ambil data dari JSON yang masuk
        symbol = data.get("symbol", "N/A")
        price = data.get("price", "N/A")
        direction = data.get("direction", "N/A")
        timeframe = data.get("timeframe", "N/A")
        note = data.get("note", "N/A")
        image = data.get("image", "") # URL gambar

        message = (f"📡 **Sinyal Baru!**\n\n"
                   f"*{symbol}*\n"
                   f"💰 *Harga:* `{price}`\n"
                   f"📈 *Arah:* `{direction}`\n"
                   f"🕐 *Timeframe:* `{timeframe}`\n"
                   f"🧠 *Catatan:* {note}")

        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }

        # Kirim pesan teks ke Telegram
        response = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json=payload)
        response.raise_for_status() # Akan error jika pengiriman gagal

        # Jika ada URL gambar, kirim juga gambarnya
        if image:
            image_payload = {
                "chat_id": CHAT_ID,
                "photo": image,
                "caption": f"Chart untuk {symbol}"
            }
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto", json=image_payload)

        return jsonify({"status": "ok", "message": "Alert sent"}), 200

    except Exception as e:
        print("Error:", str(e)) # Untuk debugging di log Render
        return jsonify({"status": "error", "message": str(e)}), 500

# Rute dasar untuk memeriksa apakah server berjalan
@app.route("/")
def index():
    return "Bot is alive!", 200

if __name__ == "__main__":
    # Port akan diatur oleh Render secara otomatis
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)