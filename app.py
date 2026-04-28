"""
TalentScout Hiring Assistant — Premium UI
"""

import streamlit as st
import os
from pathlib import Path

try:
    from openai import OpenAI
    from dotenv import load_dotenv
except ImportError:
    st.error("Run: pip3 install openai python-dotenv streamlit")
    st.stop()

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

st.set_page_config(
    page_title="TalentScout AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── PARTICLE NETWORK BACKGROUND ─────────────────────────────────────────────
st.markdown("""
<canvas id="particle-canvas"></canvas>
<script>
(function() {
    const canvas = document.getElementById('particle-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    canvas.style.cssText = `
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        z-index: 0;
        pointer-events: none;
    `;

    let W, H, particles = [];
    const COUNT = 90;
    const MAX_DIST = 140;
    const COLORS = ['rgba(99,51,255,', 'rgba(0,149,255,', 'rgba(167,139,250,'];

    function resize() {
        W = canvas.width  = window.innerWidth;
        H = canvas.height = window.innerHeight;
    }

    function rand(min, max) { return Math.random() * (max - min) + min; }

    function createParticle() {
        return {
            x: rand(0, W), y: rand(0, H),
            vx: rand(-0.4, 0.4), vy: rand(-0.4, 0.4),
            r: rand(1.5, 3),
            color: COLORS[Math.floor(Math.random() * COLORS.length)],
            alpha: rand(0.4, 0.9)
        };
    }

    function init() {
        resize();
        particles = Array.from({ length: COUNT }, createParticle);
    }

    function draw() {
        ctx.clearRect(0, 0, W, H);

        // Draw connections
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < MAX_DIST) {
                    const opacity = (1 - dist / MAX_DIST) * 0.35;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = `rgba(99,51,255,${opacity})`;
                    ctx.lineWidth = 0.8;
                    ctx.stroke();
                }
            }
        }

        // Draw particles
        particles.forEach(p => {
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = p.color + p.alpha + ')';
            ctx.shadowBlur = 8;
            ctx.shadowColor = p.color + '0.8)';
            ctx.fill();
            ctx.shadowBlur = 0;

            // Move
            p.x += p.vx;
            p.y += p.vy;

            // Bounce off edges
            if (p.x < 0 || p.x > W) p.vx *= -1;
            if (p.y < 0 || p.y > H) p.vy *= -1;
        });

        requestAnimationFrame(draw);
    }

    window.addEventListener('resize', () => { resize(); });
    init();
    draw();
})();
</script>
""", unsafe_allow_html=True)

# ─── FULL CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    font-family: 'Inter', sans-serif;
    background: #0a0a0f;
    color: #e8e8f0;
}

/* ── Background ── */
.stApp {
    background:
        radial-gradient(ellipse at 20% 20%, rgba(99,51,255,0.15) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(0,149,255,0.12) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(16,16,32,1) 0%, #0a0a0f 100%);
    min-height: 100vh;
}

/* ── Ensure all content is above canvas ── */
section[data-testid="stSidebar"],
[data-testid="stAppViewContainer"] > .main,
.stChatInput, [data-testid="stChatInput"] {
    position: relative;
    z-index: 1;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header, .stDeployButton { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stAppViewContainer"] > .main { padding: 0; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: rgba(12, 10, 28, 0.95) !important;
    border-right: 1px solid rgba(99,51,255,0.2) !important;
    backdrop-filter: blur(20px);
    width: 320px !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }

/* ── Main content padding ── */
.main .block-container { padding: 2rem 2rem 6rem 2rem !important; }

/* ── Brand header ── */
.brand-header {
    padding: 28px 24px 20px;
    border-bottom: 1px solid rgba(99,51,255,0.15);
    background: linear-gradient(180deg, rgba(99,51,255,0.08) 0%, transparent 100%);
}
.brand-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 4px;
}
.brand-logo-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #6333ff, #0095ff);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    box-shadow: 0 4px 15px rgba(99,51,255,0.4);
}
.brand-name {
    font-size: 1.1rem;
    font-weight: 700;
    color: #fff;
    letter-spacing: 0.3px;
}
.brand-tagline {
    font-size: 0.72rem;
    color: rgba(255,255,255,0.4);
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-left: 46px;
}

