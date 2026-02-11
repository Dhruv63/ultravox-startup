from fasthtml.common import *
import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
ULTRAVOX_API_KEY = os.environ.get('ULTRAVOX_API_KEY', "")
# In a real app, different agents would have different IDs. 
# For this demo, we use the single enabled ID for all visual "agents".
DEFAULT_AGENT_ID = os.environ.get("AGENT_ID", "")

# --- MOCK DATA ---
AGENTS = [
    {
        "id": "agent_booking",
        "name": "Alex Chen",
        "role": "Business Development Rep",
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Alex", 
        "specialization": ["Lead Qualification", "Meeting Scheduling", "Technical Gathering"],
        "languages": ["English (Primary)", "Hindi (Full Support)", "Regional (Basic)"],
        "status": "LIVE (24/7)",
        "is_demo": True
    }
]

HISTORY_DATA = [
    {"time": "10:45 PM", "agent": "Alex", "duration": "4:32", "lang": "English", "type": "Software Firm", "outcome": "Meeting Booked", "action": "🎧 📄"},
    {"time": "10:23 PM", "agent": "Alex", "duration": "2:15", "lang": "Hindi", "type": "Startup", "outcome": "Follow-up", "action": "🎧 📄"},
    {"time": "9:58 PM", "agent": "Alex", "duration": "1:47", "lang": "English", "type": "Not Qualified", "outcome": "Redirected", "action": "🎧 📄"},
    {"time": "9:15 PM", "agent": "Alex", "duration": "3:10", "lang": "English", "type": "Enterprise", "outcome": "Meeting Booked", "action": "🎧 📄"},
    {"time": "8:40 PM", "agent": "Alex", "duration": "0:45", "lang": "Hindi", "type": "Spam", "outcome": "Blocked", "action": "🎧 📄"},
]

ACTIVITY_FEED = [
    {"text": "Call completed (3:45)", "sub": "Outcome: Lead qualified ✓", "time": "Just now"},
    {"text": "New call started", "sub": "Caller: Looking for mobile dev", "time": "2 min ago"},
    {"text": "Meeting scheduled", "sub": "For: Thursday 3 PM", "time": "5 min ago"},
]

