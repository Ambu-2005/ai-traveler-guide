import os
import tempfile
import base64
import traceback
from pathlib import Path

import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from werkzeug.exceptions import HTTPException

load_dotenv(Path(__file__).with_name(".env"))

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
FALLBACK_MODELS = [DEFAULT_MODEL, "gemini-3.5-flash-lite", "gemini-2.5-pro"]

PROMPTS = {
    "Summary": """
You are a professional tourist guide.
Provide a high-level overview of "{place}" in {language}.

Focus on:
- The historical significance
- Why the place is famous
- Key architectural or cultural highlights

Keep the explanation concise, engaging, and easy to follow.
Avoid excessive details and dates.
Limit the response to around 200 words.

Respond ONLY in {language}.
""",

    "Detailed": """
You are a professional tourist guide.
Provide a detailed and immersive explanation of "{place}" in {language}.

Cover:
- Historical background and timeline
- Architectural design and unique features
- Cultural importance and notable events
- Interesting facts and visitor insights

Explain concepts clearly and in a storytelling manner.
Include relevant details and examples to create a rich experience.
Limit the response to around 400 words.

Respond ONLY in {language}.
"""
}

def get_google_api_key():
    return os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

def get_murf_api_key():
    return os.getenv("MURF_API_KEY")

def get_gemini_client():
    api_key = get_google_api_key()
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

def generate_speech(text, voice_id, locale):
    murf_key = get_murf_api_key()
    if not murf_key:
        raise RuntimeError("MURF_API_KEY environment variable is not configured on the server.")

    temp_audio = tempfile.NamedTemporaryFile(
        suffix=".mp3",
        delete=False
    )
    temp_audio.close()

    try:
        url = "https://global.api.murf.ai/v1/speech/stream"
        headers = {
            "api-key": murf_key,
            "Content-Type": "application/json"
        }
        data = {
            "voice_id": voice_id,
            "text": text,
            "locale": locale,
            "model": "FALCON",
            "format": "MP3",
            "sampleRate": 24000,
            "channelType": "MONO"
        }

        response = requests.post(url, headers=headers, json=data, timeout=60)

        if response.status_code == 200:
            with open(temp_audio.name, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print("Audio streaming completed")
            return temp_audio.name
        else:
            print(f"Murf API Error: {response.status_code} - {response.text}")
            raise RuntimeError(f"Murf API error ({response.status_code}): {response.text}")
    except Exception:
        # Clean up temp file on failure
        if os.path.exists(temp_audio.name):
            try:
                os.remove(temp_audio.name)
            except Exception:
                pass
        raise

def generate_description(place, answer_type, language):
    client = get_gemini_client()
    if not client:
        raise RuntimeError("GOOGLE_API_KEY environment variable is not configured on the server.")

    prompt_template = PROMPTS.get(answer_type, PROMPTS["Summary"])
    prompt = prompt_template.format(place=place, language=language)

    # De-duplicate while preserving order
    models_to_try = []
    for m in FALLBACK_MODELS:
        if m and m not in models_to_try:
            models_to_try.append(m)

    last_error = None
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            if response and response.text:
                return response.text
        except Exception as e:
            print(f"Gemini generation with {model_name} failed: {e}")
            last_error = e

    raise RuntimeError(f"Gemini generation failed on all attempted models ({', '.join(models_to_try)}): {last_error}")

@app.errorhandler(Exception)
def handle_exception(e):
    traceback.print_exc()
    if isinstance(e, HTTPException):
        return jsonify({"error": e.description}), e.code
    return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "message": "AI Traveler Guider Backend is running",
        "gemini_configured": bool(get_google_api_key()),
        "murf_configured": bool(get_murf_api_key()),
        "gemini_model": DEFAULT_MODEL
    })

@app.route("/generate-audio-guide", methods=["POST"])
def generate_audio_guide():
    data = request.get_json(silent=True) or {}
    place = data.get("place", "")
    answer_type = data.get("answerType", "Summary")
    language = data.get("language", "English")
    voice_id = data.get("voiceId", "Matthew")
    locale = data.get("locale", "en-US")

    if not place:
        return jsonify({"error": "Destination 'place' is required."}), 400

    audio_file_path = None
    try:
        text_description = generate_description(place, answer_type, language)
        audio_file_path = generate_speech(text_description, voice_id, locale)

        with open(audio_file_path, "rb") as f:
            audio_bytes = f.read()

        encoded_audio = base64.b64encode(audio_bytes).decode("utf-8")

        return jsonify({
            "description": text_description,
            "audioBase64": encoded_audio
        })
    except Exception as e:
        print(f"Error in generate_audio_guide: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if audio_file_path and os.path.exists(audio_file_path):
            try:
                os.remove(audio_file_path)
            except Exception:
                pass

if __name__ == "__main__":
    app.run(
        host="0.0.0.0", 
        port=int(os.environ.get("PORT", 5000)), 
        debug=False
    )

