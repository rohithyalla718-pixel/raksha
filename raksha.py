import streamlit as st
from groq import Groq
import random
import re

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
# SESSION STATE — impact counters (Feature 1) + example-fill flags (Feature 3)
# ---------------------------------------------------------
if "messages_checked" not in st.session_state:
    st.session_state.messages_checked = 0
if "scams_caught" not in st.session_state:
    st.session_state.scams_caught = 0
if "msg" not in st.session_state:
    st.session_state.msg = ""

# ✅ ADD – Call‑checker counters
if "calls_checked" not in st.session_state:
    st.session_state.calls_checked = 0
if "calls_scams_caught" not in st.session_state:
    st.session_state.calls_scams_caught = 0
if "call_text" not in st.session_state:          # holds the example‑filled text
    st.session_state.call_text = ""


def parse_verdict(result_text):
    """Pull the Verdict line out of the AI's reply. Returns one of
    SAFE / SUSPICIOUS / SCAM / DANGEROUS / None."""
    match = re.search(r"Verdict:\s*([A-Za-z /]+)", result_text)
    if not match:
        return None
    verdict_raw = match.group(1).upper()
    if "SCAM" in verdict_raw or "DANGEROUS" in verdict_raw:
        return "SCAM"
    if "SUSPICIOUS" in verdict_raw:
        return "SUSPICIOUS"
    if "SAFE" in verdict_raw:
        return "SAFE"
    return None


def parse_confidence(result_text):
    """Pull a 'Confidence: 90%' style line out of the AI's reply."""
    match = re.search(r"Confidence:\s*(\d{1,3})\s*%", result_text)
    if match:
        return min(int(match.group(1)), 100)
    return None


def render_verdict(result_text):
    """Feature 2: colour‑coded verdict box, red/yellow/green.
    Falls back to the neutral box if no verdict line is found."""
    verdict = parse_verdict(result_text)
    if verdict == "SCAM":
        st.error(result_text)
    elif verdict == "SUSPICIOUS":
        st.warning(result_text)
    elif verdict == "SAFE":
        st.success(result_text)
    else:
        st.markdown(f'<div class="result-box">{result_text}</div>', unsafe_allow_html=True)

    # Feature 4: confidence indicator
    confidence = parse_confidence(result_text)
    if confidence is not None:
        st.caption(f"How sure am I: {confidence}%")
        st.progress(confidence / 100)

    return verdict


