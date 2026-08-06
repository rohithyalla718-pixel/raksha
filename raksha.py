import streamlit as st
from groq import Groq
import random
import re
import calendar
from datetime import datetime, date, timedelta

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


st.set_page_config(
    page_title="Raksha — Family Digital Safety Guardian",
    page_icon="🛡️",
    layout="wide",
)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "messages_checked" not in st.session_state:
    st.session_state.messages_checked = 0
if "scams_caught" not in st.session_state:
    st.session_state.scams_caught = 0
if "msg" not in st.session_state:
    st.session_state.msg = ""


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
    """Color-coded verdict box with 3D glass effect."""
    verdict = parse_verdict(result_text)
    confidence = parse_confidence(result_text)

    if verdict == "SCAM":
        border_color, glow, icon = "#ef4444", "rgba(239,68,68,0.35)", "🚨"
    elif verdict == "SUSPICIOUS":
        border_color, glow, icon = "#f59e0b", "rgba(245,158,11,0.35)", "⚠️"
    elif verdict == "SAFE":
        border_color, glow, icon = "#10b981", "rgba(16,185,129,0.35)", "🛡️"
    else:
        border_color, glow, icon = "#4F9DF7", "rgba(79,157,247,0.35)", "ℹ️"

    box_html = f"""
    <div class="tilt-hover" style="
        background: rgba(30, 41, 59, 0.75);
        backdrop-filter: blur(12px);
        border: 1px solid {border_color};
        border-radius: 18px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4), 0 0 25px {glow};
        transform-style: preserve-3d;
        transition: transform 0.4s ease, box-shadow 0.4s ease;
    ">
        <div style="font-size: 1.8rem; margin-bottom: 0.5rem; text-shadow: 0 0 15px {glow};">{icon}</div>
        <div style="white-space: pre-wrap; color: #e2e8f0; line-height: 1.6;">{result_text}</div>
    </div>
    """
    st.markdown(box_html, unsafe_allow_html=True)

    if confidence is not None:
        st.caption(f"How sure am I: {confidence}%")
        st.progress(confidence / 100)

    return verdict


# ---------------------------------------------------------
# DATE / CALENDAR VERIFIER LOGIC
# ---------------------------------------------------------
def check_date_validity(date_str: str):
    """Returns (is_valid, parsed_datetime, msg, flags)."""
    flags = []
    s = date_str.strip()
    if not s:
        return False, None, "Empty input", ["No date provided."]

    formats = [
        "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d.%m.%Y",
        "%d/%m/%y", "%m/%d/%y", "%Y/%m/%d",
    ]

    dt = None
    for fmt in formats:
        try:
            dt = datetime.strptime(s, fmt)
            break
        except ValueError:
            continue

    if dt is None:
        return False, None, "Unparseable date", [
            "Could not understand date format. Scammers often use vague or garbled deadlines."
        ]

    is_valid = True
    if dt.year < 1900 or dt.year > 2100:
        flags.append("Year looks unrealistic.")
        is_valid = False

    today = date.today()
    delta = (dt.date() - today).days

    if delta < 0:
        flags.append("This date is in the past.")
    elif delta == 0:
        flags.append("⚡ Urgency tactic: deadline is TODAY.")
    elif delta <= 2:
        flags.append("⚡ Very short deadline — classic pressure tactic.")
    elif delta > 365 * 2:
        flags.append("Suspiciously far future date.")

    if dt.weekday() >= 5:
        flags.append("Falls on a weekend — banks & government offices are usually closed.")

    msg = f"{calendar.day_name[dt.weekday()]}, {dt.strftime('%d %B %Y')}"
    return is_valid, dt, msg, flags


