# 🤖 AI Voice Agent Platform
### Real-time Conversational AI for Web & Telephony

<div align="center">

![Status](https://img.shields.io/badge/Status-Production%20Ready%20(Web)-success)
![Telephony](https://img.shields.io/badge/Telephony-In%20Development-yellow)
[![Powered by Ultravox](https://img.shields.io/badge/Powered%20by-Ultravox-blue)](https://www.ultravox.ai/)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Live Demo](#live-demo)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Roadmap](#roadmap)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## 🎯 Overview

This project is a comprehensive AI communication platform that enables natural voice conversations with an intelligent AI agent through multiple channels. Built on the Ultravox AI platform, it provides real-time, bidirectional voice streaming for seamless human-AI interactions.

### Current Status

- ✅ **Web Interface**: Fully functional browser-based voice agent
- ⚙️ **Telephony Integration**: In development (awaiting Exotel Voicebot enablement)

---

## 🌐 Live Demo

Experience the AI agent directly in your browser:

**🔗 [Try Live Demo](https://ultravox-startup.onrender.com)**

> **Note**: Allow microphone access when prompted. The agent responds in real-time using voice.

---

## ✨ Features

### Current Features (Web)

- 🎙️ **Real-time Voice Interaction**: Natural conversation with sub-second latency
- 🌐 **Browser-Based**: No installation required - works directly in modern browsers
- 📝 **Live Transcription**: Real-time display of agent responses
- 🎯 **Intelligent Agent**: Powered by Ultravox's advanced voice AI model
- 🔒 **Secure API**: Protected API keys using server-side proxy pattern
- ⚡ **Fast Response**: WebSocket-based streaming for instant communication

### Planned Features (Telephony)

- 📞 **Inbound Calls**: Receive calls on Indian phone numbers via Exotel
- 🔄 **Call Routing**: Intelligent call flow management
- 📊 **Call Analytics**: Track call duration, quality, and outcomes
- 🇮🇳 **TRAI Compliant**: Full compliance with Indian telecom regulations

---

## 🏗️ Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Browser   │◄───────►│ Flask Server │◄───────►│  Ultravox   │
│  (Client)   │  HTTPS  │   (Proxy)    │   API   │  AI Engine  │
└─────────────┘         └──────────────┘         └─────────────┘
      │                                                   │
      │ WebSocket                                         │
      └───────────────────────────────────────────────────┘
                    (bidirectional audio)
```

### Component Overview

1. **Frontend**: Browser-based UI using `ultravox-client` JavaScript SDK
2. **Backend**: Python Flask server acting as secure API proxy
3. **AI Engine**: Ultravox platform handling voice understanding and generation
4. **Audio Transport**: WebSocket (WSS) for bidirectional real-time audio streaming

---

## 🛠️ Technology Stack

### Core Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **AI Platform** | [Ultravox](https://www.ultravox.ai/) | Voice AI engine with multimodal understanding |
| **Backend** | Python 3.x + [FastHTML](https://fastht.ml/) | Lightweight web framework |
| **Frontend** | JavaScript + `ultravox-client` | Browser-based audio streaming |
| **Web Server** | Gunicorn + Uvicorn | ASGI production server |
| **Deployment** | [Render](https://render.com/) | Cloud hosting platform |
| **Telephony** | Exotel (planned) | Indian telephony provider |

### Dependencies

```
fasthtml
requests
gunicorn
uvicorn
python-dotenv
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Ultravox API key ([Get one here](https://app.ultravox.ai/settings/))
- Modern web browser with microphone access

### Installation

1. **Clone the repository**
   ```
   git clone https://github.com/yourusername/ai-voice-agent.git
   cd ai-voice-agent
   ```

2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```
   ULTRAVOX_API_KEY=your_ultravox_api_key_here
   ```

4. **Run the application**
   ```
   python main.py
   ```

5. **Access the app**
   
   Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ULTRAVOX_API_KEY` | Your Ultravox API authentication key | Yes |
| `PORT` | Server port (default: 8000) | No |

### Agent Configuration

To use a custom Ultravox agent, modify `main.py`:

```
AGENT_ID = "your-agent-id-here"  # From Ultravox console

@rt("/start")
async def post():
    r = fixie_request("POST", f"/agents/{AGENT_ID}/calls", json={})
    # ... rest of the code
```

---

## 🌍 Deployment

### Deploy to Render

1. **Create a new Web Service** on [Render](https://render.com/)

2. **Connect your repository**

3. **Configure build settings**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

4. **Add environment variables**
   - Add `ULTRAVOX_API_KEY` in the Render dashboard

5. **Deploy**
   
   Your app will be live at: `https://your-app-name.onrender.com`

### Deploy to Other Platforms

The application is compatible with any platform that supports Python ASGI applications:
- Heroku
- Railway
- Google Cloud Run
- AWS Elastic Beanstalk

---

## 🗺️ Roadmap

### Phase 1: Web Prototype ✅ Complete
- [x] Basic web interface
- [x] Voice interaction with Ultravox
- [x] Live transcription
- [x] Production deployment

### Phase 2: Telephony Integration 🚧 In Progress
- [x] Architecture design
- [x] Exotel account setup
- [ ] Voicebot feature enablement (pending Exotel approval)
- [ ] Inbound call flow configuration
- [ ] WebSocket integration with Exotel
- [ ] Production testing

### Phase 3: Advanced Features 📅 Planned
- [ ] Call recording and playback
- [ ] Multi-language support
- [ ] Custom voice models (ElevenLabs integration)
- [ ] Analytics dashboard
- [ ] Outbound calling capability
- [ ] CRM integration

---

## 🔧 Troubleshooting

### Common Issues

#### "Invalid API Key" Error

**Solution**: Ensure your `ULTRAVOX_API_KEY` is correctly set in the `.env` file or environment variables.

```
# Verify key is loaded
export ULTRAVOX_API_KEY="your-key-here"
python main.py
```

#### Microphone Not Working

**Solution**: 
1. Check browser permissions (usually in address bar)
2. Ensure you're using HTTPS (required for microphone access)
3. Try a different browser (Chrome/Edge recommended)

#### Call Not Connecting

**Solution**:
1. Check browser console for errors (F12)
2. Verify Ultravox API key is valid
3. Check network connectivity
4. Ensure WebSocket connections aren't blocked by firewall

#### 404 Error on Call Creation

**Solution**: Verify your Agent ID is complete (not truncated). Copy it directly from the Ultravox console.

---

## 📞 Telephony Setup (For Production)

### Exotel Integration Steps

1. **Request Voicebot Feature**
   
   Email Exotel support at `hello@exotel.com` with:
   - Subject: "Enable Stream/Voicebot Applet for [Account SID]"
   - Use case description (AI voice agent integration)
   - Request for bidirectional WebSocket streaming

2. **Configure Flow** (Once enabled)
   - Add Voicebot applet to Exotel Flow
   - Point to your webhook endpoint
   - Configure call routing rules

3. **Backend Integration**
   ```
   @app.route("/exotel-inbound", methods=['POST'])
   def handle_exotel_call():
       # Create Ultravox call with agent
       r = requests.post(
           f'https://api.ultravox.ai/api/agents/{AGENT_ID}/calls',
           headers={'X-API-Key': ULTRAVOX_API_KEY},
           json={'medium': {'exotel': {}}}
       )
       return jsonify({'joinUrl': r.json()['joinUrl']})
   ```

---

## 📚 Documentation

- [Ultravox Documentation](https://docs.ultravox.ai/)
- [Exotel API Docs](https://developer.exotel.com/)
- [FastHTML Documentation](https://fastht.ml/)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Your Name / Quantumbuilds**

- GitHub: [@yourusername](https://github.com/yourusername)
- Website: [your-website.com](https://your-website.com)

---

## 🙏 Acknowledgments

- [Ultravox AI](https://www.ultravox.ai/) for the voice AI platform
- [Exotel](https://exotel.com/) for Indian telephony infrastructure
- [Render](https://render.com/) for hosting

---

<div align="center">

**⭐ Star this repo if you find it useful!**

Made with ❤️ by Quantumbuilds

</div>
```

Now you can simply copy this entire block and paste it directly into your `README.md` file! Just replace the placeholders like `@yourusername`, `your-website.com`, and your actual GitHub URL with your real information.