# --- APP SETUP ---
headers = (
    Script(src="https://cdn.tailwindcss.com"),
    Script(src="https://unpkg.com/lucide@latest"), # For icons if needed, using emojis for now to be safe
    # Font import for a more premium look
    Link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"),
    Style("""
        :root {
            --primary-blue: #2563EB;
            --accent-orange: #F59E0B;
            --success-green: #10B981;
            --bg-light: #F9FAFB;
            --card-white: #FFFFFF;
            --text-dark: #1F2937;
            --text-gray: #6B7280;
        }
        body { font-family: 'Inter', sans-serif; background-color: var(--bg-light); color: var(--text-dark); }
        
        /* Animations */
        .mic-wave { animation: pulse-ring 2s cubic-bezier(0.215, 0.61, 0.355, 1) infinite; }
        .pulsing-dot { animation: pulse-dot 2s infinite; }
        .hover-lift { transition: transform 0.2s ease, box-shadow 0.2s ease; }
        .hover-lift:hover { transform: translateY(-4px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
        
        @keyframes pulse-ring {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 20px rgba(37, 99, 235, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(37, 99, 235, 0); }
        }
        @keyframes pulse-dot {
            0% { transform: scale(0.95); opacity: 1; }
            50% { transform: scale(1.2); opacity: 0.8; }
            100% { transform: scale(0.95); opacity: 1; }
        }
        
        /* Utilities */
        .scrollbar-hide::-webkit-scrollbar { display: none; }
        .scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }

        /* --- LAYOUT FIXES --- */
        
        /* Main grid */
        .dashboard-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            max-width: 1400px;
            margin: 0 auto;
            padding: 24px;
        }

        /* Columns */
        .deployed-agents-section {
            grid-column: 1;
            max-width: 500px; /* Constrain width to prevent overflow */
        }

        .recent-calls-section {
            grid-column: 2;
            min-width: 0; /* Important for overflow fix */
        }

        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 32px;
            max-width: 1400px;
            margin-left: auto;
            margin-right: auto;
            padding: 0 24px;
        }

        .stat-card {
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            min-width: 0;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100%;
        }

        /* Agent Card */
        .agent-card {
            width: 100%;
            max-width: 460px;
            padding: 24px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 24px;
        }

        .agent-header { display: flex; gap: 16px; margin-bottom: 24px; align-items: center; }
        .agent-avatar { width: 64px; height: 64px; border-radius: 50%; flex-shrink: 0; }
        .agent-title h3 { margin: 0; font-size: 20px; font-weight: 600; color: #111827; }
        .agent-role { color: #2563EB; font-size: 12px; font-weight: 600; margin: 4px 0; text-transform: uppercase; }
        .demo-badge { display: inline-block; background: #EEF2FF; color: #4F46E5; padding: 4px 8px; border-radius: 4px; font-size: 10px; font-weight: 600; }
        
        .agent-section { margin-bottom: 20px; padding-bottom: 20px; border-bottom: 1px solid #E5E7EB; }
        .agent-section:last-of-type { border-bottom: none; }
        .section-label { display: flex; align-items: center; gap: 8px; color: #6B7280; font-size: 12px; font-weight: 600; margin-bottom: 12px; }
        
        .feature-list, .language-list { list-style: none; padding: 0; margin: 0; }
        .feature-list li, .language-list li { padding: 6px 0; padding-left: 20px; position: relative; font-size: 14px; color: #4B5563; }
        .feature-list li:before { content: "•"; position: absolute; left: 0; color: #2563EB; }
        .language-list li.primary { color: #059669; font-weight: 500; }
        
        .agent-status { display: flex; align-items: center; gap: 8px; margin: 20px 0; font-weight: 600; color: #059669; font-size: 12px; }
        .status-dot { width: 8px; height: 8px; background: #10B981; border-radius: 50%; animation: pulse-dot 2s infinite; }
        
        .agent-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 20px; }
        .btn-primary { background: #2563EB; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: all 0.2s; width: 100%; }
        .btn-primary:hover { background: #1D4ED8; transform: translateY(-2px); }
        .btn-secondary { background: white; color: #2563EB; border: 2px solid #2563EB; padding: 12px 24px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: all 0.2s; width: 100%; text-align: center;}
        .btn-secondary:hover { background: #EEF2FF; }

        /* Enterprise Features */
        .enterprise-features { width: 100%; background: #F9FAFB; padding: 32px; border-radius: 12px; margin-top: 32px; margin-bottom: 32px; }
        .features-header { display: flex; align-items: center; gap: 8px; margin-bottom: 24px; font-size: 14px; font-weight: 700; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid #E5E7EB; padding-bottom: 8px; }
        .features-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
        .feature-item { display: flex; align-items: flex-start; gap: 8px; padding: 4px 0; font-size: 14px; color: #374151; }
        .feature-item .checkmark { color: #10B981; font-size: 16px; flex-shrink: 0; font-weight: bold; }

        /* Table */
        .recent-calls-container { width: 100%; overflow-x: auto; background: white; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 24px; }
        .calls-table { width: 100%; border-collapse: collapse; min-width: 600px; }
        .calls-table th, .calls-table td { padding: 12px; text-align: left; border-bottom: 1px solid #F3F4F6; }
        .calls-table th { font-weight: 600; color: #6B7280; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; }
        .calls-table tr:last-child td { border-bottom: none; }

        /* Trust Badges */
        .trust-badges { display: flex; justify-content: space-between; align-items: center; background: white; padding: 16px 32px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-top: 32px; flex-wrap: wrap; gap: 16px; margin-left: 24px; margin-right: 24px; }
        .badge-item { display: flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 600; color: #6B7280; text-transform: uppercase; letter-spacing: 0.02em; }
        .badge-item .icon { color: #10B981; font-size: 16px; }

        /* Responsive */
        @media (max-width: 1200px) {
            .dashboard-container { grid-template-columns: 1fr; }
            .deployed-agents-section, .recent-calls-section { grid-column: 1; max-width: 100%; }
        }
        @media (max-width: 1024px) { .stats-grid { grid-template-columns: repeat(2, 1fr); } }
        @media (max-width: 768px) { .trust-badges { flex-direction: column; align-items: flex-start; } }
        @media (max-width: 640px) { 
            .stats-grid { grid-template-columns: 1fr; }
            .dashboard-container { padding: 16px; }
            .agent-card { padding: 16px; }
            .agent-actions { grid-template-columns: 1fr; }
            .features-grid { grid-template-columns: 1fr; }
        }
    """)
)