# ---------------------------------------------------------
# TRANSLATIONS
# ---------------------------------------------------------
TEXT = {
    "English": {
        "hero_title": "🛡️ Raksha — Family Digital Safety Guardian",
        "hero_sub": "Protecting families from online fraud — checks scam messages, inspects suspicious links, verifies fake deadlines, and teaches people to spot fraud themselves. Built for real families.",
        "mission_title": "🛡️ Our Mission",
        "mission_text": "Thousands of Indian families lose money to online scams every day. Elders are the biggest targets. Raksha protects, inspects, and teaches — in the family's own language.",
        "lang_label": "🌐 Choose your language",
        "lang_caption": "Raksha will reply in this language:",
        "why_title": "Why Raksha wins",
        "why_bullets": "✅ Real problem, real mission\n\n✅ 4 working safety tools\n\n✅ 5 Indian languages supported\n\n✅ 3D glass UI with live depth effects",
        "model_caption": "Model: llama-3.3-70b-versatile via Groq",
        "tab1": "📩 Message Checker",
        "tab2": "🔗 Link Inspector",
        "tab3": "📅 Date Verifier",
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
        "t3_subheader": "Verify dates & deadlines",
        "t3_caption": "Paste a date from a suspicious message. Raksha checks if it's fake, impossible, or a pressure tactic.",
        "t3_input_label": "Suspicious date / deadline:",
        "t3_date_label": "Or pick a calendar date:",
        "t3_button": "🔍 Verify Date",
        "t3_warning": "Please enter or select a date first.",
        "t3_spinner": "Analyzing date patterns...",
        "t3_valid": "✅ Valid Calendar Date",
        "t3_invalid": "❌ Invalid / Impossible Date",
        "t3_day": "Day of Week",
        "t3_flags": "Date Red Flags",
        "t3_ai_title": "AI Deadline Analysis",
        "t4_subheader": "Learn to spot scams",
        "t4_caption": "Press the button for a practice example and its red flags.",
        "t4_button": "🎓 Give me a scam example",
        "t4_spinner": "Creating a practice example...",
        "footer": "🛡️ Raksha — Protects. Inspects. Teaches. Built with one reusable ask_ai() helper across all four tools.",
    },
    "Hindi": {
        "hero_title": "🛡️ रक्षा — पारिवारिक डिजिटल सुरक्षा रक्षक",
        "hero_sub": "ऑनलाइन धोखाधड़ी से परिवारों की सुरक्षा — संदिग्ध संदेशों की जांच, लिंक और तारीख़ जांच, और धोखाधड़ी पहचानना सिखाता है।",
        "mission_title": "🛡️ हमारा मिशन",
        "mission_text": "हर दिन हज़ारों भारतीय परिवार ऑनलाइन धोखाधड़ी में पैसा गंवाते हैं। बुज़ुर्ग सबसे बड़े निशाने पर होते हैं। रक्षा सुरक्षा करता है, जांचता है, और सिखाता है।",
        "lang_label": "🌐 अपनी भाषा चुनें",
        "why_title": "रक्षा क्यों जीतता है",
        "why_bullets": "✅ असली समस्या, असली मिशन\n\n✅ 4 सुरक्षा टूल\n\n✅ 5 भारतीय भाषाएँ\n\n✅ 3D ग्लास डिज़ाइन",
        "model_caption": "मॉडल: llama-3.3-70b-versatile, Groq द्वारा",
        "tab1": "📩 संदेश जांचक",
        "tab2": "🔗 लिंक निरीक्षक",
        "tab3": "📅 तारीख़ सत्यापक",
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
        "t2_caption": "कोई भी संदिग्ध लिंक या वेबसाइट पता पेस्ट करें — हम उसे नहीं खोलेंगे, सिर्फ जांचेंगे।",
        "t2_placeholder": "जैसे: http://sbi-secure-login.xyz/verify-account",
        "t2_label": "संदिग्ध लिंक:",
        "t2_button": "🔍 लिंक जांचें",
        "t2_warning": "कृपया पहले एक लिंक पेस्ट करें।",
        "t2_spinner": "लिंक की जांच हो रही है...",
        "t3_subheader": "तारीख़ और डेडलाइन सत्यापित करें",
        "t3_caption": "किसी संदिग्ध संदेश से तारीख़ पेस्ट करें — क्या यह नकली, असंभव, या दबाव का तरीका है?",
        "t3_input_label": "संदिग्ध तारीख़ / डेडलाइन:",
        "t3_date_label": "या कैलेंडर से चुनें:",
        "t3_button": "🔍 तारीख़ सत्यापित करें",
        "t3_warning": "कृपया पहले तारीख़ दर्ज करें या चुनें।",
        "t3_spinner": "तारीख़ पैटर्न का विश्लेषण हो रहा है...",
        "t3_valid": "✅ वैध कैलेंडर तारीख़",
        "t3_invalid": "❌ अवैध / असंभव तारीख़",
        "t3_day": "सप्ताह का दिन",
        "t3_flags": "तारीख़ से जुड़े ख़तरे",
        "t3_ai_title": "AI दबाव विश्लेषण",
        "t4_subheader": "धोखाधड़ी पहचानना सीखें",
        "t4_caption": "अभ्यास उदाहरण और उसके चेतावनी संकेतों के लिए बटन दबाएं।",
        "t4_button": "🎓 मुझे एक धोखाधड़ी उदाहरण दें",
        "t4_spinner": "अभ्यास उदाहरण बनाया जा रहा है...",
        "footer": "🛡️ रक्षा — सुरक्षा करता है। जांचता है। सिखाता है।",
    },
    "Telugu": {
        "hero_title": "🛡️ రక్ష — కుటుంబ డిజిటల్ భద్రతా రక్షకుడు",
        "hero_sub": "ఆన్‌లైన్ మోసాల నుండి కుటుంబాలను రక్షిస్తుంది — సందేశాలు, లింక్‌లు, తేదీలను తనిఖీ చేస్తుంది, మోసాన్ని గుర్తించడం నేర్పిస్తుంది.",
        "mission_title": "🛡️ మా లక్ష్యం",
        "mission_text": "ప్రతిరోజూ వేలాది భారతీయ కుటుంబాలు ఆన్‌లైన్ మోసాలలో డబ్బు కోల్పోతున్నాయి. వృద్ధులు అత్యధికంగా లక్ష్యంగా ఉంటారు. రక్ష రక్షిస్తుంది, పరిశీలిస్తుంది, నేర్పిస్తుంది.",
        "lang_label": "🌐 మీ భాషను ఎంచుకోండి",
        "why_title": "రక్ష ఎందుకు గెలుస్తుంది",
        "why_bullets": "✅ నిజమైన సమస్య, నిజమైన లక్ష్యం\n\n✅ 4 భద్రతా సాధనాలు\n\n✅ 5 భారతీయ భాషలు",
        "model_caption": "మోడల్: llama-3.3-70b-versatile, Groq ద్వారా",
        "tab1": "📩 సందేశ తనిఖీ",
        "tab2": "🔗 లింక్ పరిశీలన",
        "tab3": "📅 తేదీ ధృవీకరణ",
        "tab4": "🎓 నేర్చుకోండి & క్విజ్",
        "t1_subheader": "ఈ సందేశం మోసమా?",
        "t1_caption": "మీకు అనుమానం ఉన్న ఏదైనా SMS, WhatsApp, లేదా ఇమెయిల్‌ను పేస్ట్ చేయండి.",
        "t1_placeholder": "ఉదా: అభినందనలు! మీరు KBC లాటరీలో రూ. 10,00,000 గెలుచుకున్నారు...",
        "t1_label": "అనుమానాస్పద సందేశం:",
        "t1_button": "🔍 సందేశాన్ని తనిఖీ చేయండి",
        "t1_warning": "దయచేసి ముందుగా ఒక సందేశాన్ని పేస్ట్ చేయండి.",
        "t1_spinner": "సందేశాన్ని విశ్లేషిస్తోంది...",
        "t1_examples_label": "🚀 ఒక ఉదాహరణ ప్రయత్నించండి:",
        "t1_ex_lottery": "🎰 నకిలీ లాటరీ",
        "t1_ex_bank": "🏦 నకిలీ బ్యాంక్ అలర్ట్",
        "t1_ex_delivery": "📦 నకిలీ డెలివరీ",
        "t1_tally": "🛡️ {checked} సందేశాలు తనిఖీ చేయబడ్డాయి, {caught} మోసాలు పట్టుబడ్డాయి",
        "t2_subheader": "ఈ లింక్ తెరవడం సురక్షితమేనా?",
        "t2_caption": "ఏదైనా అనుమానాస్పద లింక్ పేస్ట్ చేయండి — మేము దానిని తెరవం.",
        "t2_placeholder": "ఉదా: http://sbi-secure-login.xyz/verify-account",
        "t2_label": "అనుమానాస్పద లింక్:",
        "t2_button": "🔍 లింక్‌ను పరిశీలించండి",
        "t2_warning": "దయచేసి ముందుగా ఒక లింక్‌ను పేస్ట్ చేయండి.",
        "t2_spinner": "లింక్‌ను పరిశీలిస్తోంది...",
        "t3_subheader": "తేదీలు & డెడ్‌లైన్‌లను ధృవీకరించండి",
        "t3_caption": "అనుమానాస్పద సందేశంలోని తేదీని పేస్ట్ చేయండి — అది నకిలీ, అసాధ్యం, లేదా ఒత్తిడి ತంత్రమా?",
        "t3_input_label": "అనుమానాస్పద తేదీ / డెడ్‌లైన్:",
        "t3_date_label": "లేదా క్యాలెండర్ నుండి ఎంచుకోండి:",
        "t3_button": "🔍 తేదీని ధృవీకరించండి",
        "t3_warning": "దయచేసి ముందుగా తేదీని నమోదు చేయండి లేదా ఎంచుకోండి.",
        "t3_spinner": "తేదీ నమూనాలను విశ్లేషిస్తోంది...",
        "t3_valid": "✅ చెల్లుబాటు అయ్యే క్యాలెండర్ తేదీ",
        "t3_invalid": "❌ చెల్లని / అసాధ్యమైన తేదీ",
        "t3_day": "వారంలో రోజు",
        "t3_flags": "తేదీ ఎరుపు జెండాలు",
        "t3_ai_title": "AI ఒత్తిడి విశ్లేషణ",
        "t4_subheader": "మోసాన్ని గుర్తించడం నేర్చుకోండి",
        "t4_caption": "ప్రాక్టీస్ ఉదాహరణ మరియు దాని హెచ్చరిక సంకేతాల కోసం బటన్ నొక్కండి.",
        "t4_button": "🎓 నాకు ఒక మోస ఉదాహరణ ఇవ్వండి",
        "t4_spinner": "ప్రాక్టీస్ ఉదాహరణను సృష్టిస్తోంది...",
        "footer": "🛡️ రక్ష — రక్షిస్తుంది. పరిశీలిస్తుంది. నేర్పిస్తుంది.",
    },
    "Tamil": {
        "hero_title": "🛡️ ரக்ஷா — குடும்ப டிஜிட்டல் பாதுகாவலர்",
        "hero_sub": "ஆன்லைன் மோசடியிலிருந்து குடும்பங்களைப் பாதுகாக்கிறது — செய்திகள், இணைப்புகள், தேதிகளை சரிபார்க்கிறது, மோசடியை கண்டறிய கற்றுக்கொடுக்கிறது.",
        "mission_title": "🛡️ எங்கள் நோக்கம்",
        "mission_text": "ஒவ்வொரு நாளும் ஆயிரக்கணக்கான இந்திய குடும்பங்கள் ஆன்லைன் மோசடியில் பணத்தை இழக்கின்றன. முதியவர்களே அதிக இலக்கு.",
        "lang_label": "🌐 உங்கள் மொழியைத் தேர்ந்தெடுக்கவும்",
        "why_title": "ரக்ஷா ஏன் வெற்றி பெறுகிறது",
        "why_bullets": "✅ உண்மையான பிரச்சனை, உண்மையான நோக்கம்\n\n✅ 4 பாதுகாப்பு கருவிகள்\n\n✅ 5 இந்திய மொழிகள்",
        "model_caption": "மாடல்: llama-3.3-70b-versatile, Groq மூலம்",
        "tab1": "📩 செய்தி சரிபார்ப்பு",
        "tab2": "🔗 இணைப்பு ஆய்வு",
        "tab3": "📅 தேதி சரிபார்ப்பு",
        "tab4": "🎓 கற்றுக்கொள் & வினாடி வினா",
        "t1_subheader": "இந்த செய்தி மோசடியா?",
        "t1_caption": "நீங்கள் சந்தேகிக்கும் எந்த SMS, WhatsApp, அல்லது மின்னஞ்சலையும் ஒட்டவும்.",
        "t1_placeholder": "எ.கா: வாழ்த்துக்கள்! நீங்கள் KBC லாட்டரியில் ரூ. 10,00,000 வென்றுள்ளீர்கள்...",
        "t1_label": "சந்தேகத்திற்குரிய செய்தி:",
        "t1_button": "🔍 செய்தியை சரிபார்க்கவும்",
        "t1_warning": "முதலில் ஒரு செய்தியை ஒட்டவும்.",
        "t1_spinner": "செய்தியை பகுப்பாய்வு செய்கிறது...",
        "t1_examples_label": "🚀 ஒரு எடுத்துக்காட்டை முயற்சிக்கவும்:",
        "t1_ex_lottery": "🎰 போலி லாட்டரி",
        "t1_ex_bank": "🏦 போலி வங்கி எச்சரிக்கை",
        "t1_ex_delivery": "📦 போலி டெலிவரி",
        "t1_tally": "🛡️ {checked} செய்திகள் சரிபார்க்கப்பட்டன, {caught} மோசடிகள் பிடிக்கப்பட்டன",
        "t2_subheader": "இந்த இணைப்பைத் திறப்பது பாதுகாப்பானதா?",
        "t2_caption": "சந்தேகத்திற்குரிய இணைப்பை ஒட்டவும் — நாங்கள் அதைத் திறக்க மாட்டோம்.",
        "t2_placeholder": "எ.கா: http://sbi-secure-login.xyz/verify-account",
        "t2_label": "சந்தேகத்திற்குரிய இணைப்பு:",
        "t2_button": "🔍 இணைப்பை ஆய்வு செய்யவும்",
        "t2_warning": "முதலில் ஒரு இணைப்பை ஒட்டவும்.",
        "t2_spinner": "இணைப்பை ஆய்வு செய்கிறது...",
        "t3_subheader": "தேதிகள் & காலக்கெடுகளை சரிபார்க்கவும்",
        "t3_caption": "சந்தேகத்திற்குரிய செய்தியிலிருந்து ஒரு தேதியை ஒட்டவும் — அது போலியா, அசாத்தியமா, அல்லது அழுத்த தந்திரமா?",
        "t3_input_label": "சந்தேகத்திற்குரிய தேதி / காலக்கெடு:",
        "t3_date_label": "அல்லது ஒரு தேதியைத் தேர்ந்தெடுக்கவும்:",
        "t3_button": "🔍 தேதியை சரிபார்க்கவும்",
        "t3_warning": "முதலில் ஒரு தேதியை உள்ளிடவும் அல்லது தேர்ந்தெடுக்கவும்.",
        "t3_spinner": "தேதி முறைகளை பகுப்பாய்வு செய்கிறது...",
        "t3_valid": "✚ சரியான காலெண்டர் தேதி",
        "t3_invalid": "❌ தவறான / அசாத்தியமான தேதி",
        "t3_day": "வார நாள்",
        "t3_flags": "தேதி எச்சரிக்கைகள்",
        "t3_ai_title": "AI அழுத்த பகுப்பாய்வு",
        "t4_subheader": "மோசடியை கண்டறிய கற்றுக்கொள்ளுங்கள்",
        "t4_caption": "பயிற்சி எடுத்துக்காட்டு மற்றும் அதன் எச்சரிக்கை அறிகுறிகளுக்கு பொத்தானை அழுத்தவும்.",
        "t4_button": "🎓 எனக்கு ஒரு மோசடி எடுத்துக்காட்டு கொடுங்கள்",
        "t4_spinner": "பயிற்சி எடுத்துக்காட்டை உருவாக்குகிறது...",
        "footer": "🛡️ ரக்ஷா — பாதுகாக்கிறது. ஆய்வு செய்கிறது. கற்றுக்கொடுக்கிறது.",
    },
    "Kannada": {
        "hero_title": "🛡️ ರಕ್ಷಾ — ಕುಟುಂಬ ಡಿಜಿಟಲ್ ಸುರಕ್ಷತಾ ರಕ್ಷಕ",
        "hero_sub": "ಆನ್‌ಲೈನ್ ವಂಚನೆಯಿಂದ ಕುಟುಂಬಗಳನ್ನು ರಕ್ಷಿಸುತ್ತದೆ — ಸಂದೇಶ, ಲಿಂಕ್, ದಿನಾಂಕ ಪರಿಶೀಲನೆ ಮತ್ತು ವಂಚನೆ ಪಾಠ.",
        "mission_title": "🛡️ ನಮ್ಮ ಧ್ಯೇಯ",
        "mission_text": "ಪ್ರತಿದಿನ ಸಾವಿರಾರು ಭಾರತೀಯ ಕುಟುಂಬಗಳು ಆನ್‌ಲೈನ್ ವಂಚನೆಯಲ್ಲಿ ಹಣ ಕಳೆದುಕೊಳ್ಳುತ್ತವೆ. ಹಿರಿಯರೇ ಅತಿ ದೊಡ್ಡ ಗುರಿ.",
        "lang_label": "🌐 ನಿಮ್ಮ ಭಾಷೆಯನ್ನು ಆರಿಸಿ",
        "why_title": "ರಕ್ಷಾ ಏಕೆ ಗೆಲ್ಲುತ್ತದೆ",
        "why_bullets": "✅ ನಿಜವಾದ ಸಮಸ್ಯೆ, ನಿಜವಾದ ಧ್ಯೇಯ\n\n✅ 4 ಸುರಕ್ಷತಾ ಸಾಧನಗಳು\n\n✅ 5 ಭಾರತೀಯ ಭಾಷೆಗಳು",
        "model_caption": "ಮಾದರಿ: llama-3.3-70b-versatile, Groq ಮೂಲಕ",
        "tab1": "📩 ಸಂದೇಶ ಪರಿಶೀಲಕ",
        "tab2": "🔗 ಲಿಂಕ್ ಪರಿಶೀಲಕ",
        "tab3": "📅 ದಿನಾಂಕ ದೃಢೀಕರಣ",
        "tab4": "🎓 ಕಲಿಯಿರಿ & ರಸಪ್ರಶ್ನೆ",
        "t1_subheader": "ಈ ಸಂದೇಶ ವಂಚನೆಯೇ?",
        "t1_caption": "ನೀವು ಅನುಮಾನಿಸುವ ಯಾವುದೇ SMS, WhatsApp, ಅಥವಾ ಇಮೇಲ್ ಅನ್ನು ಅಂಟಿಸಿ.",
        "t1_placeholder": "ಉದಾ: ಅಭಿನಂದನೆಗಳು! ನೀವು KBC ಲಾಟರಿಯಲ್ಲಿ ರೂ. 10,00,000 ಗೆದ್ದಿದ್ದೀರಿ...",
        "t1_label": "ಸಂಶಯಾಸ್ಪದ ಸಂದೇಶ:",
        "t1_button": "🔍 ಸಂದೇಶವನ್ನು ಪರಿಶೀಲಿಸಿ",
        "t1_warning": "ದಯವಿಟ್ಟು ಮೊದಲು ಸಂದೇಶವನ್ನು ಅಂಟಿಸಿ.",
        "t1_spinner": "ಸಂದೇಶವನ್ನು ವಿಶ್ಲೇಷಿಸುತ್ತಿದೆ...",
        "t1_examples_label": "🚀 ಒಂದು ಉದಾಹರಣೆ ಪ್ರಯತ್ನಿಸಿ:",
        "t1_ex_lottery": "🎰 ನಕಲಿ ಲಾಟರಿ",
        "t1_ex_bank": "🏦 ನಕಲಿ ಬ್ಯಾಂಕ್ ಎಚ್ಚರಿಕೆ",
        "t1_ex_delivery": "📦 ನಕಲಿ ಡೆಲಿವರಿ",
        "t1_tally": "🛡️ {checked} ಸಂದೇಶಗಳನ್ನು ಪರಿಶೀಲಿಸಲಾಗಿದೆ, {caught} ವಂಚನೆಗಳು ಪತ್ತೆಯಾಗಿವೆ",
        "t2_subheader": "ಈ ಲಿಂಕ್ ತೆರೆಯಲು ಸುರಕ್ಷಿತವೇ?",
        "t2_caption": "ಯಾವುದೇ ಸಂಶಯಾಸ್ಪದ ಲಿಂಕ್ ಅಥವಾ ವೆಬ್‌ಸೈಟ್ ವಿಳಾಸವನ್ನು ಅಂಟಿಸಿ.",
        "t2_placeholder": "ಉದಾ: http://sbi-secure-login.xyz/verify-account",
        "t2_label": "ಸಂಶಯಾಸ್ಪದ ಲಿಂಕ್:",
        "t2_button": "🔍 ಲಿಂಕ್ ಅನ್ನು ಪರಿಶೀಲಿಸಿ",
        "t2_warning": "ದಯವಿಟ್ಟು ಮೊದಲು ಲಿಂಕ್ ಅನ್ನು ಅಂಟಿಸಿ.",
        "t2_spinner": "ಲಿಂಕ್ ಅನ್ನು ಪರಿಶೀಲಿಸುತ್ತಿದೆ...",
        "t3_subheader": "ದಿನಾಂಕಗಳು ಮತ್ತು ಗಡುವುಗಳನ್ನು ಪರಿಶೀಲಿಸಿ",
        "t3_caption": "ಸಂಶಯಾಸ್ಪದ ಸಂದೇಶದಿಂದ ದಿನಾಂಕವನ್ನು ಅಂಟಿಸಿ — ಅದು ನಕಲಿ, ಅಸಾಧ್ಯ, ಅಥವಾ ಒತ್ತಡ ಸಾಧನವೇ?",
        "t3_input_label": "ಸಂಶಯಾಸ್ಪದ ದினಾಂಕ / ಗಡುವು:",
        "t3_date_label": "ಅಥವಾ ಕ್ಯಾಲೆಂಡರ್‌ನಿಂದ ಆಯ್ಕೆಮಾಡಿ:",
        "t3_button": "🔍 ದಿನಾಂಕವನ್ನು ಪರಿಶೀಲಿಸಿ",
        "t3_warning": "ದಯವಿಟ್ಟು ಮೊದಲು ದಿನಾಂಕವನ್ನು ನಮೂದಿಸಿ ಅಥವಾ ಆಯ್ಕೆಮಾಡಿ.",
        "t3_spinner": "ದಿನಾಂಕ ವ champions ವಿಶ್ಲೇಷಿಸುತ್ತಿದೆ...",
        "t3_valid": "✅ ಮಾನ್ಯ ಕ್ಯಾಲೆಂಡರ್ ದಿನಾಂಕ",
        "t3_invalid": "❌ ಅಮಾನ್ಯ / ಅಸಾಧ್ಯ ದಿನಾಂಕ",
        "t3_day": "ವಾರದ ದಿನ",
        "t3_flags": "ದಿನಾಂಕ ಎಚ್ಚರಿಕೆಗಳು",
        "t3_ai_title": "AI ಒತ್ತಡ ವಿಶ್ಲೇಷಣೆ",
        "t4_subheader": "ವಂಚನೆಯನ್ನು ಗುರುತಿಸಲು ಕಲಿಯಿರಿ",
        "t4_caption": "ಅಭ್ಯಾಸ ಉದಾಹರಣೆ ಮತ್ತು ಅದರ ಎಚ್ಚರಿಕೆ ಚಿಹ್ನೆಗಳಿಗಾಗಿ ಬಟನ್ ಒತ್ತಿ.",
        "t4_button": "🎓 ನನಗೆ ಒಂದು ವಂಚನೆ ಉದಾಹರಣೆ ನೀಡಿ",
        "t4_spinner": "ಅಭ್ಯಾಸ ಉದಾಹರಣೆಯನ್ನು ರಚಿಸುತ್ತಿದೆ...",
        "footer": "🛡️ ರಕ್ಷಾ — ರಕ್ಷಿಸುತ್ತದೆ. ಪರಿಶೀಲಿಸುತ್ತದೆ. ಕಲಿಸುತ್ತದೆ.",
    },
}

