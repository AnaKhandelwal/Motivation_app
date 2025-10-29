from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("API_KEY")

@app.route("/generate", methods=["POST"])
def generate_motivation():
    data = request.get_json()
    mood = data.get("mood", "")

    if not API_KEY:
        return jsonify({"error": "API key not set"}), 500

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

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        quote = result["choices"][0]["message"]["content"]
        return jsonify({"quote": quote})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(port=5000)