app, rt = fast_app(pico=False, hdrs=headers)

# --- CLIENT JS ---
# This JS handles the Ultravox session, timer, and UI updates
client_js = """
import { UltravoxSession } from 'https://esm.sh/ultravox-client';

let session = null;
let timerInterval = null;
let startTime = null;

window.startCall = async (joinUrl) => {
    console.log("Starting call with URL:", joinUrl);
    
    // Cleanup previous session if any
    if (session) {
        await session.leaveCall();
        session = null;
    }

    session = new UltravoxSession();
    
    // Update UI to Connecting
    document.getElementById('call-status-badge').className = "px-3 py-1 rounded-full text-xs font-semibold bg-yellow-100 text-yellow-800 animate-pulse";
    document.getElementById('call-status-text').innerText = "Connecting...";

    session.addEventListener('status', (e) => {
        console.log("Session status:", e.target._status);
        if (e.target._status === 'active') {
             // Active State
             document.getElementById('call-status-badge').className = "px-3 py-1 rounded-full text-xs font-semibold bg-green-100 text-green-800";
             document.getElementById('call-status-text').innerText = "Active Call";
             document.getElementById('mic-icon').classList.add('mic-wave');
             
             // Start Timer
             startTime = Date.now();
             timerInterval = setInterval(updateTimer, 1000);
        } else if (e.target._status === 'disconnected') {
             handleCallEnded();
        }
    });

    session.addEventListener('transcripts', (e) => {
        const transcriptContainer = document.getElementById('transcript-container');
        if (!transcriptContainer) return;
        
        let transcripts = e.target._transcripts;
        if (transcripts && transcripts.length > 0) {
            const lastTranscript = transcripts[transcripts.length - 1];
            if (lastTranscript && lastTranscript.text) {
                const speaker = lastTranscript.speaker === "user" ? "You" : "Agent";
                const bgClass = lastTranscript.speaker === "user" ? "bg-gray-100 text-gray-800 ml-auto" : "bg-blue-50 text-blue-900";
                const alignClass = lastTranscript.speaker === "user" ? "text-right" : "text-left";
                
                // We're just appending the latest text for simplified demo effect
                // In a real app we'd diff properly. 
                // A hacky clear/re-render for demo smoothness:
                transcriptContainer.innerHTML = transcripts.map(t => `
                    <div class="mb-3 ${t.speaker === 'user' ? 'flex justify-end' : 'flex justify-start'}">
                        <div class="max-w-[80%] rounded-lg p-3 ${t.speaker === 'user' ? 'bg-gray-100 text-gray-800' : 'bg-blue-50 text-blue-900'}">
                            <p class="text-xs text-gray-400 mb-1">${t.speaker === 'user' ? 'You' : 'Agent'}</p>
                            <p class="text-sm">${t.text}</p>
                        </div>
                    </div>
                `).join('');
                
                transcriptContainer.scrollTop = transcriptContainer.scrollHeight;
            }
        }
    });

    // Resume AudioContext for mobile browsers (required for autoplay policy)
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        if (audioContext.state === 'suspended') {
            await audioContext.resume();
        }
    } catch (e) {
        console.log('AudioContext resume failed:', e);
    }

    await session.joinCall(joinUrl);
};

window.endCall = async () => {
    if (session) {
        await session.leaveCall();
        handleCallEnded();
    }
};

function updateTimer() {
    const delta = Math.floor((Date.now() - startTime) / 1000);
    const mins = Math.floor(delta / 60).toString().padStart(2, '0');
    const secs = (delta % 60).toString().padStart(2, '0');
    document.getElementById('call-timer').innerText = `${mins}:${secs}`;
}

function handleCallEnded() {
    if (timerInterval) clearInterval(timerInterval);
    document.getElementById('call-status-badge').className = "px-3 py-1 rounded-full text-xs font-semibold bg-red-100 text-red-800";
    document.getElementById('call-status-text').innerText = "Call Ended";
    document.getElementById('mic-icon').classList.remove('mic-wave');
    
    // Trigger the swap to summary view
    htmx.trigger("#call-interface", "call-ended");
}
"""