LANGUAGES = ["English", "Hindi", "Telugu", "Tamil", "Kannada"]

# ---------------------------------------------------------
# Language selector (must be first)
# ---------------------------------------------------------
with st.sidebar:
    selected_language = st.selectbox(
        "🌐 Choose your language", LANGUAGES, index=0, key="lang_select"
    )
    L = TEXT[selected_language]

# ---------------------------------------------------------
# 3D GLASSMORPHISM DESIGN SYSTEM
# ---------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

html, body, .stApp {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #0b1120 0%, #1e293b 100%);
    color: #e2e8f0;
}

/* Animated ambient background blobs */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background:
        radial-gradient(circle at 15% 25%, rgba(79,157,247,0.12) 0%, transparent 40%),
        radial-gradient(circle at 85% 75%, rgba(111,195,160,0.12) 0%, transparent 40%),
        radial-gradient(circle at 50% 50%, rgba(99,102,241,0.08) 0%, transparent 50%);
    z-index: -1;
    animation: bgShift 12s ease-in-out infinite alternate;
}
@keyframes bgShift {
    0% { transform: scale(1) translate(0,0); }
    100% { transform: scale(1.08) translate(-1%, -1%); }
}

/* Sidebar glass */
[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.95) !important;
    backdrop-filter: blur(24px) saturate(180%) !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Hero 3D Float */
