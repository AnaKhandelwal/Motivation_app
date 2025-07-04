from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_KEY = "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"

@app.route("/generate", methods=["POST"])
def generate_motivation():
    data = request.get_json()
    mood = data.get("mood", "")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "You are a motivational coach who always replies with a short quote."
            },
            {
                "role": "user",
                "content": f"I'm feeling {mood}. Give me a motivational quote."
            }
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        return jsonify({"error": response.text}), response.status_code

    return jsonify(response.json())

if __name__ == "__main__":
    app.run(port=5000)