# --- BACKEND LOGIC ---
def fixie_request(method, path, **kwargs):
    u = "https://api.ultravox.ai/api"
    return requests.request(
        method, u + path, headers={"X-API-Key": ULTRAVOX_API_KEY}, **kwargs
    )

# --- COMPONENTS ---

def MetricCard(title, value, trend, footer, icon):
    return Div(
        Div(
            Div(icon, cls="text-2xl"),
            Div(title, cls="text-xs font-bold text-gray-500 uppercase tracking-widest"),
            cls="flex items-center gap-3 mb-4"
        ),
        H3(value, cls="text-4xl font-extrabold text-gray-900 mb-2 tracking-tight"),
        Div(
            Span("↑" if "+" in trend else "↓", cls="mr-1"),
            Span(trend, cls="font-semibold"),
            cls=f"text-sm mb-4 {'text-green-600' if '+' in trend else 'text-red-600'} flex items-center"
        ),
        Div(footer, cls="text-xs text-gray-400 border-t border-gray-100 pt-3 mt-auto"),
        cls="stat-card hover-lift" # Updated class
    )

def AgentCard(agent):
    return Div(
        # Header Section
        Div(
            Img(src=agent['avatar'], cls="agent-avatar"),
            Div(
                H3(agent['name']),
                P(agent['role'], cls="agent-role"),
                Span("DEMO AGENT", cls="demo-badge"),
                cls="agent-title"
            ),
            cls="agent-header"
        ),
        
        # Specialization Section
        Div(
            Div(
                Span("🎯", cls="icon"),
                Span("SPECIALIZATION:"),
                cls="section-label"
            ),
            Ul(
                *[Li(s) for s in agent['specialization']],
                cls="feature-list"
            ),
            cls="agent-section"
        ),
        
        # Languages Section
        Div(
            Div(
                Span("🌐", cls="icon"),
                Span("LANGUAGES:"),
                cls="section-label"
            ),
            Ul(
                *[Li(l, cls="primary" if "Primary" in l else "supported") for l in agent['languages']],
                cls="language-list"
            ),
            cls="agent-section"
        ),
        
        # Status
        Div(
            Span(cls="status-dot"),
            Span(agent['status']),
            cls="agent-status"
        ),
        
        # Action Buttons
        Div(
            Button(
                "Test Agent", 
                cls="btn-primary",
                hx_post=f"/start?agent_id={agent['id']}",
                hx_target="#call-overlay-container", 
                hx_swap="innerHTML"
            ),
            Button("View Stats", cls="btn-secondary"),
            cls="agent-actions"
        ),
        cls="agent-card" # User defined class
    )

def ActivityFeedItem(item):
    # Keeping this simple as it wasn't explicitly redefined by user but needs to fit
    return Div(
        Div(cls="w-2 h-2 rounded-full bg-blue-500 mt-1.5 mr-3 flex-shrink-0"),
        Div(
            P(item['text'], cls="text-sm font-semibold text-gray-900"),
            P(item['sub'], cls="text-xs text-gray-500"),
            cls="flex-1"
        ),
        Span(item['time'], cls="text-xs text-gray-400 whitespace-nowrap ml-4"),
        cls="flex items-start mb-4 last:mb-0"
    )

def HistoryRow(item):
    # Using existing data but minimal classes to let .calls-table handle styling
    return Tr(
        Td(item['time']),
        Td(
            Div(
                Img(src="https://api.dicebear.com/7.x/avataaars/svg?seed=Alex", cls="w-6 h-6 rounded-full mr-2"),
                item['agent'],
                cls="flex items-center font-medium"
            )
        ),
        Td(item['duration'], cls="font-mono text-gray-500"),
        Td(
            Span(item['lang'], cls="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800"),
        ),
        Td(item['type'], cls="text-gray-500"),
        Td(
            Span(
                item['outcome'], 
                cls=f"px-2 py-1 text-xs font-bold rounded-full {'bg-green-100 text-green-800' if 'Booked' in item['outcome'] else 'bg-yellow-100 text-yellow-800' if 'Follow' in item['outcome'] else 'bg-gray-100 text-gray-600'}"
            )
        ),
        Td(
            Div(
                Button("🎧", cls="text-gray-400 hover:text-blue-600 mr-2", title="Play"),
                Button("📄", cls="text-gray-400 hover:text-blue-600", title="Transcript"),
                cls="flex items-center text-lg"
            )
        )
    )