.hero-3d-wrap {
    perspective: 1200px;
    transform-style: preserve-3d;
    margin-bottom: 2rem;
}
.hero-card {
    background: rgba(30, 41, 59, 0.65);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 24px;
    padding: 2.5rem;
    transform: translateZ(40px) rotateX(2deg);
    box-shadow:
        0 25px 60px rgba(0,0,0,0.5),
        0 0 0 1px rgba(255,255,255,0.06),
        inset 0 1px 0 rgba(255,255,255,0.1);
    animation: heroFloat 7s ease-in-out infinite;
    transition: transform 0.5s ease;
}
.hero-3d-wrap:hover .hero-card {
    transform: translateZ(60px) rotateX(0deg) rotateY(0deg);
}
@keyframes heroFloat {
    0%, 100% { transform: translateZ(40px) translateY(0px) rotateX(2deg); }
    50% { transform: translateZ(50px) translateY(-10px) rotateX(-1deg); }
}
.hero-card h1 {
    color: #f8fafc;
    font-size: 2.4rem;
    margin: 0;
    font-weight: 800;
    letter-spacing: -0.5px;
    text-shadow: 0 0 30px rgba(79,157,247,0.3);
}
.hero-card p {
    color: #cbd5e1;
    font-size: 1.08rem;
    margin-top: 0.6rem;
    margin-bottom: 0;
    line-height: 1.6;
}

