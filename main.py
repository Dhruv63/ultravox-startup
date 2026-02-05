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
DEFAULT_AGENT_ID = os.environ.get("AGENT_ID", "eff14921-ffad-4f32-b158-09209e5b220a")

# --- MOCK DATA ---
AGENTS = [
    {
        "id": "agent_booking",
        "name": "Sarah",
        "role": "Restaurant Booking",
        "desc": "Handles reservations, checks availability, and collects guest details.",
        "icon": "🍽️",
        "color": "blue",
        "use_case": "Reservations"
    }
]

HISTORY_DATA = [
    {"time": "Feb 5, 14:30", "agent": "Sarah", "duration": "3m 24s", "status": "Completed", "cost": "$0.34"},
    {"time": "Feb 5, 13:15", "agent": "Alex", "duration": "1m 52s", "status": "Completed", "cost": "$0.19"},
    {"time": "Feb 5, 11:42", "agent": "Mike", "duration": "4m 10s", "status": "Completed", "cost": "$0.42"},
    {"time": "Feb 5, 09:20", "agent": "Sarah", "duration": "2m 05s", "status": "Completed", "cost": "$0.21"},
    {"time": "Feb 4, 16:55", "agent": "Emma", "duration": "1m 30s", "status": "Completed", "cost": "$0.15"},
]

# --- APP SETUP ---
headers = (
    Script(src="https://cdn.tailwindcss.com"),
    Script(src="https://unpkg.com/lucide@latest"), # For icons if needed, using emojis for now to be safe
    # Font import for a more premium look
    Link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"),
    Style("""
        body { font-family: 'Inter', sans-serif; }
        .mic-wave { animation: pulse-ring 2s cubic-bezier(0.215, 0.61, 0.355, 1) infinite; }
        @keyframes pulse-ring {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 20px rgba(59, 130, 246, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
        }
        /* Custom scrollbar for transcript */
        .scrollbar-hide::-webkit-scrollbar { display: none; }
        .scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
        .scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
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

def MetricCard(title, value, subtext, icon_emoji):
    return Div(
        Div(icon_emoji, cls="text-2xl mb-2"),
        P(title, cls="text-sm font-medium text-gray-500 uppercase tracking-wide"),
        H3(value, cls="text-3xl font-bold text-gray-900 mt-1"),
        P(subtext, cls="text-xs text-green-600 font-semibold mt-2"),
        cls="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
    )

def AgentCard(agent):
    return Div(
        Div(
            Span(agent['icon'], cls="text-4xl"),
            Div(
                Span(agent['use_case'], cls=f"px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider {agent['color'].replace('text-', 'bg-').replace('bg-', 'text-').replace('100', '100').replace('800', '800')} ml-auto opacity-70"),
                cls="flex justify-between items-start w-full"
            ),
            cls="flex justify-between items-start mb-4"
        ),
        H3(agent['name'], cls="text-xl font-bold text-gray-900"),
        P(agent['role'], cls="text-sm font-semibold text-gray-600 mb-2"),
        P(agent['desc'], cls="text-sm text-gray-500 mb-6 leading-relaxed"),
        Button(
            "Test Agent", 
            cls=f"w-full py-2.5 px-4 rounded-lg font-medium text-white transition-colors bg-blue-600 hover:bg-blue-700 shadow-sm flex items-center justify-center gap-2",
            hx_post=f"/start?agent_id={agent['id']}",
            hx_target="#call-overlay-container", 
            hx_swap="innerHTML"
        ),
        cls="bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:border-blue-300 hover:shadow-lg transition-all duration-300 flex flex-col"
    )

def HistoryRow(item):
    return Tr(
        Td(item['time'], cls="px-6 py-4 whitespace-nowrap text-sm text-gray-600"),
        Td(
            Div(
                Span(cls="w-2 h-2 rounded-full bg-blue-500 mr-2 inline-block"),
                item['agent'],
                cls="flex items-center text-sm font-medium text-gray-900"
            ), cls="px-6 py-4 whitespace-nowrap"
        ),
        Td(item['duration'], cls="px-6 py-4 whitespace-nowrap text-sm text-gray-600 font-mono"),
        Td(
            Span(item['status'], cls="px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800"),
            cls="px-6 py-4 whitespace-nowrap"
        ),
        Td(item['cost'], cls="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900"),
        cls="hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-0"
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
                onclick="document.getElementById('call-overlay-container').outerHTML = '<div id=\"call-overlay-container\"></div>';",
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
        Nav(
            Div(
                Div(
                    Span("🎙️", cls="text-2xl mr-2"),
                    H1("VoiceAgent AI", cls="text-xl font-bold tracking-tight text-gray-900"), 
                    Span("Enterprise Demo", cls="ml-3 px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800"),
                    cls="flex items-center"
                ),
                Div(
                    A("Documentation", href="#", cls="text-sm font-medium text-gray-500 hover:text-gray-900 mr-6"),
                    A("Contact Sales", href="#", cls="text-sm font-medium text-blue-600 hover:text-blue-800"),
                    cls="flex items-center"
                ),
                cls="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex justify-between items-center"
            ),
            cls="bg-white border-b border-gray-200 sticky top-0 z-30"
        ),
        
        Main(
            # Info Banner
            Div(
                Div(
                    H2("🤖 Custom Voice AI Agents for Enterprise", cls="text-lg font-semibold text-gray-900 mb-1"),
                    P("Deploy branded, intelligent voice agents for support, sales, and bookings. 50% cheaper than human agents.", cls="text-sm text-gray-600"),
                ),
                cls="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-xl border border-blue-100 mb-8"
            ),
            
            # Metrics
            Div(
                MetricCard("Total Calls", "24", "+12% this week", "📞"),
                MetricCard("Minutes Used", "87", "Avg. 3.6m / call", "⏱️"),
                MetricCard("Est. Savings", "$450", "vs. Human Agents", "💰"),
                MetricCard("Active Agents", "4", "Ready to deploy", "🤖"),
                cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10"
            ),
            
            # Agents Grid
            Div(
                H2("Available Agents", cls="text-2xl font-bold text-gray-900 mb-6"),
                Div(*[AgentCard(a) for a in AGENTS], cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"),
                cls="mb-12"
            ),
            
            # Recent History
            Div(
                Div(
                    H2("Recent Test Calls", cls="text-lg font-bold text-gray-900"),
                    Button("Export CSV", cls="text-sm text-gray-500 hover:text-gray-900 border border-gray-300 px-3 py-1 rounded bg-white font-medium"),
                    cls="flex justify-between items-center mb-4"
                ),
                Div(
                    Table(
                        Thead(
                            Tr(
                                Th("Time", cls="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"),
                                Th("Agent", cls="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"),
                                Th("Duration", cls="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"),
                                Th("Status", cls="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"),
                                Th("Cost", cls="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"),
                                cls="bg-gray-50"
                            )
                        ),
                        Tbody(
                            *[HistoryRow(item) for item in HISTORY_DATA],
                            cls="bg-white divide-y divide-gray-200"
                        ),
                        cls="min-w-full divide-y divide-gray-200"
                    ),
                    cls="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg bg-white"
                ),
                cls="mb-12"
            ),
            
                cls="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8"
        ),
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
    print(f"Starting call with Agent ID: {target_agent_id}")
    
    try:
        r = fixie_request("POST", f"/agents/{target_agent_id}/calls", json={})
        r.raise_for_status()
        call_data = r.json()
        join_url = call_data.get("joinUrl")
        print(f"Call created successfully. Join URL: {join_url}")
        
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