/* ── Progress section ── */
.progress-section {
    padding: 20px 24px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.section-label {
    font-size: 0.68rem;
    font-weight: 600;
    color: rgba(255,255,255,0.35);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 14px;
}
.step-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 7px 0;
    transition: all 0.2s;
}
.step-dot {
    width: 22px; height: 22px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.65rem;
    font-weight: 700;
    flex-shrink: 0;
    transition: all 0.3s;
}
.step-dot.done {
    background: linear-gradient(135deg, #6333ff, #0095ff);
    color: white;
    box-shadow: 0 2px 8px rgba(99,51,255,0.5);
}
.step-dot.active {
    background: rgba(99,51,255,0.2);
    border: 2px solid #6333ff;
    color: #a78bfa;
    box-shadow: 0 0 12px rgba(99,51,255,0.3);
}
.step-dot.pending {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    color: rgba(255,255,255,0.25);
}
.step-label {
    font-size: 0.8rem;
    font-weight: 500;
}
.step-label.done { color: rgba(255,255,255,0.7); }
.step-label.active { color: #a78bfa; font-weight: 600; }
.step-label.pending { color: rgba(255,255,255,0.25); }

/* ── Progress bar ── */
.prog-bar-wrap {
    margin-top: 14px;
    background: rgba(255,255,255,0.06);
    border-radius: 99px;
    height: 5px;
    overflow: hidden;
}
.prog-bar-fill {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #6333ff, #0095ff);
    box-shadow: 0 0 10px rgba(99,51,255,0.6);
    transition: width 0.5s ease;
}

/* ── Candidate info cards ── */
.info-section {
    padding: 20px 24px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.info-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 10px 12px;
    margin-bottom: 8px;
    transition: all 0.2s;
}
.info-card:hover { background: rgba(255,255,255,0.06); }
.info-card-label {
    font-size: 0.65rem;
    color: rgba(255,255,255,0.35);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 2px;
}
.info-card-value {
    font-size: 0.82rem;
    color: #e8e8f0;
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* ── New session button ── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, rgba(99,51,255,0.2), rgba(0,149,255,0.2)) !important;
    border: 1px solid rgba(99,51,255,0.4) !important;
    color: #a78bfa !important;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(99,51,255,0.35), rgba(0,149,255,0.35)) !important;
    border-color: rgba(99,51,255,0.7) !important;
    color: #fff !important;
    box-shadow: 0 4px 20px rgba(99,51,255,0.3) !important;
    transform: translateY(-1px) !important;
}

/* ── Page header ── */
.page-header {
    text-align: center;
    padding: 40px 20px 24px;
}
.page-title {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #fff 0%, #a78bfa 50%, #60a5fa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 6px;
    letter-spacing: -0.5px;
}
.page-subtitle {
    font-size: 0.88rem;
    color: rgba(255,255,255,0.4);
    letter-spacing: 0.5px;
}

/* ── Chat container ── */
.chat-wrap {
    max-width: 780px;
    margin: 0 auto;
    padding: 0 16px;
}

/* ── Chat bubbles ── */
.msg-row {
    display: flex;
    align-items: flex-end;
    gap: 10px;
    margin-bottom: 18px;
    animation: fadeSlideIn 0.3s ease forwards;
}
.msg-row.user { flex-direction: row-reverse; }

@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

.avatar {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
    margin-bottom: 2px;
}
.avatar.bot {
    background: linear-gradient(135deg, #6333ff, #0095ff);
    box-shadow: 0 2px 10px rgba(99,51,255,0.4);
}
.avatar.user {
    background: linear-gradient(135deg, #f093fb, #f5576c);
    box-shadow: 0 2px 10px rgba(240,147,251,0.3);
}

.bubble {
    max-width: 68%;
    padding: 12px 16px;
    border-radius: 18px;
    font-size: 0.88rem;
    line-height: 1.6;
    word-wrap: break-word;
}
.bubble.bot {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.09);
    border-bottom-left-radius: 4px;
    color: #e8e8f0;
    backdrop-filter: blur(10px);
}
.bubble.user {
    background: linear-gradient(135deg, rgba(99,51,255,0.5), rgba(0,149,255,0.4));
    border: 1px solid rgba(99,51,255,0.3);
    border-bottom-right-radius: 4px;
    color: #fff;
    text-align: left;
}

/* ── Typing indicator ── */
.typing-row {
    display: flex;
    align-items: flex-end;
    gap: 10px;
    margin-bottom: 18px;
}
.typing-bubble {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 18px;
    border-bottom-left-radius: 4px;
    padding: 14px 18px;
    display: flex;
    gap: 5px;
    align-items: center;
}
.typing-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: rgba(167,139,250,0.7);
    animation: typingBounce 1.2s infinite ease-in-out;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes typingBounce {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
    30% { transform: translateY(-6px); opacity: 1; }
}

/* ── Input area ── */
.input-area {
    position: fixed;
    bottom: 0;
    right: 0;
    left: 320px;
    background: linear-gradient(0deg, rgba(10,10,15,0.98) 70%, transparent);
    padding: 16px 24px 20px;
    z-index: 100;
}
.input-inner {
    max-width: 780px;
    margin: 0 auto;
}

/* ── Chat input override ── */
[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(99,51,255,0.3) !important;
    border-radius: 14px !important;
    backdrop-filter: blur(10px) !important;
    transition: all 0.2s !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: rgba(99,51,255,0.7) !important;
    box-shadow: 0 0 0 3px rgba(99,51,255,0.15), 0 0 20px rgba(99,51,255,0.2) !important;
}
[data-testid="stChatInput"] textarea {
    color: #e8e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: rgba(255,255,255,0.25) !important; }
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #6333ff, #0095ff) !important;
    border-radius: 10px !important;
    border: none !important;
}

/* ── Status pill ── */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99,51,255,0.15);
    border: 1px solid rgba(99,51,255,0.3);
    border-radius: 99px;
    padding: 4px 12px;
    font-size: 0.72rem;
    color: #a78bfa;
    font-weight: 500;
    margin-bottom: 20px;
}
.status-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #6333ff;
    box-shadow: 0 0 6px #6333ff;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ── Session ended ── */