/* 3D Buttons */
.stButton > button {
    background: linear-gradient(135deg, #4F9DF7, #6366f1) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.7rem 1.8rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
    transform-style: preserve-3d;
    box-shadow:
        0 12px 20px -4px rgba(79,157,247,0.45),
        0 4px 8px -2px rgba(79,157,247,0.25) !important;
    position: relative;
    overflow: hidden;
}
.stButton > button::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(rgba(255,255,255,0.2), transparent);
    opacity: 0;
    transition: opacity 0.3s;
}
.stButton > button:hover {
    transform: translateY(-4px) translateZ(20px) rotateX(5deg) scale(1.02) !important;
    box-shadow:
        0 24px 40px -6px rgba(79,157,247,0.55),
        0 10px 15px -4px rgba(79,157,247,0.35) !important;
}
.stButton > button:hover::after {
    opacity: 1;
}
.stButton > button:active {
    transform: translateY(1px) rotateX(12deg) scale(0.97) !important;
}

/* Glass Inputs */
.stTextArea textarea, .stTextInput input, div[data-baseweb="input"] input {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    backdrop-filter: blur(4px) !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #4F9DF7 !important;
    box-shadow: 0 0 0 4px rgba(79,157,247,0.2) !important;
}

/* Tab 3D */
div[data-testid="stTabs"] button {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 12px 12px 0 0 !important;
    border: none !important;
    color: #94a3b8 !important;
    font-weight: 600 !important;
    padding: 0.7rem 1.4rem !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    background: rgba(79,157,247,0.18) !important;
    color: #60a5fa !important;
    transform: translateZ(8px) translateY(-2px);
    box-shadow: 0 -6px 20px rgba(79,157,247,0.15) !important;
    border-bottom: 2px solid #4F9DF7 !important;
}

