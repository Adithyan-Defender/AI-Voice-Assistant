# AI Voice Assistant (LLM)

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1-green)](https://www.djangoproject.com/)

Overview

AI Voice Assistant (LLM) is an advanced AI-powered voice web application built with Python Django.
It integrates voice recognition and natural language processing (LLM) to enable users to interact with the application using voice commands and receive intelligent audio responses in real time.

This project showcases:

Full-stack Django development

Real-time communication with Django Channels

Secure handling of sensitive data using environment variables

LLM integration for natural, intelligent responses

Key Features

🎙️ AI Voice Assistant – Natural voice recognition and intelligent voice responses

🤖 AI Chatbot – Conversational text-based chatbot powered by LLMs

🖼️ AI Image Generator – Generate images from text prompts

🪄 AI Background Remover – Remove image backgrounds with AI processing

---

## Demo Screenshots

Here are screenshots showcasing the AI Voice Assistant in action:

### Screenshot 1
![Screenshot 1](screenshots/1.png)

### Screenshot 2
![Screenshot 2](screenshots/2.png)

### Screenshot 3
![Screenshot 3](screenshots/3.png)

### Screenshot 4
![Screenshot 4](screenshots/4.png)

### Screenshot 5
![Screenshot 5](screenshots/5.png)

### Screenshot 6
![Screenshot 6](screenshots/6.png)




## Features
- **Voice Recognition:** Convert user speech into text using AI.
- **AI-Powered Responses:** Generate intelligent responses based on user queries.
- **Real-Time Interaction:** Seamless voice-based communication using Django Channels and ASGI.
- **User Authentication:** Secure login and custom user management.
- **Environment-Safe:** All sensitive keys are loaded from environment variables (`.env`).

---

## Technology Stack
- **Backend:** Python 3.11, Django 5.1, Django Channels
- **AI/ML Libraries:** OpenAI / GPT (or specify libraries used)
- **Database:** SQLite (development) — configurable for PostgreSQL/MySQL
- **Frontend:** HTML, CSS, JavaScript
- **Other:** dotenv for environment variables, SMTP for email OTP

---

## Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/Adithyan-Defender/AI-Voice-Assistant.git
cd AI-Voice-Assistant





Create a virtual environment

python -m venv venv


Activate the virtual environment

Windows:

venv\Scripts\activate


macOS/Linux:

source venv/bin/activate


Install dependencies

pip install -r requirements.txt


Create a .env file in the django project root and add your secrets:

DJANGO_SECRET_KEY=your-secret-key
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-email-password
GROQ_API_KEY=your-api-key

in aivoice/aivoice/aivoice/AI/jarvis/Brain.py

API_URL = "https://api.deepinfra.com/v1/openai/chat/completions"
API_KEY = "Bearer your api_key"  # Replace with actual key

and create an django superuser to login

run this
python manage.py createsuperuser

Run migrations

python manage.py migrate


Start the development server

python manage.py runserver

install ollama to run locally(offline)


Access the app at http://127.0.0.1:8000

