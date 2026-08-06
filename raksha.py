import streamlit as st
from groq import Groq
import random
import re
import math

# ---------------------------------------------------------
# PART A — Setup + the ONE reusable AI helper
# ---------------------------------------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
MODEL = "llama-3.3-70b-versatile"


def ask_ai(system_prompt, user_text):
    """The single AI helper every tab reuses."""
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
# SESSION STATE
# ---------------------------------------------------------
if "messages_checked" not in st.session_state:
    st.session_state.messages_checked = 0
if "scams_caught" not in st.session_state:
    st.session_state.scams_caught = 0
if "msg" not in st.session_state:
    st.session_state.msg = ""
if "calc_history" not in st.session_state:
    st.session_state.calc_history = []


def parse_verdict(result_text):
    """Pull the Verdict line out of the AI's reply."""
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
    """Feature 2: color-coded verdict box with 3D effect."""
    verdict = parse_verdict(result_text)
    if verdict == "SCAM":
        st.error(result_text)
    elif verdict == "SUSPICIOUS":
        st.warning(result_text)
    elif verdict == "SAFE":
        st.success(result_text)
    else:
        st.markdown(f'<div class="result-box-3d">{result_text}</div>', unsafe_allow_html=True)

    confidence = parse_confidence(result_text)
    if confidence is not None:
        st.caption(f"How sure am I: {confidence}%")
        st.progress(confidence / 100)

    return verdict


