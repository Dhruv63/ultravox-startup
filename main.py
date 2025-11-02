from fasthtml.common import (
    fast_app,
    Script,
    Main,
    Div,
    Button,
    H1,
    Span,
    serve
)
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

ULTRAVOX_API_KEY = os.environ.get('ULTRAVOX_API_KEY', "")
print(f"API Key loaded: {ULTRAVOX_API_KEY[:10]}..." if ULTRAVOX_API_KEY else "No API key found!")

app, rt = fast_app(pico=False, hdrs=(Script(src="https://cdn.tailwindcss.com"),))

def fixie_request(method, path, **kwargs):
    u = "https://api.ultravox.ai/api"
    return requests.request(
        method, u + path, headers={"X-API-Key": ULTRAVOX_API_KEY}, **kwargs
    )


js_on_load = """
import { UltravoxSession } from 'https://esm.sh/ultravox-client';
const debugMessages = new Set(["debug"]);
window.UVSession = new UltravoxSession({ experimentalMessages: debugMessages });
"""

TW_BUTTON = "bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded my-4"

def client_js(callDetails):
    return f"""
    async function joinCall() {{
        const callStatus = await window.UVSession.joinCall("{callDetails.get('joinUrl')}");
        console.log(callStatus);
    }}

    window.UVSession.addEventListener('status', (e) => {{
        let statusDiv = htmx.find("#call-status")
        statusDiv.innerText = e.target._status;
    }});

    window.UVSession.addEventListener('transcripts', (e) => {{
        let transcripts = e.target._transcripts;
        transcript = htmx.find("#transcript");
        transcript.innerText = transcripts.filter(t => t && t.speaker !== "user").map(t => t ? t.text : "").join("\\n");
    }});

    window.UVSession.addEventListener('experimental_message', (msg) => {{
      console.log('Debug: ', JSON.stringify(msg));
    }});

    joinCall();

    htmx.on("#end-call", "click", async (e) => {{
        try {{
            await UVSession.leaveCall();
        }} catch (error) {{
            console.error("Error leaving call:", error);
        }}
    }})
    """

def layout(*args, **kwargs):
    return Main(
        Div(
            Div(*args, **kwargs, cls="mx-auto max-w-3xl"),
            cls="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8",
        )
    )


@rt("/")
def get():
    button = Button("Start call", id="start-button", hx_post="/start", hx_target="#call-mgmt", hx_swap="outerHTML", cls=TW_BUTTON)
    return layout(
        Script(js_on_load, type="module"),
        H1("Genisis - Customer Support Agent", cls="text-xl font-bold mt-8"),
        Div(
            Div(
                "Status: ",
                Span("Waiting", id="call-status", cls="font-bold"),
            ),
            Div(
                "Call ID:",
                Span("N/A", id="call-id", cls="font-bold"),
            ),
            Div(button,
                # hidden end button that will be shown when a call starts
                Button("End call", id="end-button", cls=TW_BUTTON, style="display:none", hx_get="/end", hx_swap="outerHTML"),
            ),
            id="call-mgmt"
        ),
    )

@rt("/start")
async def post():
    # Use your Genisis agent ID
    AGENT_ID = os.environ.get("AGENT_ID", "48bcaeef-6414-44a1-98b2-8085e9654274")  # Your correct agent ID from the response
    
    # Create call using your agent
    r = fixie_request("POST", f"/agents/{AGENT_ID}/calls", json={})
    
    if r.status_code == 201:
        callDetails = r.json()
        js = client_js(callDetails)
        return Div(
            Div(
                "Status: ",
                Span("Initializing", id="call-status", cls="font-bold"),
            ),
            Div(
                "Call ID: ",
                Span(callDetails.get("callId"), id="call-id", cls="font-bold"),
            ),
            Button("End call", id="end-call", cls=TW_BUTTON, hx_get="/end", hx_swap="outerHTML"),
            Div("", id="transcript"),
            Script(code=js),
        )
    else:
        return Div(f"Error: {r.status_code} - {r.text}")

@rt("/end")
def get():
    return Button("Restart", cls=TW_BUTTON, hx_get="/", hx_target="body", hx_boost="false")

serve()
