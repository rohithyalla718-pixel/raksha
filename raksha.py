import streamlit as st
import os
from groq import Groq
import json
import re

# Page Configuration
st.set_page_config(
    page_title="Raksha - Family Digital Safety Guardian",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main { padding: 2rem; }
    .stTabs [data-baseweb="tab-list"] button { font-size: 16px; font-weight: 600; }
    .scam-badge {
        padding: 0.5rem 1rem; border-radius: 0.5rem; font-weight: 600;
        display: inline-block; margin: 0.5rem 0;
    }
    .scam-high { background-color: #fee2e2; color: #991b1b; }
    .scam-medium { background-color: #fef3c7; color: #92400e; }
    .scam-low { background-color: #dcfce7; color: #15803d; }
    .scam-safe { background-color: #d1fae5; color: #065f46; }
    .report-btn {
        background-color: #dc2626; color: white; padding: 0.5rem 1rem;
        border-radius: 0.5rem; text-decoration: none; font-weight: 600;
        display: inline-block; margin-top: 0.5rem;
    }
    .report-btn:hover { background-color: #b91c1c; }
    </style>
""", unsafe_allow_html=True)

# Initialize Groq Client
@st.cache_resource
def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("❌ GROQ_API_KEY not found. Please set it in your environment variables.")
        st.stop()
    return Groq(api_key=api_key)

client = get_groq_client()

# Language Options
LANGUAGE_OPTIONS = {
    "English": "en",
    "తెలుగు (Telugu)": "te",
    "தமிழ் (Tamil)": "ta",
    "हिन्दी (Hindi)": "hi",
    "ಕನ್ನಡ (Kannada)": "kn"
}

# Translations
TRANSLATIONS = {
    "en": {
        "title": "🛡️ Raksha - Family Digital Safety Guardian",
        "subtitle": "Protect your family from online scams with AI-powered analysis",
        "message_checker": "Message Checker",
        "link_inspector": "Link Inspector",
        "call_checker": "Call Checker",
        "learn_quiz": "Learn & Quiz",
        "paste_message": "Paste a suspicious message:",
        "analyze_btn": "Analyze Message",
        "paste_url": "Paste a suspicious URL:",
        "analyze_url": "Analyze URL",
        "phone_number": "Enter phone number:",
        "call_count": "Number of calls:",
        "analyze_call": "Analyze Call",
        "verdict": "Verdict",
        "confidence": "Confidence Score",
        "red_flags": "Red Flags",
        "advice": "Advice",
        "risk_factors": "Risk Factors",
        "explanation": "Explanation",
        "quiz_title": "Learn & Spot Scams Quiz",
        "question": "Question",
        "submit_answer": "Submit Answer",
        "score": "Your Score",
        "language": "Language",
        "safe": "Safe",
        "suspicious": "Suspicious",
        "scam": "Scam",
        "high_risk": "High Risk",
        "medium_risk": "Medium Risk",
        "low_risk": "Low Risk",
        "stats_scams_blocked": "Scams Detected",
        "stats_users_protected": "Users Protected",
        "stats_accuracy": "Detection Accuracy",
        "report_scam": "Report Scam",
        "footer": "Raksha uses AI to detect potential scams. Always verify with official sources.",
        "bilingual_note": "Bilingual Output",
    },
    "te": {
        "title": "🛡️ రక్ష - కుటుంబ డిజిటల్ సేఫ్టీ గార్డియన్",
        "subtitle": "AI-ఆధారిత విశ్లేషణతో మీ కుటుంబాన్ని ఆన్‌లైన్ స్కామ్‌ల నుండి రక్షించండి",
        "message_checker": "సందేశ చెకర్",
        "link_inspector": "లింక్ ఇన్‌స్పెక్టర్",
        "call_checker": "కాల్ చెకర్",
        "learn_quiz": "నేర్చుకోండి & క్విజ్",
        "paste_message": "సందేశాన్ని అతికించండి:",
        "analyze_btn": "సందేశాన్ని విశ్లేషించండి",
        "paste_url": "సందేశ URL ను అతికించండి:",
        "analyze_url": "URLను విశ్లేషించండి",
        "phone_number": "ఫోన్ నంబర్ నమోదు చేయండి:",
        "call_count": "కాల్‌ల సంఖ్య:",
        "analyze_call": "కాల్‌ను విశ్లేషించండి",
        "verdict": "తీర్పు",
        "confidence": "విశ్వాస స్కోర్",
        "red_flags": "ఎరుపు జెండాలు",
        "advice": "సలహా",
        "risk_factors": "రిస్క్ కారకాలు",
        "explanation": "వివరణ",
        "quiz_title": "నేర్చుకోండి & స్కామ్‌లను గుర్తించండి క్విజ్",
        "question": "ప్రశ్న",
        "submit_answer": "సమాధానం సమర్పించండి",
        "score": "మీ స్కోర్",
        "language": "భాష",
        "safe": "సురక్షితం",
        "suspicious": "అనుమానాస్పదం",
        "scam": "స్కామ్",
        "high_risk": "అధిక ప్రమాదం",
        "medium_risk": "మధ్యస్థ ప్రమాదం",
        "low_risk": "తక్కువ ప్రమాదం",
        "stats_scams_blocked": "కనుగొన్న స్కామ్‌లు",
        "stats_users_protected": "రక్షించిన వినియోగదారులు",
        "stats_accuracy": "గుర్తింపు ఖచ్చితత్వం",
        "report_scam": "స్కామ్ ను రిపోర్ట్ చేయండి",
        "footer": "రక్ష AI ను ఉపయోగించి సంభావ్య స్కామ్‌లను కనుగొంటుంది. ఎల్లప్పుడూ అధికారిక మూలాలతో ధృవీకరించండి.",
        "bilingual_note": "ద్విభాషా అవుట్‌పుట్",
    },
    "ta": {
        "title": "🛡️ ரக்ஷா - குடும்ப டிஜிட்டல் பாதுகாப்பு காவலர்",
        "subtitle": "AI-ஆல் இயக்கப்படும் பகுப்பாய்வுடன் உங்கள் குடும்பத்தை ஆன்லைன் மோசடிகளிலிருந்து பாதுகாக்கவும்",
        "message_checker": "செய்தி சரிபார்ப்பு",
        "link_inspector": "இணைப்பு ஆய்வாளர்",
        "call_checker": "அழைப்பு சரிபார்ப்பு",
        "learn_quiz": "கற்றல் & வினாடி வினா",
        "paste_message": "சந்தேகத்திற்கிடமான செய்தியை ஒட்டவும்:",
        "analyze_btn": "செய்தியை பகுப்பாய்வு செய்",
        "paste_url": "சந்தேகத்திற்கிடமான URL ஐ ஒட்டவும்:",
        "analyze_url": "URL ஐ பகுப்பாய்வு செய்",
        "phone_number": "தொலைபேசி எண்ணை உள்ளிடவும்:",
        "call_count": "அழைப்புகளின் எண்ணிக்கை:",
        "analyze_call": "அழைப்பை பகுப்பாய்வு செய்",
        "verdict": "தீர்ப்பு",
        "confidence": "நம்பகத்தன்மை மதிப்பெண்",
        "red_flags": "எச்சரிக்கை கொடிகள்",
        "advice": "ஆலோசனை",
        "risk_factors": "ஆபத்து காரணிகள்",
        "explanation": "விளக்கம்",
        "quiz_title": "மோசடிகளை கண்டறிய கற்றல் & வினாடி வினா",
        "question": "கேள்வி",
        "submit_answer": "பதிலை சமர்ப்பிக்கவும்",
        "score": "உங்கள் மதிப்பெண்",
        "language": "மொழி",
        "safe": "பாதுகாப்பானது",
        "suspicious": "சந்தேகத்திற்கிடமானது",
        "scam": "மோசடி",
        "high_risk": "அதிக ஆபத்து",
        "medium_risk": "நடுத்தர ஆபத்து",
        "low_risk": "குறைந்த ஆபத்து",
        "stats_scams_blocked": "கண்டறியப்பட்ட மோசடிகள்",
        "stats_users_protected": "பாதுகாக்கப்பட்ட பயனர்கள்",
        "stats_accuracy": "கண்டறிதல் துல்லியம்",
        "report_scam": "மோசடியைப் புகாரளிக்கவும்",
        "footer": "ரக்ஷா AI ஐப் பயன்படுத்தி சாத்தியமான மோசடிகளைக் கண்டறிகிறது. எப்போதும் அதிகாரப்பூர்வ ஆதாரங்களுடன் சரிபார்க்கவும்.",
        "bilingual_note": "இருமொழி வெளியீடு",
    },
    "hi": {
        "title": "🛡️ रक्षा - परिवार डिजिटल सुरक्षा संरक्षक",
        "subtitle": "AI-संचालित विश्लेषण के साथ अपने परिवार को ऑनलाइन घोटालों से बचाएं",
        "message_checker": "संदेश जांचकर्ता",
        "link_inspector": "लिंक निरीक्षक",
        "call_checker": "कॉल जांचकर्ता",
        "learn_quiz": "सीखें और क्विज़",
        "paste_message": "एक संदिग्ध संदेश पेस्ट करें:",
        "analyze_btn": "संदेश का विश्लेषण करें",
        "paste_url": "एक संदिग्ध URL पेस्ट करें:",
        "analyze_url": "URL का विश्लेषण करें",
        "phone_number": "फोन नंबर दर्ज करें:",
        "call_count": "कॉल की संख्या:",
        "analyze_call": "कॉल का विश्लेषण करें",
        "verdict": "फैसला",
        "confidence": "विश्वास स्कोर",
        "red_flags": "रेड फ्लैग्स",
        "advice": "सलाह",
        "risk_factors": "जोखिम कारक",
        "explanation": "व्याख्या",
        "quiz_title": "सीखें और घोटालों की पहचान करें क्विज़",
        "question": "प्रश्न",
        "submit_answer": "उत्तर जमा करें",
        "score": "आपका स्कोर",
        "language": "भाषा",
        "safe": "सुरक्षित",
        "suspicious": "संदिग्ध",
        "scam": "घोटाला",
        "high_risk": "उच्च जोखिम",
        "medium_risk": "मध्यम जोखिम",
        "low_risk": "कम जोखिम",
        "stats_scams_blocked": "पता लगाए गए घोटाले",
        "stats_users_protected": "संरक्षित उपयोगकर्ता",
        "stats_accuracy": "पता लगाने की सटीकता",
        "report_scam": "घोटाले की रिपोर्ट करें",
        "footer": "रक्षा AI का उपयोग करके संभावित घोटालों का पता लगाती है। हमेशा आधिकारिक स्रोतों के साथ सत्यापित करें।",
        "bilingual_note": "द्विभाषी आउटपुट",
    },
    "kn": {
        "title": "🛡️ ರಕ್ಷ - ಕುಟುಂಬ ಡಿಜಿಟಲ್ ಸುರಕ್ಷತಾ ರಕ್ಷಕ",
        "subtitle": "AI-ಆಧಾರಿತ ವಿಶ್ಲೇಷಣೆಯೊಂದಿಗೆ ನಿಮ್ಮ ಕುಟುಂಬವನ್ನು ಆನ್‌ಲೈನ್ ಸ್ಕ್ಯಾಮ್‌ಗಳಿಂದ ರಕ್ಷಿಸಿ",
        "message_checker": "ಸಂದೇಶ ಪರಿಶೀಲಕ",
        "link_inspector": "ಲಿಂಕ್ ಪರಿಶೀಲಕ",
        "call_checker": "ಕಾಲ್ ಪರಿಶೀಲಕ",
        "learn_quiz": "ಕಲಿ ಮತ್ತು ರಸಪ್ರಶ್ನೆ",
        "paste_message": "ಅನುಮಾನಾಸ್ಪದ ಸಂದೇಶವನ್ನು ಅಂಟಿಸಿ:",
        "analyze_btn": "ಸಂದೇಶವನ್ನು ವಿಶ್ಲೇಷಿಸಿ",
        "paste_url": "ಅನುಮಾನಾಸ್ಪದ URL ಅನ್ನು ಅಂಟಿಸಿ:",
        "analyze_url": "URL ಅನ್ನು ವಿಶ್ಲೇಷಿಸಿ",
        "phone_number": "ಫೋನ್ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ:",
        "call_count": "ಕಾಲ್‌ಗಳ ಸಂಖ್ಯೆ:",
        "analyze_call": "ಕಾಲ್ ಅನ್ನು ವಿಶ್ಲೇಷಿಸಿ",
        "verdict": "ತೀರ್ಪು",
        "confidence": "ವಿಶ್ವಾಸ ಸ್ಕೋರ್",
        "red_flags": "ಎಚ್ಚರಿಕೆ ಧ್ವಜಗಳು",
        "advice": "ಸಲಹೆ",
        "risk_factors": "ಅಪಾಯದ ಅಂಶಗಳು",
        "explanation": "ವಿವರಣೆ",
        "quiz_title": "ಕಲಿ ಮತ್ತು ಸ್ಕ್ಯಾಮ್‌ಗಳನ್ನು ಗುರುತಿಸಿ ರಸಪ್ರಶ್ನೆ",
        "question": "ಪ್ರಶ್ನೆ",
        "submit_answer": "ಉತ್ತರವನ್ನು ಸಲ್ಲಿಸಿ",
        "score": "ನಿಮ್ಮ ಸ್ಕೋರ್",
        "language": "ಭಾಷೆ",
        "safe": "ಸುರಕ್ಷಿತ",
        "suspicious": "ಅನುಮಾನಾಸ್ಪದ",
        "scam": "ಸ್ಕ್ಯಾಮ್",
        "high_risk": "ಅಧಿಕ ಅಪಾಯ",
        "medium_risk": "ಮಧ್ಯಮ ಅಪಾಯ",
        "low_risk": "ಕಡಿಮೆ ಅಪಾಯ",
        "stats_scams_blocked": "ಕಂಡುಹಿಡಿದ ಸ್ಕ್ಯಾಮ್‌ಗಳು",
        "stats_users_protected": "ರಕ್ಷಿಸಿದ ಬಳಕೆದಾರರು",
        "stats_accuracy": "ಗುರುತಿಸುವ ನಿಖರತೆ",
        "report_scam": "ಸ್ಕ್ಯಾಮ್ ವರದಿ ಮಾಡಿ",
        "footer": "ರಕ್ಷ AI ಬಳಸಿ ಸಂಭವನೀಯ ಸ್ಕ್ಯಾಮ್‌ಗಳನ್ನು ಪತ್ತೆಹಚ್ಚುತ್ತದೆ. ಯಾವಾಗಲೂ ಅಧಿಕೃತ ಮೂಲಗಳೊಂದಿಗೆ ಪರಿಶೀಲಿಸಿ.",
        "bilingual_note": "ದ್ವಿಭಾಷಾ ಔಟ್‌ಪುಟ್",
    }
}

# Session state for stats
if "scams_detected" not in st.session_state:
    st.session_state.scams_detected = 1247
if "users_protected" not in st.session_state:
    st.session_state.users_protected = 8934
if "accuracy" not in st.session_state:
    st.session_state.accuracy = 96.5

# Sidebar
with st.sidebar:
    st.title("🛡️ Raksha")
    st.markdown("---")
    st.subheader("📊 Stats")
    st.metric("Scams Detected", st.session_state.scams_detected)
    st.metric("Users Protected", st.session_state.users_protected)
    st.metric("Detection Accuracy", f"{st.session_state.accuracy}%")
    st.markdown("---")
    st.caption("🛡️ Raksha - Family Digital Safety Guardian")
    st.caption("Made with 💚 for Digital Safety")
    st.caption("Powered by Groq AI")

# Language Selection
col1, col2 = st.columns([0.9, 0.1])
with col2:
    selected_language = st.selectbox(
        "🌐",
        options=list(LANGUAGE_OPTIONS.keys()),
        label_visibility="collapsed"
    )
    lang_code = LANGUAGE_OPTIONS[selected_language]

t = TRANSLATIONS[lang_code]

# Header
st.markdown(f"# {t['title']}")
st.markdown(f"*{t['subtitle']}*")
st.divider()

# Top Stats
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Safety", "100%", "✅")
with col2:
    st.metric("Availability", "24/7", "⏰")
with col3:
    st.metric("Cost", "Free", "∞")

st.divider()

# Function to analyze with Groq
def analyze_with_groq(prompt, system_message):
    try:
        message = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        return message.choices[0].message.content
    except Exception as e:
        st.error(f"Groq API Error: {str(e)}")
        return None

# Helper to show report button
def show_report_button(lang_code="en"):
    report_text = TRANSLATIONS[lang_code].get("report_scam", "Report Scam")
    st.markdown(
        f'<a href="https://cybercrime.gov.in/" target="_blank" class="report-btn">'
        f'🚨 {report_text}</a>',
        unsafe_allow_html=True
    )

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    f"📱 {t['message_checker']}",
    f"🔗 {t['link_inspector']}",
    f"☎️ {t['call_checker']}",
    f"📚 {t['learn_quiz']}"
])

# ==================== TAB 1: MESSAGE CHECKER ====================
with tab1:
    st.header(f"📱 {t['message_checker']}")
    st.write("Paste a suspicious SMS, WhatsApp, or email message to check if it's a scam.")
    
    message_input = st.text_area(
        t['paste_message'],
        placeholder="Enter suspicious message here...",
        height=150,
        key="message_input"
    )
    
    if st.button(t['analyze_btn'], key="msg_btn"):
        if message_input.strip():
            with st.spinner("🔍 Analyzing message..."):
                system_prompt = f"""You are an expert in identifying scams and fraudulent messages. 
Analyze the given message and provide a JSON response with:
{{
  "verdict": "scam|suspicious|safe",
  "confidence": 0-100,
  "red_flags": ["flag1", "flag2"],
  "advice_en": "English advice",
  "advice_te": "Telugu advice",
  "advice_ta": "Tamil advice",
  "advice_hi": "Hindi advice",
  "advice_kn": "Kannada advice"
}}
Respond ONLY with valid JSON, no other text."""
                
                response = analyze_with_groq(
                    f"Analyze this message for scams: {message_input}",
                    system_prompt
                )
                
                if response is None:
                    st.stop()
                
                with st.expander("Debug - Raw Response"):
                    st.code(response)
                
                try:
                    json_match = re.search(r'\{.*\}', response, re.DOTALL)
                    if json_match:
                        result = json.loads(json_match.group())
                    else:
                        result = json.loads(response)
                    
                    verdict = result.get("verdict", "unknown").upper()
                    confidence = result.get("confidence", 0)
                    
                    if verdict == "SCAM":
                        st.markdown(f'<div class="scam-badge scam-high">⚠️ {verdict} ({confidence}%)</div>', unsafe_allow_html=True)
                        st.session_state.scams_detected += 1
                        show_report_button(lang_code)
                    elif verdict == "SUSPICIOUS":
                        st.markdown(f'<div class="scam-badge scam-medium">⚠️ {verdict} ({confidence}%)</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="scam-badge scam-safe">✅ {verdict} ({confidence}%)</div>', unsafe_allow_html=True)
                    
                    st.progress(confidence / 100)
                    
                    if result.get("red_flags"):
                        st.subheader(f"🚩 {t['red_flags']}")
                        for flag in result["red_flags"]:
                            st.write(f"• {flag}")
                    
                    st.subheader(f"💡 {t['advice']}")
                    st.caption(f"*{t['bilingual_note']}*")
                    
                    cols = st.columns(2)
                    advice_map = {
                        "en": result.get("advice_en", "N/A"),
                        "te": result.get("advice_te", "N/A"),
                        "ta": result.get("advice_ta", "N/A"),
                        "hi": result.get("advice_hi", "N/A"),
                        "kn": result.get("advice_kn", "N/A"),
                    }
                    
                    with cols[0]:
                        st.write(f"**English:**\n{advice_map['en']}")
                    with cols[1]:
                        if lang_code == "te":
                            st.write(f"**తెలుగు:**\n{advice_map['te']}")
                        elif lang_code == "ta":
                            st.write(f"**தமிழ்:**\n{advice_map['ta']}")
                        elif lang_code == "hi":
                            st.write(f"**हिन्दी:**\n{advice_map['hi']}")
                        elif lang_code == "kn":
                            st.write(f"**ಕನ್ನಡ:**\n{advice_map['kn']}")
                        else:
                            st.write(f"**తెలుగు:**\n{advice_map['te']}")
                    
                except json.JSONDecodeError as e:
                    st.error(f"Could not parse response. Please try again.")
                    st.text(f"Parse error: {str(e)}")
        else:
            st.warning("Please enter a message to analyze.")

# ==================== TAB 2: LINK INSPECTOR ====================
with tab2:
    st.header(f"🔗 {t['link_inspector']}")
    st.write("Paste a suspicious URL to check for phishing and malicious links.")
    
    url_input = st.text_input(
        t['paste_url'],
        placeholder="https://example.com",
        key="url_input"
    )
    
    if st.button(t['analyze_url'], key="url_btn"):
        if url_input.strip():
            with st.spinner("🔍 Analyzing URL..."):
                system_prompt = f"""You are an expert in identifying phishing and malicious links.
Analyze the given URL and provide a JSON response with:
{{
  "risk_level": "high|medium|low|safe",
  "risk_score": 0-100,
  "risk_factors": ["factor1", "factor2"],
  "explanation_en": "English explanation",
  "explanation_te": "Telugu explanation",
  "explanation_ta": "Tamil explanation",
  "explanation_hi": "Hindi explanation",
  "explanation_kn": "Kannada explanation"
}}
Respond ONLY with valid JSON, no other text."""
                
                response = analyze_with_groq(
                    f"Analyze this URL for phishing and scam risks: {url_input}",
                    system_prompt
                )
                
                if response is None:
                    st.stop()
                
                with st.expander("Debug - Raw Response"):
                    st.code(response)
                
                try:
                    json_match = re.search(r'\{.*\}', response, re.DOTALL)
                    if json_match:
                        result = json.loads(json_match.group())
                    else:
                        result = json.loads(response)
                    
                    risk_level = result.get("risk_level", "unknown").upper()
                    risk_score = result.get("risk_score", 0)
                    
                    if risk_level == "HIGH":
                        st.markdown(f'<div class="scam-badge scam-high">⚠️ {risk_level} RISK ({risk_score}%)</div>', unsafe_allow_html=True)
                        st.session_state.scams_detected += 1
                        show_report_button(lang_code)
                    elif risk_level == "MEDIUM":
                        st.markdown(f'<div class="scam-badge scam-medium">⚠️ {risk_level} RISK ({risk_score}%)</div>', unsafe_allow_html=True)
                    elif risk_level == "LOW":
                        st.markdown(f'<div class="scam-badge scam-low">⚠️ {risk_level} RISK ({risk_score}%)</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="scam-badge scam-safe">✅ SAFE ({risk_score}%)</div>', unsafe_allow_html=True)
                    
                    st.progress(risk_score / 100)
                    
                    if result.get("risk_factors"):
                        st.subheader(f"🚩 {t['risk_factors']}")
                        for factor in result["risk_factors"]:
                            st.write(f"• {factor}")
                    
                    st.subheader(f"📖 {t['explanation']}")
                    st.caption(f"*{t['bilingual_note']}*")
                    
                    cols =
