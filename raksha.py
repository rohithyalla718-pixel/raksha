import streamlit as st
from groq import Groq
import random
import re

# ---------------------------------------------------------
# PART A — Setup + the ONE reusable AI helper (your core idea)
# ---------------------------------------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
MODEL = "llama-3.3-70b-versatile"


def ask_ai(system_prompt: str, user_text: str) -> str:
    """Send a prompt + user text to Groq and return the raw reply."""
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
    )
    return completion.choices[0].message.content


st.set_page_config(
    page_title="Raksha — Family Digital Safety Guardian",
    page_icon="🛡️",
    layout="wide",
)

# ---------------------------------------------------------
# SESSION STATE — counters, example placeholders, etc.
# ---------------------------------------------------------
for key, default in {
    "messages_checked": 0,
    "scams_caught": 0,
    "suspicious_caught": 0,
    "links_checked": 0,
    "dangerous_links": 0,
    "calls_checked": 0,
    "spam_calls_caught": 0,
    "suspicious_calls": 0,
    "example_text": "",
    "call_number_example": "",
    "call_context_example": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ---------------------------------------------------------
# HELPERS – verdict & confidence parsing + coloured rendering
# ---------------------------------------------------------
def parse_verdict(text: str) -> str | None:
    """Return one of SAFE / SUSPICIOUS / SCAM / None."""
    m = re.search(r"Verdict:\s*([A-Za-z /]+)", text, re.IGNORECASE)
    if not m:
        # fallback search for common keywords
        up = text.upper()
        if any(k in up for k in ["LIKELY SCAM", "DANGEROUS", "SPAM", "SCAM"]):
            return "SCAM"
        if "SUSPICIOUS" in up:
            return "SUSPICIOUS"
        if "SAFE" in up or "LEGITIMATE" in up:
            return "SAFE"
        return None

    raw = m.group(1).upper()
    if any(k in raw for k in ["LIKELY SCAM", "SCAM", "DANGEROUS", "SPAM"]):
        return "SCAM"
    if "SUSPICIOUS" in raw:
        return "SUSPICIOUS"
    if "SAFE" in raw or "LEGITIMATE" in raw:
        return "SAFE"
    return None


def parse_confidence(text: str) -> int | None:
    m = re.search(r"Confidence:\s*(\d{1,3})\s*%", text)
    if m:
        return min(int(m.group(1)), 100)
    return None


def render_verdict(raw_text: str) -> str | None:
    """Shows a coloured box + confidence bar and returns the verdict."""
    verdict = parse_verdict(raw_text)

    # ---- coloured verdict box ------------------------------------------------
    if verdict == "SCAM":
        st.error("🚨 **LIKELY SCAM / SPAM DETECTED**")
        bg = "#FEE2E2"
        border = "#DC2626"
        color = "#991B1B"
    elif verdict == "SUSPICIOUS":
        st.warning("⚠️ **SUSPICIOUS — Be Careful**")
        bg = "#FEF3C7"
        border = "#D97706"
        color = "#92400E"
    elif verdict == "SAFE":
        st.success("✅ **SAFE — Looks Legitimate**")
        bg = "#D1FAE5"
        border = "#059669"
        color = "#065F46"
    else:
        st.markdown(
            f'<div class="result-box">{raw_text}</div>',
            unsafe_allow_html=True,
        )
        bg = border = color = None

    if verdict:
        st.markdown(
            f"""<div style="
                background:{bg};
                border-left:5px solid {border};
                border-radius:10px;
                padding:1.2rem 1.4rem;
                margin-top:0.5rem;
                color:{color};
                line-height:1.7;">{raw_text}</div>""",
            unsafe_allow_html=True,
        )

    # ---- confidence bar -------------------------------------------------------
    conf = parse_confidence(raw_text)
    if conf is not None:
        if verdict == "SCAM":
            conf_color = "#DC2626"
        elif verdict == "SUSPICIOUS":
            conf_color = "#D97706"
        else:
            conf_color = "#059669"

        st.markdown(
            f"""<div style="margin-top:1rem; padding:0.6rem 1rem;
                background:#F8FAFC; border-radius:8px; border:1px solid #E2E8F0;">
                <span style="font-weight:700; font-size:1rem;">
                🎯 Confidence Level:
                <span style="color:{conf_color}; font-size:1.2rem;">{conf}%</span>
                </span>
                </div>""",
            unsafe_allow_html=True,
        )
        st.progress(conf / 100)

    return verdict


# ---------------------------------------------------------
# TRANSLATIONS – UI strings for 5 languages
# ---------------------------------------------------------
TEXT = {
    "English": {
        "hero_title": "🛡️ Raksha — Family Digital Safety Guardian",
        "hero_sub": "Protecting families from online fraud — checks scam messages, inspects suspicious links, verifies spam calls, and teaches people to spot fraud themselves.",
        "mission_title": "🛡️ Our Mission",
        "mission_text": "Thousands of Indian families lose money to online scams every day. Elders are the biggest targets. Raksha protects, inspects, verifies, and teaches — in the family's own language.",
        "lang_label": "🌐 Choose your language",
        "why_title": "Why Raksha wins",
        "why_bullets": "✅ Real problem, real mission\n\n✅ 4 working tools\n\n✅ 5 Indian languages\n\n✅ One clean ask_ai() helper reused everywhere",
        "model_caption": "Model: llama-3.3-70b-versatile via Groq",
        "tab1": "📩 Message Checker",
        "tab2": "🔗 Link Inspector",
        "tab3": "📞 Call Verifier",
        "tab4": "🎓 Learn & Quiz",
        # ---- Tab‑1 strings ----------------------------------------------------
        "t1_subheader": "Is this message a scam?",
        "t1_caption": "Paste any SMS, WhatsApp, or email you're unsure about.",
        "t1_placeholder": "e.g. Congratulations! You won Rs 10,00,000 in KBC lottery...",
        "t1_label": "Suspicious message:",
        "t1_button": "🔍 Check Message",
        "t1_warning": "Please paste a message first.",
        "t1_spinner": "Analyzing message...",
        "t1_examples_label": "🚀 Try an example (one‑click demo!):",
        "t1_ex_lottery": "🎰 Fake Lottery",
        "t1_ex_bank": "🏦 Fake Bank Alert",
        "t1_ex_delivery": "📦 Fake Delivery",
        "t1_tally": "🛡️ {checked} messages checked, {caught} scams caught, {suspicious} suspicious",
        # ---- Tab‑2 strings ----------------------------------------------------
        "t2_subheader": "Is this link safe to open?",
        "t2_caption": "Paste any suspicious link — we won't open it, just inspect it.",
        "t2_placeholder": "e.g. http://sbi-secure-login.xyz/verify-account",
        "t2_label": "Suspicious link:",
        "t2_button": "🔍 Inspect Link",
        "t2_warning": "Please paste a link first.",
        "t2_spinner": "Inspecting link...",
        "t2_tally": "🔗 {links} links inspected, {dangerous} dangerous found",
        # ---- Tab‑3 strings (Call Verifier) ------------------------------------
        "t3_subheader": "📞 Is this call / number spam?",
        "t3_caption": "Enter the phone number AND describe what the caller said. Raksha will analyse the patterns and red flags.",
        "t3_number_label": "Phone number:",
        "t3_number_placeholder": "+91 9876543210",
        "t3_context_label": "What did the caller say? (describe the call):",
        "t3_context_placeholder": "e.g. Someone called saying they are from SBI bank and my account will be blocked. They asked for my OTP and card details...",
        "t3_button": "📞 Verify Call",
        "t3_warning": "Please enter a phone number and describe what the caller said.",
        "t3_spinner": "Analyzing call pattern...",
        "t3_examples_label": "🚀 Try an example call:",
        "t3_ex_bank_call": "🏦 Fake Bank Call",
        "t3_ex_insurance": "📋 Fake Insurance",
        "t3_ex_police": "🚔 Fake Police/CBI",
        "t3_tally": "📞 {calls} calls verified, {spam} spam detected, {suspicious} suspicious",
        # ---- Tab‑4 strings ----------------------------------------------------
        "t4_subheader": "Learn to spot scams",
        "t4_caption": "Press the button for a practice example and its red flags.",
        "t4_button": "🎓 Give me a scam example",
        "t4_spinner": "Creating a practice example...",
        "footer": "🛡️ Raksha — Protects. Inspects. Verifies. Teaches. Built with one reusable ask_ai() helper across all four tools.",
    },

    # -------------------------------------------------------------------------
    #   The rest of the languages (Hindi, Telugu, Tamil, Kannada) are identical in
    #   structure – only the strings change. For brevity they have been omitted
    #   from this snippet, but **they exist in the original file**. You can copy‑paste
    #   them from the previous version you posted.
    # -------------------------------------------------------------------------
}


LANGUAGES = ["English", "Hindi", "Telugu", "Tamil", "Kannada"]

# ---------------------------------------------------------
# Sample data – messages, links, calls
# ---------------------------------------------------------
EXAMPLES = {
    "lottery": "Congratulations! Your mobile number has won Rs 25,00,000 in the KBC Lucky Draw 2026. To claim your prize, pay a processing fee of Rs 4,999 via UPI to unlock ID KBC2026 within 24 hours or the prize will be cancelled.",
    "bank": "Dear Customer, your SBI account will be BLOCKED today due to KYC expiry. Update immediately by clicking http://sbi-kyc-verify.xyz and entering your card number, CVV and OTP to avoid suspension.",
    "delivery": "Your Amazon package could not be delivered due to an unpaid customs fee of Rs 49. Click http://indpost-delivery.co to pay now and reschedule delivery, or your parcel will be returned.",
}

CALL_EXAMPLES = {
    "bank_call": {
        "number": "+91 8800123456",
        "context": "Someone called saying they are from SBI Bank's fraud department. They said my account has been compromised and I need to immediately share my OTP and debit card CVV number to 'secure' my account. They said if I don't do it in 10 minutes, all my money will be stolen.",
    },
    "insurance": {
        "number": "+91 7700987654",
        "context": "A person called claiming to be from LIC Insurance. They said I have an unclaimed policy maturity amount of Rs 3,50,000. To release the funds, they asked me to pay Rs 2,500 as 'processing fee' via Google Pay. They said the offer expires today.",
    },
    "police": {
        "number": "+91 6600456789",
        "context": "Someone called claiming to be a CBI officer. They said a case has been registered against my Aadhaar number for money laundering. They said I need to transfer Rs 50,000 to a 'government verification account' or they will arrest me within 2 hours. They sent a fake arrest warrant on WhatsApp.",
    },
}

# ---------------------------------------------------------
# Language selector (must run before any UI)
# ---------------------------------------------------------
with st.sidebar:
    selected_language = st.selectbox(
        "🌐 Choose your language", LANGUAGES, index=0, key="lang_select"
    )
    L = TEXT[selected_language]

# ---------------------------------------------------------
# DESIGN & CSS
# ---------------------------------------------------------
st.markdown(
    """
<style>
.hero {
    background: linear-gradient(135deg, #1E3A5F 0%, #2D6A4F 50%, #40916C 100%);
    padding: 2.5rem 2rem;
    border-radius: 18px;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(30,58,95,.25);
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute;
    top: -50%; right: -20%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(255,255,255,.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero h1 { color:white; font-size:2.3rem; margin:0; font-weight:800; text-shadow:0 2px 4px rgba(0,0,0,.2); }
.hero p { color:#D8F3DC; font-size:1.05rem; margin-top:.5rem; margin-bottom:0; }

div[data-testid="stTabs"] button { font-size:1.05rem; font-weight:600; padding:.6rem 1.2rem; }
div[data-testid="stTabs"] button[aria-selected="true"] { border-bottom:3px solid #2D6A4F; color:#1E3A5F; }

.result-box { background:#F2F5FA; border-left:5px solid #1E63D0; border-radius:10px; padding:1.2rem 1.4rem; margin-top:1rem; color:#1A1A2E; line-height:1.7; }

.tally-box {
    background:linear-gradient(135deg,#D8F3DC,#B7E4C7);
    border:1px solid #40916C;
    border-radius:12px;
    padding:.8rem 1.2rem;
    margin-bottom:1rem;
    font-weight:600;
    color:#1B4332;
    box-shadow:0 2px 8px rgba(45,106,79,.15);
}
.stats-grid {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:.8rem;
    margin-bottom:1rem;
}
.stat-card {
    background:white;
    border-radius:12px;
    padding:1rem;
    text-align:center;
    box-shadow:0 2px 8px rgba(0,0,0,.06);
    border:1px solid #E2E8F0;
}
.stat-card .number { font-size:1.8rem; font-weight:800; color:#1E3A5F; }
.stat-card .label { font-size:.8rem; color:#64748B; margin-top:.2rem; }

.call-info-box {
    background:linear-gradient(135deg,#EEF2FF,#E0E7FF);
    border-left:5px solid #6366F1;
    border-radius:10px;
    padding:1.2rem 1.4rem;
    margin:1rem 0;
}
.call-info-box h4 { color:#4338CA; margin:0 0 .5rem 0; }
.call-info-box p { color:#3730A3; margin:.2rem 0; font-size:.95rem; }

.footer-tag {
    text-align:center; color:#6b7280; font-size:.85rem;
    margin-top:2.5rem; padding-top:1rem;
    border-top:1px solid #e5e7eb;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# HERO BANNER
# ---------------------------------------------------------
st.markdown(
    f"""
<div class="hero">
    <h1>{L['hero_title']}</h1>
    <p>{L['hero_sub']}</p>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# SIDEBAR – Impact Dashboard
# ---------------------------------------------------------
with st.sidebar:
    st.markdown(f"### {L['mission_title']}")
    st.write(L["mission_text"])
    st.markdown("---")
    st.markdown(f"**{L['why_title']}**")
    st.write(L["why_bullets"])
    st.markdown("---")
    st.caption(L["model_caption"])
    st.markdown("---")

    total_checks = (
        st.session_state.messages_checked
        + st.session_state.links_checked
        + st
