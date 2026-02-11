# VoiceAgent AI - Enterprise Demo 🎙️

A high-fidelity, production-ready MVP demo of an AI-powered voice agent platform for enterprise use cases. Built with **FastHTML**, **Ultravox API**, and **Tailwind CSS**.

![VoiceAgent AI Dashboard](https://via.placeholder.com/1200x600?text=VoiceAgent+AI+Dashboard+Preview)

## 🚀 Overview

**VoiceAgent AI** demonstrates the power of modern real-time voice AI for business. This application serves as a dashboard and interaction portal where users can:
- View business metrics (Calls, Savings, Active Agents).
- Interact with a custom-trained AI Agent ("Alex" - Restaurant Booking).
- Experience real-time voice conversations with <500ms latency.
- View call history and analytics.

This project is optimized for deployment on **Railway** and is designed to look and feel like a premium SaaS product.

## ✨ Features

- **Real-time Voice AI**: Powered by [Ultravox](https://ultravox.ai), enabling natural, low-latency conversations.
- **Interactive Dashboard**: clean, modern UI built with Tailwind CSS.
- **Live Call Analytics**: Real-time timer, status tracking, and mic visualization.
- **Responsive Design**: Fully mobile-compatible with touch-optimized controls.
- **AudioContext Fixes**: Includes specific logic to handle mobile browser autoplay policies.
- **Mock Business Data**: Demonstrates potential ROI with simulated call metrics and cost savings.

## 🛠️ Tech Stack

- **Backend**: Python (FastHTML, Uvicorn)
- **Frontend**: FastHTML (Server-Side Rendering), HTMX (Dynamic interactions), Tailwind CSS (Styling)
- **AI Core**: Ultravox Real-time API
- **Client Library**: `ultravox-client` (via ESM)

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Dhruv63/ultravox-startup.git
    cd ultravox-startup
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file in the root directory:
    ```env
    ULTRAVOX_API_KEY=your_api_key_here
    AGENT_ID=your_agent_id_here
    ```

4.  **Run the Application:**
    ```bash
    python main.py
    ```
    Visit `http://localhost:5001` in your browser.

## 🚀 Deployment (Railway)

This project is configured for seamless deployment on [Railway](https://railway.app).

1.  Connect your GitHub repository to Railway.
2.  Add the `ULTRAVOX_API_KEY` and `AGENT_ID` variables in the Railway project settings.
3.  Deploy! Python dependencies will be installed automatically via `requirements.txt`.

## 📱 Mobile Support

The application includes specific optimizations for mobile devices:
- **Touch-friendly buttons**.
- **Audio Context Management**: Automatically resumes AudioContext on user interaction to comply with mobile browser policies (iOS/Android).
- **Responsive Layout**: Adjusts grid and font sizes for smaller screens.

## 📝 License

This project is a demo and is available for educational and evaluation purposes.

---
*Built for Raw Engineering Proposal*