/* Progress glow */
.stProgress > div > div {
    background: linear-gradient(90deg, #4F9DF7, #6FC3A0) !important;
    box-shadow: 0 0 12px rgba(79,157,247,0.6);
    border-radius: 999px;
}

/* Tally box */
.tally-box-3d {
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16,185,129,0.35);
    border-radius: 14px;
    padding: 1rem;
    backdrop-filter: blur(10px);
    transform: translateZ(10px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
    font-weight: 700;
    color: #34d399;
    text-shadow: 0 0 12px rgba(52,211,153,0.25);
}

/* Calendar card */
.cal-card {
    background: rgba(30,41,59,0.6);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.2rem;
    backdrop-filter: blur(8px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    transform: translateZ(5px);
    transition: transform 0.3s ease;
}
.cal-card:hover {
    transform: translateY(-4px) translateZ(15px);
}

/* Footer */
.footer-tag {
    text-align: center;
    color: #64748b;
    font-size: 0.85rem;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.06);
}

/* Smooth tilt interaction helper */
.tilt-hover {
    transition: transform 0.1s linear;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HERO BANNER (3D)
# ---------------------------------------------------------
st.markdown(f"""
<div class="hero-3d-wrap">
    <div class="hero-card">
        <h1>{L['hero_title']}</h1>
        <p>{L['hero_sub']}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR
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
        f'<div class="tally-box-3d">{L["t1_tally"].format(checked=st.session_state.messages_checked, caught=st.session_state.scams_caught)}</div>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# EXAMPLE SCAMS
# ---------------------------------------------------------
EXAMPLES = {
    "lottery": "Congratulations! Your mobile number has won Rs 25,00,000 in the KBC Lucky Draw 2026. To claim your prize, pay a processing fee of Rs 4,999 via UPI to unlock ID KBC2026 within 24 hours or the prize will be cancelled.",
    "bank": "Dear Customer, your SBI account will be BLOCKED today due to KYC expiry. Update immediately by clicking http://sbi-kyc-verify.xyz and entering your card number, CVV and OTP to avoid suspension.",
    "delivery": "Your Amazon package could not be delivered due to an unpaid customs fee of Rs 49. Click http://indpost-delivery.co to pay now and reschedule delivery, or your parcel will be returned.",
}

# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([L["tab1"], L["tab2"], L["tab3"], L["tab4"]])

# ---------------------------------------------------------
# TAB 1 — Message Checker
# ---------------------------------------------------------
with tab1:
    st.subheader(L["t1_subheader"])
    st.caption(L["t1_caption"])

    st.markdown(
        f'<div class="tally-box-3d">{L["t1_tally"].format(checked=st.session_state.messages_checked, caught=st.session_state.scams_caught)}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(f"**{L['t1_examples_label']}**")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button(L["t1_ex_lottery"], use_container_width=True):
            st.session_state.msg = EXAMPLES["lottery"]
            st.rerun()
    with c2:
        if st.button(L["t1_ex_bank"], use_container_width=True):
            st.session_state.msg = EXAMPLES["bank"]
            st.rerun()
    with c3:
        if st.button(L["t1_ex_delivery"], use_container_width=True):
            st.session_state.msg = EXAMPLES["delivery"]
            st.rerun()

    message = st.text_area(
        L["t1_label"], height=160, key="msg", placeholder=L["t1_placeholder"]
    )

    if st.button(L["t1_button"], use_container_width=False):
        if not message.strip():
            st.warning(L["t1_warning"])
        else:
            system = (
                "You are Raksha, a scam-detection guardian. Reply as:\n"
                "Verdict: SAFE / SUSPICIOUS / LIKELY SCAM\n"
                "Risk: Low / Medium / High\n"
                "Confidence: a percentage from 0 to 100\n"
                "Warning signs: exact red flags found\n"
                "What to do: simple advice.\n"
                f"Use very simple, everyday language. Reply entirely in {selected_language}, "
                "regardless of what language the input message is in."
            )
            with st.spinner(L["t1_spinner"]):
                result = ask_ai(system, message)

            verdict = render_verdict(result)
            st.session_state.messages_checked += 1
            if verdict == "SCAM":
                st.session_state.scams_caught += 1

# ---------------------------------------------------------
# TAB 2 — Link Inspector
# ---------------------------------------------------------
with tab2:
    st.subheader(L["t2_subheader"])
    st.caption(L["t2_caption"])

    link = st.text_area(
        L["t2_label"], height=100, key="link", placeholder=L["t2_placeholder"]
    )

    if st.button(L["t2_button"], use_container_width=False):
        if not link.strip():
            st.warning(L["t2_warning"])
        else:
            system = (
                "You are Raksha, a link-safety guardian. Reply as:\n"
                "Verdict: SAFE / SUSPICIOUS / DANGEROUS\n"
                "Confidence: 0-100%\n"
                "Reasons: red flags (fake domain, misspelled brand, strange characters, urgency).\n"
                "Advice: what the person should do.\n"
                "Never tell the user to open the link. "
                f"Use simple language. Reply entirely in {selected_language}."
            )
            with st.spinner(L["t2_spinner"]):
                result = ask_ai(system, link)

            render_verdict(result)

# ---------------------------------------------------------
# TAB 3 — Date / Calendar Verifier (NEW)
# ---------------------------------------------------------
with tab3:
    st.subheader(L["t3_subheader"])
    st.caption(L["t3_caption"])

    dc1, dc2 = st.columns([2, 3])

    with dc1:
        date_text = st.text_input(
            L["t3_input_label"],
            placeholder="e.g. 30/02/2025 or Pay by 31st Aug",
        )
        picker_date = st.date_input(
            L["t3_date_label"], value=date.today(), key="date_picker"
        )

    with dc2:
        st.markdown(
            f"""
            <div class="cal-card" style="height: 100%;">
                <strong style="color:#4F9DF7;">📅 {L['t3_ai_title']}</strong>
                <p style="color:#94a3b8; font-size:0.95rem; margin-top:0.5rem;">
                    Raksha checks calendar validity, impossible dates, weekend traps, and urgency pressure tactics commonly used in payment scams.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.button(L["t3_button"], use_container_width=False):
        raw = date_text.strip()
        if not raw:
            # use picker
            raw = picker_date.strftime("%d/%m/%Y")

        is_valid, dt, msg, flags = check_date_validity(raw)

        # Glass result card
        if is_valid:
            card_border = "rgba(16,185,129,0.4)"
            card_glow = "rgba(16,185,129,0.25)"
            status_icon = "✅"
            status_text = L["t3_valid"]
        else:
            card_border = "rgba(239,68,68,0.4)"
            card_glow = "rgba(239,68,68,0.25)"
            status_icon = "🚨"
            status_text = L["t3_invalid"]

        flag_html = ""
        if flags:
            flag_html = "<ul style='margin:0.5rem 0 0 1.2rem; padding:0;'>"
            for f in flags:
                flag_html += f"<li style='margin-bottom: 0.3rem;'>{f}</li>"
            flag_html += "</ul>"

        st.markdown(
            f"""
            <div class="tilt-hover" style="
                background: rgba(30,41,59,0.7);
                backdrop-filter: blur(10px);
                border: 1px solid {card_border};
                border-radius: 18px;
                padding: 1.5rem;
                margin: 1.2rem 0;
                box-shadow: 0 15px 35px rgba(0,0,0,0.4), 0 0 25px {card_glow};
            ">
                <div style="font-size: 1.3rem; font-weight: 800; margin-bottom: 0.6rem;">
                    {status_icon} {status_text}
                </div>
                <div style="margin-bottom: 0.8rem;"><strong>Result:</strong> {msg}</div>
                <div style="color:#cbd5e1;"><strong>{L['t3_flags']}:</strong>{flag_html if flags else '<div style="margin-top:0.3rem;">No obvious date red flags.</div>'}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # AI analysis on the deadline context
        system = (
            "You are Raksha, a scam-detection guardian analyzing deadlines and dates. "
            "Reply as:\n"
            "Verdict: SAFE / SUSPICIOUS / LIKELY SCAM\n"
            "Confidence: 0-100%\n"
            "Date Analysis: Is this an impossible date? Weekend pressure? Fake urgency?\n"
            "Advice: What should the user do?\n"
            f"Use very simple language. Reply entirely in {selected_language}."
        )
        with st.spinner(L["t3_spinner"]):
            ai_result = ask_ai(system, f"The user found this deadline / date in a message: '{raw}'. Analysis?")

        st.markdown(f"<div style='margin-top:0.8rem; color:#94a3b8; font-weight:600;'>{L['t3_ai_title']}</div>", unsafe_allow_html=True)
        render_verdict(ai_result)

# ---------------------------------------------------------
# TAB 4 — Learn & Quiz
# ---------------------------------------------------------
with tab4:
    st.subheader(L["t4_subheader"])
    st.write(L["t4_caption"])

    topics = [
        "lottery/prize", "fake delivery/OTP", "bank KYC update",
        "job offer", "fake tech support", "UPI refund scam",
    ]

    if st.button(L["t4_button"], use_container_width=False):
        chosen = random.choice(topics)
        system = (
            "You are Raksha, a friendly teacher. Create ONE realistic scam message "
            "targeting Indian families, then list its red flags in simple points. "
            "Keep it short and educational. "
            f"Write entirely in {selected_language}."
        )
        with st.spinner(L["t4_spinner"]):
            result = ask_ai(system, f"Give one {chosen} scam example with red flags.")

        st.markdown(
            f"""
            <div class="tilt-hover" style="
                background: rgba(30,41,59,0.7);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(79,157,247,0.35);
                border-radius: 18px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 15px 35px rgba(0,0,0,0.4), 0 0 20px rgba(79,157,247,0.2);
            ">
                <pre style="white-space: pre-wrap; font-family: inherit; color: #e2e8f0; margin:0;">{result}</pre>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown(f'<div class="footer-tag">{L["footer"]}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Interactive 3D Tilt Engine (injected once)
# ---------------------------------------------------------
st.components.v1.html(
    """
    <script>
    document.querySelectorAll('.tilt-hover').forEach(card => {
        card.addEventListener('mousemove', e => {
            const r = card.getBoundingClientRect();
            const x = e.clientX - r.left;
            const y = e.clientY - r.top;
            const cx = r.width / 2;
            const cy = r.height / 2;
            const rx = (y - cy) / -15;
            const ry = (x - cx) / 15;
            card.style.transform = `perspective(1000px) rotateX(${rx}deg) rotateY(${ry}deg) translateZ(20px)`;
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateZ(0)';
        });
    });
    </script>
    """,
    height=0,
    width=0,
)