# ---------------------------------------------------------
# TRANSLATIONS
# ---------------------------------------------------------
TEXT = {
    "English": {
        "hero_title": "🛡️ Raksha — Family Digital Safety Guardian",
        "hero_sub": "Protecting families from online fraud — checks scam messages, inspects suspicious links, verifies calculations, and teaches people to spot fraud themselves. Built for real families. Works in English, Hindi, Telugu, Tamil, and Kannada.",
        "mission_title": "🛡️ Our Mission",
        "mission_text": "Thousands of Indian families lose money to online scams every day. Elders are the biggest targets. Raksha protects, inspects, verifies, and teaches — in the family's own language.",
        "lang_label": "🌐 Choose your language",
        "lang_caption": "Raksha will reply in this language:",
        "why_title": "Why Raksha wins",
        "why_bullets": "✅ Real problem, real mission\n\n✅ 4 working tools, not 1\n\n✅ 5 Indian languages supported\n\n✅ 3D Effects & Smooth Animations\n\n✅ One clean ask_ai() helper reused everywhere",
        "model_caption": "Model: llama-3.3-70b-versatile via Groq",
        "tab1": "📩 Message Checker",
        "tab2": "🔗 Link Inspector",
        "tab3": "🧮 Calculator Verifier",
        "tab4": "🎓 Learn & Quiz",
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
        "t3_subheader": "🧮 Verify Calculations",
        "t3_caption": "Scammers often use fake math to confuse elders. Paste any calculation and we'll verify it.",
        "t3_placeholder": "e.g. Rs 500 × 12 months = Rs 7000 or You won Rs 25 lakh, pay Rs 5000 fee = net Rs 24,95,000",
        "t3_label": "Calculation to verify:",
        "t3_button": "🧮 Verify Calculation",
        "t3_warning": "Please paste a calculation first.",
        "t3_spinner": "Verifying calculation...",
        "t3_result_correct": "✅ This calculation is CORRECT",
        "t3_result_wrong": "❌ This calculation is WRONG",
        "t3_explanation": "Explanation",
        "t3_tally": "Verification History",
        "t4_subheader": "Learn to spot scams",
        "t4_caption": "Press the button for a practice example and its red flags.",
        "t4_button": "🎓 Give me a scam example",
        "t4_spinner": "Creating a practice example...",
        "footer": "🛡️ Raksha — Protects. Inspects. Verifies. Teaches. With stunning 3D effects and smooth animations.",
    },
    "Hindi": {
        "hero_title": "🛡️ रक्षा — पारिवारिक डिजिटल सुरक्षा रक्षक",
        "hero_sub": "ऑनलाइन धोखाधड़ी से परिवारों की सुरक्षा — संदिग्ध संदेशों की जांच, लिंक की जांच, गणना की पुष्टि, और लोगों को धोखाधड़ी पहचानना सिखाता है। असली परिवारों के लिए। अंग्रेज़ी, हिंदी, तेलुगु, तमिल और कन्नड़ में।",
        "mission_title": "🛡️ हमारा मिशन",
        "mission_text": "हर दिन हज़ारों भारतीय परिवार ऑनलाइन धोखाधड़ी में पैसा गंवाते हैं। रक्षा सुरक्षा करता है, जांचता है, पुष्टि करता है, और सिखाता है।",
        "lang_label": "🌐 अपनी भाषा चुनें",
        "lang_caption": "रक्षा इस भाषा में जवाब देगा:",
        "why_title": "रक्षा क्यों जीतता है",
        "why_bullets": "✅ असली समस्या, असली मिशन\n\n✅ 4 काम करने वाले टूल\n\n✅ 5 भारतीय भाषाएँ\n\n✅ 3D इफेक्ट्स और एनिमेशन\n\n✅ एक साफ ask_ai() हेल्पर",
        "model_caption": "मॉडल: llama-3.3-70b-versatile, Groq द्वारा",
        "tab1": "📩 संदेश जांचक",
        "tab2": "🔗 लिंक निरीक्षक",
        "tab3": "🧮 गणना सत्यापक",
        "tab4": "🎓 सीखें और प्रश्नोत्तरी",
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
        "t2_caption": "कोई भी संदिग्ध लिंक या वेबसाइट पता पेस्ट करें।",
        "t2_placeholder": "जैसे: http://sbi-secure-login.xyz/verify-account",
        "t2_label": "संदिग्ध लिंक:",
        "t2_button": "🔍 लिंक जांचें",
        "t2_warning": "कृपया पहले एक लिंक पेस्ट करें।",
        "t2_spinner": "लिंक की जांच हो रही है...",
        "t3_subheader": "🧮 गणना की पुष्टि करें",
        "t3_caption": "धोखेबाज़ अक्सर बुज़ुर्गों को भ्रमित करने के लिए गलत गणना करते हैं।",
        "t3_placeholder": "जैसे: 500 × 12 महीने = 7000 रुपये या 25 लाख जीते, 5000 फीस = 24,95,000 शुद्ध",
        "t3_label": "गणना की पुष्टि करें:",
        "t3_button": "🧮 गणना सत्यापित करें",
        "t3_warning": "कृपया पहले एक गणना पेस्ट करें।",
        "t3_spinner": "गणना की जांच हो रही है...",
        "t3_result_correct": "✅ यह गणना सही है",
        "t3_result_wrong": "❌ यह गणना गलत है",
        "t3_explanation": "विवरण",
        "t3_tally": "सत्यापन इतिहास",
        "t4_subheader": "धोखाधड़ी पहचानना सीखें",
        "t4_caption": "अभ्यास उदाहरण के लिए बटन दबाएं।",
        "t4_button": "🎓 मुझे एक धोखाधड़ी उदाहरण दें",
        "t4_spinner": "उदाहरण बनाया जा रहा है...",
        "footer": "🛡️ रक्षा — 3D इफेक्ट्स और एनिमेशन के साथ।",
    },
    "Telugu": {
        "hero_title": "🛡️ రక్ష — కుటుంబ డిజిటల్ భద్రతా రక్షకుడు",
        "hero_sub": "ఆన్‌లైన్ మోసాల నుండి కుటుంబాలను రక్షిస్తుంది — సందేశాలను, లింక్‌లను, గణనలను సరిచేస్తుంది.",
        "mission_title": "🛡️ మా లక్ష్యం",
        "mission_text": "ప్రతిరోజూ వేలాది భారతీయ కుటుంబాలు ఆన్‌లైన్ మోసాలలో డబ్బు కోల్పోతున్నాయి.",
        "lang_label": "🌐 మీ భాషను ఎంచుకోండి",
        "lang_caption": "రక్ష ఈ భాషలో సమాధానం ఇస్తుంది:",
        "why_title": "రక్ష ఎందుకు గెలుస్తుంది",
        "why_bullets": "✅ నిజమైన సమస్య\n\n✅ 4 సాధనాలు\n\n✅ 3D ఎఫెక్ట్‌లు\n\n✅ 5 భాషలు",
        "model_caption": "మోడల్: llama-3.3-70b-versatile, Groq ద్వారా",
        "tab1": "📩 సందేశ తనిఖీ",
        "tab2": "🔗 లింక్ పరిశీలన",
        "tab3": "🧮 గణన సత్యాపనం",
        "tab4": "🎓 నేర్చుకోండి",
        "t1_subheader": "ఈ సందేశం మోసమా?",
        "t1_caption": "ఏదైనా సందిగ్ధ సందేశాన్ని పేస్ట్ చేయండి.",
        "t1_placeholder": "ఉదా: KBC లాటరీలో రూ. 10,00,000 గెలుచుకున్నారు...",
        "t1_label": "సందేశం:",
        "t1_button": "🔍 తనిఖీ చేయండి",
        "t1_warning": "దయచేసి సందేశాన్ని పేస్ట్ చేయండి.",
        "t1_spinner": "విశ్లేషిస్తోంది...",
        "t1_examples_label": "🚀 ఉదాహరణ:",
        "t1_ex_lottery": "🎰 నకిలీ లాటరీ",
        "t1_ex_bank": "🏦 నకిలీ బ్యాంక్",
        "t1_ex_delivery": "📦 నకిలీ డెలివరీ",
        "t1_tally": "🛡️ {checked} తనిఖీ, {caught} పట్టుబడ్డ",
        "t2_subheader": "లింక్ సురక్షితమేనా?",
        "t2_caption": "సందిగ్ధ లింక్‌ను పేస్ట్ చేయండి.",
        "t2_placeholder": "ఉదా: http://sbi-secure-login.xyz",
        "t2_label": "లింక్:",
        "t2_button": "🔍 పరిశీలించండి",
        "t2_warning": "లింక్‌ను పేస్ట్ చేయండి.",
        "t2_spinner": "పరిశీలిస్తోంది...",
        "t3_subheader": "🧮 గణన సత్యాపనం",
        "t3_caption": "ధోకెబాజీ గణనలను సరిచేయండి.",
        "t3_placeholder": "ఉదా: 500 × 12 = 7000",
        "t3_label": "గణన:",
        "t3_button": "🧮 సరిచేయండి",
        "t3_warning": "గణనను పేస్ట్ చేయండి.",
        "t3_spinner": "సరిచేస్తోంది...",
        "t3_result_correct": "✅ సరైనది",
        "t3_result_wrong": "❌ తప్పు",
        "t3_explanation": "వివరణ",
        "t3_tally": "చరిత్ర",
        "t4_subheader": "మోసాన్ని నేర్చుకోండి",
        "t4_caption": "ఉదాహరణ కోసం బటన్ నొక్కండి.",
        "t4_button": "🎓 ఉదాహరణ ఇవ్వండి",
        "t4_spinner": "సృష్టిస్తోంది...",
        "footer": "🛡️ రక్ష — 3D ఎఫెక్ట్‌లు మరియు యానిమేషన్‌లు.",
    },
    "Tamil": {
        "hero_title": "🛡️ ரக்ஷா — குடும்ப டிஜிட்டல் பாதுகாவலர்",
        "hero_sub": "ஆன்லைன் மோசடியிலிருந்து குடும்பங்களைப் பாதுகாக்கிறது.",
        "mission_title": "🛡️ எங்கள் நோக்கம்",
        "mission_text": "ஒவ்வொரு நாளும் ஆயிரக்கணக்கான இந்திய குடும்பங்கள் ஆன்லைன் மோசடியில் பணம் இழக்கின்றன.",
        "lang_label": "🌐 மொழியைத் தேர்ந்தெடுக்கவும்",
        "lang_caption": "ரக்ஷா இந்த மொழியில் பதிலளிக்கும்:",
        "why_title": "ரக்ஷா ஏன் வெற்றி பெறுகிறது",
        "why_bullets": "✅ உண்மையான பிரச்சனை\n\n✅ 4 கருவிகள்\n\n✅ 3D விளைவுகள்\n\n✅ 5 மொழிகள்",
        "model_caption": "மாடல்: llama-3.3-70b-versatile, Groq மூலம்",
        "tab1": "📩 செய்தி சரிபார்ப்பு",
        "tab2": "🔗 இணைப்பு ஆய்வு",
        "tab3": "🧮 கணக்கீடு சரிபார்ப்பு",
        "tab4": "🎓 கற்றுக்கொள்ளுங்கள்",
        "t1_subheader": "இந்த செய்தி மோசடியா?",
        "t1_caption": "சந்தேகத்திற்குரிய செய்தியை ஒட்டவும்.",
        "t1_placeholder": "எ.கா: KBC லாட்டரியில் ரூ. 10,00,000 வென்றுள்ளீர்கள்...",
        "t1_label": "செய்தி:",
        "t1_button": "🔍 சரிபார்க்கவும்",
        "t1_warning": "செய்தியை ஒட்டவும்.",
        "t1_spinner": "பகுப்பாய்வு செய்கிறது...",
        "t1_examples_label": "🚀 உதாரணம்:",
        "t1_ex_lottery": "🎰 போலி லாட்டரி",
        "t1_ex_bank": "🏦 போலி வங்கி",
        "t1_ex_delivery": "📦 போலி டெலிவரி",
        "t1_tally": "🛡️ {checked} சரிபார்ப்பு, {caught} பிடிக்கப்பட்டவை",
        "t2_subheader": "இணைப்பு பாதுகாப்பா?",
        "t2_caption": "சந்தேகத்திற்குரிய இணைப்பை ஒட்டவும்.",
        "t2_placeholder": "எ.கா: http://sbi-secure-login.xyz",
        "t2_label": "இணைப்பு:",
        "t2_button": "🔍 ஆய்வு செய்யவும்",
        "t2_warning": "இணைப்பை ஒட்டவும்.",
        "t2_spinner": "ஆய்வு செய்கிறது...",
        "t3_subheader": "🧮 கணக்கீடு சரிபார்ப்பு",
        "t3_caption": "மோசடி கணக்கீடுகளை சரிபார்க்கவும்.",
        "t3_placeholder": "எ.கா: 500 × 12 = 7000",
        "t3_label": "கணக்கீடு:",
        "t3_button": "🧮 சரிபார்க்கவும்",
        "t3_warning": "கணக்கீட்டை ஒட்டவும்.",
        "t3_spinner": "சரிபார்க்கிறது...",
        "t3_result_correct": "✅ சரி",
        "t3_result_wrong": "❌ தவறு",
        "t3_explanation": "விளக்கம்",
        "t3_tally": "வரலாறு",
        "t4_subheader": "மோசடியை கற்றுக்கொள்ளுங்கள்",
        "t4_caption": "உதாரணத்திற்கு பொத்தானை அழுத்தவும்.",
        "t4_button": "🎓 உதாரணம் கொடுங்கள்",
        "t4_spinner": "உருவாக்குகிறது...",
        "footer": "🛡️ ரக்ஷா — 3D விளைவுகள் மற்றும் அனிமேশன்.",
    },
    "Kannada": {
        "hero_title": "🛡️ ರಕ್ಷಾ — ಕುಟುಂಬ ಡಿಜಿಟಲ್ ಸುರಕ್ಷತಾ ರಕ್ಷಕ",
        "hero_sub": "ಆನ್‌ಲೈನ್ ವಂಚನೆಯಿಂದ ಕುಟುಂಬಗಳನ್ನು ರಕ್ಷಿಸುತ್ತದೆ.",
        "mission_title": "🛡️ ನಮ್ಮ ಧ್ಯೇಯ",
        "mission_text": "ಪ್ರತಿದಿನ ಸಾವಿರಾರು ಭಾರತೀಯ ಕುಟುಂಬಗಳು ಆನ್‌ಲೈನ್ ವಂಚನೆಯಲ್ಲಿ ಹಣ ಕಳೆದುಕೊಳ್ಳುತ್ತವೆ.",
        "lang_label": "🌐 ನಿಮ್ಮ ಭಾಷೆ ಆರಿಸಿ",
        "lang_caption": "ರಕ್ಷಾ ಈ ಭಾಷೆಯಲ್ಲಿ ಉತ್ತರಿಸುತ್ತದೆ:",
        "why_title": "ರಕ್ಷಾ ಏಕೆ ಜಿತ್ತುಬೆಳಿಸುತ್ತದೆ",
        "why_bullets": "✅ ನಿಜವಾದ ಸಮಸ್ಯೆ\n\n✅ 4 ಸಾಧನಗಳು\n\n✅ 3D ಪರಿಣಾಮಗಳು\n\n✅ 5 ಭಾಷೆಗಳು",
        "model_caption": "ಮಾದರಿ: llama-3.3-70b-versatile, Groq ಮೂಲಕ",
        "tab1": "📩 ಸಂದೇಶ ಪರಿಶೀಲಕ",
        "tab2": "🔗 ಲಿಂಕ್ ಪರಿಶೀಲನ",
        "tab3": "🧮 ಲೆಕ್ಕಾಚಾರ ಪರಿಶೀಲನ",
        "tab4": "🎓 ಕಲಿಯಿರಿ",
        "t1_subheader": "ಈ ಸಂದೇಶ ವಂಚನೆಯೇ?",
        "t1_caption": "ಅನುಮಾನಾಸ್ಪದ ಸಂದೇಶವನ್ನು ಅಂಟಿಸಿ.",
        "t1_placeholder": "ಉದಾ: KBC ಲಾಟರಿಯಲ್ಲಿ ರೂ. 10,00,000 ಗೆದ್ದಿದ್ದೀರಿ...",
        "t1_label": "ಸಂದೇಶ:",
        "t1_button": "🔍 ಪರಿಶೀಲಿಸಿ",
        "t1_warning": "ಸಂದೇಶ ಅಂಟಿಸಿ.",
        "t1_spinner": "ವಿಶ್ಲೇಷಿಸುತ್ತಿದೆ...",
        "t1_examples_label": "🚀 ಉದಾಹರಣೆ:",
        "t1_ex_lottery": "🎰 ನಕಲಿ ಲಾಟರಿ",
        "t1_ex_bank": "🏦 ನಕಲಿ ಬ್ಯಾಂಕ್",
        "t1_ex_delivery": "📦 ನಕಲಿ ಡೆಲಿವರಿ",
        "t1_tally": "🛡️ {checked} ಪರಿಶೀಲನೆ, {caught} ಹಿಡಿದವು",
        "t2_subheader": "ಲಿಂಕ್ ಸುರಕ್ಷಿತವೇ?",
        "t2_caption": "ಅನುಮಾನಾಸ್ಪದ ಲಿಂಕ್ ಅಂಟಿಸಿ.",
        "t2_placeholder": "ಉದಾ: http://sbi-secure-login.xyz",
        "t2_label": "ಲಿಂಕ್:",
        "t2_button": "🔍 ಪರಿಶೀಲಿಸಿ",
        "t2_warning": "ಲಿಂಕ್ ಅಂಟಿಸಿ.",
        "t2_spinner": "ಪರಿಶೀಲಿಸುತ್ತಿದೆ...",
        "t3_subheader": "🧮 ಲೆಕ್ಕಾಚಾರ ಪರಿಶೀಲನ",
        "t3_caption": "ವಂಚನೆಯ ಲೆಕ್ಕಾಚಾರವನ್ನು ಪರಿಶೀಲಿಸಿ.",
        "t3_placeholder": "ಉದಾ: 500 × 12 = 7000",
        "t3_label": "ಲೆಕ್ಕಾಚಾರ:",
        "t3_button": "🧮 ಪರಿಶೀಲಿಸಿ",
        "t3_warning": "ಲೆಕ್ಕಾಚಾರ ಅಂಟಿಸಿ.",
        "t3_spinner": "ಪರಿಶೀಲಿಸುತ್ತಿದೆ...",
        "t3_result_correct": "✅ ಸರಿಯಾದ",
        "t3_result_wrong": "❌ ತಪ್ಪು",
        "t3_explanation": "ವಿವರಣೆ",
        "t3_tally": "ಇತಿಹಾಸ",
        "t4_subheader": "ವಂಚನೆಯನ್ನು ಕಲಿಯಿರಿ",
        "t4_caption": "ಉದಾಹರಣೆಗಾಗಿ ಬಟನ್ ಒತ್ತಿ.",
        "t4_button": "🎓 ಉದಾಹರಣೆ ನೀಡಿ",
        "t4_spinner": "ರಚಿಸುತ್ತಿದೆ...",
        "footer": "🛡️ ರಕ್ಷಾ — 3D ಪರಿಣಾಮಗಳು ಮತ್ತು ಅನಿಮೇಷನ್‌ಗಳು.",
    },
}