# ---------------------------------------------------------
# TRANSLATIONS — every UI string, per language
# ---------------------------------------------------------
TEXT = {
    "English": {
        "hero_title": "🛡️ Raksha — Family Digital Safety Guardian",
        "hero_sub": "Protecting families from online fraud — checks scam messages, inspects suspicious links, and teaches people to spot fraud themselves. Built for real families. Works in English, Hindi, Telugu, Tamil, and Kannada.",
        "mission_title": "🛡️ Our Mission",
        "mission_text": "Thousands of Indian families lose money to online scams every day. Elders are the biggest targets. Raksha protects, inspects, and teaches — in the family's own language.",
        "lang_label": "🌐 Choose your language",
        "lang_caption": "Raksha will reply in this language:",
        "why_title": "Why Raksha wins",
        "why_bullets": "✅ Real problem, real mission\n\n✅ 3 working tools, not 1\n\n✅ 5 Indian languages supported\n\n✅ One clean ask_ai() helper reused everywhere",
        "model_caption": "Model: llama-3.3-70b-versatile via Groq",
        "tab1": "📩 Message Checker",
        "tab2": "🔗 Link Inspector",
        "tab3": "🎓 Learn & Quiz",
        "tab4": "📞 Call Checker",
        "t1_subheader": "Is this message a scam?",
        "t1_caption": "Paste any SMS, WhatsApp, or email you're unsure about.",
        "t1_placeholder": "e.g. Congratulations! You won Rs 10,00,000 in KBC lottery. Pay Rs 5000 fee to claim...",
        "t1_label": "Suspicious message:",
        "t1_button": "🔍 Check Message",
        "t1_warning": "Please paste a message first.",
        "t1_spinner": "Analyzing message...",
        "t1_examples_label": "🚀 Try an example:",
        "t1_ex_lottery": "🎰 Fake Lottery",
        "t1_ex_bank": "🏦 Fake Bank Alert",
        "t1_ex_delivery": "📦 Fake Delivery",
        "t1_tally": "🛡️ {checked} messages checked, {caught} scams caught",
        "t2_subheader": "Is this link safe to open?",
        "t2_caption": "Paste any suspicious link or website address — we won't open it, just inspect it.",
        "t2_placeholder": "e.g. http://sbi-secure-login.xyz/verify-account",
        "t2_label": "Suspicious link:",
        "t2_button": "🔍 Inspect Link",
        "t2_warning": "Please paste a link first.",
        "t2_spinner": "Inspecting link...",
        "t3_subheader": "Learn to spot scams",
        "t3_caption": "Press the button for a practice example and its red flags.",
        "t3_button": "🎓 Give me a scam example",
        "t3_spinner": "Creating a practice example...",
        # ----- CALL CHECKER strings -----
        "t4_subheader": "Is this phone call a scam?",
        "t4_caption": "Paste a transcript or description of the call you received.",
        "t4_placeholder": "e.g. 'Hello, this is Microsoft Technical Support. Your computer has a virus. Please give us remote access…'",
        "t4_label": "Call transcript / description:",
        "t4_button": "🔍 Check Call",
        "t4_warning": "Please paste a call description first.",
        "t4_spinner": "Analyzing call...",
        "t4_examples_label": "🚀 Try an example:",
        "t4_ex_tech": "💻 Fake Tech Support",
        "t4_ex_irs": "💰 IRS / Tax Scam",
        "t4_ex_bank": "🏦 Bank OTP Scam",
        "t4_tally": "🛡️ {checked} calls checked, {caught} scam calls caught",
        "footer": "🛡️ Raksha — Protects. Inspects. Teaches. Built with one reusable ask_ai() helper across all three tools.",
    },
    "Hindi": {
        "hero_title": "🛡️ रक्षा — पारिवारिक डिजिटल सुरक्षा रक्षक",
        "hero_sub": "ऑनलाइन धोखाधड़ी से परिवारों की सुरक्षा — संदिग्ध संदेशों की जांच, संदिग्ध लिंक की जांच, और लोगों को धोखाधड़ी पहचानना सिखाता है। असली परिवारों के लिए बनाया गया। अंग्रेज़ी, हिंदी, तेलुगु, तमिल और कन्नड़ में उपलब्ध।",
        "mission_title": "🛡️ हमारा मिशन",
        "mission_text": "हर दिन हज़ारों भारतीय परिवार ऑनलाइन धोखाधड़ी में पैसा गंवाते हैं। बुज़ुर्ग सबसे बड़े निशाने पर होते हैं। रक्षा सुरक्षा करता है, जांचता है, और परिवार की अपनी भाषा में सिखाता है।",
        "lang_label": "🌐 अपनी भाषा चुनें",
        "lang_caption": "रक्षा इस भाषा में जवाब देगा:",
        "why_title": "रक्षा क्यों जीतता है",
        "why_bullets": "✅ असली समस्या, असली मिशन\n\n✅ 1 नहीं, 3 काम करने वाले टूल\n\n✅ 5 भारतीय भाषाएँ समर्थित\n\n✅ एक साफ ask_ai() हेल्पर हर जगह उपयोग किया गया",
        "model_caption": "मॉडल: llama-3.3-70b-versatile, Groq द्वारा",
        "tab1": "📩 संदेश जांचक",
        "tab2": "🔗 लिंक निरीक्षक",
        "tab3": "🎓 सीखें और प्रश्नोत्तरी",
        "tab4": "📞 कॉल जांचक",
        "t1_subheader": "क्या यह संदेश धोखाधड़ी है?",
        "t1_caption": "कोई भी संदिग्ध SMS, WhatsApp, या ईमेल यहाँ पेस्ट करें।",
        "t1_placeholder": "जैसे: बधाई हो! आपने KBC लॉटरी में 10,00,000 रुपये जीते हैं। दावा करने के लिए 5000 रुपये फीस भेजें...",
        "t1_label": "संदिग्ध संदेश:",
        "t1_button": "🔍 संदेश जांचें",
        "t1_warning": "कृपया पहले एक संदेश पेस्ट करें।",
        "t1_spinner": "संदेश की जांच हो रही है...",
        "t1_examples_label": "🚀 एक उदाहरण आज़माएं:",
        "t1_ex_lottery": "🎰 फर्जी लॉटरी",
        "t1_ex_bank": "🏦 फर्जी बैंक अलर्ट",
        "t1_ex_delivery": "📦 फर्जी डिलीवरी",
        "t1_tally": "🛡️ {checked} संदेश जांचे गए, {caught} धोखाधड़ी पकड़ी गई",
        "t2_subheader": "क्या यह लिंक खोलना सुरक्षित है?",
        "t2_caption": "कोई भी संदिग्ध लिंक या वेबसाइट पता पेस्ट करें — हम उसे नहीं खोलेंगे, सिर्फ जांचेंगे।",
        "t2_placeholder": "जैसे: http://sbi-secure-login.xyz/verify-account",
        "t2_label": "संदिग्ध लिंक:",
        "t2_button": "🔍 लिंक जांचें",
        "t2_warning": "कृपया पहले एक लिंक पेस्ट करें।",
        "t2_spinner": "लिंक की जांच हो रही है...",
        "t3_subheader": "धोखाधड़ी पहचानना सीखें",
        "t3_caption": "अभ्यास उदाहरण और उसके चेतावनी संकेतों के लिए बटन दबाएं।",
        "t3_button": "🎓 मुझे एक धोखाधड़ी उदाहरण दें",
        "t3_spinner": "अभ्यास उदाहरण बनाया जा रहा है...",
        # ----- CALL CHECKER strings (Hindi) -----
        "t4_subheader": "क्या यह फ़ोन कॉल धोखाधड़ी है?",
        "t4_caption": "कॉल का ट्रांस्क्रिप्ट या विवरण यहाँ पेस्ट करें।",
        "t4_placeholder": "उदाहरण: 'नमस्ते, मैं माइक्रोसॉफ्ट टेक्निकल सपोर्ट से बोल रहा हूँ। आपके कंप्यूटर में वायरस है। कृपया हमें रिमोट एक्सेस दें…'",
        "t4_label": "कॉल ट्रांस्क्रिप्ट / विवरण:",
        "t4_button": "🔍 कॉल जांचें",
        "t4_warning": "कृपया पहले एक कॉल विवरण पेस्ट करें।",
        "t4_spinner": "कॉल का विश्लेषण हो रहा है...",
        "t4_examples_label": "🚀 एक उदाहरण आज़माएं:",
        "t4_ex_tech": "💻 नकली टेक सपोर्ट",
        "t4_ex_irs": "💰 आईआरएस / टैक्स धोखाधड़ी",
        "t4_ex_bank": "🏦 बैंक OTP धोखाधड़ी",
        "t4_tally": "🛡️ {checked} कॉल जांचे गए, {caught} धोखाधड़ी कॉल पकड़ी गई",
        "footer": "🛡️ रक्षा — सुरक्षा करता है। जांचता है। सिखाता है। तीनों टूल में एक ही ask_ai() हेल्पर के साथ बनाया गया।",
    },
    "Telugu": {
        "hero_title": "🛡️
