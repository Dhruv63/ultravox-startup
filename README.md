AI Voice Agent (Web & Telephony)

This is a prototype for an AI voice agent that can talk to users via a web browser (live demo) and is designed to handle traditional phone calls (in-progress).

🚀 Live Demo (Web Prototype)

You can talk to the web-based AI agent live at:

https://ultravox-startup.onrender.com

(Note: This is your default Render URL. You can customize it in your Render settings.)

💡 Project Vision

This project is a two-part prototype for a comprehensive AI communication platform. The goal is to allow users to interact with a sophisticated Ultravox-powered AI agent through two different channels:

Web Interface (✅ Working): A web application where users can talk to the agent directly from their browser's microphone.

Telephony (⚠️ On Hold): A system to handle real-world phone calls, allowing the agent to make and receive calls on a domestic Indian phone number using Exotel.

✨ Key Features (Web Prototype)

Real-time, voice-to-voice conversation with an AI agent.

Browser-based audio streaming (no phone required).

Live transcript of the agent's responses.

Simple, fast interface built with fasthtml.

🛠️ Technology Stack

AI: Ultravox

Web Framework: fasthtml (Python)

Frontend Client: ultravox-client (JavaScript)

Web Server: gunicorn + uvicorn

Deployment: Render

🔧 How to Run Locally

Clone the repository:

git clone [https://github.com/Dhruv63/ultravox-startup.git](https://github.com/Dhruv63/ultravox-startup.git)
cd ultravox-startup


Create a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`


Install dependencies:

pip install -r requirements.txt


Set up your API Key:

Create a file named .env in the root of the folder.

Add your Ultravox API key and Agent ID to it:

ULTRAVOX_API_KEY=mXfxxr7B.IOYvzcM4gzA7jyqjvHE4ubC1y9R73iMp
AGENT_ID=48bcaeef-6414-44a1-98b2-8085e9654274


Run the application:

python main.py


Open your browser to http://localhost:5001.

☁️ Deployment to Render (Free)

This app is configured for easy deployment on Render's free tier.

Push to GitHub: Make sure your code is on this GitHub repository.

Create a Render Account: Sign up at render.com with your GitHub.

Create a New "Web Service" and connect your ultravox-startup repository.

Use these settings:

Runtime: Python 3

Build Command: pip install -r requirements.txt

Start Command: gunicorn main:app --worker-class uvicorn.workers.UvicornWorker

Add Environment Variables:

Go to the "Environment" tab for your new service.

Add a variable with the Key ULTRAVOX_API_KEY and your secret key as the Value.

Add another variable with the Key AGENT_ID and your agent's ID as the Value.

Deploy! Render will automatically build and launch your site at your public URL.

📊 Project Status

Web Prototype: ✅ Working and Deployed.

Telephony Prototype (/call agent): ⚠️ On Hold. This prototype (designed to use Exotel for real phone calls in India) is currently blocked. The required "Voicebot" applet for WebSocket streaming is not enabled on the Exotel account. The next step is to contact Exotel support to request this feature.

📄 License

This project is licensed under the MIT License. See the LICENSE file for details.