def FeatureShowcase():
    features = [
        "24/7 Availability - Never Miss a Call",
        "Multilingual Support - English + Hindi",
        "CRM Integration - Auto-sync leads",
        "Real-time Analytics - Live dashboard",
        "Call Recording - 100% quality assurance",
        "Custom Training - Your business, your AI"
    ]
    return Div(
        Div(
            Span("⚡", cls="mr-2"),
            "ENTERPRISE FEATURES", 
            cls="features-header"
        ),
        Div(
            *[Div(Span("✓", cls="checkmark"), f, cls="feature-item") for f in features],
            cls="features-grid"
        ),
        cls="enterprise-features"
    )

def TrustFooter():
    return Div(
        Div(Span("✓", cls="icon"), "Enterprise-Grade Security", cls="badge-item"),
        Div(Span("✓", cls="icon"), "99.9% Uptime SLA", cls="badge-item"),
        Div(Span("✓", cls="icon"), "SOC 2 Compliant", cls="badge-item"),
        Div(Span("✓", cls="icon"), "GDPR Compliant", cls="badge-item"),
        cls="trust-badges"
    )

def CallOverlay(agent_name, join_url):
    return Div(
        # Modal Backdrop
        Div(cls="fixed inset-0 bg-gray-900/50 backdrop-blur-sm z-40 transition-opacity"),
        # Modal Content
        Div(
            # Header
            Div(
                Div(
                    H3(f"Call with {agent_name}", cls="text-lg font-bold text-gray-900"),
                    Div(
                        Span("Connecting...", id="call-status-text", cls="mr-2"),
                        Span(id="call-status-badge", cls="px-3 py-1 rounded-full text-xs font-semibold bg-gray-100 text-gray-800"),
                        cls="flex items-center"
                    ),
                    cls="flex justify-between items-center border-b border-gray-100 pb-4 mb-4"
                ),
                # Active Call Area
                Div(
                    # Timer & Visualizer
                    Div(
                        Div("00:00", id="call-timer", cls="text-4xl font-mono font-bold text-gray-900 tracking-wider mb-2"),
                        Div("Recording & Transcribing", cls="text-xs text-gray-400 uppercase tracking-widest"),
                        # Mic Icon with Pulse
                        Div(
                            "🎤", 
                            id="mic-icon",
                            cls="text-4xl w-20 h-20 bg-blue-50 rounded-full flex items-center justify-center mt-8 mb-4 mx-auto transition-all duration-500"
                        ),
                        cls="text-center py-6 w-1/3 border-r border-gray-100 pr-4"
                    ),
                    # Transcript
                    Div(
                        Div("Conversation started...", cls="text-center text-gray-400 italic text-sm mt-4"),
                        id="transcript-container",
                        cls="h-64 overflow-y-auto w-2/3 pl-6 pr-2 scrollbar-hide"
                    ),
                    cls="flex flex-row gap-4"
                ),
                # Footer Controls
                Div(
                    Button(
                        "End Call", 
                        onclick="window.endCall()",
                        cls="bg-red-500 hover:bg-red-600 text-white font-bold py-3 px-8 rounded-full shadow-lg transform active:scale-95 transition-all text-sm uppercase tracking-wide"
                    ),
                    # HTMX trigger for summary view (hidden)
                    Div(id="call-interface", hx_get="/end-summary", hx_trigger="call-ended", hx_target="#call-modal-content", hx_swap="outerHTML"),
                    cls="border-t border-gray-100 pt-6 mt-4 flex justify-center"
                ),
                id="call-modal-content",
                cls="bg-white rounded-2xl shadow-2xl max-w-2xl w-full p-6 relative z-50 transform transition-all scale-100 opacity-100"
            ),
            cls="fixed inset-0 z-50 flex items-center justify-center p-4",
            id="call-modal-wrapper"
        ),
        # Init Script
        Script(f"window.startCall('{join_url}')"),
        id="call-overlay-container"
    )