LANGUAGES = ["English", "Hindi", "Telugu", "Tamil", "Kannada"]

EXAMPLES = {
    "lottery": "Congratulations! Your mobile number has won Rs 25,00,000 in the KBC Lucky Draw 2026. To claim your prize, pay a processing fee of Rs 4,999 via UPI to unlock ID KBC2026 within 24 hours or the prize will be cancelled.",
    "bank": "Dear Customer, your SBI account will be BLOCKED today due to KYC expiry. Update immediately by clicking http://sbi-kyc-verify.xyz and entering your card number, CVV and OTP to avoid suspension.",
    "delivery": "Your Amazon package could not be delivered due to an unpaid customs fee of Rs 49. Click http://indpost-delivery.co to pay now and reschedule delivery, or your parcel will be returned.",
}

# ---------------------------------------------------------
# LANGUAGE SELECTION
# ---------------------------------------------------------
with st.sidebar:
    selected_language = st.selectbox(
        TEXT["English"]["lang_label"], LANGUAGES, index=0, key="lang_select"
    )
    L = TEXT[selected_language]

# ---------------------------------------------------------
# ENHANCED 3D DESIGN WITH ANIMATIONS
# ---------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

/* 3D HERO BANNER WITH PERSPECTIVE */
.hero {
    background: linear-gradient(135deg, #4F9DF7 0%, #6FC3A0 100%);
    padding: 2.5rem 2rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    box-shadow: 
        0 20px 60px rgba(79, 157, 247, 0.25),
        0 0 60px rgba(111, 195, 160, 0.15);
    transform: perspective(1200px) rotateX(2deg);
    animation: heroFloating 3s ease-in-out infinite;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    filter: blur(40px);
    animation: orbiting 8s linear infinite;
}

.hero h1 {
    color: white;
    font-size: 2.6rem;
    margin: 0;
    font-weight: 800;
    letter-spacing: -0.8px;
    text-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    position: relative;
    z-index: 1;
    animation: slideInDown 0.8s ease-out;
}

.hero p {
    color: rgba(255, 255, 255, 0.95);
    font-size: 1.1rem;
    margin-top: 0.8rem;
    margin-bottom: 0;
    position: relative;
    z-index: 1;
    animation: slideInUp 0.8s ease-out 0.2s both;
}

/* 3D RESULT BOXES */
.result-box-3d {
    background: linear-gradient(135deg, #F2F5FA 0%, #E8F0FF 100%);
    border-left: 6px solid #1E63D0;
    border-radius: 15px;
    padding: 1.5rem 1.8rem;
    margin-top: 1.2rem;
    color: #1A1A2E;
    box-shadow: 
        0 10px 40px rgba(30, 99, 208, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.8);
    transform: translateY(0) perspective(1000px) rotateX(0deg);
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    animation: slideInUp 0.6s ease-out;
}

.result-box-3d:hover {
    transform: translateY(-5px) perspective(1000px) rotateX(2deg);
    box-shadow: 
        0 20px 60px rgba(30, 99, 208, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.8);
}

/* 3D TALLY BOX */
.tally-box {
    background: linear-gradient(135deg, #EAF6F0 0%, #D4F1E4 100%);
    border: 2px solid #6FC3A0;
    border-radius: 12px;
    padding: 1rem 1.3rem;
    margin-bottom: 1.2rem;
    font-weight: 700;
    color: #1A1A2E;
    box-shadow: 
        0 8px 25px rgba(111, 195, 160, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.6);
    animation: scaleIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* 3D BUTTONS */
button {
    background: linear-gradient(135deg, #4F9DF7 0%, #357ABD 100%);
    border: none;
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 12px;
    font-weight: 700;
    font-size: 1rem;
    cursor: pointer;
    box-shadow: 
        0 8px 20px rgba(79, 157, 247, 0.3),
        0 0 0 0 rgba(79, 157, 247, 0.3);
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    transform: translateY(0);
    animation: buttonPulse 0.3s ease-out;
}

button:hover {
    transform: translateY(-3px);
    box-shadow: 
        0 12px 30px rgba(79, 157, 247, 0.4),
        0 0 20px rgba(79, 157, 247, 0.2);
}

button:active {
    transform: translateY(-1px);
    box-shadow: 
        0 6px 15px rgba(79, 157, 247, 0.3),
        0 0 10px rgba(79, 157, 247, 0.15);
}

/* CALCULATOR CARD 3D */
.calc-card {
    background: linear-gradient(135deg, #FFF9E6 0%, #FFF3CC 100%);
    border: 2px solid #FFB700;
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 
        0 10px 40px rgba(255, 183, 0, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.8);
    transform: perspective(1000px) rotateY(-2deg);
    animation: slideInRight 0.6s ease-out;
}

.calc-card.correct {
    background: linear-gradient(135deg, #E6F9F0 0%, #CCF3E6 100%);
    border-color: #4CAF50;
}

.calc-card.wrong {
    background: linear-gradient(135deg, #FFE6E6 0%, #FFCCCC 100%);
    border-color: #F44336;
}

/* TABS 3D EFFECT */
div[data-testid="stTabs"] {
    margin-top: 1.5rem;
}

div[data-testid="stTabs"] button {
    font-size: 1.05rem;
    font-weight: 700;
    padding: 0.75rem 1.5rem;
    border-radius: 12px 12px 0 0;
    margin-right: 0.3rem;
    box-shadow: 0 -4px 15px rgba(79, 157, 247, 0.1);
    transition: all 0.3s ease-out;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    box-shadow: 
        0 -8px 25px rgba(79, 157, 247, 0.3),
        inset 0 -2px 0 rgba(255, 255, 255, 0.4);
    transform: translateY(-3px);
}

/* TEXT AREA 3D */
textarea {
    border: 2px solid #4F9DF7 !important;
    border-radius: 12px !important;
    box-shadow: 
        0 5px 20px rgba(79, 157, 247, 0.1),
        inset 0 1px 3px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease-out;
    font-family: 'Poppins', sans-serif;
}

textarea:focus {
    border: 2px solid #357ABD !important;
    box-shadow: 
        0 10px 40px rgba(79, 157, 247, 0.25),
        inset 0 1px 3px rgba(0, 0, 0, 0.05);
    transform: scale(1.01);
}

/* ANIMATIONS */
@keyframes heroFloating {
    0%, 100% { transform: perspective(1200px) rotateX(2deg) translateY(0); }
    50% { transform: perspective(1200px) rotateX(2deg) translateY(-10px); }
}

@keyframes orbiting {
    0% { transform: rotate(0deg) translate(200px) rotate(0deg); }
    100% { transform: rotate(360deg) translate(200px) rotate(-360deg); }
}

@keyframes slideInDown {
    from {
        opacity: 0;
        transform: translate3d(0, -50px, 0);
    }
    to {
        opacity: 1;
        transform: translate3d(0, 0, 0);
    }
}

@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translate3d(0, 50px, 0);
    }
    to {
        opacity: 1;
        transform: translate3d(0, 0, 0);
    }
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translate3d(50px, 0, 0) perspective(1000px) rotateY(-5deg);
    }
    to {
        opacity: 1;
        transform: translate3d(0, 0, 0) perspective(1000px) rotateY(0deg);
    }
}

@keyframes scaleIn {
    from {
        opacity: 0;
        transform: scale(0.9);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

@keyframes buttonPulse {
    0% { box-shadow: 0 0 0 0 rgba(79, 157, 247, 0.4); }
    70% { box-shadow: 0 0 0 15px rgba(79, 157, 247, 0); }
    100% { box-shadow: 0 0 0 0 rgba(79, 157, 247, 0); }
}

/* FOOTER */
.footer-tag {
    text-align: center;
    color: #6b7280;
    font-size: 0.95rem;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 2px solid #e5e7eb;
    animation: fadeIn 1s ease-out 0.5s both;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* SMOOTH SCROLL */
html {
    scroll-behavior: smooth;
}

/* PROGRESS BAR 3D */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #4F9DF7 0%, #6FC3A0 100%);
    box-shadow: 0 4px 15px rgba(79, 157, 247, 0.3);
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HERO BANNER
# ---------------------------------------------------------
st.markdown(f"""
<div class="hero">
    <h1>{L['hero_title']}</h1>
    <p>{L['hero_sub']}</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR CONTENT
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
    st.markdown(
        f'<div class="tally-box">{L["t1_tally"].format(checked=st.session_state.messages_checked, caught=st.session_state.scams_caught)}</div>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([L["tab1"], L["tab2"], L["tab3"], L["tab4"]])

# ---------------------------------------------------------
# TAB 1: MESSAGE CHECKER
# ---------------------------------------------------------
with tab1:
    st.subheader(L["t1_subheader"])
    st.caption(L["t1_caption"])

    st.markdown(
        f'<div class="tally-box">{L["t1_tally"].format(checked=st.session_state.messages_checked, caught=st.session_state.scams_caught)}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(f"**{L['t1_examples_label']}**")
    ex_col1, ex_col2, ex_col3 = st.columns(3)
    with ex_col1:
        if st.button(L["t1_ex_lottery"], use_container_width=True, key="ex_lottery"):
            st.session_state.msg = EXAMPLES["lottery"]
            st.rerun()
    with ex_col2:
        if st.button(L["t1_ex_bank"], use_container_width=True, key="ex_bank"):
            st.session_state.msg = EXAMPLES["bank"]
            st.rerun()
    with ex_col3:
        if st.button(L["t1_ex_delivery"], use_container_width=True, key="ex_delivery"):
            st.session_state.msg = EXAMPLES["delivery"]
            st.rerun()

    message = st.text_area(
        L["t1_label"], height=160, key="msg",
        placeholder=L["t1_placeholder"]
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        check_clicked = st.button(L["t1_button"], use_container_width=True, key="check_msg")

    if check_clicked:
        if not message.strip():
            st.warning(L["t1_warning"])
        else:
            system = (
                "You are Raksha, a scam-detection guardian. Reply as:\n"
                "Verdict: SAFE / SUSPICIOUS / LIKELY SCAM\n"
                "Risk: Low / Medium / High\n"
                "Confidence: a percentage from 0 to 100\n"
                "Warning signs: exact red flags you found\n"
                "What to do: simple advice.\n"
                f"Use simple language. Reply entirely in {selected_language}."
            )
            with st.spinner(L["t1_spinner"]):
                result = ask_ai(system, message)

            verdict = render_verdict(result)

            st.session_state.messages_checked += 1
            if verdict == "SCAM":
                st.session_state.scams_caught += 1
            st.rerun()

# ---------------------------------------------------------
# TAB 2: LINK INSPECTOR
# ---------------------------------------------------------
with tab2:
    st.subheader(L["t2_subheader"])
    st.caption(L["t2_caption"])

    link = st.text_area(
        L["t2_label"], height=100, key="link",
        placeholder=L["t2_placeholder"]
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        inspect_clicked = st.button(L["t2_button"], use_container_width=True, key="inspect_link")

    if inspect_clicked:
        if not link.strip():
            st.warning(L["t2_warning"])
        else:
            system = (
                "You are Raksha, a link-safety guardian. Reply as:\n"
                "Verdict: SAFE / SUSPICIOUS / DANGEROUS\n"
                "Confidence: percentage from 0 to 100\n"
                "Reasons: red flags (fake domain, misspellings, urgency).\n"
                "Advice: what person should do. Never tell them to open it.\n"
                f"Use simple language. Reply entirely in {selected_language}."
            )
            with st.spinner(L["t2_spinner"]):
                result = ask_ai(system, link)

            render_verdict(result)

# ---------------------------------------------------------
# TAB 3: CALCULATOR VERIFIER (NEW!)
# ---------------------------------------------------------
with tab3:
    st.subheader(L["t3_subheader"])
    st.caption(L["t3_caption"])

    calc_input = st.text_area(
        L["t3_label"], height=100, key="calc",
        placeholder=L["t3_placeholder"]
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        verify_clicked = st.button(L["t3_button"], use_container_width=True, key="verify_calc")

    if verify_clicked:
        if not calc_input.strip():
            st.warning(L["t3_warning"])
        else:
            system = (
                "You are Raksha, a calculation verifier. Check if the math in this calculation is correct.\n"
                "Reply as:\n"
                "Result: CORRECT or WRONG\n"
                "Explanation: Why this is correct or wrong (simple words)\n"
                "What to watch for: common scam tricks with numbers\n"
                f"Use simple language. Reply entirely in {selected_language}."
            )
            with st.spinner(L["t3_spinner"]):
                result = ask_ai(system, f"Verify this calculation: {calc_input}")

            # Parse result
            is_correct = "CORRECT" in result.upper()
            
            if is_correct:
                st.markdown(
                    f'<div class="calc-card correct">✅ {L["t3_result_correct"]}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="calc-card wrong">❌ {L["t3_result_wrong"]}</div>',
                    unsafe_allow_html=True
                )

            st.markdown(f'<div class="result-box-3d">{result}</div>', unsafe_allow_html=True)
            
            # Store in history
            st.session_state.calc_history.append({
                "input": calc_input,
                "result": is_correct,
                "analysis": result
            })

    # Show history
    if st.session_state.calc_history:
        with st.expander(f"📋 {L['t3_tally']} ({len(st.session_state.calc_history)})"):
            for i, entry in enumerate(reversed(st.session_state.calc_history), 1):
                status = "✅ Correct" if entry["result"] else "❌ Wrong"
                st.write(f"**{i}. {entry['input'][:50]}...** → {status}")

# ---------------------------------------------------------
# TAB 4: LEARN & QUIZ
# ---------------------------------------------------------
with tab4:
    st.subheader(L["t4_subheader"])
    st.write(L["t4_caption"])

    topics = ["lottery/prize", "fake delivery/OTP", "bank KYC update",
              "job offer", "fake tech support", "UPI refund scam"]

    if st.button(L["t4_button"], use_container_width=False, key="learn_example"):
        chosen = random.choice(topics)
        system = (
            "You are Raksha, a friendly teacher. Create ONE realistic "
            "scam message targeting Indian families, then list red flags in simple points. "
            "Keep it short and educational. "
            f"Write entirely in {selected_language}."
        )
        with st.spinner(L["t4_spinner"]):
            result = ask_ai(system, f"Give one {chosen} scam example with red flags.")
        st.markdown(f'<div class="result-box-3d">{result}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown(f'<div class="footer-tag">{L["footer"]}</div>', unsafe_allow_html=True)