.ended-banner {
    max-width: 780px;
    margin: 0 auto 20px;
    background: rgba(99,51,255,0.1);
    border: 1px solid rgba(99,51,255,0.3);
    border-radius: 14px;
    padding: 16px 20px;
    text-align: center;
    color: #a78bfa;
    font-size: 0.88rem;
    font-weight: 500;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,51,255,0.3); border-radius: 99px; }
</style>
""", unsafe_allow_html=True)

# ─── Constants ───────────────────────────────────────────────────────────────
MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """
You are TalentScout, a professional AI Hiring Assistant for a recruitment agency specializing in technology roles.
Your ONLY purpose is to conduct structured candidate screening interviews. Never deviate from this role.

RULES:
- Ask ONE question at a time. Wait for the answer before proceeding.
- Be concise, warm, and professional.
- Never hallucinate. Stay within the hiring assistant role only.
- If off-topic, politely redirect back.
- If user says "exit", "quit", "bye", "stop" → end the conversation gracefully.
- Validate: email must have "@" and ".", phone must be numeric 7-15 digits.

STAGES (follow in order):
1. GREETING: Introduce yourself as TalentScout Hiring Assistant. Explain purpose. Ask consent.
2. INFO GATHERING (one at a time): Full Name → Email → Phone → Years of Experience → Desired Role(s) → Current Location
3. TECH STACK: Ask candidate to list languages, frameworks, databases, tools they are proficient in.
4. TECHNICAL QUESTIONS: Generate 3-5 questions PER major technology declared. Easy → Medium → Advanced. Ask one at a time. Acknowledge each answer.
5. WRAP UP: Thank candidate. Summarize collected info. Say "Our team will review and reach out within 3-5 business days."

