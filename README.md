# ✈️ QuietMiles — AI Travel Planning Agent

QuietMiles is an AI-powered travel planning application that generates personalized travel itineraries using **OpenAI** and **real-time flight data from SerpAPI**.

## ✨ Features

* 🤖 AI-generated personalized travel itineraries
* ✈️ Real-time flight search using SerpAPI
* 🧩 Modular multi-step pipeline designed to evolve into an agent-based system
* 🛡️ Fallback handling for external API limitations
* 🔐 Secure API key management
* ⚡ ~3s typical response time
* ☁️ Deployed on Streamlit Cloud

## 🛠️ Tech Stack

**Python · Streamlit · OpenAI API · SerpAPI**

## ⚙️ How It Works

```text
User Preferences
       ↓
Travel Requirements
       ↓
Flight Search (SerpAPI)
       ↓
AI Planning (OpenAI)
       ↓
Personalized Itinerary
```

## 🚀 Run Locally

```bash
git clone https://github.com/<your-username>/QuietMiles.git
cd QuietMiles
pip install -r requirements.txt
streamlit run app.py
```

Add your API keys through environment variables or Streamlit secrets:

```env
OPENAI_API_KEY=your_key
SERPAPI_API_KEY=your_key
```

## 🌐 Live Demo

[Streamlit Cloud](https://quietmiles.streamlit.app/)

---

Built with Python, OpenAI, and SerpAPI.