def CallSummary():
    return Div(
        Div(
            H3("Call Completed", cls="text-xl font-bold text-gray-900 text-center mb-2"),
            P("Great! The call data has been processed.", cls="text-gray-500 text-center mb-8"),
            
            # Simulated Stats
            Div(
                Div(
                    P("Duration", cls="text-xs text-gray-500 uppercase"),
                    P("02:14", cls="text-lg font-bold text-gray-900"),
                    cls="text-center p-4 bg-gray-50 rounded-lg"
                ),
                Div(
                    P("Turns", cls="text-xs text-gray-500 uppercase"),
                    P("12", cls="text-lg font-bold text-gray-900"),
                    cls="text-center p-4 bg-gray-50 rounded-lg"
                ),
                Div(
                    P("Est. Cost", cls="text-xs text-gray-500 uppercase"),
                    P("$0.22", cls="text-lg font-bold text-green-600"),
                    cls="text-center p-4 bg-green-50 rounded-lg border border-green-100"
                ),
                cls="grid grid-cols-3 gap-4 mb-8"
            ),
            
            Button(
                "Close & Return", 
                onclick="document.getElementById('call-overlay-container').innerHTML = '';",
                cls="w-full bg-gray-900 hover:bg-gray-800 text-white font-bold py-3 rounded-lg transition-colors"
            ),
            cls="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 relative z-50 animate-fade-in-up"
        ),
        cls="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/50 backdrop-blur-sm"
    )


# --- ROUTES ---

