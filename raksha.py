import streamlit as st
from groq import Groq
import random

# ---------------------------------------------------------
# PART A — Setup + the ONE reusable AI helper (your core idea)
# ---------------------------------------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
MODEL = "llama-3.3-70b-versatile"


def ask_ai(system_prompt, user_text):
    """The single AI helper every tab reuses. Write once, use everywhere."""
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
    )
    return completion.choices[0].message.content


st.set_page_config(page_title="Raksha — Family Digital Safety Guardian",
                    page_icon="🛡️", layout="wide")

# ---------------------------------------------------------
# DESIGN LAYER — custom CSS for a polished, judge-ready look
# ---------------------------------------------------------
st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #0f1419 0%, #1a2332 100%); }

    .hero {
        background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 50%, #be185d 100%);
        padding: 2.2rem 2rem;
        border-radius: 18px;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(124, 58, 237, 0.25);
    }
    .hero h1 {
        color: white; font-size: 2.3rem; margin: 0; font-weight: 800;
        letter-spacing: -0.5px;
    }
    .hero p {
        color: #e0e7ff; font-size: 1.05rem; margin-top: 0.5rem; margin-bottom: 0;
    }

    .stat-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 0.6rem;
    }
    .stat-card .num { font-size: 1.6rem; font-weight: 800; color: #a78bfa; }
    .stat-card .lbl { font-size: 0.8rem; color: #cbd5e1; }

    div[data-testid="stTabs"] button {
        font-size: 1.05rem; font-weight: 600; padding: 0.6rem 1.2rem;
    }

    .result-box {
        background: rgba(255,255,255,0.04);
        border-left: 4px solid #7c3aed;
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
        margin-top: 1rem;
        color: #e5e7eb;
    }

    .footer-tag {
        text-align: center; color: #6b7280; font-size: 0.85rem;
        margin-top: 2.5rem; padding-top: 1rem;
        border-top: 1px solid rgba(255,255,255,0.08);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HERO BANNER
# ---------------------------------------------------------
st.markdown("""
<div class="hero">
    <h1>🛡️ Raksha — Family Digital Safety Guardian</h1>
    <p>Protecting families from online fraud — checks scam messages, inspects suspicious links,
    and teaches people to spot fraud themselves. Built for real families. Works in Telugu.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR — mission + stats (great pitch backdrop)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🛡️ Our Mission")
    st.write(
        "Thousands of Indian families lose money to online scams every day. "
        "Elders are the biggest targets. Raksha protects, inspects, and teaches — "
        "in the family's own language."
    )
    st.markdown("---")
    st.markdown("**Why Raksha wins**")
    st.write("✅ Real problem, real mission\n\n✅ 3 working tools, not 1\n\n✅ Telugu support\n\n✅ One clean `ask_ai()` helper reused everywhere")
    st.markdown("---")
    st.caption("Model: llama-3.3-70b-versatile via Groq")

# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs(
    ["📩 Message Checker", "🔗 Link Inspector", "🎓 Learn & Quiz"]
)

# ---------------------------------------------------------
# PART B — Tab 1: Message Checker
# ---------------------------------------------------------
with tab1:
    st.subheader("Is this message a scam?")
    st.caption("Paste any SMS, WhatsApp, or email you're unsure about.")

    message = st.text_area(
        "Suspicious message:",
        height=160, key="msg",
        placeholder="e.g. Congratulations! You won Rs 10,00,000 in KBC lottery. Pay Rs 5000 fee to claim..."
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        check_clicked = st.button("🔍 Check Message", use_container_width=True)

    if check_clicked:
        if not message.strip():
            st.warning("Please paste a message first.")
        else:
            system = (
                "You are Raksha, a scam-detection guardian. Reply as:\n"
                "Verdict: SAFE / SUSPICIOUS / LIKELY SCAM\n"
                "Risk: Low / Medium / High\n"
                "Warning signs: the exact red flags you found\n"
                "What to do: simple advice.\n"
                "Simple language. If the message is Telugu, reply in Telugu."
            )
            with st.spinner("Analyzing message..."):
                result = ask_ai(system, message)
            st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# PART C — Tab 2: Link Inspector
# ---------------------------------------------------------
with tab2:
    st.subheader("Is this link safe to open?")
    st.caption("Paste any suspicious link or website address — we won't open it, just inspect it.")

    link = st.text_area(
        "Suspicious link:",
        height=100, key="link",
        placeholder="e.g. http://sbi-secure-login.xyz/verify-account"
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        inspect_clicked = st.button("🔍 Inspect Link", use_container_width=True)

    if inspect_clicked:
        if not link.strip():
            st.warning("Please paste a link first.")
        else:
            system = (
                "You are Raksha, a link-safety guardian. Reply as:\n"
                "Verdict: SAFE / SUSPICIOUS / DANGEROUS\n"
                "Reasons: red flags (fake or lookalike domain, misspelled "
                "brand, strange characters, urgency).\n"
                "Advice: what the person should do.\n"
                "Never tell the user to open the link. Simple language; "
                "reply in Telugu if the input is Telugu."
            )
            with st.spinner("Inspecting link..."):
                result = ask_ai(system, link)
            st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# PART D — Tab 3: Learn & Quiz
# ---------------------------------------------------------
with tab3:
    st.subheader("Learn to spot scams")
    st.caption("Get a fresh, realistic scam example with its red flags explained — great for practice.")

    topics = ["lottery/prize", "fake delivery/OTP", "bank KYC update",
              "job offer", "fake tech support", "UPI refund scam"]

    if st.button("🎓 Give me a scam example", use_container_width=False):
        chosen = random.choice(topics)
        system = (
            "You are Raksha, a friendly teacher. Create ONE realistic "
            "scam message that targets Indian families, then list its "
            "red flags in simple points. Keep it short and educational."
        )
        with st.spinner("Creating a practice example..."):
            result = ask_ai(system, f"Give one {chosen} scam example with red flags.")
        st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown(
    '<div class="footer-tag">🛡️ Raksha — Protects. Inspects. Teaches. '
    'Built with one reusable ask_ai() helper across all three tools.</div>',
    unsafe_allow_html=True
)
