# AI Traveler Guider

An AI-powered travel guide application that generates rich destination descriptions and realistic streaming audio guides using the **Google Gemini (GenAI)** and **Murf AI** APIs.

---

## Features

- **AI Destination Guides**: Generates concise summaries or detailed storytelling descriptions of world-famous travel spots using Google Gemini.
- **Realistic Voice Narration**: Streams lifelike audio narration powered by Murf AI's FALCON model.
- **Multilingual Support**: Supports English, Hindi, Tamil, and Telugu with tailored male and female voices.
- **Interactive Web Interface**: Responsive destination cards, voice/style selectors, and integrated audio player with expandable text transcripts.

---

## Project Structure

```text
AI_traveler_guider/
├── Backend/
│   ├── app.py              # Flask server handling AI generation and TTS streaming
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example        # Environment variable template
│   └── .env                # Local secrets (ignored by Git)
├── Frontend/
│   ├── index.html          # UI markup and Tailwind styling
│   └── index.js            # Client logic and API integration
├── .gitignore              # Git ignore rules
└── README.md               # Project documentation
```

---

## Prerequisites

- **Python 3.10+** (tested on Python 3.14)
- **Google GenAI API Key** ([Google AI Studio](https://aistudio.google.com/))
- **Murf AI API Key** ([Murf.ai](https://murf.ai/api))

---

## Quick Start Guide

### 1. Backend Setup

Open a terminal (PowerShell on Windows) in the `Backend` directory:

```powershell
cd Backend
```

#### Create Virtual Environment & Install Dependencies

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

#### Configure Environment Variables

Create your local `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

Open `Backend/.env` and insert your API keys:

```env
MURF_API_KEY=your_murf_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

> **Note:** `.env` is included in `.gitignore` and should never be committed to source control.

#### Start the Backend Server

```powershell
python app.py
```

The Flask backend runs by default on **`http://127.0.0.1:5000`**.

---

### 2. Frontend Setup

In a separate terminal window from the workspace root:

#### Option A: Run a Local Web Server (Recommended)

```powershell
python -m http.server 8000 --directory Frontend
```

Open your browser and navigate to:
**[http://localhost:8000/index.html](http://localhost:8000/index.html)**

#### Option B: Direct Browser Open

You can also directly open `Frontend/index.html` in any modern web browser:

```powershell
Start-Process Frontend\index.html
```

---

## API Endpoints

### `GET /`
Health check endpoint.
- **Response**: `{"status": "ok", "message": "AI Traveler Guider Backend is running"}`

### `POST /generate-audio-guide`
Generates the text description and audio narration for a chosen destination.

- **Request Body (JSON)**:
  ```json
  {
    "place": "Taj Mahal",
    "answerType": "Summary",
    "language": "English",
    "voiceId": "Matthew",
    "locale": "en-US"
  }
  ```
- **Response Body (JSON)**:
  ```json
  {
    "description": "The Taj Mahal is an ivory-white marble mausoleum...",
    "audioBase64": "<base64_encoded_mp3_data>"
  }
  ```

---

## Technologies Used

- **Backend**: Python, Flask, Flask-CORS, `google-genai`, `requests`, `python-dotenv`
- **Frontend**: HTML5, Vanilla JavaScript, Tailwind CSS
- **AI Models**: Google Gemini (`gemini-3.1-flash-lite`), Murf AI Speech API (`FALCON`)