@rt("/")
def get():
    return Title("VoiceAgent AI - Dashboard"), Body(
        # Navbar
        # Navbar
        Nav(
            Div(
                # Left: Brand
                Div(
                    Span("🎙️", cls="text-2xl mr-2 text-blue-600"),
                    Div(
                        H1("VoiceForge AI", cls="text-xl font-bold tracking-tight text-gray-900"), 
                        P("Enterprise Voice Platform", cls="text-[10px] text-gray-500 uppercase tracking-wider font-semibold"),
                        cls="flex flex-col"
                    ),
                    Span("LIVE DEMO", cls="ml-4 px-2 py-0.5 rounded text-[10px] font-bold bg-green-100 text-green-700 border border-green-200 animate-pulse"),
                    cls="flex items-center"
                ),
                # Center: Links
                Div(
                    A("Dashboard", href="#", cls="text-sm font-medium text-blue-600 px-3 py-2 rounded-md bg-blue-50"),
                    A("Analytics", href="#", cls="text-sm font-medium text-gray-500 hover:text-gray-900 px-3 py-2 transition-colors"),
                    A("Agents", href="#", cls="text-sm font-medium text-gray-500 hover:text-gray-900 px-3 py-2 transition-colors"),
                    A("Pricing", href="#", cls="text-sm font-medium text-gray-500 hover:text-gray-900 px-3 py-2 transition-colors"),
                    A("Documentation", href="#", cls="text-sm font-medium text-gray-500 hover:text-gray-900 px-3 py-2 transition-colors"),
                    cls="hidden md:flex items-center space-x-1"
                ),
                # Right: Actions & Profile
                Div(
                    Button("Contact Sales", cls="hidden md:block mr-6 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold py-2 px-4 rounded-full shadow-sm transition-transform hover:scale-105"),
                    # User Dropdown
                    Div(
                        Img(src="https://api.dicebear.com/7.x/avataaars/svg?seed=Amrut", cls="h-8 w-8 rounded-full border border-gray-200 bg-gray-50"),
                        Div(
                            P("Amrut-Eng...", cls="text-sm font-medium text-gray-700"),
                            P("Admin", cls="text-xs text-gray-400"),
                            cls="hidden lg:block ml-2 text-left"
                        ),
                        cls="flex items-center cursor-pointer pl-4 border-l border-gray-100"
                    ),
                    cls="flex items-center"
                ),
                cls="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex justify-between items-center"
            ),
            cls="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-30"
        ),
        
        Main(
            # Hero Metrics
            Div(
                MetricCard("Total Calls", "24", "↑ +12% this week", "Peak: Today at 6 PM", "📞"),
                MetricCard("Minutes Used", "87", "↑ 3.6m / avg", "Efficiency: 96%", "⏱️"),
                MetricCard("Est. Savings", "₹450", "↑ vs. Humans", "Monthly Proj: ₹1,950", "💰"),
                MetricCard("Active Agents", "4", "● Ready", "Uptime: 99.9%", "🤖"),
                cls="stats-grid" # Updated grid class
            ),
            
            # Application Main Grid
            Div(
                # Left Column: Agent Card
                Div(
                    H2("DEPLOYED AGENTS", cls="text-lg font-bold text-gray-900 mb-4 tracking-tight"),
                    AgentCard(AGENTS[0]),
                    FeatureShowcase(),
                    cls="deployed-agents-section"
                ),
                
                # Right Column: Recent Calls & Analytics
                Div(
                    # Live Activity Feed (Moved to right column top)
                    Div(
                        H2("🔴 LIVE ACTIVITY", cls="text-sm font-bold text-red-600 uppercase tracking-widest mb-4 flex items-center gap-2"),
                        Div(
                            *[ActivityFeedItem(item) for item in ACTIVITY_FEED],
                            cls="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 mb-8"
                        ),
                    ),
                    
                    Div(
                        Div(
                            H2("RECENT TEST CALLS", cls="text-lg font-bold text-gray-900 tracking-tight"),
                            Div(
                                Button("Filter", cls="text-xs font-bold text-gray-500 hover:text-gray-900 mr-4"),
                                Button("Export CSV", cls="text-xs bg-gray-900 text-white px-3 py-1.5 rounded hover:bg-gray-800 transition-colors"),
                                cls="flex items-center"
                            ),
                            cls="flex justify-between items-center mb-4"
                        ),
                        Div(
                            Table(
                                Thead(
                                    Tr(
                                        Th("Time"),
                                        Th("Agent"),
                                        Th("Duration"),
                                        Th("Lang"),
                                        Th("Caller Type"),
                                        Th("Outcome"),
                                        Th("Action"),
                                    )
                                ),
                                Tbody(
                                    *[HistoryRow(item) for item in HISTORY_DATA],
                                    # No explicit class needed on body if table has one, 
                                    # but keeping it clean doesn't hurt.
                                ),
                                cls="calls-table" # Updated table class
                            ),
                            cls="recent-calls-container" # Updated container class
                        ),
                        cls="h-full"
                    ),
                    cls="recent-calls-section"
                ),
                cls="dashboard-container" # Updated main grid container
            ),
            
            TrustFooter(),

            cls="bg-gray-50 min-h-screen text-gray-900"
        ),
        # HTMX target for Call Overlay
        Div(id="call-overlay-container"),
        Script(client_js, type="module"),
        cls="bg-gray-50 min-h-screen text-gray-900"
    )

@rt("/start")
def post(agent_id: str):
    # Retrieve agent details for the UI
    agent = next((a for a in AGENTS if a["id"] == agent_id), AGENTS[0])
    
    # Create the call via Ultravox API
    # NOTE: In a real app we'd use the specific agent ID. For the demo, we use the fallback.
    target_agent_id = DEFAULT_AGENT_ID
    
    try:
        r = fixie_request("POST", f"/agents/{target_agent_id}/calls", json={})
        r.raise_for_status()
        call_data = r.json()
        join_url = call_data.get("joinUrl")
        
        return CallOverlay(agent["name"], join_url)
    except Exception as e:
        print(f"Error creating call: {e}")
        return Div(
            Div(
                H3("Error Connecting", cls="text-lg font-bold text-red-600"),
                P(f"Could not start call: {str(e)}", cls="text-sm text-gray-600 mt-2"),
                Button("Close", onclick="document.getElementById('call-overlay-container').innerHTML = '';", cls="mt-4 bg-gray-200 px-4 py-2 rounded"),
                cls="bg-white p-6 rounded-xl shadow-xl max-w-md mx-auto"
            ),
            cls="fixed inset-0 z-50 flex items-center justify-center bg-black/20"
        )

@rt("/end-summary")
def get():
    return CallSummary()

serve()
