# 🌍 AI Traveler Guide

An AI-powered travel companion that generates historical information about tourist destinations and converts it into audio guides, making travel more informative and engaging.

## ✨ Features

- 📖 **AI-Generated Travel Information:** Generate informative descriptions of tourist destinations using Google Gemini.
- 🔊 **AI-Powered Audio Guides:** Convert generated travel descriptions into speech using the Murf AI API.
- 🌐 **Web Interface:** Interact with the application through a simple frontend built with HTML, CSS, and JavaScript.
- 🔗 **Full-Stack Integration:** Connect a JavaScript frontend to a Python Flask backend.
- ☁️ **Cloud Deployment:** Deploy the frontend and backend using Render.

> Features such as multilingual support, voice customization, destination search, and itinerary planning should be listed as available only after they have been implemented and tested.

## 🚀 Live Demo

**Frontend:** https://ai-traveler-guide.onrender.com

**Backend:** https://ai-traveler-guide-api.onrender.com

## 🛠️ Technology Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **AI Text Generation:** Google Gemini API
- **Text-to-Speech:** Murf AI API
- **Deployment:** Render
- **Version Control:** Git and GitHub

## 📁 Project Structure

```text
AI_traveler_guider/
├── Backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── .env.example
│   └── .env
├── Frontend/
│   ├── index.html
│   └── index.js
├── .gitignore
└── README.md
```

**Note:** The `.env` file contains private API keys and must never be uploaded to GitHub. The `venv/` directory is a local Python virtual environment and should not be committed.

## ⚙️ Prerequisites

Before running the project locally, install:

- Python 3.10 or a compatible version required by your dependencies
- pip
- A modern web browser
- A Google Gemini API key
- A Murf AI API key

## 💻 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Ambu-2005/ai-traveler-guide.git
cd ai-traveler-guide
```

### 2. Set up the backend

Open a terminal in the project root:

```bash
cd Backend
python -m venv venv
```

Activate the virtual environment.

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```bat
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file inside the `Backend/` directory. Add your own API keys:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
MURF_API_KEY=your_murf_api_key
```

Replace the placeholder values with your actual API keys.

**Security:** Never share your API keys or commit the `.env` file to GitHub. If a key has been exposed publicly, revoke or rotate it before using the application.

### 4. Start the backend

From the `Backend/` directory, run:

```bash
python app.py
```

If your Flask application uses a different startup configuration, follow the instructions in `Backend/app.py`.

### 5. Configure and open the frontend

Open `Frontend/index.js` and ensure the API URL points to the backend you are running or your deployed backend URL.

For local development, if Flask runs on port 5000, the URL may be:

```javascript
const API_URL = "http://127.0.0.1:5000";
```

Use the actual route and request format defined by your frontend and backend code.

Open `Frontend/index.html` in your browser, or serve the frontend using a local development server.

## ☁️ Deployment

The application can be deployed using Render.

### Frontend

- Create a **Static Site** on Render.
- Connect the GitHub repository.
- Set the publish directory to `Frontend` if deploying from the repository root.
- Deploy the site and test its interface.

### Backend

- Create a **Web Service** on Render.
- Connect the same GitHub repository.
- Set the root directory to `Backend`.
- Install dependencies with:

```bash
pip install -r requirements.txt
```

- Use the following start command if the Flask application object is named `app` in `app.py`:

```bash
gunicorn app:app --timeout 120
```

- Add `GOOGLE_API_KEY` and `MURF_API_KEY` in the Render service's environment-variable settings.
- Update the frontend API URL to use the deployed backend URL.
- Ensure the backend CORS configuration allows requests from the deployed frontend.

## 🔒 Security

- Keep all API keys in environment variables.
- Never commit `.env`, virtual environments, or private credentials.
- Use `.env.example` to document required variable names without including real values.
- Rotate any credentials that may have been exposed.

## 🧪 Testing Checklist

Before submitting the project, verify:

- [ ] The live frontend opens successfully.
- [ ] A user can enter a destination or travel-related prompt supported by the app.
- [ ] The backend returns generated travel information.
- [ ] Audio generation works and the audio can be played.
- [ ] The frontend communicates with the deployed backend.
- [ ] API keys are configured securely.
- [ ] The public GitHub repository contains setup instructions.
- [ ] The deployed project link is accessible to reviewers.

## 🎯 Project Goal

The goal of AI Traveler Guide is to make travel information more accessible and engaging by combining generative AI with speech synthesis.

## 👨‍💻 Author

**Ambadas**

GitHub: [Ambu-2005](https://github.com/Ambu-2005)

## 📄 License

This project was created for educational and hands-on AI learning purposes. Add a specific open-source license if you intend to distribute the project under one.
