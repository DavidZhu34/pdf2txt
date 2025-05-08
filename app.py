from flask import Flask, request, jsonify
import requests
import pdfplumber
import tempfile

app = Flask(__name__)

@app.route("/extract", methods=["POST"])
def extract_text():
    data = request.get_json()
    pdf_url = data.get("url")
    if not pdf_url:
        return jsonify({"error": "Missing URL"}), 400

    try:
        res = requests.get(pdf_url)
        res.raise_for_status()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(res.content)
            tmp.flush()
            with pdfplumber.open(tmp.name) as pdf:
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        return jsonify({"text": text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)