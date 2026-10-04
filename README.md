# 🌙 DreamTales

DreamTales is a personalized AI bedtime-story companion that creates gentle, imaginative stories based on a child's preferences.

Built for the Hacktoberfest Weekend Challenge: Build for a Friend.

## ✨ Features

- Personalized bedtime stories
- Custom child name, favorite animal, character, setting, mood, and story length
- AI-generated stories
- Optional AI voice narration
- Simple, child-friendly interface

## 🧠 How It Works

1. The user provides the child's story preferences.
2. DreamTales creates a personalized prompt.
3. Gemma generates the bedtime story.
4. ElevenLabs converts the story into natural-sounding narration.
5. Render hosts the application.

🌐 LIVE DEMO
  [Try DreamTales Live](https://bedtime-ai.onrender.com/)

## 🛠️ Tech Stack

- **Gemma** — Story generation
- **ElevenLabs** — Voice narration
- **Render** — Deployment

## 🚀 Run Locally

1. Clone the repository
git clone YOUR_GITHUB_REPO_URL
cd DreamTales
2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

On Windows:

.venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Add environment variables

Create a .env file:

ELEVENLABS_API_KEY=your_api_key_here
GEMMA_MODEL=google/gemma-3-1b-it

Never commit your .env file.

5. Run the app
streamlit run app.py