DATA PRIVACY: Handle personal info with discretion. Never repeat phone/email unnecessarily.
FALLBACK: If unclear input, ask for clarification. Never guess.
"""

GREETING_TRIGGER = "Start the conversation. Greet the candidate professionally, introduce yourself as TalentScout Hiring Assistant, explain your purpose, and ask for consent to begin."
EXIT_WORDS = {"exit", "quit", "stop", "bye", "goodbye", "done", "end"}

STEPS = [
    ("Greeting",            "👋"),
    ("Personal Info",       "👤"),
    ("Tech Stack",          "🛠️"),
    ("Technical Questions", "💡"),
    ("Wrap Up",             "✅"),
]

INFO_FIELDS = [
    ("full_name",    "👤", "Full Name"),
    ("email",        "📧", "Email"),
    ("phone",        "📞", "Phone"),
    ("experience",   "🗓️", "Experience"),
    ("desired_role", "💼", "Desired Role"),
    ("location",     "📍", "Location"),
    ("tech_stack",   "🛠️", "Tech Stack"),
]


# ─── OpenAI ──────────────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    try:
        # Streamlit Cloud
        api_key = st.secrets["OPENAI_API_KEY"]
    except:
        # Local fallback
        api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return None

    return OpenAI(api_key=api_key)


def call_openai(history: list[dict]) -> str:
    client = get_client()
    if client is None:
        return "⚠️ API key not found. Add it in Streamlit Secrets or .env"
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
    try:
        resp = client.chat.completions.create(
            model=MODEL, messages=messages, temperature=0.7, max_tokens=800
        )
        return resp.choices[0].message.content
    except Exception as e:
        err = str(e)
        if "401" in err:            return "⚠️ Invalid API key."
        if "429" in err:            return "⚠️ Rate limit hit. Please wait and try again."
        if "quota" in err.lower():  return "⚠️ Quota exceeded. Check your OpenAI billing."
        return f"⚠️ Error: {err}"


# ─── Session state ────────────────────────────────────────────────────────────
for k, v in [("messages", []), ("ended", False), ("greeted", False),
             ("candidate", {}), ("current_step", 0)]:
    if k not in st.session_state:
        st.session_state[k] = v


def detect_info(messages):
    """Heuristically extract candidate info from conversation for sidebar display."""
    info = st.session_state.candidate
    for msg in messages:
        if msg["role"] == "user":
            txt = msg["content"].strip()
            if not info.get("full_name") and 2 <= len(txt.split()) <= 4 and txt.replace(" ","").isalpha():
                info["full_name"] = txt
            if not info.get("email") and "@" in txt and "." in txt:
                info["email"] = txt
            if not info.get("phone") and txt.replace(" ","").replace("+","").replace("-","").isdigit() and 7 <= len(txt.replace(" ","")) <= 15:
                info["phone"] = txt
            if not info.get("experience") and any(w in txt.lower() for w in ["year","yr","yrs","experience"]):
                info["experience"] = txt
    st.session_state.candidate = info


def get_current_step(messages) -> int:
    user_msgs = [m for m in messages if m["role"] == "user"]
    n = len(user_msgs)
    if n == 0:   return 0
    if n <= 6:   return 1
    if n == 7:   return 2
    if n >= 8:   return 3
    return 4


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    # Brand
    st.markdown("""
    <div class="brand-header">
        <div class="brand-logo">
            <div class="brand-logo-icon">🎯</div>
            <span class="brand-name">TalentScout</span>
        </div>
        <div class="brand-tagline">Smart Screening. Smarter Hiring.</div>
    </div>
    """, unsafe_allow_html=True)

    # Progress steps
    current_step = get_current_step(st.session_state.messages)
    total = len(STEPS)
    pct = int((current_step / total) * 100)

    steps_html = '<div class="progress-section"><div class="section-label">Interview Progress</div>'
    for i, (label, icon) in enumerate(STEPS):
        if i < current_step:
            state = "done";   dot_content = "✓"
        elif i == current_step:
            state = "active"; dot_content = str(i + 1)
        else:
            state = "pending"; dot_content = str(i + 1)
        steps_html += f"""
        <div class="step-item">
            <div class="step-dot {state}">{dot_content}</div>
            <span class="step-label {state}">{icon} {label}</span>
        </div>"""
    steps_html += f"""
        <div class="prog-bar-wrap">
            <div class="prog-bar-fill" style="width:{pct}%"></div>
        </div>
    </div>"""
    st.markdown(steps_html, unsafe_allow_html=True)

    # Candidate info
    detect_info(st.session_state.messages)
    info = st.session_state.candidate
    if info:
        cards_html = '<div class="info-section"><div class="section-label">Candidate Profile</div>'
        for key, icon, label in INFO_FIELDS:
            val = info.get(key)
            if val:
                display = val if len(val) <= 28 else val[:25] + "..."
                cards_html += f"""
                <div class="info-card">
                    <div class="info-card-label">{icon} {label}</div>
                    <div class="info-card-value">{display}</div>
                </div>"""
        cards_html += "</div>"
        st.markdown(cards_html, unsafe_allow_html=True)

    # API status
    st.markdown('<div style="padding: 12px 24px 8px;">', unsafe_allow_html=True)
    api_key_check = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

    if api_key_check:
        st.markdown('<div class="status-pill"><div class="status-dot"></div>GPT-4o-mini Connected</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:#f87171;font-size:0.78rem;padding:8px 0;">⚠️ API key missing</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # New session button
    st.markdown('<div style="padding: 8px 24px 24px;">', unsafe_allow_html=True)
    if st.button("↺  Start New Session"):
        for k in ["messages", "ended", "greeted", "candidate", "current_step"]:
            del st.session_state[k]
        get_client.clear()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ─── MAIN AREA ────────────────────────────────────────────────────────────────

# Page header
st.markdown("""
<div class="page-header">
    <div class="page-title">TalentScout AI Hiring Assistant</div>
    <div class="page-subtitle">Smart Screening. Smarter Hiring.</div>
