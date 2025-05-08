from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import pdfplumber
import tempfile

app = Flask(__name__)
CORS(app)  # ✅ This enables CORS for all routes and origins

@app.route("/extract", methods=["POST"])
def extract_text():
    try:
        data = request.get_json(force=True)
        pdf_url = data.get("url")

        if not pdf_url:
            return jsonify({"error": "Missing URL"}), 400

        res = requests.get(pdf_url)
        res.raise_for_status()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(res.content)
            tmp.flush()
            with pdfplumber.open(tmp.name) as pdf:
                text = "\n".join(p.extract_text() or "" for p in pdf.pages)

        return jsonify({"text": text.strip()}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)