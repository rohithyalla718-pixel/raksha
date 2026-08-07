import streamlit as st
import os
from groq import Groq
import json
import re
import requests
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Raksha - Family Digital Safety Guardian",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS (3D + Glass + Hero) ====================
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #f0f4ff 0%, #e8f4f8 100%);
    }
    
    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 24px;
        padding: 3rem 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 25px 80px rgba(79, 172, 254, 0.35);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .hero-banner h1 {
        margin: 0;
        font-size: 2.8rem;
        font-weight: 800;
        text-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .hero-banner p {
        margin-top: 1rem;
        font-size: 1.15rem;
        opacity: 0.95;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
    }
    
    /* 3D Buttons */
    .stButton > button {
        background: linear-gradient(145deg, #3b82f6, #2563eb) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.8rem 2.2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        box-shadow: 0 6px 0 #1d4ed8, 0 10px 25px rgba(37, 99, 235, 0.35) !important;
        transition: all 0.15s ease !important;
        transform: translateY(0) !important;
    }
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 9px 0 #1d4ed8, 0 15px 35px rgba(37, 99, 235, 0.45) !important;
    }
    .stButton > button:active {
        transform: translateY(6px) !important;
        box-shadow: 0 0 0 #1d4ed8, 0 3px 8px rgba(37, 99, 235, 0.3) !important;
    }
    
    /* Secondary buttons */
    .stButton > button[kind="secondary"] {
        background: linear-gradient(145deg, #10b981, #059669) !important;
        box-shadow: 0 6px 0 #047857, 0 10px 25px rgba(5, 150, 105, 0.35) !important;
    }
    .stButton > button[kind="secondary"]:hover {
        box-shadow: 0 9px 0 #047857, 0 15px 35px rgba(5, 150, 105, 0.45) !important;
    }
    .stButton > button[kind="secondary"]:active {
        transform: translateY(6px) !important;
        box-shadow: 0 0 0 #047857, 0 3px 8px rgba(5, 150, 105, 0.3) !important;
    }
    
    /* Example Buttons (subtle glass) */
    div[data-testid="stHorizontalBlock"] .stButton > button {
        background: rgba(255,255,255,0.85) !important;
        color: #334155 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08) !important;
        border: 1px solid rgba(255,255,255,0.6) !important;
        font-weight: 600 !important;
    }
    div[data-testid="stHorizontalBlock"] .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.12) !important;
        background: rgba(255,255,255,0.95) !important;
    }
    
    /* Glassmorphism Badges */
    .scam-badge {
        padding: 0.7rem 1.4rem;
        border-radius: 1rem;
        font-weight: 700;
        display: inline-block;
        margin: 0.5rem 0;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.4);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .scam-high {
        background: rgba(254, 226, 226, 0.85);
        color: #991b1b;
        box-shadow: 0 4px 20px rgba(153, 27, 27, 0.2);
    }
    .scam-medium {
        background: rgba(254, 243, 199, 0.85);
        color: #92400e;
        box-shadow: 0 4px 20px rgba(146, 64, 14, 0.2);
    }
    .scam-low {
        background: rgba(220, 252, 231, 0.85);
        color: #15803d;
        box-shadow: 0 4px 20px rgba(21, 128, 61, 0.2);
    }
    .scam-safe {
        background: rgba(209, 250, 229, 0.85);
        color: #065f46;
        box-shadow: 0 4px 20px rgba(6, 95, 70, 0.2);
    }
    
    /* Counter Badge */
    .counter-badge {
        background: rgba(209, 250, 229, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1rem 1.5rem;
        border: 1px solid rgba(255,255,255,0.5);
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        display: inline-block;
        margin: 1rem 0;
    }
    .counter-badge span {
        color: #065f46;
        font-weight: 700;
        font-size: 1.1rem;
    }
    
    /* 3D Report Button */
    .report-btn {
        background: linear-gradient(145deg, #dc2626, #b91c1c);
        color: white;
        padding: 0.8rem 1.8rem;
        border-radius: 14px;
        text-decoration: none;
        font-weight: 700;
        display: inline-block;
        margin-top: 0.5rem;
        box-shadow: 0 6px 0 #991b1b, 0 10px 25px rgba(220, 38, 38, 0.35);
        transition: all 0.15s ease;
    }
    .report-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 9px 0 #991b1b, 0 15px 35px rgba(220, 38, 38, 0.45);
    }
    .report-btn:active {
        transform: translateY(6px);
        box-shadow: 0 0 0 #991b1b, 0 3px 8px rgba(220, 38, 38, 0.3);
    }
    
    /* Sidebar Glass */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.6);
    }
    
    /* Inputs */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        border-radius: 16px !important;
        border: 2px solid #e2e8f0 !important;
        box-shadow: inset 0 2px 6px rgba(0,0,0,0.06) !important;
        transition: all 0.3s ease !important;
        background: rgba(255,255,255,0.8) !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15), inset 0 2px 6px rgba(0,0,0,0.06) !important;
        background: white !important;
    }
    
    /* Metrics 3D */
    [data-testid="stMetric"] {
        background: white;
        border-radius: 20px;
        padding: 1.2rem;
        box-shadow: 0 12px 30px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.6);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab-list"] button:hover {
        transform: translateY(-2px);
        color: #2563eb !important;
    }
    
    /* Floating Action Button */
    .fab-report {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 64px;
        height: 64px;
        background: linear-gradient(145deg, #ff6b6b, #ee5a5a);
        border-radius: 50%;
        box-shadow: 0 10px 35px rgba(255, 107, 107, 0.45);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.6rem;
        text-decoration: none;
        z-index: 9999;
        transition: all 0.3s ease;
        border: 3px solid rgba(255,255,255,0.3);
    }
    .fab-report:hover {
        transform: translateY(-5px) scale(1.1);
        box-shadow: 0 18px 45px rgba(255, 107, 107, 0.55);
    }
    </style>
""", unsafe_allow_html=True)

# ==================== GROQ CLIENT ====================
@st.cache_resource
def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("❌ GROQ_API_KEY not found. Please set it in your environment variables.")
        st.stop()
    return Groq(api_key=api_key)

client = get_groq_client()

# ==================== LANGUAGE SETUP ====================
LANGUAGE_OPTIONS = {
    "English": "en",
    "తెలుగు (Telugu)": "te",
    "தமிழ் (Tamil)": "ta",
    "हिन्दी (Hindi)": "hi",
    "ಕನ್ನಡ (Kannada)": "kn"
}

TRANSLATIONS = {
    "en": {
        "title": "Raksha - Family Digital Safety Guardian",
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
        "check_message": "Check Message",
        "is_scam": "Is this message a scam?",
        "paste_any": "Paste any SMS, WhatsApp, or email you're unsure about.",
        "try_example": "Try an example:",
        "messages_checked": "messages checked",
        "scams_caught": "scams caught",
    },
    "te": {
        "title": "రక్ష - కుటుంబ డిజిటల్ సేఫ్టీ గార్డియన్",
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
        "check_message": "సందేశాన్ని పరిశీలించండి",
        "is_scam": "ఈ సందేశం స్కామ్ అయ్యే అవకాశం ఉందా?",
        "paste_any": "మీకు అనుమానం ఉన్న ఏదైనా SMS, WhatsApp, లేదా ఇమెయిల్‌ను అతికించండి.",
        "try_example": "ఉదాహరణను ప్రయత్నించండి:",
        "messages_checked": "సందేశాలు పరిశీలించబడ్డాయి",
        "scams_caught": "స్కామ్‌లు పట్టుబడ్డాయి",
    },
    "ta": {
        "title": "ரக்ஷா - குடும்ப டிஜிட்டல் பாதுகாப்பு காவலர்",
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
        "check_message": "செய்தியை சரிபார்க்கவும்",
        "is_scam": "இந்த செய்தி மோசடியா?",
        "paste_any": "நீங்கள் உறுதியாக இல்லாத எந்த SMS, WhatsApp, அல்லது மின்னஞ்சலையும் ஒட்டவும்.",
        "try_example": "ஒரு உதாரணத்தை முயற்சிக்கவும்:",
        "messages_checked": "செய்திகள் சரிபார்க்கப்பட்டன",
        "scams_caught": "மோசடிகள் பிடிக்கப்பட்டன",
    },
    "hi": {
        "title": "रक्षा - परिवार डिजिटल सुरक्षा संरक्षक",
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
        "check_message": "संदेश जांचें",
        "is_scam": "क्या यह संदेश घोटाला है?",
        "paste_any": "कोई भी SMS, WhatsApp, या ईमेल पेस्ट करें जिसके बारे में आपको संदेह है।",
        "try_example": "एक उदाहरण आजमाएं:",
        "messages_checked": "संदेश जांचे गए",
        "scams_caught": "घोटाले पकड़े गए",
    },
    "kn": {
        "title": "ರಕ್ಷ - ಕುಟುಂಬ ಡಿಜಿಟಲ್ ಸುರಕ್ಷತಾ ರಕ್ಷಕ",
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
        "check_message": "ಸಂದೇಶವನ್ನು ಪರಿಶೀಲಿಸಿ",
        "is_scam": "ಈ ಸಂದೇಶ ಸ್ಕ್ಯಾಮ್ ಆಗಿದೆಯೇ?",
        "paste_any": "ನಿಮಗೆ ಅನುಮಾನವಿರುವ ಯಾವುದೇ SMS, WhatsApp, ಅಥವಾ ಇಮೇಲ್ ಅನ್ನು ಅಂಟಿಸಿ.",
        "try_example": "ಉದಾಹರಣೆಯನ್ನು ಪ್ರಯತ್ನಿಸಿ:",
        "messages_checked": "ಸಂದೇಶಗಳನ್ನು ಪರಿಶೀಲಿಸಲಾಗಿದೆ",
        "scams_caught": "ಸ್ಕ್ಯಾಮ್‌ಗಳನ್ನು ಹಿಡಿದುಕೊಂಡಿದೆ",
    }
}

# ==================== COMPLETE UI TRANSLATIONS ====================
# These keys cover the parts of the interface that were previously hard-coded.
UI_TRANSLATIONS = {
    "en": {
        "language_label": "Language",
        "mission": "Our Mission",
        "mission_text": "Thousands of Indian families lose money to online scams every day. Raksha protects, inspects, and teaches families to stay safe in their own language.",
        "stats": "Stats",
        "why_raksha": "Why Raksha wins",
        "why_1": "☑️ Real problem, real mission",
        "why_2": "☑️ 4 working safety tools",
        "why_3": "☑️ 5 Indian languages supported",
        "why_4": "☑️ 3D glass UI with live depth effects",
        "made_for": "Made with 💚 for Digital Safety",
        "hero_title": "Raksha — Family Digital Safety Guardian",
        "hero_subtitle": "Protecting families from online fraud — checks scam messages, inspects suspicious links, analyzes calls, and teaches people to spot fraud themselves.",
        "fake_lottery": "🎰 Fake Lottery",
        "fake_bank": "🏦 Fake Bank Alert",
        "fake_delivery": "📦 Fake Delivery",
        "suspicious_message": "Suspicious message:",
        "url_description": "Check suspicious URLs for phishing and malicious links.",
        "call_description_label": "🗣️ What did the caller say or ask?",
        "call_description_placeholder": "Example: Caller said he was from my bank and asked for my OTP to unblock my account. He demanded that I act immediately.",
        "call_checker_description": "Check telecom intelligence, registered number location, call behavior and scam indicators before trusting a caller.",
        "location_notice": "📍 Location shown here is the phone number's registered telecom location/region when available — it is NOT the caller's live GPS location.",
        "privacy_notice": "🔐 Privacy: the full phone number is used only for telecom lookup. Raksha sends a masked number plus call details to the AI analysis.",
        "checking_call": "🔍 Checking number, carrier, registered region and scam indicators...",
        "invalid_phone": "❌ Invalid phone number. For Indian numbers, enter 10 digits or use +91 followed by the number.",
        "telecom_intelligence": "📡 Telecom & SIM/Network Intelligence",
        "number_valid": "Number Valid",
        "yes": "Yes",
        "no": "No",
        "unknown": "Unknown",
        "carrier": "Carrier / Network",
        "line_type": "Line Type",
        "line_status": "Line Status",
        "country": "🌍 Country",
        "region": "📍 Region",
        "registered_city": "🏙️ Registered City",
        "timezone": "🕐 Timezone",
        "lookup_unavailable": "⚠️ Telecom lookup is unavailable. Call can still be analyzed with call behavior and AI indicators.",
        "lookup_detail": "Lookup detail",
        "risk_evidence": "📊 Risk Evidence",
        "behavior_risk": "Behavior Risk",
        "calls_received": "Calls Received",
        "overall_risk": "Overall Risk",
        "telecom_assessment": "📡 Telecom Assessment",
        "telecom_not_verdict": "Telecom data is supporting evidence only; it cannot prove the caller is a scammer.",
        "quiz_description": "Test your knowledge and learn to spot scams before they happen.",
        "correct": "✅ Correct!",
        "incorrect": "❌ Incorrect!",
        "select_answer": "Please select an answer first.",
        "perfect_score": "🎉 Perfect score! You're a scam detection expert!",
        "report_scam_title": "Report Scam",
        "raw_response": "Debug - Raw Response",
        "groq_error": "Groq API Error",
        "parse_error": "Could not read response. Please try again.",
        "enter_message": "Enter a message to analyze.",
        "enter_url": "Enter a URL to analyze.",
        "enter_phone": "Enter a phone number to analyze.",
        "safe_label": "Safe",
        "suspicious_label": "Suspicious",
        "scam_label": "Scam",
        "english": "English",
        "report": "Report Scam",
        "footer_model": "Made with 💚 for Digital Safety | Model: llama-3.1-8b-instant via Groq",
    },
    "te": {
        "language_label": "భాష",
        "mission": "మా లక్ష్యం",
        "mission_text": "ప్రతి రోజు వేలాది భారతీయ కుటుంబాలు ఆన్‌లైన్ స్కామ్‌ల వల్ల డబ్బు కోల్పోతున్నాయి. రక్ష మీ కుటుంబాన్ని వారి స్వంత భాషలో రక్షిస్తుంది, పరిశీలిస్తుంది మరియు నేర్పిస్తుంది.",
        "stats": "గణాంకాలు",
        "why_raksha": "రక్ష ఎందుకు గెలుస్తుంది",
        "why_1": "☑️ నిజమైన సమస్య, నిజమైన లక్ష్యం",
        "why_2": "☑️ 4 పనిచేసే భద్రతా సాధనాలు",
        "why_3": "☑️ 5 భారతీయ భాషలకు మద్దతు",
        "why_4": "☑️ 3D గ్లాస్ UI మరియు లైవ్ డెప్త్ ఎఫెక్ట్స్",
        "made_for": "డిజిటల్ భద్రత కోసం 💚 తో తయారు చేయబడింది",
        "hero_title": "రక్ష — కుటుంబ డిజిటల్ సేఫ్టీ గార్డియన్",
        "hero_subtitle": "ఆన్‌లైన్ మోసాల నుండి కుటుంబాలను రక్షిస్తుంది — స్కామ్ సందేశాలను పరిశీలిస్తుంది, అనుమానాస్పద లింక్‌లను తనిఖీ చేస్తుంది, కాల్‌లను విశ్లేషిస్తుంది మరియు మోసాలను గుర్తించడం నేర్పిస్తుంది.",
        "fake_lottery": "🎰 నకిలీ లాటరీ",
        "fake_bank": "🏦 నకిలీ బ్యాంక్ అలర్ట్",
        "fake_delivery": "📦 నకిలీ డెలివరీ",
        "suspicious_message": "అనుమానాస్పద సందేశం:",
        "url_description": "ఫిషింగ్ మరియు హానికరమైన లింక్‌ల కోసం అనుమానాస్పద URL ను తనిఖీ చేయండి.",
        "call_description_label": "🗣️ కాలర్ ఏమి చెప్పాడు లేదా ఏమి అడిగాడు?",
        "call_description_placeholder": "ఉదాహరణ: కాలర్ తాను నా బ్యాంక్ నుండి అని చెప్పి, ఖాతాను అన్‌బ్లాక్ చేయడానికి OTP అడిగాడు. వెంటనే చేయాలని ఒత్తిడి చేశాడు.",
        "call_checker_description": "కాలర్‌ను నమ్మే ముందు టెలికాం సమాచారం, నమోదైన నంబర్ ప్రాంతం, కాల్ ప్రవర్తన మరియు స్కామ్ సూచనలను తనిఖీ చేయండి.",
        "location_notice": "📍 ఇక్కడ చూపించే ప్రాంతం అందుబాటులో ఉన్నప్పుడు ఫోన్ నంబర్ నమోదైన టెలికాం ప్రాంతం మాత్రమే — ఇది కాలర్ యొక్క లైవ్ GPS స్థానం కాదు.",
        "privacy_notice": "🔐 గోప్యత: పూర్తి ఫోన్ నంబర్ టెలికాం లుక్‌అప్ కోసం మాత్రమే ఉపయోగించబడుతుంది. AI విశ్లేషణకు మాస్క్ చేసిన నంబర్ మరియు కాల్ వివరాలు మాత్రమే పంపబడతాయి.",
        "checking_call": "🔍 నంబర్, క్యారియర్, నమోదైన ప్రాంతం మరియు స్కామ్ సూచనలను తనిఖీ చేస్తున్నాం...",
        "invalid_phone": "❌ చెల్లని ఫోన్ నంబర్. భారతీయ నంబర్ల కోసం 10 అంకెలు లేదా +91 తో నంబర్ నమోదు చేయండి.",
        "telecom_intelligence": "📡 టెలికాం & SIM/నెట్‌వర్క్ సమాచారం",
        "number_valid": "నంబర్ చెల్లుబాటు",
        "yes": "అవును",
        "no": "కాదు",
        "unknown": "తెలియదు",
        "carrier": "క్యారియర్ / నెట్‌వర్క్",
        "line_type": "లైన్ రకం",
        "line_status": "లైన్ స్థితి",
        "country": "🌍 దేశం",
        "region": "📍 ప్రాంతం",
        "registered_city": "🏙️ నమోదైన నగరం",
        "timezone": "🕐 టైమ్‌జోన్",
        "lookup_unavailable": "⚠️ టెలికాం లుక్‌అప్ అందుబాటులో లేదు. కాల్ ప్రవర్తన మరియు AI సూచనలతో కాల్‌ను ఇంకా విశ్లేషించవచ్చు.",
        "lookup_detail": "లుక్‌అప్ వివరాలు",
        "risk_evidence": "📊 రిస్క్ ఆధారాలు",
        "behavior_risk": "ప్రవర్తన రిస్క్",
        "calls_received": "అందుకున్న కాల్స్",
        "overall_risk": "మొత్తం రిస్క్",
        "telecom_assessment": "📡 టెలికాం అంచనా",
        "telecom_not_verdict": "టెలికాం డేటా సహాయక ఆధారం మాత్రమే; దానితో కాలర్ స్కామర్ అని నిర్ధారించలేము.",
        "quiz_description": "మీ జ్ఞానాన్ని పరీక్షించుకోండి మరియు స్కామ్‌లు జరగకముందే వాటిని గుర్తించడం నేర్చుకోండి.",
        "correct": "✅ సరైన సమాధానం!",
        "incorrect": "❌ తప్పు సమాధానం!",
        "select_answer": "దయచేసి ముందుగా ఒక సమాధానాన్ని ఎంచుకోండి.",
        "perfect_score": "🎉 అద్భుతమైన స్కోర్! మీరు స్కామ్ గుర్తింపు నిపుణులు!",
        "report_scam_title": "స్కామ్‌ను రిపోర్ట్ చేయండి",
        "raw_response": "డీబగ్ - ముడి స్పందన",
        "groq_error": "Groq API లోపం",
        "parse_error": "స్పందనను చదవలేకపోయాం. దయచేసి మళ్లీ ప్రయత్నించండి.",
        "enter_message": "విశ్లేషించడానికి సందేశాన్ని నమోదు చేయండి.",
        "enter_url": "విశ్లేషించడానికి URL ను నమోదు చేయండి.",
        "enter_phone": "విశ్లేషించడానికి ఫోన్ నంబర్‌ను నమోదు చేయండి.",
        "safe_label": "సురక్షితం",
        "suspicious_label": "అనుమానాస్పదం",
        "scam_label": "స్కామ్",
        "english": "ఆంగ్లం",
        "report": "స్కామ్‌ను రిపోర్ట్ చేయండి",
        "footer_model": "డిజిటల్ భద్రత కోసం 💚 తో తయారు చేయబడింది | మోడల్: llama-3.1-8b-instant via Groq",
    },
    "ta": {
        "language_label": "மொழி", "mission": "எங்கள் நோக்கம்", "mission_text": "ஆயிரக்கணக்கான இந்திய குடும்பங்கள் தினமும் ஆன்லைன் மோசடிகளில் பணத்தை இழக்கின்றனர். ரக்ஷா உங்கள் குடும்பத்தை அவர்களின் சொந்த மொழியில் பாதுகாக்கிறது, ஆய்வு செய்கிறது மற்றும் கற்றுக்கொடுக்கிறது.", "stats": "புள்ளிவிவரங்கள்", "why_raksha": "ரக்ஷா ஏன் வெல்லும்", "why_1": "☑️ உண்மையான பிரச்சனை, உண்மையான நோக்கம்", "why_2": "☑️ 4 செயல்படும் பாதுகாப்பு கருவிகள்", "why_3": "☑️ 5 இந்திய மொழிகளுக்கு ஆதரவு", "why_4": "☑️ 3D கண்ணாடி UI மற்றும் லைவ் டெப்த் எஃபெக்ட்ஸ்", "made_for": "டிஜிட்டல் பாதுகாப்புக்காக 💚 உருவாக்கப்பட்டது", "hero_title": "ரக்ஷா — குடும்ப டிஜிட்டல் பாதுகாப்பு காவலர்", "hero_subtitle": "ஆன்லைன் மோசடிகளில் இருந்து குடும்பங்களை பாதுகாக்கிறது — மோசடி செய்திகளை ஆய்வு செய்கிறது, சந்தேகமான இணைப்புகளை சரிபார்க்கிறது, அழைப்புகளை பகுப்பாய்வு செய்கிறது மற்றும் மோசடிகளை அடையாளம் காண கற்றுக்கொடுக்கிறது.", "fake_lottery": "🎰 போலி லாட்டரி", "fake_bank": "🏦 போலி வங்கி எச்சரிக்கை", "fake_delivery": "📦 போலி டெலிவரி", "suspicious_message": "சந்தேகமான செய்தி:", "url_description": "ஃபிஷிங் மற்றும் தீங்கிழைக்கும் இணைப்புகளுக்கான சந்தேகமான URL ஐ சரிபார்க்கவும்.", "call_description_label": "🗣️ அழைப்பாளர் என்ன சொன்னார் அல்லது என்ன கேட்டார்?", "call_description_placeholder": "உதாரணம்: அழைப்பாளர் வங்கியிலிருந்து வந்ததாகக் கூறி கணக்கைத் திறக்க OTP கேட்டார்.", "call_checker_description": "அழைப்பாளரை நம்புவதற்கு முன் தொலைத்தொடர்பு தகவல், பதிவு செய்யப்பட்ட பகுதி, அழைப்பு நடத்தை மற்றும் மோசடி அறிகுறிகளை சரிபார்க்கவும்.", "location_notice": "📍 இங்கு காட்டப்படும் பகுதி, கிடைக்கும் போது, தொலைபேசி எண்ணின் பதிவு செய்யப்பட்ட தொலைத்தொடர்பு பகுதி மட்டுமே — இது அழைப்பாளரின் நேரடி GPS இருப்பிடம் அல்ல.", "privacy_notice": "🔐 தனியுரிமை: முழு தொலைபேசி எண் தொலைத்தொடர்பு சரிபார்ப்புக்கு மட்டுமே பயன்படுத்தப்படுகிறது. AI க்கு மறைக்கப்பட்ட எண் மற்றும் அழைப்பு விவரங்கள் மட்டுமே அனுப்பப்படும்.", "checking_call": "🔍 எண், கேரியர், பதிவு செய்யப்பட்ட பகுதி மற்றும் மோசடி அறிகுறிகளை சரிபார்க்கிறது...", "invalid_phone": "❌ தவறான தொலைபேசி எண். இந்திய எண்ணுக்கு 10 இலக்கங்கள் அல்லது +91 உடன் எண்ணை உள்ளிடவும்.", "telecom_intelligence": "📡 தொலைத்தொடர்பு & SIM/நெட்வொர்க் தகவல்", "number_valid": "எண் சரியானதா", "yes": "ஆம்", "no": "இல்லை", "unknown": "தெரியவில்லை", "carrier": "கேரியர் / நெட்வொர்க்", "line_type": "லைன் வகை", "line_status": "லைன் நிலை", "country": "🌍 நாடு", "region": "📍 பகுதி", "registered_city": "🏙️ பதிவு செய்யப்பட்ட நகரம்", "timezone": "🕐 நேர மண்டலம்", "lookup_unavailable": "⚠️ தொலைத்தொடர்பு சரிபார்ப்பு கிடைக்கவில்லை. அழைப்பு நடத்தை மற்றும் AI அறிகுறிகளைக் கொண்டு இன்னும் பகுப்பாய்வு செய்யலாம்.", "lookup_detail": "சரிபார்ப்பு விவரம்", "risk_evidence": "📊 ஆபத்து ஆதாரங்கள்", "behavior_risk": "நடத்தை ஆபத்து", "calls_received": "பெறப்பட்ட அழைப்புகள்", "overall_risk": "மொத்த ஆபத்து", "telecom_assessment": "📡 தொலைத்தொடர்பு மதிப்பீடு", "telecom_not_verdict": "தொலைத்தொடர்பு தரவு ஆதாரம் மட்டுமே; அதனால் அழைப்பாளர் மோசடி செய்பவர் என்று உறுதியாக கூற முடியாது.", "quiz_description": "உங்கள் அறிவை சோதித்து, மோசடிகள் நடக்கும் முன் அவற்றை அடையாளம் காண கற்றுக்கொள்ளுங்கள்.", "correct": "✅ சரியான பதில்!", "incorrect": "❌ தவறான பதில்!", "select_answer": "முதலில் ஒரு பதிலைத் தேர்ந்தெடுக்கவும்.", "perfect_score": "🎉 சரியான மதிப்பெண்! நீங்கள் மோசடி கண்டறிதல் நிபுணர்!", "report_scam_title": "மோசடியைப் புகாரளிக்கவும்", "raw_response": "டீபக் - மூல பதில்", "groq_error": "Groq API பிழை", "parse_error": "பதிலை படிக்க முடியவில்லை. மீண்டும் முயற்சிக்கவும்.", "enter_message": "பகுப்பாய்வு செய்ய ஒரு செய்தியை உள்ளிடவும்.", "enter_url": "பகுப்பாய்வு செய்ய URL ஐ உள்ளிடவும்.", "enter_phone": "பகுப்பாய்வு செய்ய தொலைபேசி எண்ணை உள்ளிடவும்.", "safe_label": "பாதுகாப்பானது", "suspicious_label": "சந்தேகமானது", "scam_label": "மோசடி", "english": "ஆங்கிலம்", "report": "மோசடியைப் புகாரளிக்கவும்", "footer_model": "டிஜிட்டல் பாதுகாப்புக்காக 💚 உருவாக்கப்பட்டது | மாடல்: llama-3.1-8b-instant via Groq"
    },
    "hi": {
        "language_label": "भाषा", "mission": "हमारा मिशन", "mission_text": "हर दिन हजारों भारतीय परिवार ऑनलाइन घोटालों में पैसा खोते हैं। रक्षा आपके परिवार को उनकी अपनी भाषा में सुरक्षित रखता है, जांचता है और सिखाता है।", "stats": "आंकड़े", "why_raksha": "रक्षा क्यों जीतेगा", "why_1": "☑️ असली समस्या, असली मिशन", "why_2": "☑️ 4 काम करने वाले सुरक्षा उपकरण", "why_3": "☑️ 5 भारतीय भाषाओं का समर्थन", "why_4": "☑️ 3D ग्लास UI और लाइव डेप्थ इफेक्ट्स", "made_for": "डिजिटल सुरक्षा के लिए 💚 बनाया गया", "hero_title": "रक्षा — परिवार डिजिटल सुरक्षा संरक्षक", "hero_subtitle": "परिवारों को ऑनलाइन धोखाधड़ी से बचाता है — घोटाले के संदेशों की जांच करता है, संदिग्ध लिंक देखता है, कॉल का विश्लेषण करता है और लोगों को धोखाधड़ी पहचानना सिखाता है।", "fake_lottery": "🎰 नकली लॉटरी", "fake_bank": "🏦 नकली बैंक अलर्ट", "fake_delivery": "📦 नकली डिलीवरी", "suspicious_message": "संदिग्ध संदेश:", "url_description": "फिशिंग और दुर्भावनापूर्ण लिंक के लिए संदिग्ध URL की जांच करें।", "call_description_label": "🗣️ कॉल करने वाले ने क्या कहा या क्या मांगा?", "call_description_placeholder": "उदाहरण: कॉल करने वाले ने बैंक से होने का दावा किया और खाता खोलने के लिए OTP मांगा।", "call_checker_description": "कॉलर पर भरोसा करने से पहले टेलीकॉम जानकारी, पंजीकृत क्षेत्र, कॉल व्यवहार और घोटाले के संकेत जांचें।", "location_notice": "📍 यहां दिखाया गया स्थान, उपलब्ध होने पर, फोन नंबर का पंजीकृत टेलीकॉम क्षेत्र है — यह कॉलर का लाइव GPS स्थान नहीं है।", "privacy_notice": "🔐 गोपनीयता: पूरा फोन नंबर केवल टेलीकॉम लुकअप के लिए उपयोग होता है। AI को केवल छिपा हुआ नंबर और कॉल विवरण भेजे जाते हैं।", "checking_call": "🔍 नंबर, कैरियर, पंजीकृत स्थान और घोटाले के संकेत जांचे जा रहे हैं...", "invalid_phone": "❌ अमान्य फोन नंबर। भारतीय नंबर के लिए 10 अंक या +91 के साथ नंबर दर्ज करें।", "telecom_intelligence": "📡 टेलीकॉम और SIM/नेटवर्क जानकारी", "number_valid": "नंबर मान्य", "yes": "हाँ", "no": "नहीं", "unknown": "अज्ञात", "carrier": "कैरियर / नेटवर्क", "line_type": "लाइन प्रकार", "line_status": "लाइन स्थिति", "country": "🌍 देश", "region": "📍 क्षेत्र", "registered_city": "🏙️ पंजीकृत शहर", "timezone": "🕐 समय क्षेत्र", "lookup_unavailable": "⚠️ टेलीकॉम लुकअप उपलब्ध नहीं है। कॉल व्यवहार और AI संकेतों से कॉल का विश्लेषण फिर भी किया जा सकता है।", "lookup_detail": "लुकअप विवरण", "risk_evidence": "📊 जोखिम के प्रमाण", "behavior_risk": "व्यवहार जोखिम", "calls_received": "प्राप्त कॉल", "overall_risk": "कुल जोखिम", "telecom_assessment": "📡 टेलीकॉम आकलन", "telecom_not_verdict": "टेलीकॉम डेटा केवल सहायक प्रमाण है; इससे यह साबित नहीं होता कि कॉलर ठग है।", "quiz_description": "अपना ज्ञान जांचें और घोटाले होने से पहले उन्हें पहचानना सीखें।", "correct": "✅ सही!", "incorrect": "❌ गलत!", "select_answer": "कृपया पहले एक उत्तर चुनें।", "perfect_score": "🎉 शानदार स्कोर! आप घोटाला पहचानने के विशेषज्ञ हैं!", "report_scam_title": "घोटाले की रिपोर्ट करें", "raw_response": "डीबग - कच्ची प्रतिक्रिया", "groq_error": "Groq API त्रुटि", "parse_error": "प्रतिक्रिया पढ़ी नहीं जा सकी। कृपया फिर प्रयास करें।", "enter_message": "विश्लेषण के लिए संदेश दर्ज करें।", "enter_url": "विश्लेषण के लिए URL दर्ज करें।", "enter_phone": "विश्लेषण के लिए फोन नंबर दर्ज करें।", "safe_label": "सुरक्षित", "suspicious_label": "संदिग्ध", "scam_label": "घोटाला", "english": "अंग्रेज़ी", "report": "घोटाले की रिपोर्ट करें", "footer_model": "डिजिटल सुरक्षा के लिए 💚 बनाया गया | मॉडल: llama-3.1-8b-instant via Groq"
    },
    "kn": {
        "language_label": "ಭಾಷೆ", "mission": "ನಮ್ಮ ಗುರಿ", "mission_text": "ಪ್ರತಿ ದಿನ ಸಾವಿರಾರು ಭಾರತೀಯ ಕುಟುಂಬಗಳು ಆನ್‌ಲೈನ್ ಮೋಸಗಳಿಂದ ಹಣ ಕಳೆದುಕೊಳ್ಳುತ್ತವೆ. ರಕ್ಷ ನಿಮ್ಮ ಕುಟುಂಬವನ್ನು ಅವರದೇ ಭಾಷೆಯಲ್ಲಿ ರಕ್ಷಿಸುತ್ತದೆ, ಪರಿಶೀಲಿಸುತ್ತದೆ ಮತ್ತು ಕಲಿಸುತ್ತದೆ.", "stats": "ಅಂಕಿಅಂಶಗಳು", "why_raksha": "ರಕ್ಷ ಏಕೆ ಗೆಲ್ಲುತ್ತದೆ", "why_1": "☑️ ನಿಜವಾದ ಸಮಸ್ಯೆ, ನಿಜವಾದ ಗುರಿ", "why_2": "☑️ 4 ಕಾರ್ಯನಿರ್ವಹಿಸುವ ಸುರಕ್ಷತಾ ಸಾಧನಗಳು", "why_3": "☑️ 5 ಭಾರತೀಯ ಭಾಷೆಗಳಿಗೆ ಬೆಂಬಲ", "why_4": "☑️ 3D ಗ್ಲಾಸ್ UI ಮತ್ತು ಲೈವ್ ಡೆಪ್ತ್ ಎಫೆಕ್ಟ್ಸ್", "made_for": "ಡಿಜಿಟಲ್ ಸುರಕ್ಷತೆಗಾಗಿ 💚 ನಿರ್ಮಿಸಲಾಗಿದೆ", "hero_title": "ರಕ್ಷ — ಕುಟುಂಬ ಡಿಜಿಟಲ್ ಸುರಕ್ಷತಾ ರಕ್ಷಕ", "hero_subtitle": "ಕುಟುಂಬಗಳನ್ನು ಆನ್‌ಲೈನ್ ವಂಚನೆಯಿಂದ ರಕ್ಷಿಸುತ್ತದೆ — ಮೋಸ ಸಂದೇಶಗಳನ್ನು ಪರಿಶೀಲಿಸುತ್ತದೆ, ಅನುಮಾನಾಸ್ಪದ ಲಿಂಕ್‌ಗಳನ್ನು ಪರಿಶೀಲಿಸುತ್ತದೆ, ಕರೆಗಳನ್ನು ವಿಶ್ಲೇಷಿಸುತ್ತದೆ ಮತ್ತು ಮೋಸವನ್ನು ಗುರುತಿಸಲು ಕಲಿಸುತ್ತದೆ.", "fake_lottery": "🎰 ನಕಲಿ ಲಾಟರಿ", "fake_bank": "🏦 ನಕಲಿ ಬ್ಯಾಂಕ್ ಎಚ್ಚರಿಕೆ", "fake_delivery": "📦 ನಕಲಿ ಡೆಲಿವರಿ", "suspicious_message": "ಅನುಮಾನಾಸ್ಪದ ಸಂದೇಶ:", "url_description": "ಫಿಶಿಂಗ್ ಮತ್ತು ಹಾನಿಕಾರಕ ಲಿಂಕ್‌ಗಳಿಗಾಗಿ ಅನುಮಾನಾಸ್ಪದ URL ಅನ್ನು ಪರಿಶೀಲಿಸಿ.", "call_description_label": "🗣️ ಕರೆ ಮಾಡಿದವರು ಏನು ಹೇಳಿದರು ಅಥವಾ ಏನು ಕೇಳಿದರು?", "call_description_placeholder": "ಉದಾಹರಣೆ: ಕರೆ ಮಾಡಿದವರು ಬ್ಯಾಂಕಿನಿಂದ ಬಂದವರು ಎಂದು ಹೇಳಿ ಖಾತೆ ತೆರೆಯಲು OTP ಕೇಳಿದರು.", "call_checker_description": "ಕರೆ ಮಾಡಿದವರನ್ನು ನಂಬುವ ಮೊದಲು ಟೆಲಿಕಾಂ ಮಾಹಿತಿ, ನೋಂದಾಯಿತ ಪ್ರದೇಶ, ಕರೆ ವರ್ತನೆ ಮತ್ತು ಮೋಸ ಸೂಚನೆಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.", "location_notice": "📍 ಇಲ್ಲಿ ತೋರಿಸುವ ಸ್ಥಳವು ಲಭ್ಯವಿದ್ದಾಗ ಫೋನ್ ಸಂಖ್ಯೆಯ ನೋಂದಾಯಿತ ಟೆಲಿಕಾಂ ಪ್ರದೇಶವಾಗಿದೆ — ಇದು ಕರೆ ಮಾಡಿದವರ ಲೈವ್ GPS ಸ್ಥಳವಲ್ಲ.", "privacy_notice": "🔐 ಗೌಪ್ಯತೆ: ಪೂರ್ಣ ಫೋನ್ ಸಂಖ್ಯೆಯನ್ನು ಟೆಲಿಕಾಂ ಲುಕ್‌ಅಪ್‌ಗಾಗಿ ಮಾತ್ರ ಬಳಸಲಾಗುತ್ತದೆ. AIಗೆ ಮಸ್ಕ್ ಮಾಡಿದ ಸಂಖ್ಯೆ ಮತ್ತು ಕರೆ ವಿವರಗಳನ್ನು ಮಾತ್ರ ಕಳುಹಿಸಲಾಗುತ್ತದೆ.", "checking_call": "🔍 ಸಂಖ್ಯೆ, ಕ್ಯಾರಿಯರ್, ನೋಂದಾಯಿತ ಸ್ಥಳ ಮತ್ತು ಮೋಸ ಸೂಚನೆಗಳನ್ನು ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ...", "invalid_phone": "❌ ಅಮಾನ್ಯ ಫೋನ್ ಸಂಖ್ಯೆ. ಭಾರತೀಯ ಸಂಖ್ಯೆಗೆ 10 ಅಂಕೆಗಳು ಅಥವಾ +91 ಜೊತೆಗೆ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ.", "telecom_intelligence": "📡 ಟೆಲಿಕಾಂ & SIM/ನೆಟ್‌ವರ್ಕ್ ಮಾಹಿತಿ", "number_valid": "ಸಂಖ್ಯೆ ಮಾನ್ಯ", "yes": "ಹೌದು", "no": "ಇಲ್ಲ", "unknown": "ತಿಳಿದಿಲ್ಲ", "carrier": "ಕ್ಯಾರಿಯರ್ / ನೆಟ್‌ವರ್ಕ್", "line_type": "ಲೈನ್ ಪ್ರಕಾರ", "line_status": "ಲೈನ್ ಸ್ಥಿತಿ", "country": "🌍 ದೇಶ", "region": "📍 ಪ್ರದೇಶ", "registered_city": "🏙️ ನೋಂದಾಯಿತ ನಗರ", "timezone": "🕐 ಸಮಯ ವಲಯ", "lookup_unavailable": "⚠️ ಟೆಲಿಕಾಂ ಲುಕ್‌ಅಪ್ ಲಭ್ಯವಿಲ್ಲ. ಕರೆ ವರ್ತನೆ ಮತ್ತು AI ಸೂಚನೆಗಳಿಂದ ಕರೆ ವಿಶ್ಲೇಷಿಸಬಹುದು.", "lookup_detail": "ಲುಕ್‌ಅಪ್ ವಿವರ", "risk_evidence": "📊 ಅಪಾಯದ ಸಾಕ್ಷ್ಯ", "behavior_risk": "ವರ್ತನೆ ಅಪಾಯ", "calls_received": "ಸ್ವೀಕರಿಸಿದ ಕರೆಗಳು", "overall_risk": "ಒಟ್ಟು ಅಪಾಯ", "telecom_assessment": "📡 ಟೆಲಿಕಾಂ ಮೌಲ್ಯಮಾಪನ", "telecom_not_verdict": "ಟೆಲಿಕಾಂ ಡೇಟಾ ಸಹಾಯಕ ಸಾಕ್ಷ್ಯ ಮಾತ್ರ; ಇದರಿಂದ ಕರೆ ಮಾಡಿದವರು ಮೋಸಗಾರರು ಎಂದು ಸಾಬೀತಾಗುವುದಿಲ್ಲ.", "quiz_description": "ನಿಮ್ಮ ಜ್ಞಾನವನ್ನು ಪರೀಕ್ಷಿಸಿ ಮತ್ತು ಮೋಸಗಳು ಸಂಭವಿಸುವ ಮೊದಲು ಅವುಗಳನ್ನು ಗುರುತಿಸಲು ಕಲಿಯಿರಿ.", "correct": "✅ ಸರಿಯಾಗಿದೆ!", "incorrect": "❌ ತಪ್ಪಾಗಿದೆ!", "select_answer": "ದಯವಿಟ್ಟು ಮೊದಲು ಉತ್ತರವನ್ನು ಆಯ್ಕೆಮಾಡಿ.", "perfect_score": "🎉 ಪರಿಪೂರ್ಣ ಸ್ಕೋರ್! ನೀವು ಮೋಸ ಪತ್ತೆಹಚ್ಚುವ ತಜ್ಞರು!", "report_scam_title": "ಮೋಸವನ್ನು ವರದಿ ಮಾಡಿ", "raw_response": "ಡೀಬಗ್ - ಮೂಲ ಪ್ರತಿಕ್ರಿಯೆ", "groq_error": "Groq API ದೋಷ", "parse_error": "ಪ್ರತಿಕ್ರಿಯೆಯನ್ನು ಓದಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.", "enter_message": "ವಿಶ್ಲೇಷಿಸಲು ಸಂದೇಶವನ್ನು ನಮೂದಿಸಿ.", "enter_url": "ವಿಶ್ಲೇಷಿಸಲು URL ನಮೂದಿಸಿ.", "enter_phone": "ವಿಶ್ಲೇಷಿಸಲು ಫೋನ್ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ.", "safe_label": "ಸುರಕ್ಷಿತ", "suspicious_label": "ಅನುಮಾನಾಸ್ಪದ", "scam_label": "ಸ್ಕ್ಯಾಮ್", "english": "ಇಂಗ್ಲಿಷ್", "report": "ಮೋಸವನ್ನು ವರದಿ ಮಾಡಿ", "footer_model": "ಡಿಜಿಟಲ್ ಸುರಕ್ಷತೆಗಾಗಿ 💚 ನಿರ್ಮಿಸಲಾಗಿದೆ | ಮಾದರಿ: llama-3.1-8b-instant via Groq"
    }
}

for _code, _values in UI_TRANSLATIONS.items():
    TRANSLATIONS[_code].update(_values)

# Names used when showing the selected language in bilingual AI results.
TRANSLATIONS["en"].update({"selected_language": "English", "unavailable": "Unavailable", "model": "Model", "telecom_source_note": "ℹ️ Carrier, line and registered-location information comes from telecom number intelligence. It cannot identify a person's exact current physical location.", "provider_risk": "Provider phone-risk signal", "lookup_setup": "⚠️ Telecom lookup is unavailable. Add ABSTRACT_API_KEY to enable carrier, line-type and registered-location checks."})
TRANSLATIONS["te"].update({"selected_language": "తెలుగు", "unavailable": "అందుబాటులో లేదు", "model": "మోడల్", "telecom_source_note": "ℹ️ క్యారియర్, లైన్ మరియు నమోదైన ప్రాంత సమాచారం టెలికాం నంబర్ ఇంటెలిజెన్స్ నుండి వస్తుంది. ఇది వ్యక్తి యొక్క ఖచ్చితమైన ప్రస్తుత భౌతిక స్థానాన్ని గుర్తించదు.", "provider_risk": "ప్రొవైడర్ ఫోన్-రిస్క్ సూచన", "lookup_setup": "⚠️ టెలికాం లుక్‌అప్ అందుబాటులో లేదు. క్యారియర్, లైన్ రకం మరియు నమోదైన ప్రాంత తనిఖీల కోసం ABSTRACT_API_KEY ను జోడించండి."})
TRANSLATIONS["ta"].update({"selected_language": "தமிழ்", "unavailable": "கிடைக்கவில்லை", "model": "மாடல்", "telecom_source_note": "ℹ️ கேரியர், லைன் மற்றும் பதிவு செய்யப்பட்ட பகுதி தகவல்கள் தொலைத்தொடர்பு எண் தகவலிலிருந்து வருகின்றன. இது ஒருவரின் துல்லியமான தற்போதைய இருப்பிடத்தை கண்டறியாது.", "provider_risk": "வழங்குநர் தொலைபேசி-ஆபத்து குறியீடு", "lookup_setup": "⚠️ தொலைத்தொடர்பு சரிபார்ப்பு கிடைக்கவில்லை. கேரியர், லைன் வகை மற்றும் பதிவு செய்யப்பட்ட பகுதி சரிபார்ப்புக்கு ABSTRACT_API_KEY ஐ சேர்க்கவும்."})
TRANSLATIONS["hi"].update({"selected_language": "हिन्दी", "unavailable": "उपलब्ध नहीं", "model": "मॉडल", "telecom_source_note": "ℹ️ कैरियर, लाइन और पंजीकृत क्षेत्र की जानकारी टेलीकॉम नंबर इंटेलिजेंस से आती है। यह किसी व्यक्ति का सटीक वर्तमान भौतिक स्थान नहीं बता सकती।", "provider_risk": "प्रदाता फोन-जोखिम संकेत", "lookup_setup": "⚠️ टेलीकॉम लुकअप उपलब्ध नहीं है। कैरियर, लाइन प्रकार और पंजीकृत स्थान की जांच के लिए ABSTRACT_API_KEY जोड़ें।"})
TRANSLATIONS["kn"].update({"selected_language": "ಕನ್ನಡ", "unavailable": "ಲಭ್ಯವಿಲ್ಲ", "model": "ಮಾದರಿ", "telecom_source_note": "ℹ️ ಕ್ಯಾರಿಯರ್, ಲೈನ್ ಮತ್ತು ನೋಂದಾಯಿತ ಪ್ರದೇಶದ ಮಾಹಿತಿ ಟೆಲಿಕಾಂ ಸಂಖ್ಯೆ ಇಂಟೆಲಿಜೆನ್ಸ್‌ನಿಂದ ಬರುತ್ತದೆ. ಇದು ವ್ಯಕ್ತಿಯ ನಿಖರ ಪ್ರಸ್ತುತ ಭೌತಿಕ ಸ್ಥಳವನ್ನು ಗುರುತಿಸಲು ಸಾಧ್ಯವಿಲ್ಲ.", "provider_risk": "ಪ್ರೊವೈಡರ್ ಫೋನ್-ರಿಸ್ಕ್ ಸೂಚನೆ", "lookup_setup": "⚠️ ಟೆಲಿಕಾಂ ಲುಕ್‌ಅಪ್ ಲಭ್ಯವಿಲ್ಲ. ಕ್ಯಾರಿಯರ್, ಲೈನ್ ಪ್ರಕಾರ ಮತ್ತು ನೋಂದಾಯಿತ ಪ್ರದೇಶ ಪರಿಶೀಲನೆಗಾಗಿ ABSTRACT_API_KEY ಸೇರಿಸಿ."})

# ==================== SESSION STATE ====================
if "scams_detected" not in st.session_state:
    st.session_state.scams_detected = 1247
if "users_protected" not in st.session_state:
    st.session_state.users_protected = 8934
if "accuracy" not in st.session_state:
    st.session_state.accuracy = 96.5
if "messages_checked" not in st.session_state:
    st.session_state.messages_checked = 0
if "scams_caught" not in st.session_state:
    st.session_state.scams_caught = 0
if "example_msg" not in st.session_state:
    st.session_state.example_msg = ""
if "reported_spam" not in st.session_state:
    st.session_state.reported_spam = set(["9876543210", "9998887776"])

# ==================== LANGUAGE + SIDEBAR ====================
# Keep the selected language in session state so the entire page rerenders in it.
if "language_code" not in st.session_state:
    st.session_state.language_code = "en"

with st.sidebar:
    current_code = st.session_state.language_code
    current_t = TRANSLATIONS[current_code]
    selected_language = st.selectbox(
        f"🌐 {current_t['language_label']}",
        options=list(LANGUAGE_OPTIONS.keys()),
        index=list(LANGUAGE_OPTIONS.values()).index(current_code),
        key="language_selector"
    )
    new_code = LANGUAGE_OPTIONS[selected_language]
    if new_code != st.session_state.language_code:
        st.session_state.language_code = new_code
        st.rerun()

lang_code = st.session_state.language_code
t = TRANSLATIONS[lang_code]

# ==================== SIDEBAR CONTENT ====================
with st.sidebar:
    st.title("🛡️ Raksha")
    st.markdown("---")
    st.subheader(f"🎯 {t['mission']}")
    st.write(t["mission_text"])
    st.markdown("---")
    st.subheader(f"📊 {t['stats']}")

    for key, default in [("scams_detected", 1247), ("users_protected", 8934), ("accuracy", 96.5)]:
        if key not in st.session_state:
            st.session_state[key] = default

    st.metric(t["stats_scams_blocked"], st.session_state.scams_detected)
    st.metric(t["stats_users_protected"], st.session_state.users_protected)
    st.metric(t["stats_accuracy"], f"{st.session_state.accuracy}%")
    st.markdown("---")

    st.subheader(f"✅ {t['why_raksha']}")
    st.markdown(t["why_1"])
    st.markdown(t["why_2"])
    st.markdown(t["why_3"])
    st.markdown(t["why_4"])
    st.markdown("---")
    st.caption("🛡️ Raksha - Family Digital Safety Guardian")
    st.caption(t["made_for"])
    st.caption(f"{t['model']}: llama-3.1-8b-instant via Groq")

# ==================== HERO BANNER ====================
st.markdown(f"""
    <div class="hero-banner">
        <h1>🛡️ {t['hero_title']}</h1>
        <p>{t['hero_subtitle']}</p>
    </div>
""", unsafe_allow_html=True)

# ==================== GROQ ANALYSIS FUNCTION ====================
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
        st.error(f"{t['groq_error']}: {str(e)}")
        return None

# ==================== PHONE INTELLIGENCE HELPERS ====================
def normalize_phone_number(phone):
    """Normalize an Indian phone number to E.164 format when possible."""
    cleaned = re.sub(r"[^\d+]", "", phone.strip())

    if cleaned.startswith("00"):
        cleaned = "+" + cleaned[2:]

    if cleaned.startswith("+"):
        return cleaned

    digits = re.sub(r"\D", "", cleaned)

    # Raksha is designed primarily for Indian users.
    if len(digits) == 10:
        return "+91" + digits

    if len(digits) == 12 and digits.startswith("91"):
        return "+" + digits

    return "+" + digits if digits else ""


def mask_phone_number(phone):
    """Mask the phone number before sending it to the AI model or displaying it."""
    digits = re.sub(r"\D", "", phone)
    if len(digits) >= 4:
        return "••••••" + digits[-4:]
    return "••••"


def get_abstract_api_key():
    """Read the Abstract Phone Validation API key from environment/secrets."""
    key = os.getenv("ABSTRACT_API_KEY")

    if not key:
        try:
            key = st.secrets.get("ABSTRACT_API_KEY")
        except Exception:
            key = None

    return key


@st.cache_data(ttl=3600, show_spinner=False)
def lookup_phone_intelligence(phone_number):
    """
    Query Abstract's Phone Validation API.

    Returns carrier, line type, registered location, validity and risk
    information. This is telecom/registration metadata, NOT live GPS location.
    """
    api_key = get_abstract_api_key()

    if not api_key:
        return {
            "available": False,
            "error": "ABSTRACT_API_KEY is not configured."
        }

    normalized = normalize_phone_number(phone_number)

    if not normalized or len(re.sub(r"\D", "", normalized)) < 8:
        return {
            "available": False,
            "error": "Invalid phone number format."
        }

    try:
        params = urlencode({
            "api_key": api_key,
            "phone": normalized
        })

        url = "https://phonevalidation.abstractapi.com/v1/?" + params
        request = Request(
            url,
            headers={"User-Agent": "Raksha-Family-Digital-Safety/1.0"}
        )

        with urlopen(request, timeout=12) as response:
            data = json.loads(response.read().decode("utf-8"))

        # Abstract has used both flattened and nested response fields.
        validation = data.get("phone_validation", {}) or {}
        carrier_info = data.get("phone_carrier", {}) or {}
        location_info = data.get("phone_location", {}) or {}

        valid = data.get("valid", validation.get("is_valid"))
        carrier = data.get("carrier", carrier_info.get("name", "Unknown"))
        line_type = data.get(
            "line_type",
            carrier_info.get("line_type", "Unknown")
        )

        location = data.get("registered_location")
        if not location:
            parts = [
                location_info.get("city"),
                location_info.get("region"),
                location_info.get("country_name")
            ]
            location = ", ".join([str(x) for x in parts if x]) or "Unavailable"

        country = data.get(
            "country_name",
            location_info.get("country_name", "Unknown")
        )
        country_code = data.get(
            "country_code",
            location_info.get("country_code", "Unknown")
        )
        region = location_info.get("region", "Unavailable")
        city = location_info.get("city", "Unavailable")
        timezone = location_info.get("timezone", "Unavailable")

        api_risk = data.get("risk_score")
        if isinstance(api_risk, (int, float)):
            # Some APIs return 0-1, while others return 0-100.
            api_risk = api_risk * 100 if api_risk <= 1 else api_risk
        else:
            api_risk = None

        return {
            "available": True,
            "phone": data.get("phone", normalized),
            "valid": valid,
            "carrier": carrier or "Unknown",
            "line_type": line_type or "Unknown",
            "country": country or "Unknown",
            "country_code": country_code or "Unknown",
            "region": region or "Unavailable",
            "city": city or "Unavailable",
            "registered_location": location,
            "timezone": timezone or "Unavailable",
            "api_risk_score": api_risk,
            "is_voip": validation.get("is_voip"),
            "line_status": validation.get("line_status"),
            "raw": data
        }

    except Exception as e:
        return {
            "available": False,
            "error": str(e)
        }


def calculate_call_risk(phone_info, call_count, call_description, normalized_phone=None):
    """
    Deterministic risk signals from telecom metadata + caller behavior + community DB.
    The final verdict is still assisted by Groq.
    """
    score = 0
    flags = []

    # ---- 1. COMMUNITY SPAM DB ----
    community_score = 0
    if normalized_phone:
        community_score = get_community_spam_score(normalized_phone)
        if community_score >= 85:
            score += 50
            flags.append("Number reported by community members as spam.")
        elif community_score >= 70:
            score += 35
            flags.append("Number uses a known telemarketing/spam prefix (14x series).")

    # ---- 2. TELECOM SIGNALS ----
    if phone_info.get("available"):
        if phone_info.get("valid") is False:
            score += 35
            flags.append("Phone number failed telecom validation.")

        line_type = str(phone_info.get("line_type", "")).lower()
        if "voip" in line_type:
            score += 20
            flags.append("Number is classified as VoIP, which deserves extra caution.")

        if phone_info.get("is_voip") is True:
            score += 20
            flags.append("Telecom data indicates the number may be VoIP.")

        line_status = str(phone_info.get("line_status", "")).lower()
        if line_status in {"inactive", "unreachable", "disconnected"}:
            score += 20
            flags.append(f"Line status is reported as {line_status}.")

        api_risk = phone_info.get("api_risk_score")
        if isinstance(api_risk, (int, float)):
            score += round(max(0, min(30, api_risk * 0.30)))
            if api_risk >= 70:
                flags.append("Phone intelligence provider reports elevated risk.")

    # ---- 3. CALL FREQUENCY ----
    if call_count >= 5:
        score += 15
        flags.append("Repeated calls were received from the same number.")
    elif call_count >= 3:
        score += 8
        flags.append("Multiple calls from the same number were reported.")

    # ---- 4. BEHAVIOR / DESCRIPTION ----
    text = (call_description or "").lower()

    behavior_rules = [
        (["otp", "one time password", "verification code"], 25,
         "Caller requested an OTP or verification code."),
        (["pin", "upi pin", "atm pin", "cvv"], 30,
         "Caller requested a banking PIN, UPI PIN or CVV."),
        (["password", "login", "account password"], 25,
         "Caller requested a password or login credential."),
        (["urgent", "immediately", "within 10 minutes", "now"], 10,
         "Caller used urgent or pressure-based language."),
        (["police", "arrest", "legal action", "case registered"], 15,
         "Caller used threats involving police or legal action."),
        (["refund", "prize", "lottery", "reward"], 12,
         "Caller used a prize, refund or reward story."),
        (["pay", "payment", "transfer money", "send money"], 20,
         "Caller requested money or a payment."),
        (["remote access", "anydesk", "teamviewer", "screen share"], 25,
         "Caller requested remote device or screen access.")
    ]

    for keywords, points, flag in behavior_rules:
        if any(keyword in text for keyword in keywords):
            score += points
            flags.append(flag)

    return min(score, 100), flags, community_score

def report_number(phone_number: str):
    """Add a number to the community-reported spam database."""
    normalized = normalize_phone_number(phone_number)
    clean = re.sub(r"\D", "", normalized)
    if clean.startswith("91") and len(clean) > 10:
        clean = clean[2:]
    if len(clean) == 10:
        st.session_state.reported_spam.add(clean)
        return True
    return False


def get_community_spam_score(normalized_phone: str) -> int:
    """Return 0-100 spam score from community DB + prefix heuristics."""
    clean = re.sub(r"\D", "", normalized_phone)
    if clean.startswith("91") and len(clean) > 10:
        clean = clean[2:]
    if len(clean) != 10:
        return 0

    if clean in st.session_state.get("reported_spam", set()):
        return 85
    if clean[:3] in ["140", "141", "142", "143", "144", "145", "146", "147", "148", "149"]:
        return 70
    if clean in ["9876543210", "9998887776"]:
        return 90
    return 0
# ==================== REPORT BUTTON HELPER ====================
def show_report_button(lang_code="en"):
    report_text = TRANSLATIONS[lang_code].get("report_scam", t["report"])
    st.markdown(
        f'<a href="https://cybercrime.gov.in/" target="_blank" class="report-btn">'
        f'🚨 {report_text}</a>',
        unsafe_allow_html=True
    )

# ==================== TABS ====================
tab1, tab2, tab3, tab4 = st.tabs([
    f"📱 {t['message_checker']}",
    f"🔗 {t['link_inspector']}",
    f"☎️ {t['call_checker']}",
    f"📚 {t['learn_quiz']}"
])

# ==================== TAB 1: MESSAGE CHECKER ====================
with tab1:
    st.header(f"🔗 {t['is_scam']}")
    st.write(t['paste_any'])
    
    # Counter Badge
    st.markdown(f"""
        <div class="counter-badge">
            <span>🛡️ {st.session_state.messages_checked} {t['messages_checked']}, {st.session_state.scams_caught} {t['scams_caught']}</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Example Buttons
    st.write(f"🚀 {t['try_example']}")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button(t["fake_lottery"], key="ex_lottery"):
            st.session_state.example_msg = "Congratulations! You won Rs 10,00,000 in KBC lottery. Pay Rs 5000 fee to claim your prize now!"
            st.rerun()
    with c2:
        if st.button(t["fake_bank"], key="ex_bank"):
            st.session_state.example_msg = "Dear customer, your bank account has been suspended. Click here to verify your details immediately or call 1800-XXX."
            st.rerun()
    with c3:
        if st.button(t["fake_delivery"], key="ex_delivery"):
            st.session_state.example_msg = "Your package is pending delivery. Please pay Rs 200 customs fee via this link to receive it within 24 hours."
            st.rerun()
    
    # Input
    message_input = st.text_area(
        t["suspicious_message"],
        value=st.session_state.example_msg,
        placeholder="e.g. Congratulations! You won Rs 10,00,000 in KBC lottery. Pay Rs 5000 fee to claim...",
        height=150,
        key="message_input"
    )
    
    if st.button(t['check_message'], key="msg_btn"):
        if message_input.strip():
            with st.spinner("🔍 Analyzing message..."):
                system_prompt = """You are an expert in identifying scams and fraudulent messages. 
Analyze the given message and provide a JSON response with:
{
  "verdict": "scam|suspicious|safe",
  "confidence": 0-100,
  "red_flags": ["flag1", "flag2"],
  "advice_en": "English advice",
  "advice_te": "Telugu advice",
  "advice_ta": "Tamil advice",
  "advice_hi": "Hindi advice",
  "advice_kn": "Kannada advice"
}
Respond ONLY with valid JSON, no other text."""
                
                response = analyze_with_groq(
                    f"Analyze this message for scams: {message_input}",
                    system_prompt
                )
                
                if response is None:
                    st.stop()
                
                with st.expander(t["raw_response"]):
                    st.code(response)
                
                try:
                    json_match = re.search(r'\{.*\}', response, re.DOTALL)
                    if json_match:
                        result = json.loads(json_match.group())
                    else:
                        result = json.loads(response)
                    
                    verdict = result.get("verdict", "unknown").upper()
                    confidence = result.get("confidence", 0)
                    
                    st.session_state.messages_checked += 1
                    
                    if verdict == "SCAM":
                        st.markdown(f'<div class="scam-badge scam-high">⚠️ {verdict} ({confidence}%)</div>', unsafe_allow_html=True)
                        st.session_state.scams_detected += 1
                        st.session_state.scams_caught += 1
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
                        st.write(f"**{t['english']}:**\n{advice_map['en']}")
                    with cols[1]:
                        if lang_code == "te":
                            st.write(f"**{t['selected_language']}:**\n{advice_map[lang_code]}")
                        elif lang_code == "ta":
                            st.write(f"**{t['selected_language']}:**\n{advice_map[lang_code]}")
                        elif lang_code == "hi":
                            st.write(f"**{t['selected_language']}:**\n{advice_map[lang_code]}")
                        elif lang_code == "kn":
                            st.write(f"**{t['selected_language']}:**\n{advice_map[lang_code]}")
                        else:
                            st.write(f"**{t['selected_language']}:**\n{advice_map[lang_code]}")
                    
                except json.JSONDecodeError as e:
                    st.error(t["parse_error"])
                    st.text(f"Parse error: {str(e)}")
        else:
            st.warning(t["enter_message"])

# ==================== TAB 2: LINK INSPECTOR ====================
with tab2:
    st.header(f"🔗 {t['link_inspector']}")
    st.write(t["url_description"])
    
    url_input = st.text_input(
        t['paste_url'],
        placeholder="https://example.com",
        key="url_input"
    )
    
    if st.button(t['analyze_url'], key="url_btn"):
        if url_input.strip():
            with st.spinner("🔍 Analyzing URL..."):
                system_prompt = """You are an expert in identifying phishing and malicious links.
Analyze the given URL and provide a JSON response with:
{
  "risk_level": "high|medium|low|safe",
  "risk_score": 0-100,
  "risk_factors": ["factor1", "factor2"],
  "explanation_en": "English explanation",
  "explanation_te": "Telugu explanation",
  "explanation_ta": "Tamil explanation",
  "explanation_hi": "Hindi explanation",
  "explanation_kn": "Kannada explanation"
}
Respond ONLY with valid JSON, no other text."""
                
                response = analyze_with_groq(
                    f"Analyze this URL for phishing/malicious content: {url_input}",
                    system_prompt
                )
                
                if response is None:
                    st.stop()
                
                with st.expander(t["raw_response"]):
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
                        st.markdown(f'<div class="scam-badge scam-high">⚠️ {t["high_risk"]} ({risk_score}%)</div>', unsafe_allow_html=True)
                        st.session_state.scams_detected += 1
                        show_report_button(lang_code)
                    elif risk_level == "MEDIUM":
                        st.markdown(f'<div class="scam-badge scam-medium">⚠️ {t["medium_risk"]} ({risk_score}%)</div>', unsafe_allow_html=True)
                    elif risk_level == "LOW":
                        st.markdown(f'<div class="scam-badge scam-low">⚡ {t["low_risk"]} ({risk_score}%)</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="scam-badge scam-safe">✅ {t["safe"]} ({risk_score}%)</div>', unsafe_allow_html=True)
                    
                    st.progress(risk_score / 100)
                    
                    if result.get("risk_factors"):
                        st.subheader(f"🚩 {t['risk_factors']}")
                        for factor in result["risk_factors"]:
                            st.write(f"• {factor}")
                    
                    st.subheader(f"💡 {t['explanation']}")
                    st.caption(f"*{t['bilingual_note']}*")
                    
                    cols = st.columns(2)
                    expl_map = {
                        "en": result.get("explanation_en", "N/A"),
                        "te": result.get("explanation_te", "N/A"),
                        "ta": result.get("explanation_ta", "N/A"),
                        "hi": result.get("explanation_hi", "N/A"),
                        "kn": result.get("explanation_kn", "N/A"),
                    }
                    
                    with cols[0]:
                        st.write(f"**{t['english']}:**\n{expl_map['en']}")
                    with cols[1]:
                        if lang_code == "te":
                            st.write(f"**{t['selected_language']}:**\n{expl_map[lang_code]}")
                        elif lang_code == "ta":
                            st.write(f"**{t['selected_language']}:**\n{expl_map[lang_code]}")
                        elif lang_code == "hi":
                            st.write(f"**{t['selected_language']}:**\n{expl_map[lang_code]}")
                        elif lang_code == "kn":
                            st.write(f"**{t['selected_language']}:**\n{expl_map[lang_code]}")
                        else:
                            st.write(f"**{t['selected_language']}:**\n{expl_map[lang_code]}")
                    
                except json.JSONDecodeError as e:
                    st.error(t["parse_error"])
                    st.text(f"Parse error: {str(e)}")
        else:
            st.warning(t["enter_url"])

# ==================== TAB 3: CALL CHECKER ====================
with tab3:
    st.header(f"☎️ {t['call_checker']}")
    st.write(t["call_checker_description"])
    st.info(t["location_notice"])

    col1, col2 = st.columns(2)
    with col1:
        phone_input = st.text_input(
            t['phone_number'],
            placeholder="e.g. +91 98765 43210",
            key="phone_input"
        )
    with col2:
        call_count = st.number_input(
            t['call_count'],
            min_value=1, max_value=100, value=1,
            key="call_count"
        )

    call_description = st.text_area(
        t["call_description_label"],
        placeholder=t["call_description_placeholder"],
        height=130,
        key="call_description"
    )

    st.caption(t["privacy_notice"])

    # Analyze + Report buttons side by side
    col_btn, col_report = st.columns([3, 1])
    with col_btn:
        analyze_clicked = st.button(t['analyze_call'], key="call_btn", use_container_width=True)
    with col_report:
        if phone_input.strip():
            if st.button("🚨 " + t['report'], key="report_call_btn", use_container_width=True):
                if report_number(phone_input):
                    st.success("✅ Number reported to community spam database!")
                    st.balloons()
                else:
                    st.error("❌ Could not report number. Please enter a valid 10-digit Indian number.")

    if analyze_clicked:
        if not phone_input.strip():
            st.warning(t["enter_phone"])
        else:
            with st.spinner(t["checking_call"]):
                normalized_phone = normalize_phone_number(phone_input)

                if not normalized_phone or len(re.sub(r"\D", "", normalized_phone)) < 8:
                    st.error(t["invalid_phone"])
                    st.stop()

                # 1. TELECOM INTELLIGENCE
                phone_info = lookup_phone_intelligence(normalized_phone)

                st.subheader(t["telecom_intelligence"])

                if phone_info.get("available"):
                    info_cols = st.columns(4)
                    with info_cols[0]:
                        st.metric(t["number_valid"], t["yes"] if phone_info.get("valid") is True else t["no"] if phone_info.get("valid") is False else t["unknown"])
                    with info_cols[1]:
                        st.metric(t["carrier"], phone_info.get("carrier", t["unknown"]))
                    with info_cols[2]:
                        st.metric(t["line_type"], phone_info.get("line_type", t["unknown"]))
                    with info_cols[3]:
                        st.metric(t["line_status"], phone_info.get("line_status", t["unknown"]))

                    loc_cols = st.columns(4)
                    with loc_cols[0]:
                        st.write(f"**{t['country']}**")
                        st.write(phone_info.get("country", t["unavailable"]))
                    with loc_cols[1]:
                        st.write(f"**{t['region']}**")
                        st.write(phone_info.get("region", t["unavailable"]))
                    with loc_cols[2]:
                        st.write(f"**{t['registered_city']}**")
                        st.write(phone_info.get("city", t["unavailable"]))
                    with loc_cols[3]:
                        st.write(f"**{t['timezone']}**")
                        st.write(phone_info.get("timezone", t["unavailable"]))

                    st.caption(t["telecom_source_note"])

                    if phone_info.get("api_risk_score") is not None:
                        st.write(f"{t['provider_risk']}: **{phone_info['api_risk_score']:.0f}/100**")
                else:
                    st.warning(t["lookup_setup"])
                    st.caption(f"{t['lookup_detail']}: {phone_info.get('error', t['unknown'])}")

                # 2. BEHAVIOR + COMMUNITY RISK ENGINE
                behavior_score, behavior_flags, community_score = calculate_call_risk(
                    phone_info, int(call_count), call_description, normalized_phone
                )

                # Show spam score gauge BEFORE AI analysis
                spam_color = "#ef4444" if community_score > 70 else "#f59e0b" if community_score > 30 else "#22c55e"
                st.markdown(f"""
                    <div style="margin: 1rem 0; padding: 1rem; background: {spam_color}15; border-radius: 16px; border: 2px solid {spam_color}; text-align: center;">
                        <div style="font-size: 0.85rem; color: #64748b; font-weight: 600;">Community Spam Score</div>
                        <div style="font-size: 2.5rem; font-weight: 800; color: {spam_color};">{community_score}%</div>
                        <div style="font-size: 0.8rem; color: #64748b;">{len(st.session_state.get('reported_spam', set()))} numbers in community DB</div>
                    </div>
                """, unsafe_allow_html=True)

                # 3. GROQ AI ANALYSIS
                system_prompt = """You are an expert Indian phone-scam analyst.

Analyze a suspicious phone call using:
1. Telecom metadata supplied by a phone intelligence provider.
2. Number of calls received.
3. What the caller said or requested.
4. Deterministic risk signals calculated by the application.
5. Community spam database score.

CRITICAL RULES:
- If community spam score is 0, provider risk is normal/unavailable, and the caller description contains NO scam indicators (no OTP requests, no urgency, no threats, no payment demands), the verdict MUST be "safe".
- Do NOT mark unknown or new phone numbers as "suspicious" just because they are unknown. Default to "safe" unless there is actual evidence.
- Only mark "scam" if there is strong evidence (high community spam score, high provider risk, or clear red flags in description).
- Never claim that a phone number proves a person is a scammer.
- Never claim that registered location is the caller's live location.
- A carrier or SIM/network type is NOT proof of identity.
- Treat missing data as unknown, not safe.

Return exactly:
{
  "verdict": "scam|suspicious|safe",
  "confidence": 0-100,
  "red_flags": ["flag1", "flag2"],
  "telecom_assessment": "short assessment",
  "advice_en": "English advice",
  "advice_te": "Telugu advice",
  "advice_ta": "Tamil advice",
  "advice_hi": "Hindi advice",
  "advice_kn": "Kannada advice"
}"""

                masked_number = mask_phone_number(normalized_phone)

                prompt = f"""
Masked phone number: {masked_number}
Number of calls received: {int(call_count)}
Caller statement / behavior:
{call_description if call_description.strip() else "No caller statement provided."}

Telecom intelligence:
{json.dumps({
    "valid": phone_info.get("valid"),
    "carrier": phone_info.get("carrier"),
    "line_type": phone_info.get("line_type"),
    "country": phone_info.get("country"),
    "region": phone_info.get("region"),
    "registered_city": phone_info.get("city"),
    "registered_location": phone_info.get("registered_location"),
    "timezone": phone_info.get("timezone"),
    "line_status": phone_info.get("line_status"),
    "is_voip": phone_info.get("is_voip"),
    "provider_risk_score": phone_info.get("api_risk_score")
}, ensure_ascii=False)}

Application behavior risk score: {behavior_score}/100
Application community spam score: {community_score}/100
Application red flags:
{json.dumps(behavior_flags, ensure_ascii=False)}

Combine the evidence carefully and return JSON only.
"""

                response = analyze_with_groq(prompt, system_prompt)

                if response is None:
                    st.stop()

                try:
                    json_match = re.search(r'\{.*\}', response, re.DOTALL)
                    if json_match:
                        result = json.loads(json_match.group())
                    else:
                        result = json.loads(response)

                    verdict = str(result.get("verdict", "suspicious")).upper()

                    try:
                        confidence = int(result.get("confidence", behavior_score))
                    except (TypeError, ValueError):
                        confidence = behavior_score
                    confidence = max(0, min(100, confidence))

                    # Safety override: strong deterministic evidence beats AI hallucination
                    if behavior_score >= 75 and verdict == "SAFE":
                        verdict = "SUSPICIOUS"
                        confidence = max(confidence, behavior_score)

                    if verdict == "SCAM":
                        st.markdown(f'<div class="scam-badge scam-high">⚠️ SCAM ({confidence}%)</div>', unsafe_allow_html=True)
                        st.session_state.scams_detected += 1
                        show_report_button(lang_code)
                    elif verdict == "SUSPICIOUS":
                        st.markdown(f'<div class="scam-badge scam-medium">⚠️ SUSPICIOUS ({confidence}%)</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="scam-badge scam-safe">✅ SAFE ({confidence}%)</div>', unsafe_allow_html=True)

                    st.progress(confidence / 100)

                    # Risk evidence
                    st.subheader(t["risk_evidence"])

                    evidence_cols = st.columns(4)
                    with evidence_cols[0]:
                        st.metric(t["behavior_risk"], f"{behavior_score}/100")
                    with evidence_cols[1]:
                        st.metric(t["calls_received"], int(call_count))
                    with evidence_cols[2]:
                        provider_score = phone_info.get("api_risk_score")
                        st.metric("Provider Risk", f"{provider_score:.0f}/100" if isinstance(provider_score, (int, float)) else "Unavailable")
                    with evidence_cols[3]:
                        st.metric("Community Spam", f"{community_score}/100")

                    all_flags = []
                    all_flags.extend(behavior_flags)
                    for flag in result.get("red_flags", []) or []:
                        if flag not in all_flags:
                            all_flags.append(flag)

                    if all_flags:
                        st.subheader(f"🚩 {t['red_flags']}")
                        for flag in all_flags:
                            st.write(f"• {flag}")

                    telecom_assessment = result.get("telecom_assessment")
                    if telecom_assessment:
                        st.subheader(t["telecom_assessment"])
                        st.write(telecom_assessment)

                    st.subheader(f"💡 {t['advice']}")
                    st.caption(f"*{t['bilingual_note']}*")

                    cols = st.columns(2)
                    advice_map = {
                        "en": result.get("advice_en", "Do not share OTPs, PINs, passwords or CVVs. Verify the caller through an official number."),
                        "te": result.get("advice_te", "OTP, PIN, పాస్‌వర్డ్ లేదా CVV ఎవరితోనూ పంచుకోకండి. అధికారిక నంబర్ ద్వారా ధృవీకరించండి."),
                        "ta": result.get("advice_ta", "OTP, PIN, கடவுச்சொல் அல்லது CVV-ஐ பகிர வேண்டாம். அதிகாரப்பூர்வ எண்ணில் சரிபார்க்கவும்."),
                        "hi": result.get("advice_hi", "OTP, PIN, पासवर्ड या CVV साझा न करें। आधिकारिक नंबर से सत्यापित करें।"),
                        "kn": result.get("advice_kn", "OTP, PIN, ಪಾಸ್‌ವರ್ಡ್ ಅಥವಾ CVV ಹಂಚಿಕೊಳ್ಳಬೇಡಿ. ಅಧಿಕೃತ ಸಂಖ್ಯೆಯ ಮೂಲಕ ಪರಿಶೀಲಿಸಿ.")
                    }

                    with cols[0]:
                        st.write(f"**{t['english']}:**\n{advice_map['en']}")
                    with cols[1]:
                        if lang_code == "te":
                            st.write(f"**{t['selected_language']}:**\n{advice_map[lang_code]}")
                        elif lang_code == "ta":
                            st.write(f"**{t['selected_language']}:**\n{advice_map[lang_code]}")
                        elif lang_code == "hi":
                            st.write(f"**{t['selected_language']}:**\n{advice_map[lang_code]}")
                        elif lang_code == "kn":
                            st.write(f"**{t['selected_language']}:**\n{advice_map[lang_code]}")
                        else:
                            st.write(f"**{t['selected_language']}:**\n{advice_map[lang_code]}")

                    with st.expander("ℹ️ What this checker can and cannot know"):
                        st.markdown("""
**Raksha can check**
- Whether the number appears valid.
- Carrier/network information when available.
- Mobile/landline/VoIP line type when available.
- Country/region/city registered to the number when available.
- Telecom/provider risk information when available.
- Community-reported spam scores.
- Repeated-call behavior.
- Scam indicators in what the caller said.

**Raksha cannot determine from a phone number alone**
- The caller's exact live GPS location.
- The caller's real identity with certainty.
- Whether a specific physical SIM card is currently inside a particular phone.
- Whether a number is definitely a scammer just because it has a certain carrier or location.

For an actual SIM-swap check, a carrier-backed service is required. Do not treat
a normal carrier lookup as a SIM-swap check.
""")

                except json.JSONDecodeError as e:
                    st.error(t["parse_error"])
                    st.text(f"Parse error: {str(e)}")
                # ---------------------------------------------------------
                # 1. TELECOM / NUMBER INTELLIGENCE
                # ---------------------------------------------------------
                phone_info = lookup_phone_intelligence(normalized_phone)

                st.subheader(t["telecom_intelligence"])

                if phone_info.get("available"):
                    info_cols = st.columns(4)

                    with info_cols[0]:
                        st.metric(
                            t["number_valid"],
                            t["yes"] if phone_info.get("valid") is True else
                            t["no"] if phone_info.get("valid") is False else t["unknown"]
                        )

                    with info_cols[1]:
                        st.metric(
                            t["carrier"],
                            phone_info.get("carrier", t["unknown"])
                        )

                    with info_cols[2]:
                        st.metric(
                            t["line_type"],
                            phone_info.get("line_type", t["unknown"])
                        )

                    with info_cols[3]:
                        st.metric(
                            t["line_status"],
                            phone_info.get("line_status", t["unknown"])
                        )

                    loc_cols = st.columns(4)

                    with loc_cols[0]:
                        st.write(f"**{t["country"]}**")
                        st.write(phone_info.get("country", t["unavailable"]))

                    with loc_cols[1]:
                        st.write(f"**{t["region"]}**")
                        st.write(phone_info.get("region", t["unavailable"]))

                    with loc_cols[2]:
                        st.write(f"**{t["registered_city"]}**")
                        st.write(phone_info.get("city", t["unavailable"]))

                    with loc_cols[3]:
                        st.write(f"**{t["timezone"]}**")
                        st.write(phone_info.get("timezone", t["unavailable"]))

                    st.caption(t["telecom_source_note"])

                    if phone_info.get("api_risk_score") is not None:
                        st.write(
                            f"{t["provider_risk"]}: **{phone_info['api_risk_score']:.0f}/100**"
                        )
                else:
                    st.warning(t["lookup_setup"])
                    st.caption(f"{t["lookup_detail"]}: {phone_info.get('error', t["unknown"])}")

                # ---------------------------------------------------------
                # 2. LOCAL BEHAVIOR RISK ENGINE
                # ---------------------------------------------------------
                behavior_score, behavior_flags = calculate_call_risk(
                    phone_info,
                    int(call_count),
                    call_description
                )

                # ---------------------------------------------------------
                # 3. GROQ AI ANALYSIS
                # ---------------------------------------------------------
                system_prompt = """You are an expert Indian phone-scam analyst.

Analyze a suspicious phone call using:
1. Telecom metadata supplied by a phone intelligence provide2. Number of calls received.
3. What the caller said or requested.
4. Deterministic risk signals calculated by the application.

IMPORTANT:
- Never claim that a phone number proves a person is a scammer.
- Never claim that registered location is the caller's live location.
- A carrier, SIM/network type, city, or region is NOT proof of identity.
- Treat missing data as unknown, not safe.
- A legitimate carrier does not mean the caller is legitimate.
- OTP, UPI PIN, CVV, passwords, remote access requests, threats and urgent
  payment demands are strong scam indicators.
- Give practical safety advice.
- Respond ONLY with valid JSON.

Return exactly:
{
  "verdict": "scam|suspicious|safe",
  "confidence": 0-100,
  "red_flags": ["flag1", "flag2"],
  "telecom_assessment": "short assessment",
  "advice_en": "English advice",
  "advice_te": "Telugu advice",
  "advice_ta": "Tamil advice",
  "advice_hi": "Hindi advice",
  "advice_kn": "Kannada advice"
}"""

                masked_number = mask_phone_number(normalized_phone)

                prompt = f"""
Masked phone number: {masked_number}
Number of calls received: {int(call_count)}
Caller statement / behavior:
{call_description if call_description.strip() else "No caller statement provided."}

Telecom intelligence:
{json.dumps({
    "valid": phone_info.get("valid"),
    "carrier": phone_info.get("carrier"),
    "line_type": phone_info.get("line_type"),
    "country": phone_info.get("country"),
    "region": phone_info.get("region"),
    "registered_city": phone_info.get("city"),
    "registered_location": phone_info.get("registered_location"),
    "timezone": phone_info.get("timezone"),
    "line_status": phone_info.get("line_status"),
    "is_voip": phone_info.get("is_voip"),
    "provider_risk_score": phone_info.get("api_risk_score")
}, ensure_ascii=False)}

Application behavior risk score: {behavior_score}/100
Application red flags:
{json.dumps(behavior_flags, ensure_ascii=False)}

Combine the evidence carefully and return JSON only.
"""

                response = analyze_with_groq(prompt, system_prompt)

                if response is None:
                    st.stop()

                try:
                    json_match = re.search(r'\{.*\}', response, re.DOTALL)
                    if json_match:
                        result = json.loads(json_match.group())
                    else:
                        result = json.loads(response)

                    verdict = str(result.get("verdict", "suspicious")).upper()

                    try:
                        confidence = int(result.get("confidence", behavior_score))
                    except (TypeError, ValueError):
                        confidence = behavior_score

                    confidence = max(0, min(100, confidence))

                    # Never allow a "SAFE" verdict when the deterministic
                    # engine has strong scam evidence.
                    if behavior_score >= 75 and verdict == "SAFE":
                        verdict = "SUSPICIOUS"
                        confidence = max(confidence, behavior_score)

                    if verdict == "SCAM":
                        st.markdown(
                            f'<div class="scam-badge scam-high">⚠️ SCAM ({confidence}%)</div>',
                            unsafe_allow_html=True
                        )
                        st.session_state.scams_detected += 1
                        show_report_button(lang_code)

                    elif verdict == "SUSPICIOUS":
                        st.markdown(
                            f'<div class="scam-badge scam-medium">⚠️ SUSPICIOUS ({confidence}%)</div>',
                            unsafe_allow_html=True
                        )

                    else:
                        st.markdown(
                            f'<div class="scam-badge scam-safe">✅ SAFE-LOOKING ({confidence}%)</div>',
                            unsafe_allow_html=True
                        )

                    st.progress(confidence / 100)

                    # -----------------------------------------------------
                    # Risk evidence
                    # -----------------------------------------------------
                    st.subheader(t["risk_evidence"])

                    evidence_cols = st.columns(3)

                    with evidence_cols[0]:
                        st.metric(t["behavior_risk"], f"{behavior_score}/100")

                    with evidence_cols[1]:
                        st.metric(t["calls_received"], int(call_count))

                    with evidence_cols[2]:
                        provider_score = phone_info.get("api_risk_score")
                        st.metric(
                            "Provider Risk",
                            f"{provider_score:.0f}/100"
                            if isinstance(provider_score, (int, float))
                            else "Unavailable"
                        )

                    all_flags = []
                    all_flags.extend(behavior_flags)
                    for flag in result.get("red_flags", []) or []:
                        if flag not in all_flags:
                            all_flags.append(flag)

                    if all_flags:
                        st.subheader(f"🚩 {t['red_flags']}")
                        for flag in all_flags:
                            st.write(f"• {flag}")

                    telecom_assessment = result.get("telecom_assessment")
                    if telecom_assessment:
                        st.subheader(t["telecom_assessment"])
                        st.write(telecom_assessment)

                    st.subheader(f"💡 {t['advice']}")
                    st.caption(f"*{t['bilingual_note']}*")

                    cols = st.columns(2)
                    advice_map = {
                        "en": result.get("advice_en", "Do not share OTPs, PINs, passwords or CVVs. Verify the caller through an official number."),
                        "te": result.get("advice_te", "OTP, PIN, పాస్‌వర్డ్ లేదా CVV ఎవరితోనూ పంచుకోకండి. అధికారిక నంబర్ ద్వారా ధృవీకరించండి."),
                        "ta": result.get("advice_ta", "OTP, PIN, கடவுச்சொல் அல்லது CVV-ஐ பகிர வேண்டாம். அதிகாரப்பூர்வ எண்ணில் சரிபார்க்கவும்."),
                        "hi": result.get("advice_hi", "OTP, PIN, पासवर्ड या CVV साझा न करें। आधिकारिक नंबर से सत्यापित करें।"),
                        "kn": result.get("advice_kn", "OTP, PIN, ಪಾಸ್‌ವರ್ಡ್ ಅಥವಾ CVV ಹಂಚಿಕೊಳ್ಳಬೇಡಿ. ಅಧಿಕೃತ ಸಂಖ್ಯೆಯ ಮೂಲಕ ಪರಿಶೀಲಿಸಿ.")
                    }

                    with cols[0]:
                        st.write(f"**{t['english']}:**\n{advice_map['en']}")

                    with cols[1]:
                        if lang_code == "te":
                            st.write(f"**{t['selected_language']}:**\n{advice_map[lang_code]}")
                        elif lang_code == "ta":
                            st.write(f"**{t['selected_language']}:**\n{advice_map[lang_code]}")
                        elif lang_code == "hi":
                            st.write(f"**{t['selected_language']}:**\n{advice_map[lang_code]}")
                        elif lang_code == "kn":
                            st.write(f"**{t['selected_language']}:**\n{advice_map[lang_code]}")
                        else:
                            st.write(f"**{t['selected_language']}:**\n{advice_map[lang_code]}")

                    # -----------------------------------------------------
                    # 4. IMPORTANT LIMITATIONS
                    # -----------------------------------------------------
                    with st.expander("ℹ️ What this checker can and cannot know"):
                        st.markdown(
                            """
**Raksha can check**
- Whether the number appears valid.
- Carrier/network information when available.
- Mobile/landline/VoIP line type when available.
- Country/region/city registered to the number when available.
- Telecom/provider risk information when available.
- Repeated-call behavior.
- Scam indicators in what the caller said.

**Raksha cannot determine from a phone number alone**
- The caller's exact live GPS location.
- The caller's real identity with certainty.
- Whether a specific physical SIM card is currently inside a particular phone.
- Whether a number is definitely a scammer just because it has a certain carrier or location.

For an actual SIM-swap check, a carrier-backed service is required. Do not treat
a normal carrier lookup as a SIM-swap check.
"""
                        )

                except json.JSONDecodeError as e:
                    st.error(t["parse_error"])
                    st.text(f"Parse error: {str(e)}")

# ==================== TAB 4: LEARN & QUIZ ====================
with tab4:
    st.header(f"📚 {t['quiz_title']}")
    st.write(t["quiz_description"])
    
    # Quiz questions
    quiz_data = [
        {
            "question_en": "You receive a WhatsApp message saying you won ₹10 lakh in a lottery you never entered. What should you do?",
            "question_te": "మీరు ఎప్పుడూ పాల్గొనని లాటరీలో ₹10 లక్షలు గెలిచారని WhatsApp సందేశం వస్తే మీరు ఏమి చేయాలి?",
            "question_ta": "நீங்கள் எப்போதும் பங்கேற்காத லாட்டரியில் ₹10 லட்சம் வென்றதாக WhatsApp செய்தி வந்தால் என்ன செய்வீர்கள்?",
            "question_hi": "आपको एक WhatsApp संदेश मिलता है कि आपने एक लॉटरी में ₹10 लाख जीते हैं जिसमें आपने कभी भाग नहीं लिया। आपको क्या करना चाहिए?",
            "question_kn": "ನೀವು ಎಂದಿಗೂ ಭಾಗವಹಿಸದ ಲಾಟರಿಯಲ್ಲಿ ₹10 ಲಕ್ಷ ಗೆದ್ದಿರುವಿರಿ ಎಂದು WhatsApp ಸಂದೇಶ ಬಂದರೆ ನೀವು ಏನು ಮಾಡಬೇಕು?",
            "options_en": ["Pay the processing fee immediately", "Ignore and delete the message", "Share your bank details to receive the prize"],
            "options_te": ["వెంటనే ప్రాసెసింగ్ ఫీజు చెల్లించండి", "విస్మరించి సందేశాన్ని తొలగించండి", "బహుమతి పొందడానికి మీ బ్యాంక్ వివరాలను పంచుకోండి"],
            "options_ta": ["உடனடியாக செயலாக்க கட்டணத்தை செலுத்துங்கள்", "புறக்கணித்து செய்தியை நீக்குங்கள்", "பரிசைப் பெற உங்கள் வங்கி விவரங்களைப் பகிர்ந்து கொள்ளுங்கள்"],
            "options_hi": ["तुरंत प्रोसेसिंग शुल्क का भुगतान करें", "संदेश को अनदेखा करें और हटा दें", "इनाम प्राप्त करने के लिए अपने बैंक विवरण साझा करें"],
            "options_kn": ["ತಕ್ಷಣ ಪ್ರೊಸೆಸಿಂಗ್ ಶುಲ್ಕವನ್ನು ಪಾವತಿಸಿ", "ನಿರ್ಲಕ್ಷಿಸಿ ಸಂದೇಶವನ್ನು ಅಳಿಸಿ", "ಬಹುಮತಿಯನ್ನು ಪಡೆಯಲು ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ವಿವರಗಳನ್ನು ಹಂಚಿಕೊಳ್ಳಿ"],
            "correct": 1,
            "explanation_en": "Legitimate lotteries never ask winners to pay fees upfront. If you didn't enter, you can't win.",
            "explanation_te": "ధ్రువీకరించబడిన లాటరీలు గెలుపొందినవారిని ఎప్పుడూ ముందుగా ఫీజులు చెల్లించమని అడగవు. మీరు పాల్గొనకపోతే, గెలవలేరు.",
            "explanation_ta": "சட்டபூர்வமான லாட்டரிகள் வெற்றியாளர்களிடம் முன்பணம் கேட்காது. நீங்கள் பங்கேற்கவில்லை என்றால், வெற்றி பெற முடியாது.",
            "explanation_hi": "वैध लॉटरी विजेताओं से कभी भी अग्रिम शुल्क नहीं मांगती। यदि आपने भाग नहीं लिया, तो आप जीत नहीं सकते।",
            "explanation_kn": "ಕಾನೂನುಬದ್ಧ ಲಾಟರಿಗಳು ವಿಜೇತರಿಂದ ಎಂದಿಗೂ ಮುಂಗಡ ಶುಲ್ಕವನ್ನು ಕೇಳುವುದಿಲ್ಲ. ನೀವು ಭಾಗವಹಿಸದಿದ್ದರೆ, ಗೆಲ್ಲಲು ಸಾಧ್ಯವಿಲ್ಲ."
        },
        {
            "question_en": "A caller claims to be from your bank and asks for your OTP to 'unblock' your account. What do you do?",
            "question_te": "ఒక కాలర్ మీ బ్యాంక్ నుండి వచ్చారని చెప్పి మీ ఖాతాను 'అన్‌బ్లాక్' చేయడానికి మీ OTPని అడుగుతారు. మీరు ఏమి చేస్తారు?",
            "question_ta": "ஒரு அழைப்பாளர் உங்கள் வங்கியிலிருந்து வந்ததாகக் கூறி, உங்கள் கணக்கை 'தடைநீக்க' உங்கள் OTP ஐக் கேட்கிறார். நீங்கள் என்ன செய்வீர்கள்?",
            "question_hi": "एक कॉलर आपके बैंक से होने का दावा करता है और आपके खाते को 'अनब्लॉक' करने के लिए आपका OTP मांगता है। आप क्या करेंगे?",
            "question_kn": "ಒಬ್ಬ ಕರೆ ಮಾಡುವವರು ನಿಮ್ಮ ಬ್ಯಾಂಕಿನಿಂದ ಬಂದವರು ಎಂದು ಹೇಳಿ ನಿಮ್ಮ ಖಾತೆಯನ್ನು 'ಅನ್‌ಬ್ಲಾಕ್' ಮಾಡಲು ನಿಮ್ಮ OTP ಅನ್ನು ಕೇಳುತ್ತಾರೆ. ನೀವು ಏನು ಮಾಡುತ್ತೀರಿ?",
            "options_en": ["Give the OTP quickly to avoid account suspension", "Hang up and call your bank's official number", "Ask them to send a confirmation email first"],
            "options_te": ["ఖాతా సస్పెన్షన్‌ను నివారించడానికి వేగంగా OTP ఇవ్వండి", "ఫోన్ కట్ చేసి మీ బ్యాంక్ అధికారిక నంబర్‌కు కాల్ చేయండి", "ముందుగా ధృవీకరణ ఇమెయిల్ పంపమని అడగండి"],
            "options_ta": ["கணக்கு இடைநீக்கத்தைத் தவிர்க்க விரைவாக OTP ஐ வழங்குங்கள்", "தொலைபேசியைத் துண்டித்து உங்கள் வங்கியின் அதிகாரப்பூர்வ எண்ணை அழைக்கவும்", "முதலில் உறுதிப்படுத்தும் மின்னஞ்சலை அனுப்புமாறு கேட்கவும்"],
            "options_hi": ["खाता निलंबन से बचने के लिए तुरंत OTP दें", "फोन काटें और अपने बैंक की आधिकारिक संख्या पर कॉल करें", "पहले एक पुष्टि ईमेल भेजने के लिए कहें"],
            "options_kn": ["ಖಾತೆ ಅಮಾನತುಗೊಳ್ಳುವುದನ್ನು ತಪ್ಪಿಸಲು ತಕ್ಷಣ OTP ನೀಡಿ", "ಕಾಲ್ ಕಟ್ ಮಾಡಿ ನಿಮ್ಮ ಬ್ಯಾಂಕಿನ ಅಧಿಕೃತ ಸಂಖ್ಯೆಗೆ ಕರೆ ಮಾಡಿ", "ಮೊದಲು ದೃಢೀಕರಣ ಇಮೇಲ್ ಕಳುಹಿಸಲು ಹೇಳಿ"],
            "correct": 1,
            "explanation_en": "Banks NEVER ask for OTPs. OTPs are for your use only. Always hang up and call the official number.",
            "explanation_te": "బ్యాంకులు ఎప్పుడూ OTPలను అడగవు. OTPలు మీ వ్యక్తిగత ఉపయోగానికి మాత్రమే. ఎల్లప్పుడూ ఫోన్ కట్ చేసి అధికారిక నంబర్‌కు కాల్ చేయండి.",
            "explanation_ta": "வங்கிகள் எப்போதும் OTP ஐக் கேட்காது. OTPகள் உங்கள் பயன்பாட்டிற்கு மட்டுமே. எப்போதும் தொலைபேசியைத் துண்டித்து அதிகாரப்பூர்வ எண்ணை அழைக்கவும்.",
            "explanation_hi": "बैंक कभी भी OTP नहीं मांगते। OTP केवल आपके उपयोग के लिए हैं। हमेशा फोन काटें और आधिकारिक नंबर पर कॉल करें।",
            "explanation_kn": "ಬ್ಯಾಂಕುಗಳು ಎಂದಿಗೂ OTP ಅನ್ನು ಕೇಳುವುದಿಲ್ಲ. OTPಗಳು ನಿಮ್ಮ ಬಳಕೆಗೆ ಮಾತ್ರ. ಯಾವಾಗಲೂ ಕಾಲ್ ಕಟ್ ಮಾಡಿ ಅಧಿಕೃತ ಸಂಖ್ಯೆಗೆ ಕರೆ ಮಾಡಿ."
        },
        {
            "question_en": "You get an SMS with a link saying 'Your package is pending. Pay customs fee.' You didn't order anything. What is this?",
            "question_te": "మీరు ఏమీ ఆర్డర్ చేయకపోతే, 'మీ ప్యాకేజీ పెండింగ్‌లో ఉంది. కస్టమ్స్ ఫీజు చెల్లించండి' అని లింక్‌తో SMS వస్తే ఇది ఏమిటి?",
            "question_ta": "நீங்கள் எதுவும் ஆர்டர் செய்யவில்லை என்றால், 'உங்கள் பொதி நிலுவையில் உள்ளது. சுங்கக் கட்டணம் செலுத்தவும்' என்ற இணைப்புடன் SMS வந்தால் இது என்ன?",
            "question_hi": "आपको एक SMS मिलता है जिसमें लिंक है 'आपका पैकेज लंबित है। कस्टम शुल्क दें।' आपने कुछ भी ऑर्डर नहीं किया। यह क्या है?",
            "question_kn": "ನೀವು ಏನನ್ನೂ ಆರ್ಡರ್ ಮಾಡದಿದ್ದರೆ, 'ನಿಮ್ಮ ಪ್ಯಾಕೇಜ್ ಬಾಕಿ ఉಂದಿ. ಕಸ್ಟಮ್ಸ್ ಶುಲ್ಕ ಪಾವತಿಸಿ' ಎಂದು ಲಿಂಕ್‌ನೊಂದಿಗೆ SMS ಬಂದರೆ ಇದು ಏನು?",
            "options_en": ["A genuine delivery notification", "A delivery scam", "A mistake by the courier company"],
            "options_te": ["అసలైన డెలివరీ నోటిఫికేషన్", "డెలివరీ స్కామ్", "కూరియర్ కంపెనీ యొక్క తప్పు"],
            "options_ta": ["உண்மையான விநியோக அறிவிப்பு", "விநியோக மோசடி", "கூரியர் நிறுவனத்தின் தவறு"],
            "options_hi": ["एक genuine डिलीवरी सूचना", "एक डिलीवरी घोटाला", "कूरियर कंपनी की गलती"],
            "options_kn": ["ನಿಜವಾದ ಡೆಲಿವರಿ ಸೂಚನೆ", "ಡೆಲಿವರಿ ಸ್ಕ್ಯಾಮ್", "ಕೂರಿಯರ್ ಕಂಪನಿಯ ತಪ್ಪು"],
            "correct": 1,
            "explanation_en": "This is a common delivery scam. If you didn't order anything, there's no package. Never pay for unexpected deliveries.",
            "explanation_te": "ఇది సాధారణ డెలివరీ స్కామ్. మీరు ఏమీ ఆర్డర్ చేయకపోతే, ప్యాకేజీ లేదు. ఊహించని డెలివరీల కోసం ఎప్పుడూ చెల్లించవద్దు.",
            "explanation_ta": "இது ஒரு பொதுவான விநியோக மோசடி. நீங்கள் எதுவும் ஆர்டர் செய்யவில்லை என்றால், பொதி இல்லை. எதிர்பாராத விநியோகங்களுக்கு ஒருபோதும் பணம் செலுத்த வேண்டாம்.",
            "explanation_hi": "यह एक सामान्य डिलीवरी घोटाला है। यदि आपने कुछ भी ऑर्डर नहीं किया, तो कोई पैकेज नहीं है। अप्रत्याशित डिलीवरी के लिए कभी भुगतान न करें।",
            "explanation_kn": "ಇದು ಸಾಮಾನ್ಯ ಡೆಲಿವರಿ ಸ್ಕ್ಯಾಮ್. ನೀವು ಏನನ್ನೂ ಆರ್ಡರ್ ಮಾಡದಿದ್ದರೆ, ಪ್ಯಾಕೇಜ್ ಇಲ್ಲ. ಅನಿರೀಕ್ಷಿತ ಡೆಲಿವರಿಗಳಿಗೆ ಎಂದಿಗೂ ಹಣ ಪಾವತಿಸಬೇಡಿ."
        }
    ]
    
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = [False] * len(quiz_data)
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = [None] * len(quiz_data)
    
    for i, q in enumerate(quiz_data):
        st.markdown(f"**{t['question']} {i+1}:**")
        
        # Display question in selected language
        if lang_code == "te":
            st.write(q["question_te"])
            options = q["options_te"]
            explanation = q["explanation_te"]
        elif lang_code == "ta":
            st.write(q["question_ta"])
            options = q["options_ta"]
            explanation = q["explanation_ta"]
        elif lang_code == "hi":
            st.write(q["question_hi"])
            options = q["options_hi"]
            explanation = q["explanation_hi"]
        elif lang_code == "kn":
            st.write(q["question_kn"])
            options = q["options_kn"]
            explanation = q["explanation_kn"]
        else:
            st.write(q["question_en"])
            options = q["options_en"]
            explanation = q["explanation_en"]
        
        answer = st.radio(
            f"select_{i}",
            options=options,
            index=None,
            key=f"quiz_q_{i}",
            label_visibility="collapsed"
        )
        
        if st.button(t['submit_answer'], key=f"submit_{i}") and not st.session_state.quiz_submitted[i]:
            if answer is not None:
                selected_idx = options.index(answer)
                st.session_state.quiz_answers[i] = selected_idx
                st.session_state.quiz_submitted[i] = True
                
                if selected_idx == q["correct"]:
                    st.session_state.quiz_score += 1
                    st.success(t["correct"])
                else:
                    st.error(t["incorrect"])
                
                st.info(f"💡 {explanation}")
            else:
                st.warning(t["select_answer"])
        
        if st.session_state.quiz_submitted[i]:
            if st.session_state.quiz_answers[i] == q["correct"]:
                st.success(t["correct"])
            else:
                st.error(t["incorrect"])
            st.info(f"💡 {explanation}")
        
        st.markdown("---")
    
    # Score display
    st.subheader(f"🏆 {t['score']}: {st.session_state.quiz_score}/{len(quiz_data)}")
    progress = st.session_state.quiz_score / len(quiz_data)
    st.progress(progress)
    
    if st.session_state.quiz_score == len(quiz_data):
        st.balloons()
        st.success(t["perfect_score"])

# ==================== FLOATING REPORT BUTTON ====================
st.markdown(f"""
    <a href="https://cybercrime.gov.in/" target="_blank" class="fab-report" title="{t['report_scam_title']}">
        🚨
    </a>
""", unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("---")
st.caption(f"🛡️ {t['footer']}")
st.caption(t["footer_model"])