</div>
""", unsafe_allow_html=True)

# Auto-greeting
if not st.session_state.greeted:
    with st.spinner(""):
        greeting = call_openai([{"role": "user", "content": GREETING_TRIGGER}])
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    st.session_state.greeted = True

# Render messages
st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"].replace("\n", "<br>")
    if role == "assistant":
        st.markdown(f"""
        <div class="msg-row bot">
            <div class="avatar bot">🤖</div>
            <div class="bubble bot">{content}</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="msg-row user">
            <div class="avatar user">👤</div>
            <div class="bubble user">{content}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Session ended banner
if st.session_state.ended:
    st.markdown("""
    <div class="chat-wrap">
        <div class="ended-banner">
            ✅ Interview session complete — click <strong>Start New Session</strong> to begin again.
        </div>
    </div>""", unsafe_allow_html=True)

# ─── Chat input ───────────────────────────────────────────────────────────────
if not st.session_state.ended:
    user_input = st.chat_input("Type your response here…")

    if user_input and user_input.strip():
        text = user_input.strip()
        st.session_state.messages.append({"role": "user", "content": text})

        if text.lower() in EXIT_WORDS:
            reply = "Thank you for your time! 🙏 Our team will review your responses and reach out within **3–5 business days**. Best of luck! 🌟"
            st.session_state.ended = True
        else:
            # Show typing indicator while waiting
            placeholder = st.empty()
            placeholder.markdown("""
            <div class="chat-wrap">
                <div class="typing-row">
                    <div class="avatar bot">🤖</div>
                    <div class="typing-bubble">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)
            reply = call_openai(st.session_state.messages)
            placeholder.empty()

        st.session_state.messages.append({"role": "assistant", "content": reply})

        if any(p in reply.lower() for p in ["best of luck", "3-5 business days", "3–5 business days"]):
            st.session_state.ended = True

        st.rerun()
