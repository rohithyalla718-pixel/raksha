import streamlit as st
import os
from groq import Groq
import json
import re

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
        "suspicious_message": "Suspicious Message:",
        "url_description": "Check suspicious URLs for phishing and malicious links.",
        "call_description_label": "🗣️ What did the caller say or ask for?",
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
        "lookup_unavailable": "⚠️ Telecom lookup unavailable. Call can still be analyzed using call behavior and AI indicators.",
        "lookup_detail": "Lookup detail",
        "risk_evidence": "📊 Risk Evidence",
        "behavior_risk": "Behavior Risk",
        "calls_received": "Calls Received",
        "overall_risk": "Overall Risk",
        "telecom_assessment": "📡 Telecom Assessment",
        "telecom_not_verdict": "Telecom data is supporting evidence only; it does not prove the caller is a scammer.",
        "quiz_description": "Test your knowledge and learn to spot scams before they happen.",
        "correct": "✅ Correct!",
        "incorrect": "❌ Incorrect!",
        "select_answer": "Please select an answer first.",
        "perfect_score": "🎉 Perfect Score! You're a scam detection expert!",
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
        "language_label": "భాష", "mission": "మా లక్ష్యం", "mission_text": "ప్రతి రోజు వేలాది భారతీయ కుటుంబాలు ఆన్‌లైన్ స్కామ్‌ల వల్ల డబ్బు కోల్పోతున్నాయి. రక్ష మీ కుటుంబాన్ని వారి స్వంత భాషలో రక్షిస్తుంది, పరిశీలిస్తుంది మరియు నేర్పిస్తుంది.", "stats": "గణాంకాలు", "why_raksha": "రక్ష ఎందుకు గెలుస్తుంది", "why_1": "☑️ నిజమైన సమస్య, నిజమైన లక్ష్యం", "why_2": "☑️ 4 పనిచేసే భద్రతా సాధనాలు", "why_3": "☑️ 5 భారతీయ భాషలకు మద్దతు", "why_4": "☑️ 3D గ్లాస్ UI మరియు లైవ్ డెప్త్ ఎఫెక్ట్స్", "made_for": "డిజిటల్ భద్రత కోసం 💚 తో తయారు చేయబడింది", "hero_title": "రక్ష — కుటుంబ డిజిటల్ సేఫ్టీ గార్డియన్", "hero_subtitle": "ఆన్‌లైన్ మోసాల నుండి కుటుంబాలను రక్షిస్తుంది — స్కామ్ సందేశాలను పరిశీలిస్తుంది, అనుమానాస్పద లింక్‌లను తనిఖీ చేస్తుంది, కాల్‌లను విశ్లేషిస్తుంది మరియు మోసాలను గుర్తించడం నేర్పిస్తుంది.", "fake_lottery": "🎰 నకిలీ లాటరీ", "fake_bank": "🏦 నకిలీ బ్యాంక్ అలర్ట్", "fake_delivery": "📦 నకిలీ డెలివరీ", "suspicious_message": "అనుమానాస్పద సందేశం:", "url_description": "ఫిషింగ్ మరియు హానికరమైన లింక్‌ల కోసం అనుమానాస్పద URL ను తనిఖీ చేయండి.", "call_description_label": "🗣️ కాలర్ ఏమి చెప్పాడు లేదా ఏమి అడిగాడు?", "call_description_placeholder": "ఉదాహరణ: కాలర్ తాను నా బ్యాంక్ నుండి అని చెప్పి, ఖాతాను అన్‌బ్లాక్ చేయడానికి OTP అడిగాడు. వెంటనే చేయాలని ఒత్తిడి చేశాడు.", "call_checker_description": "కాలర్‌ను నమ్మే ముందు టెలికాం సమాచారం, నమోదైన నంబర్ ప్రాంతం, కాల్ ప్రవర్తన మరియు స్కామ్ సూచనలను తనిఖీ చేయండి.", "location_notice": "📍 ఇక్కడ చూపించే ప్రాంతం అందుబాటులో ఉన్నప్పుడు ఫోన్ నంబర్ నమోదైన టెలికాం ప్రాంతం మాత్రమే — ఇది కాలర్ యొక్క లైవ్ GPS స్థానం కాదు.", "privacy_notice": "🔐 గోప్యత: పూర్తి ఫోన్ నంబర్ టెలికాం లుక్‌అప్ కోసం మాత్రమే ఉపయోగించబడుతుంది. AI విశ్లేషణకు మాస్క్ చేసిన నంబర్ మరియు కాల్ వివరాలు మాత్రమే పంపబడతాయి.", "checking_call": "🔍 నంబర్, క్యారియర్, నమోదైన ప్రాంతం మరియు స్కామ్ సూచనలను తనిఖీ చేస్తున్నాం...", "invalid_phone": "❌ చెల్లని ఫోన్ నంబర్. భారతీయ నంబర్ల కోసం 10 అంకెలు లేదా +91 తో నంబర్ నమోదు చేయండి.", "telecom_intelligence": "📡 టెలికాం & SIM/నెట్‌వర్క్ సమాచారం", "number_valid": "నంబర్ చెల్లుబాటు", "yes": "అవును", "no": "కాదు", "unknown": "తెలియదు", "carrier": "క్యారియర్ / నెట్‌వర్క్", "line_type": "లైన్ రకం", "line_status": "లైన్ స్థితి", "country": "🌍 దేశం", "region": "📍 ప్రాంతం", "registered_city": "🏙️ నమోదైన నగరం", "timezone": "🕐 టైమ్‌జోన్", "lookup_unavailable": "⚠️ టెలికాం లుక్‌అప్ అందుబాటులో లేదు. కాల్ ప్రవర్తన మరియు AI సూచనలతో కాల్‌ను ఇంకా విశ్లేషించవచ్చు.", "lookup_detail": "లుక్‌అప్ వివరాలు", "risk_evidence": "📊 రిస్క్ ఆధారాలు", "behavior_risk": "ప్రవర్తన రిస్క్", "calls_received": "అందుకున్న కాల్స్", "overall_risk": "మొత్తం రిస్క్", "telecom_assessment": "📡 టెలికాం అంచనా", "telecom_not_verdict": "టెలికాం డేటా సహాయక ఆధారం మాత్రమే; దానితో కాలర్ స్కామర్ అని నిర్ధారించలేము.", "quiz_description": "మీ జ్ఞానాన్ని పరీక్షించుకోండి మరియు స్కామ్‌లు జరగకముందే వాటిని గుర్తించడం నేర్చుకోండి.", "correct": "✅ సరైన సమాధానం!", "incorrect": "❌ తప్పు సమాధానం!", "select_answer": "దయచేసి ముందుగా ఒక సమాధానాన్ని ఎంచుకోండి.", "perfect_score": "🎉 అద్భుతమైన స్కోర్! మీరు స్కామ్ గుర్తింపు నిపుణులు!", "report_scam_title": "స్కామ్‌ను రిపోర్ట్ చేయండి", "raw_response": "డీబగ్ - ముడి స్పందన", "groq_error": "Groq API లోపం", "parse_error": "స్పందనను చదవలేకపోయాం. దయచేసి మళ్లీ ప్రయత్నించండి.", "enter_message": "విశ్లేషించడానికి సందేశాన్ని నమోదు చేయండి.", "enter_url": "విశ్లేషించడానికి URL ను నమోదు చేయండి.", "enter_phone": "విశ్లేషించడానికి ఫోన్ నంబర్‌ను నమోదు చేయండి.", "safe_label": "సురక్షితం", "suspicious_label": "అనుమానాస్పదం", "scam_label": "స్కామ్", "english": "ఆంగ్లం", "report": "స్కామ్‌ను రిపోర్ట్ చేయండి", "footer_model": "డిజిటల్ భద్రత కోసం 💚 తో తయారు చేయబడింది | మోడల్: llama-3.1-8b-instant via Groq",
    },
    "ta": {
        "language_label": "மொழி", "mission": "எங்கள் நோக்கம்", "mission_text": "ஆயிரக்கணக்கான இந்திய குடும்பங்கள் தினமும் ஆன்லைன் மோசடிகளில் பணத்தை இழக்கின்றனர். ரக்ஷா உங்கள் குடும்பத்தை அவர்களின் சொந்த மொழியில் பாதுகாக்கிறது, ஆய்வு செய்கிறது மற்றும் கற்றுக்கொடுக்கிறது.", "stats": "புள்ளிவிவரங்கள்", "why_raksha": "ரக்ஷா ஏன் வெல்லும்", "why_1": "☑️ உண்மையான பிரச்சனை, உண்மையான நோக்கம்", "why_2": "☑️ 4 செயல்படும் பாதுகாப்பு கருவிகள்", "why_3": "☑️ 5 இந்திய மொழிகளுக்கு ஆதரவு", "why_4": "☑️ 3D கண்ணாடி UI மற்றும் லைவ் டெப்த் எஃபெக்ட்ஸ்", "made_for": "டிஜிட்டல் பாதுகாப்புக்காக 💚 உருவாக்கப்பட்டது", "hero_title": "ரக்ஷா — குடும்ப டிஜிட்டல் பாதுகாப்பு காவலர்", "hero_subtitle": "ஆன்லைன் மோசடிகளில் இருந்து குடும்பங்களை பாதுகாக்கிறது — மோசடி செய்திகளை ஆய்வு செய்கிறது, சந்தேகமான இணைப்புகளை சரிபார்க்கிறது, அழைப்புகளை பகுப்பாய்வு செய்கிறது மற்றும் மோசடிகளை அடையாளம் காண கற்றுக்கொடுக்கிறது.", "fake_lottery": "🎰 போலி லாட்டரி", "fake_bank": "🏦 போலி வங்கி எச்சரிக்கை", "fake_delivery": "📦 போலி டெலிவரி", "suspicious_message": "சந்தேகமான செய்தி:", "url_description": "ஃபிஷிங் மற்றும் தீங்கிழைக்கும் இணைப்புகளுக்கான சந்தேகமான URL ஐ சரிபார்க்கவும்.", "call_description_label": "🗣️ அழைப்பாளர் என்ன சொன்னார் அல்லது என்ன கேட்டார்?", "call_description_placeholder": "உதாரணம்: அழைப்பாளர் வங்கியிலிருந்து வந்ததாகக் கூறி கணக்கைத் திறக்க OTP கேட்டார்.", "call_checker_description": "அழைப்பாளரை நம்புவதற்கு முன் தொலைத்தொடர்பு தகவல், பதிவு செய்யப்பட்ட பகுதி, அழைப்பு நடத்தை மற்றும் மோசடி அறிகுறிகளை சரிபார்க்கவும்.", "location_notice": "📍 இங்கு காட்டப்படும் பகுதி, கிடைக்கும் போது, தொலைபேசி எண்ணின் பதிவு செய்யப்பட்ட தொலைத்தொடர்பு பகுதி மட்டுமே — இது அழைப்பாளரின் நேரடி GPS இருப்பிடம் அல்ல.", "privacy_notice": "🔐 தனியுரிமை: முழு தொலைபேசி எண் தொலைத்தொடர்பு சரிபார்ப்புக்கு மட்டுமே பயன்படுத்தப்படுகிறது. AI க்கு மறைக்கப்பட்ட எண் மற்றும் அழைப்பு விவரங்கள் மட்டுமே அனுப்பப்படும்.", "checking_call": "🔍 எண், கேரியர், பதிவு செய்யப்பட்ட பகுதி மற்றும் மோசடி அறிகுறிகளை சரிபார்க்கிறது...", "invalid_phone": "❌ தவறான தொலைபேசி எண். இந்திய எண்ணுக்கு 10 இலக்கங்கள் அல்லது +91 உடன் எண்ணை உள்ளிடவும்.", "telecom_intelligence": "📡 தொலைத்தொடர்பு & SIM/நெட்வொர்க் தகவல்", "number_valid": "எண் சரியானதா", "yes": "ஆம்", "no": "இல்லை", "unknown": "தெரியவில்லை", "carrier": "கேரியர் / நெட்வொர்க்", "line_type": "லைன் வகை", "line_status": "லைன் நிலை", "country": "🌍 நாடு", "region": "📍 பகுதி", "registered_city": "🏙️ பதிவு செய்யப்பட்ட நகரம்", "timezone": "🕐 நேர மண்டலம்", "lookup_unavailable": "⚠️ தொலைத்தொடர்பு சரிபார்ப்பு கிடைக்கவில்லை. அழைப்பு நடத்தை மற்றும் AI அறிகுறிகளைக் கொண்டு இன்னும் பகுப்பாய்வு செய்யலாம்.", "lookup_detail": "சரிபார்ப்பு விவரம்", "risk_evidence": "📊 ஆபத்து ஆதாரங்கள்", "behavior_risk": "நடத்தை ஆபத்து", "calls_received": "பெறப்பட்ட அழைப்புகள்", "overall_risk": "மொத்த ஆபத்து", "telecom_assessment": "📡 தொலைத்தொடர்பு மதிப்பீடு", "telecom_not_verdict": "தொலைத்தொடர்பு தரவு ஆதாரம் மட்டுமே; அதனால் அழைப்பாளர் மோசடி செய்பவர் என்று உறுதியாக கூற முடியாது.", "quiz_description": "உங்கள் அறிவை சோதித்து, மோசடிகள் நடக்கும் முன் அவற்றை அடையாளம் காண கற்றுக்கொள்ளுங்கள்.", "correct": "✅ சரியான பதில்!", "incorrect": "❌ தவறான பதில்!", "select_answer": "முதலில் ஒரு பதிலைத் தேர்ந்தெடுக்கவும்.", "perfect_score": "🎉 சரியான மதிப்பெண்! நீங்கள் மோசடி கண்டறிதல் நிபுணர்!", "report_scam_title": "மோசடியைப் புகாரளிக்கவும்", "raw_response": "டீபக் - மூல பதில்", "groq_error": "Groq API பிழை", "parse_error": "பதிலை படிக்க முடியவில்லை. மீண்டும் முயற்சிக்கவும்.", "enter_message": "பகுப்பாய்வு செய்ய ஒரு செய்தியை உள்ளிடவும்.", "enter_url": "பகுப்பாய்வு செய்ய URL ஐ உள்ளிடவும்.", "enter_phone": "பகுப்பாய்வு செய்ய தொலைபேசி எண்ணை உள்ளிடவும்.", "safe_label": "பாதுகாப்பானது", "suspicious_label": "சந்தேகமானது", "scam_label": "மோசடி", "english": "ஆங்கிலம்", "report": "மோசடியைப் புகாரளிக்கவும்", "footer_model": "டிஜிட்டல் பாதுகாப்புக்காக 💚 உருவாக்கப்பட்டது | மாடல்: llama-3.1-8b-instant via Groq"
    },
    "hi": {
        "language_label": "भाषा", "mission": "हमारा मिशन", "mission_text": "हर दिन हजारों भारतीय परिवार ऑनलाइन घोटालों में पैसा खोते हैं। रक्षा आपके परिवार को उनकी अपनी भाषा में सुरक्षित रखता है, जांचता है और सिखाता है।", "stats": "आंकड़े", "why_raksha": "रक्षा क्यों जीतेगा", "why_1": "☑️ असली समस्या, असली मिशन", "why_2": "☑️ 4 काम करने वाले सुरक्षा उपकरण", "why_3": "☑️ 5 भारतीय भाषाओं का समर्थन", "why_4": "☑️ 3D ग्लास UI और लाइव डेप्थ इफेक्ट्स", "made_for": "डिजिटल सुरक्षा के लिए 💚 बनाया गया", "hero_title": "रक्षा — परिवार डिजिटल सुरक्षा संरक्षक", "hero_subtitle": "परिवारों को ऑनलाइन धोखाधड़ी से बचाता है — घोटाले के संदेशों की जांच करता है, संदिग्ध लिंक देखता है, कॉल का विश्लेषण करता है और लोगों को धोखाधड़ी पहचानना सिखाता है।", "fake_lottery": "🎰 नकली लॉटरी", "fake_bank": "🏦 नकली बैंक अलर्ट", "fake_delivery": "📦 नकली डिलीवरी", "suspicious_message": "संदिग्ध संदेश:", "url_description": "फिशिंग और दुर्भावनापूर्ण लिंक के लिए संदिग्ध URL की जांच करें।", "call_description_label": "🗣️ कॉल करने वाले ने क्या कहा या क्या मांगा?", "call_description_placeholder": "उदाहरण: कॉल करने वाले ने बैंक से होने का दावा किया और खाता खोलने के लिए OTP मांगा।", "call_checker_description": "कॉलर पर भरोसा करने से पहले टेलीकॉम जानकारी, पंजीकृत क्षेत्र, कॉल व्यवहार और घोटाले के संकेत जांचें।", "location_notice": "📍 यहां दिखाया गया स्थान, उपलब्ध होने पर, फोन नंबर का पंजीकृत टेलीकॉम क्षेत्र है — यह कॉलर का लाइव GPS स्थान नहीं है।", "privacy_notice": "🔐 गोपनीयता: पूरा फोन नंबर केवल टेलीकॉम लुकअप के लिए उपयोग होता है। AI को केवल छिपा हुआ नंबर और कॉल विवरण भेजे जाते हैं।", "checking_call": "🔍 नंबर, कैरियर, पंजीकृत स्थान और घोटाले के संकेत जांचे जा रहे हैं...", "invalid_phone": "❌ अमान्य फोन नंबर। भारतीय नंबर के लिए 10 अंक या +91 के साथ नंबर दर्ज करें।", "telecom_intelligence": "📡 टेलीकॉम और SIM/नेटवर्क जानकारी", "number_valid": "नंबर मान्य", "yes": "हाँ", "no": "नहीं", "unknown": "अज्ञात", "carrier": "कैरियर / नेटवर्क", "line_type": "लाइन प्रकार", "line_status": "लाइन स्थिति", "country": "🌍 देश", "region": "📍 क्षेत्र", "registered_city": "🏙️ पंजीकृत शहर", "timezone": "🕐 समय क्षेत्र", "lookup_unavailable": "⚠️ टेलीकॉम लुकअप उपलब्ध नहीं है। कॉल व्यवहार और AI संकेतों से कॉल का विश्लेषण फिर भी किया जा सकता है।", "lookup_detail": "लुकअप विवरण", "risk_evidence": "📊 जोखिम के प्रमाण", "behavior_risk": "व्यवहार जोखिम", "calls_received": "प्राप्त कॉल", "overall_risk": "कुल जोखिम", "telecom_assessment": "📡 टेलीकॉम आकलन", "telecom_not_verdict": "टेलीकॉम डेटा केवल सहायक प्रमाण है; इससे यह साबित नहीं होता कि कॉलर ठग है।", "quiz_description": "अपना ज्ञान जांचें और घोटाले होने से पहले उन्हें पहचानना सीखें।", "correct": "✅ सही!", "incorrect": "❌ गलत!", "select_answer": "कृपया पहले एक उत्तर चुनें।", "perfect_score": "🎉 शानदार स्कोर! आप घोटाला पहचानने के विशेषज्ञ हैं!", "report_scam_title": "घोटाले की रिपोर्ट करें", "raw_response": "डीबग - कच्ची प्रतिक्रिया", "groq_error": "Groq API त्रुटि", "parse_error": "प्रतिक्रिया पढ़ी नहीं जा सकी। कृपया फिर प्रयास करें।", "enter_message": "विश्लेषण के लिए संदेश दर्ज करें।", "enter_url": "विश्लेषण के लिए URL दर्ज करें।", "enter_phone": "विश्लेषण के लिए फोन नंबर दर्ज करें।", "safe_label": "सुरक्षित", "suspicious_label": "संदिग्ध", "scam_label": "घोटाला", "english": "अंग्रेज़ी", "report": "घोटाले की रिपोर्ट करें", "footer_model": "डिजिटल सुरक्षा के लिए 💚 बनाया गया | मॉडल: llama-3.1-8b-instant via Groq"
    },
    "kn": {
        "language_label": "ಭಾಷೆ", "mission": "ನಮ್ಮ ಗುರಿ", "mission_text": "ಪ್ರತಿ ದಿನ ಸಾವಿರಾರು ಭಾರತೀಯ ಕುಟುಂಬಗಳು ಆನ್‌ಲೈನ್ ಮೋಸಗಳಿಂದ ಹಣ ಕಳೆದುಕೊಳ್ಳುತ್ತವೆ. ರಕ್ಷ ನಿಮ್ಮ ಕುಟುಂಬವನ್ನು ಅವರದೇ ಭಾಷೆಯಲ್ಲಿ ರಕ್ಷಿಸುತ್ತದೆ, ಪರಿಶೀಲಿಸುತ್ತದೆ ಮತ್ತು ಕಲಿಸುತ್ತದೆ.", "stats": "ಅಂಕಿಅಂಶಗಳು", "why_raksha": "ರಕ್ಷ ಏಕೆ ಗೆಲ್ಲುತ್ತದೆ", "why_1": "☑️ ನಿಜವಾದ ಸಮಸ್ಯೆ, ನಿಜವಾದ ಗುರಿ", "why_2": "☑️ 4 ಕಾರ್ಯನಿರ್ವಹಿಸುವ ಸುರಕ್ಷತಾ ಸಾಧನಗಳು", "why_3": "☑️ 5 ಭಾರತೀಯ ಭಾಷೆಗಳಿಗೆ ಬೆಂಬಲ", "why_4": "☑️ 3D ಗ್ಲಾಸ್ UI ಮತ್ತು ಲೈವ್ ಡೆಪ್ತ್ ಎಫೆಕ್ಟ್ಸ್", "made_for": "ಡಿಜಿಟಲ್ ಸುರಕ್ಷತೆಗಾಗಿ 💚 ನಿರ್ಮಿಸಲಾಗಿದೆ", "hero_title": "ರಕ್ಷ — ಕುಟುಂಬ ಡಿಜಿಟಲ್ ಸುರಕ್ಷತಾ ರಕ್ಷಕ", "hero_subtitle": "ಕುಟುಂಬಗಳನ್ನು ಆನ್‌ಲೈನ್ ವಂಚನೆಯಿಂದ ರಕ್ಷಿಸುತ್ತದೆ — ಮೋಸ ಸಂದೇಶಗಳನ್ನು ಪರಿಶೀಲಿಸುತ್ತದೆ, ಅನುಮಾನಾಸ್ಪದ ಲಿಂಕ್‌ಗಳನ್ನು ಪರಿಶೀಲಿಸುತ್ತದೆ, ಕರೆಗಳನ್ನು ವಿಶ್ಲೇಷಿಸುತ್ತದೆ ಮತ್ತು ಮೋಸವನ್ನು ಗುರುತಿಸಲು ಕಲಿಸುತ್ತದೆ.", "fake_lottery": "🎰 ನಕಲಿ ಲಾಟರಿ", "fake_bank": "🏦 ನಕಲಿ ಬ್ಯಾಂಕ್ ಎಚ್ಚರಿಕೆ", "fake_delivery": "📦 ನಕಲಿ ಡೆಲಿವರಿ", "suspicious_message": "ಅನುಮಾನಾಸ್ಪದ ಸಂದೇಶ:", "url_description": "ಫಿಶಿಂಗ್ ಮತ್ತು ಹಾನಿಕಾರಕ ಲಿಂಕ್‌ಗಳಿಗಾಗಿ ಅನುಮಾನಾಸ್ಪದ URL ಅನ್ನು ಪರಿಶೀಲಿಸಿ.", "call_description_label": "🗣️ ಕರೆ ಮಾಡಿದವರು ಏನು ಹೇಳಿದರು ಅಥವಾ ಏನು ಕೇಳಿದರು?", "call_description_placeholder": "ಉದಾಹರಣೆ: ಕರೆ ಮಾಡಿದವರು ಬ್ಯಾಂಕಿನಿಂದ ಬಂದವರು ಎಂದು ಹೇಳಿ ಖಾತೆ ತೆರೆಯಲು OTP ಕೇಳಿದರು.", "call_checker_description": "ಕರೆ ಮಾಡಿದವರನ್ನು ನಂಬುವ ಮೊದಲು ಟೆಲಿಕಾಂ ಮಾಹಿತಿ, ನೋಂದಾಯಿತ ಪ್ರದೇಶ, ಕರೆ ವರ್ತನೆ ಮತ್ತು ಮೋಸ ಸೂಚನೆಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.", "location_notice": "📍 ಇಲ್ಲಿ ತೋರಿಸುವ ಸ್ಥಳವು ಲಭ್ಯವಿದ್ದಾಗ ಫೋನ್ ಸಂಖೆಯ ನೋಂದಾಯಿತ ಟೆಲಿಕಾಂ ಪ್ರದೇಶವಾಗಿದೆ — ಇದು ಕರೆ ಮಾಡಿದವರ ಲೈವ್ GPS ಸ್ಥಳವಲ್ಲ.", "privacy_notice": "🔐 ಗೌಪ್ಯತೆ: ಪೂರ್ಣ ಫೋನ್ ಸಂಖೆಯನ್ನು ಟೆಲಿಕಾಂ ಲುಕ್‌ಅಪ್‌ಗಾಗಿ ಮಾತ್ರ ಬಳಸಲಾಗುತ್ತದೆ. AIಗೆ ಮಸ್ಕ್ ಮಾಡಿದ ಸಂಖ್ಯೆ ಮತ್ತು ಕರೆ ವಿವರಗಳನ್ನು ಮಾತ್ರ ಕಳುಹಿಸಲಾಗುತ್ತದೆ.", "checking_call": "🔍 ಸಂಖ್ಯೆ, ಕ್ಯಾರಿಯರ್, ನೋಂದಾಯಿತ ಸ್ಥಳ ಮತ್ತು ಮೋಸ ಸೂಚನೆಗಳನ್ನು ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ...", "invalid_phone": "❌ ಅಮಾನ್ಯ ಫೋನ್ ಸಂಖ್ಯೆ. ಭಾರತೀಯ ಸಂಖ್ಯೆಗೆ 10 ಅಂಕೆಗಳು ಅಥವಾ +91 ಜೊತೆಗೆ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ.", "telecom_intelligence": "📡 ಟೆಲಿಕಾಂ & SIM/ನೆಟ್‌ವರ್ಕ್ ಮಾಹಿತಿ", "number_valid": "ಸಂಖ್ಯೆ ಮಾನ್ಯ", "yes": "ಹೌದು", "no": "ಇಲ್ಲ", "unknown": "ತಿಳಿದಿಲ್ಲ", "carrier": "ಕ್ಯಾರಿಯರ್ / ನೆಟ್‌ವರ್ಕ್", "line_type": "ಲೈನ್ ಪ್ರಕಾರ", "line_status": "ಲೈನ್ ಸ್ಥಿತಿ", "country": "🌍 ದೇಶ", "region": "📍 ಪ್ರದೇಶ", "registered_city": "🏙️ ನೋಂದಾಯಿತ ನಗರ", "timezone": "🕐 ಸಮಯ ವಲಯ", "lookup_unavailable": "⚠️ ಟೆಲಿಕಾಂ ಲುಕ್‌ಅಪ್ ಲಭ್ಯವಿಲ್ಲ. ಕರೆ ವರ್ತನೆ ಮತ್ತು AI ಸೂಚನೆಗಳಿಂದ ಕರೆ ವಿಶ್ಲೇಷಿಸಬಹುದು.", "lookup_detail": "ಲುಕ್‌ಅಪ್ ವಿವರ", "risk_evidence": "📊 ಅಪಾಯದ ಸಾಕ್ಷ್ಯ", "behavior_risk": "ವರ್ತನೆ ಅಪಾಯ", "calls_received": "ಸ್ವೀಕರಿಸಿದ ಕರೆಗಳು", "overall_risk": "ಒಟ್ಟು ಅಪಾಯ", "telecom_assessment": "📡 ಟೆಲಿಕಾಂ ಮೌಲ್ಯಮಾಪನ", "telecom_not_verdict": "ಟೆಲಿಕಾಂ ಡೇಟಾ ಸಹಾಯಕ ಸಾಕ್ಷ್ಯ ಮಾತ್ರ; ಇದರಿಂದ ಕರೆ ಮಾಡಿದವರು ಮೋಸಗಾರರು ಎಂದು ಸಾಬೀತಾಗುವುದಿಲ್ಲ.", "quiz_description": "ನಿಮ್ಮ ಜ್ಞಾನವನ್ನು ಪರೀಕ್ಷಿಸಿ ಮತ್ತು ಮೋಸಗಳು ಸಂಭವಿಸುವ ಮೊದಲು ಅವುಗಳನ್ನು ಗುರುತಿಸಲು ಕಲಿಯಿರಿ.", "correct": "✅ ಸರಿಯಾಗಿದೆ!", "incorrect": "❌ ತಪ್ಪಾಗಿದೆ!", "select_answer": "ದಯವಿಟ್ಟು ಮೊದಲು ಉತ್ತರವನ್ನು ಆಯ್ಕೆಮಾಡಿ.", "perfect_score": "🎉 ಪರಿಪೂರ್ಣ ಸ್ಕೋರ್! ನೀವು ಮೋಸ ಪತ್ತೆಹಚ್ಚುವ ತಜ್ಞರು!", "report_scam_title": "ಮೋಸವನ್ನು ವರದಿ ಮಾಡಿ",
        "raw_response": "ಡೀಬಗ್ - ಮೂಲ ಪ್ರತಿಸ್ಪಂದನ",
        "groq_error": "Groq API ದೋಷ",
        "parse_error": "ಪ್ರತಿಸ್ಪಂದನವನ್ನು ಓದಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "enter_message": "ವಿಶ್ಲೇಷಿಸಲು ಸಂದೇಶವನ್ನು ನಮೂದಿಸಿ.",
        "enter_url": "ವಿಶ್ಲೇಷಿಸಲು URL ಅನ್ನು ನಮೂದಿಸಿ.",
        "enter_phone": "ವಿಶ್ಲೇಷಿಸಲು ಫೋನ್ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ.",
        "safe_label": "ಸುರಕ್ಷಿತ",
        "suspicious_label": "ಅನುಮಾನಾಸ್ಪದ",
        "scam_label": "ಸ್ಕ್ಯಾಮ್",
        "english": "ಆಂಗ್ಲ",
        "report": "ಸ್ಕ್ಯಾಮ್ ವರದಿ ಮಾಡಿ",
        "footer_model": "ಡಿಜಿಟಲ್ ಸುರಕ್ಷತೆಗಾಗಿ 💚 ನಿರ್ಮಿಸಲಾಗಿದೆ | ಮಾದರಿ: llama-3.1-8b-instant via Groq"
    }
}

# ==================== EXAMPLE MESSAGES ====================
EXAMPLE_MESSAGES = {
    "en": [
        "🎰 Congratulations! You've won Rs. 5,00,000 in the Lucky Draw! Call this number immediately to claim your prize before it expires!",
        "🏦 Dear Customer, your bank account has been suspended due to suspicious activity. Click here to verify immediately: http://fake-bank-verify.in",
        "📦 Your Amazon package is on hold due to unpaid customs fees. Pay Rs. 499 now to release it: http://amz-delivery.in/pay"
    ],
    "te": [
        "🎰 అభినందనలు! మీరు లక్కీ డ్రా‌లో Rs. 5,00,000 గెలుచుకున్నారు! బహుమతి క్లెయిమ్ చేయడానికి వెంటనే ఈ నంబర్‌కు కాల్ చేయండి!",
        "🏦 ప్రియ కస్టమర్, అనుమానాస్పద కార్యకలాపాల కారణంగా మీ బ్యాంక్ ఖాతా సస్పెండ్ చేయబడింది. వెంటనే ధృవీకరించడానికి ఇక్కడ క్లిక్ చేయండి: http://fake-bank-verify.in",
        "📦 మీ Amazon ప్యాకేజీ చెల్లించని కస్టమ్స్ ఫీజుల కారణంగా హోల్డ్‌లో ఉంది. విడుదల చేయడానికి ఇప్పుడే Rs. 499 చెల్లించండి: http://amz-delivery.in/pay"
    ],
    "ta": [
        "🎰 வாழ்த்துக்கள்! லக்கி டிராவில் நீங்கள் Rs. 5,00,000 வென்றுள்ளீர்கள்! பரிசைப் பெற இந்த எண்ணுக்கு உடனடியாக அழைக்கவும்!",
        "🏦 அன்பு வாடிக்கையாளரே, சந்தேகத்திற்கிடமான செயல்பாடுகளால் உங்கள் வங்கி கணக்கு இடைநிறுத்தப்பட்டுள்ளது. உடனடியாக சரிபார்க்க இங்கே கிளிக் செய்யவும்: http://fake-bank-verify.in",
        "📦 உங்கள் Amazon பார்சல் செலுத்தப்படாத சுங்கக் கட்டணங்களால் நிறுத்தப்பட்டுள்ளது. விடுவிக்க இப்போது Rs. 499 செலுத்தவும்: http://amz-delivery.in/pay"
    ],
    "hi": [
        "🎰 बधाई हो! आप लकी ड्रॉ में Rs. 5,00,000 जीत गए हैं! पुरस्कार प्राप्त करने के लिए तुरंत इस नंबर पर कॉल करें!",
        "🏦 प्रिय ग्राहक, संदिग्ध गतिविधि के कारण आपका बैंक खाता निलंबित कर दिया गया है। तुरंत सत्यापित करने के लिए यहां क्लिक करें: http://fake-bank-verify.in",
        "📦 आपका Amazon पैकेज अवैतनिक सीमा शुल्क के कारण होल्ड पर है। इसे जारी करने के लिए अभी Rs. 499 का भुगतान करें: http://amz-delivery.in/pay"
    ],
    "kn": [
        "🎰 ಅಭಿನಂದನೆಗಳು! ನೀವು ಲಕ್ಕಿ ಡ್ರಾ‌ವಿನಲ್ಲಿ Rs. 5,00,000 ಗೆದ್ದಿದ್ದೀರಿ! ಬಹುಮತಿಯನ್ನು ಪಡೆಯಲು ತಕ್ಷಣ ಈ ಸಂಖ್ಯೆಗೆ ಕರೆ ಮಾಡಿ!",
        "🏦 ಪ್ರಿಯ ಗ್ರಾಹಕ, ಅನುಮಾನಾಸ್ಪದ ಚಟುವಟಿಕೆಯ ಕಾರಣ ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಖಾತೆಯನ್ನು ನಿಲ್ಲಿಸಲಾಗಿದೆ. ತಕ್ಷಣ ಧೃವೀಕರಿಸಲು ಇಲ್ಲಿ ಕ್ಲಿಕ್ ಮಾಡಿ: http://fake-bank-verify.in",
        "📦 ನಿಮ್ಮ Amazon ಪ್ಯಾಕೇಜ್ ಅನುಪಜೀವಿ ಸುಂಕದ ಶುಲ್ಕದ ಕಾರಣ ಹೋಲ್ಡ್‌ನಲ್ಲಿದೆ. ಬಿಡುಗಡೆ ಮಾಡಲು ಈಗ Rs. 499 ಪಾವತಿಸಿ: http://amz-delivery.in/pay"
    ]
}

# ==================== QUIZ DATA ====================
QUIZ_DATA = {
    "en": [
        {
            "question": "You receive a message saying you've won a lottery you never entered. What should you do?",
            "options": ["Call the number immediately to claim", "Ignore and delete the message", "Pay the processing fee to receive the prize", "Share it with friends"],
            "correct": 1,
            "explanation": "Legitimate lotteries don't ask winners to pay fees upfront. If you didn't enter, you can't win."
        },
        {
            "question": "A caller claims to be from your bank and asks for your OTP. What is the correct response?",
            "options": ["Provide the OTP immediately", "Ask them to wait while you verify", "Never share OTPs — banks never ask for them", "Give them the last 4 digits instead"],
            "correct": 2,
            "explanation": "Banks and legitimate institutions NEVER ask for your OTP or PIN. This is a sure sign of a scam."
        },
        {
            "question": "You get a link that looks like your bank's website but the URL is slightly different. What should you do?",
            "options": ["Click and enter your details quickly", "Check the URL carefully and don't click", "Forward it to family members", "Download any attached files"],
            "correct": 1,
            "explanation": "Phishing sites often use URLs that look similar to real ones. Always verify the exact domain name."
        },
        {
            "question": "A delivery message asks you to pay a small customs fee via a link. What do you do?",
            "options": ["Pay immediately to get your package", "Check your actual order on the official website", "Call the number in the message", "Share your card details"],
            "correct": 1,
            "explanation": "Always verify through official channels. Scammers use fake delivery messages to steal payment information."
        },
        {
            "question": "Someone on a dating app asks you to invest in cryptocurrency after a week of chatting. What is this?",
            "options": ["A genuine investment opportunity", "A romance scam", "A bank offer", "A lucky chance"],
            "correct": 1,
            "explanation": "This is a classic 'pig butchering' or romance scam. Scammers build trust before asking for money."
        }
    ],
    "te": [
        {
            "question": "మీరు ఎప్పుడూ ప్రవేశించని లాటరీలో గెలిచారని ఒక సందేశం వస్తే మీరు ఏమి చేయాలి?",
            "options": ["బహుమతి క్లెయిమ్ చేయడానికి వెంటనే కాల్ చేయండి", "సందేశాన్ని ఇగ్నోర్ చేసి డిలీట్ చేయండి", "బహుమతి అందుకోవడానికి ప్రాసెసింగ్ ఫీజు చెల్లించండి", "స్నేహితులతో షేర్ చేయండి"],
            "correct": 1,
            "explanation": "అసలైన లాటరీలు గెలుపొందినవారి నుండి ముందుగా ఫీజులు అడగవు. మీరు ప్రవేశించకపోతే గెలవలేరు."
        },
        {
            "question": "ఒక కాలర్ మీ బ్యాంక్ నుండి వచ్చానని చెప్పి OTP అడిగితే సరైన స్పందన ఏమిటి?",
            "options": ["OTP వెంటనే ఇవ్వండి", "ధృవీకరించే వరకు వేచి ఉండమని చెప్పండి", "OTP లు ఎప్పుడూ షేర్ చేయకండి — బ్యాంకులు ఎప్పుడూ అడగవు", "చివరి 4 అంకెలను ఇవ్వండి"],
            "correct": 2,
            "explanation": "బ్యాంకులు మరియు అధికారిక సంస్థలు ఎప్పుడూ మీ OTP లేదా PIN అడగవు. ఇది స్కామ్ యొక్క ఖచ్చితమైన సంకేతం."
        },
        {
            "question": "మీ బ్యాంక్ వెబ్‌సైట్ లాగా కనిపించే లింక్ వచ్చింది, కానీ URL కొంచెం భిన్నంగా ఉంది. మీరు ఏమి చేయాలి?",
            "options": ["వేగంగా క్లిక్ చేసి వివరాలు నమోదు చేయండి", "URL ను జాగ్రత్తగా చూసి క్లిక్ చేయకండి", "కుటుంబ సభ్యులకు ఫార్వార్డ్ చేయండి", "జోడించిన ఫైళ్లను డౌన్‌లోడ్ చేయండి"],
            "correct": 1,
            "explanation": "ఫిషింగ్ సైట్లు అసలైనవి లాంటి URL లను ఉపయోగిస్తాయి. ఎల్లప్పుడూ ఖచ్చితమైన డొమైన్ పేరును ధృవీకరించండి."
        },
        {
            "question": "డెలివరీ సందేశం ఒక లింక్ ద్వారా చిన్న కస్టమ్స్ ఫీజు చెల్లించమని అడుగుతోంది. మీరు ఏమి చేయాలి?",
            "options": ["ప్యాకేజీ కోసం వెంటనే చెల్లించండి", "అధికారిక వెబ్‌సైట్‌లో మీ ఆర్డర్‌ను చూసుకోండి", "సందేశంలోని నంబర్‌కు కాల్ చేయండి", "మీ కార్డు వివరాలను షేర్ చేయండి"],
            "correct": 1,
            "explanation": "ఎల్లప్పుడూ అధికారిక ఛానెల్‌ల ద్వారా ధృవీకరించండి. స్కామర్లు నకిలీ డెలివరీ సందేశాలతో పేమెంట్ సమాచారాన్ని దొంగిలిస్తారు."
        },
        {
            "question": "డేటింగ్ యాప్‌లో ఎవరో వారం రోజుల చాటింగ్ తర్వాత క్రిప్టోకరెన్సీలో పెట్టుబడి పెట్టమని అడుగుతున్నారు. ఇది ఏమిటి?",
            "options": ["ఒక నిజమైన పెట్టుబడి అవకాశం", "ఒక రొమాన్స్ స్కామ్", "ఒక బ్యాంక్ ఆఫర్", "ఒక అదృష్ట అవకాశం"],
            "correct": 1,
            "explanation": "ఇది క్లాసిక్ 'పిగ్ బుచరింగ్' లేదా రొమాన్స్ స్కామ్. స్కామర్లు డబ్బు అడగడానికి ముందు నమ్మకం పెంచుకుంటారు."
        }
    ],
    "ta": [
        {
            "question": "நீங்கள் ஒருபோதும் நுழையாத லாட்டரியில் வென்றுவிட்டீர்கள் என்று ஒரு செய்தி வருகிறது. நீங்கள் என்ன செய்வீர்கள்?",
            "options": ["பரிசைப் பெற உடனடியாக அழைக்கவும்", "செய்தியை புறக்கணித்து நீக்கவும்", "பரிசைப் பெற செயலாக்கக் கட்டணம் செலுத்தவும்", "நண்பர்களுடன் பகிரவும்"],
            "correct": 1,
            "explanation": "சட்டபூர்வமான லாட்டரிகள் வெற்றியாளர்களிடம் முன்பணம் கேட்காது. நீங்கள் நுழையாவிட்டால், வெல்ல முடியாது."
        },
        {
            "question": "ஒரு அழைப்பாளர் உங்கள் வங்கியிலிருந்து வந்ததாகக் கூறி OTP ஐ கேட்கிறார். சரியான பதில் என்ன?",
            "options": ["OTP ஐ உடனடியாக வழங்கவும்", "சரிபார்க்கும் வரை காத்திருக்கச் சொல்லவும்", "OTP களை ஒருபோதும் பகிர வேண்டாம் — வங்கிகள் ஒருபோதும் கேட்காது", "கடைசி 4 இலக்கங்களை கொடுக்கவும்"],
            "correct": 2,
            "explanation": "வங்கிகள் மற்றும் சட்டபூர்வமான நிறுவனங்கள் உங்கள் OTP அல்லது PIN ஐ ஒருபோதும் கேட்காது. இது மோசடியின் நிச்சயமான அறிகுறி."
        },
        {
            "question": "உங்கள் வங்கி இணையதளம் போல் தோன்றும் இணைப்பு வந்துள்ளது, ஆனால் URL சற்று வேறுபட்டுள்ளது. நீங்கள் என்ன செய்வீர்கள்?",
            "options": ["விரைவாக கிளிக் செய்து விவரங்களை உள்ளிடவும்", "URL ஐ கவனமாக சரிபார்த்து கிளிக் செய்ய வேண்டாம்", "குடும்ப உறுப்பினர்களுக்கு அனுப்பவும்", "இணைக்கப்பட்ட கோப்புகளை பதிவிறக்கவும்"],
            "correct": 1,
            "explanation": "பிஷிங் தளங்கள் அசலானவை போன்ற URL களை பயன்படுத்துகின்றன. எப்போதும் சரியான டொமைன் பெயரை சரிபார்க்கவும்."
        },
        {
            "question": "டெலிவரி செய்தி ஒரு இணைப்பு வழியாக சிறிய சுங்கக் கட்டணத்தை செலுத்த கேட்கிறது. நீங்கள் என்ன செய்வீர்கள்?",
            "options": ["பார்சலைப் பெற உடனடியாக செலுத்தவும்", "அதிகாரப்பூர்வ இணையதளத்தில் உங்கள் ஆர்டரை சரிபார்க்கவும்", "செய்தியில் உள்ள எண்ணுக்கு அழைக்கவும்", "உங்கள் அட்டை விவரங்களை பகிரவும்"],
            "correct": 1,
            "explanation": "எப்போதும் அதிகாரப்பூர்வ சேனல்கள் வழியாக சரிபார்க்கவும். மோசடியாளர்கள் போலி டெலிவரி செய்திகள் மூலம் கட்டண தகவலை திருடுகின்றனர்."
        },
        {
            "question": "டேட்டிங் செயலியில் யாரோ ஒரு வாரம் அரட்டையடித்த பிறகு கிரிப்டோகரன்சியில் முதலீடு செய்ய கேட்கிறார். இது என்ன?",
            "options": ["ஒரு நேர்மையான முதலீட்டு வாய்ப்பு", "ஒரு ரொமான்ஸ் மோசடி", "ஒரு வங்கி சலுகை", "ஒரு அதிர்ஷ்ட வாய்ப்பு"],
            "correct": 1,
            "explanation": "இது கிளாசிக் 'பிக் பட்சரிங்' அல்லது ரொமான்ஸ் மோசடி. மோசடியாளர்கள் பணம் கேட்பதற்கு முன் நம்பிக்கையை உருவாக்குகிறார்கள்."
        }
    ],
    "hi": [
        {
            "question": "आपको एक संदेश आता है कि आप एक लॉटरी जीत गए हैं जिसमें आपने कभी प्रवेश नहीं किया। आपको क्या करना चाहिए?",
            "options": ["पुरस्कार प्राप्त करने के लिए तुरंत कॉल करें", "संदेश को अनदेखा करें और हटा दें", "पुरस्कार प्राप्त करने के लिए प्रोसेसिंग शुल्क दें", "दोस्तों के साथ साझा करें"],
            "correct": 1,
            "explanation": "वैध लॉटरियाँ विजेताओं से अग्रिम शुल्क नहीं मांगतीं। यदि आपने प्रवेश नहीं किया, तो आप जीत नहीं सकते।"
        },
        {
            "question": "एक कॉलर आपके बैंक से होने का दावा करता है और आपका OTP मांगता है। सही प्रतिक्रिया क्या है?",
            "options": ["OTP तुरंत प्रदान करें", "सत्यापित होने तक इंतजार करने के लिए कहें", "OTP कभी साझा न करें — बैंक कभी नहीं मांगते", "अंतिम 4 अंक दें"],
            "correct": 2,
            "explanation": "बैंक और वैध संस्थान कभी भी आपका OTP या PIN नहीं मांगते। यह घोटाले का निश्चित संकेत है।"
        },
        {
            "question": "आपको एक लिंक मिलता है जो आपके बैंक की वेबसाइट जैसा दिखता है लेकिन URL थोड़ा अलग है। आपको क्या करना चाहिए?",
            "options": ["जल्दी से क्लिक करें और विवरण दर्ज करें", "URL को ध्यान से जांचें और क्लिक न करें", "इसे परिवार के सदस्यों को भेजें", "संलग्न फाइलें डाउनलोड करें"],
            "correct": 1,
            "explanation": "फिशिंग साइटें अक्सर असली लोगों जैसे URL का उपयोग करती हैं। हमेशा सटीक डोमेन नाम सत्यापित करें।"
        },
        {
            "question": "एक डिलीवरी संदेश आपसे एक लिंक के माध्यम से एक छोटा सीमा शुल्क भुगतान करने के लिए कहता है। आप क्या करेंगे?",
            "options": ["पैकेज प्राप्त करने के लिए तुरंत भुगतान करें", "आधिकारिक वेबसाइट पर अपने ऑर्डर की जांच करें", "संदेश में दिए गए नंबर पर कॉल करें", "अपने कार्ड विवरण साझा करें"],
            "correct": 1,
            "explanation": "हमेशा आधिकारिक चैनलों के माध्यम से सत्यापित करें। घोटालेबाज नकली डिलीवरी संदेशों का उपयोग करके भुगतान जानकारी चुराते हैं।"
        },
        {
            "question": "डेटिंग ऐप पर कोई एक हफ्ते की बातचीत के बाद क्रिप्टोकरेंसी में निवेश करने के लिए कहता है। यह क्या है?",
            "options": ["एक वास्तविक निवेश अवसर", "एक रोमांस घोटाला", "एक बैंक ऑफर", "एक भाग्यशाली मौका"],
            "correct": 1,
            "explanation": "यह एक क्लासिक 'पिग बुचरिंग' या रोमांस घोटाला है। घोटालेबाज पैसे मांगने से पहले विश्वास बनाते हैं।"
        }
    ],
    "kn": [
        {
            "question": "ನೀವು ಎಂದಿಗೂ ಪ್ರವೇಶಿಸದ ಲಾಟರಿಯಲ್ಲಿ ಗೆದ್ದಿರುವೀರಿ ಎಂದು ಸಂದೇಶ ಬಂದರೆ ನೀವು ಏನು ಮಾಡಬೇಕು?",
            "options": ["ಬಹುಮತಿಯನ್ನು ಪಡೆಯಲು ತಕ್ಷಣ ಕರೆ ಮಾಡಿ", "ಸಂದೇಶವನ್ನು ನಿರ್ಲಕ್ಷಿಸಿ ಅಳಿಸಿ", "ಬಹುಮತಿಯನ್ನು ಪಡೆಯಲು ಪ್ರಾಸೆಸಿಂಗ್ ಶುಲ್ಕ ಪಾವತಿಸಿ", "ಸ್ನೇಹಿತರೊಂದಿಗೆ ಹಂಚಿಕೊಳ್ಳಿ"],
            "correct": 1,
            "explanation": "ಕಾನೂನುಬದ್ಧ ಲಾಟರಿಗಳು ವಿಜೇತರಿಂದ ಮುಂಗಡ ಶುಲ್ಕಗಳನ್ನು ಕೇಳುವುದಿಲ್ಲ. ನೀವು ಪ್ರವೇಶಿಸದಿದ್ದರೆ, ಗೆಲ್ಲಲು ಸಾಧ್ಯವಿಲ್ಲ."
        },
        {
            "question": "ಒಬ್ಬ ಕಾಲರ್ ನಿಮ್ಮ ಬ್ಯಾಂಕ್‌ನಿಂದ ಬಂದವನು ಎಂದು ಹೇಳಿ OTP ಕೇಳುತ್ತಾನೆ. ಸರಿಯಾದ ಪ್ರತಿಕ್ರಿಯೆ ಏನು?",
            "options": ["OTP ಅನ್ನು ತಕ್ಷಣ ಒದಗಿಸಿ", "ಧೃವೀಕರಿಸುವವರೆಗೆ ಕಾಯಲು ಹೇಳಿ", "OTP ಗಳನ್ನು ಎಂದಿಗೂ ಹಂಚಿಕೊಳ್ಳಬೇಡಿ — ಬ್ಯಾಂಕುಗಳು ಎಂದಿಗೂ ಕೇಳುವುದಿಲ್ಲ", "ಕೊನೆಯ 4 ಅಂಕೆಗಳನ್ನು ನೀಡಿ"],
            "correct": 2,
            "explanation": "ಬ್ಯಾಂಕುಗಳು ಮತ್ತು ಕಾನೂನುಬದ್ಧ ಸಂಸ್ಥೆಗಳು ಎಂದಿಗೂ ನಿಮ್ಮ OTP ಅಥವಾ PIN ಅನ್ನು ಕೇಳುವುದಿಲ್ಲ. ಇದು ಸ್ಕ್ಯಾಮ್‌ನ ನಿಶ್ಚಿತ ಸಂಕೇತ."
        },
        {
            "question": "ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ವೆಬ್‌ಸೈಟ್‌ನಂತೆ ಕಾಣುವ ಲಿಂಕ್ ಬಂದಿದೆ, ಆದರೆ URL ಸ್ವಲ್ಪ ಭಿನ್ನವಾಗಿದೆ. ನೀವು ಏನು ಮಾಡಬೇಕು?",
            "options": ["ವೇಗವಾಗಿ ಕ್ಲಿಕ್ ಮಾಡಿ ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ", "URL ಅನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ಪರಿಶೀಲಿಸಿ ಕ್ಲಿಕ್ ಮಾಡಬೇಡಿ", "ಕುಟುಂಬ ಸದಸ್ಯರಿಗೆ ಫಾರ್ವರ್ಡ್ ಮಾಡಿ", "ಜೋಡಿಸಿದ ಫೈಲ್‌ಗಳನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ"],
            "correct": 1,
            "explanation": "ಫಿಶಿಂಗ್ ಸೈಟ್‌ಗಳು ಸಾಮಾನ್ಯವಾಗಿ ನಿಜವಾದವುಗಳನ್ನು ಹೋಲುವ URL ಗಳನ್ನು ಬಳಸುತ್ತವೆ. ಎಂದಿಗೂ ನಿಖರವಾದ ಡೊಮೇನ್ ಹೆಸರನ್ನು ಧೃವೀಕರಿಸಿ."
        },
        {
            "question": "ಡೆಲಿವರಿ ಸಂದೇಶವು ಒಂದು ಲಿಂಕ್ ಮೂಲಕ ಸಣ್ಣ ಸುಂಕದ ಶುಲ್ಕವನ್ನು ಪಾವತಿಸಲು ಕೇಳುತ್ತದೆ. ನೀವು ಏನು ಮಾಡುತ್ತೀರಿ?",
            "options": ["ಪ್ಯಾಕೇಜ್ ಪಡೆಯಲು ತಕ್ಷಣ ಪಾವತಿಸಿ", "ಅಧಿಕೃತ ವೆಬ್‌ಸೈಟ್‌ನಲ್ಲಿ ನಿಮ್ಮ ಆರ್ಡರ್ ಪರಿಶೀಲಿಸಿ", "ಸಂದೇಶದಲ್ಲಿನ ಸಂಖ್ಯೆಗೆ ಕರೆ ಮಾಡಿ", "ನಿಮ್ಮ ಕಾರ್ಡ್ ವಿವರಗಳನ್ನು ಹಂಚಿಕೊಳ್ಳಿ"],
            "correct": 1,
            "explanation": "ಎಂದಿಗೂ ಅಧಿಕೃತ ಚಾನೆಲ್‌ಗಳ ಮೂಲಕ ಧೃವೀಕರಿಸಿ. ಸ್ಕ್ಯಾಮರ್‌ಗಳು ನಕಲಿ ಡೆಲಿವರಿ ಸಂದೇಶಗಳನ್ನು ಬಳಸಿ ಪಾವತಿ ಮಾಹಿತಿಯನ್ನು ಕದಿಯುತ್ತಾರೆ."
        },
        {
            "question": "ಡೇಟಿಂಗ್ ಯಾಪ್‌ನಲ್ಲಿ ಯಾರೋ ಒಂದು ವಾರ ಚಾಟಿಂಗ್ ನಂತರ ಕ್ರಿಪ್ಟೋಕರೆನ್ಸಿಯಲ್ಲಿ ಹೂಡಿಕೆ ಮಾಡಲು ಕೇಳುತ್ತಾರೆ. ಇದು ಏನು?",
            "options": ["ಒಂದು ನಿಜವಾದ ಹೂಡಿಕೆ ಅವಕಾಶ", "ಒಂದು ರೊಮಾನ್ಸ್ ಸ್ಕ್ಯಾಮ್", "ಒಂದು ಬ್ಯಾಂಕ್ ಆಫರ್", "ಒಂದು ಅದೃಷ್ಟದ ಅವಕಾಶ"],
            "correct": 1,
            "explanation": "ಇದು ಕ್ಲಾಸಿಕ್ 'ಪಿಗ್ ಬುಚರಿಂಗ್' ಅಥವಾ ರೊಮಾನ್ಸ್ ಸ್ಕ್ಯಾಮ್. ಸ್ಕ್ಯಾಮರ್‌ಗಳು ಹಣ ಕೇಳುವ ಮೊದಲು ವಿಶ್ವಾಸವನ್ನು ನಿರ್ಮಿಸುತ್ತಾರೆ."
        }
    ]
}

# ==================== TELECOM LOOKUP ====================
def lookup_telecom_info(phone_number: str):
    """Basic telecom lookup for Indian numbers using simple heuristics."""
    import requests

    # Clean the number
    clean = re.sub(r"[^\d]", "", phone_number)
    if clean.startswith("91") and len(clean) > 10:
        clean = clean[2:]

    if len(clean) != 10:
        return None

    # Indian carrier prefixes (simplified)
    PREFIX_CARRIERS = {
        "6": "Reliance Jio / Vi / Airtel",
        "7": "Airtel / Vi / BSNL",
        "8": "Airtel / Reliance Jio / Vi",
        "9": "Airtel / Reliance Jio / Vi / BSNL"
    }

    first_digit = clean[0]
    carrier = PREFIX_CARRIERS.get(first_digit, "Unknown Carrier")

    # Circle lookup from first 4 digits (simplified mapping)
    CIRCLE_MAP = {
        "6000": "Tamil Nadu", "6001": "Tamil Nadu", "6002": "Tamil Nadu",
        "6100": "Kerala", "6200": "Karnataka", "6300": "Andhra Pradesh",
        "6400": "West Bengal", "6500": "Maharashtra", "6600": "Gujarat",
        "6700": "Punjab", "6800": "Haryana", "6900": "Bihar",
        "7000": "West Bengal", "7100": "Odisha", "7200": "Assam",
        "7300": "Jammu & Kashmir", "7400": "Karnataka", "7500": "Madhya Pradesh",
        "7600": "Rajasthan", "7700": "Maharashtra", "7800": "Uttar Pradesh",
        "7900": "Gujarat", "8000": "Karnataka", "8100": "Karnataka",
        "8200": "Kerala", "8300": "West Bengal", "8400": "Bihar",
        "8500": "Andhra Pradesh", "8600": "Tamil Nadu", "8700": "Punjab",
        "8800": "Kolkata", "8900": "Kolkata", "9000": "Maharashtra",
        "9100": "Andhra Pradesh", "9200": "Mumbai", "9300": "Madhya Pradesh",
        "9400": "Kerala", "9500": "Tamil Nadu", "9600": "Karnataka",
        "9700": "Andhra Pradesh", "9800": "West Bengal", "9900": "Delhi"
    }

    prefix4 = clean[:4]
    circle = CIRCLE_MAP.get(prefix4, "Unknown Region")

    return {
        "valid": True,
        "carrier": carrier,
        "line_type": "Mobile",
        "line_status": "Active",
        "country": "India",
        "region": circle,
        "city": circle,
        "timezone": "IST (UTC+5:30)"
    }

# ==================== AI ANALYSIS FUNCTIONS ====================
def analyze_message_ai(message: str, lang: str):
    """Use Groq AI to analyze a message for scam indicators."""
    prompt = f"""You are Raksha, a digital safety guardian AI. Analyze the following message for scam indicators.

Respond ONLY in valid JSON format with this exact structure:
{{
  "verdict": "Scam" | "Suspicious" | "Safe",
  "confidence": 0-100,
  "red_flags": ["list of specific red flags found"],
  "advice": "specific advice for the user",
  "risk_factors": ["list of risk factors"],
  "explanation": "brief explanation of the analysis"
}}

Message to analyze: """ + json.dumps(message) + """

Respond in English only, with the JSON structure above."""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert specializing in scam detection for Indian users."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=800
        )

        content = response.choices[0].message.content
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            return None
    except Exception as e:
        st.error(f"Analysis error: {str(e)}")
        return None

def analyze_url_ai(url: str, lang: str):
    """Use Groq AI to analyze a URL for phishing/scam indicators."""
    prompt = f"""You are Raksha, a digital safety guardian AI. Analyze the following URL for phishing and scam indicators.

Respond ONLY in valid JSON format with this exact structure:
{{
  "verdict": "Scam" | "Suspicious" | "Safe",
  "confidence": 0-100,
  "red_flags": ["list of specific red flags found"],
  "advice": "specific advice for the user",
  "risk_factors": ["list of risk factors"],
  "explanation": "brief explanation of the analysis"
}}

URL to analyze: {url}

Respond in English only, with the JSON structure above."""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert specializing in phishing and malicious URL detection."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=800
        )

        content = response.choices[0].message.content
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            return None
    except Exception as e:
        st.error(f"Analysis error: {str(e)}")
        return None

def analyze_call_ai(phone: str, description: str, call_count: int, lang: str):
    """Use Groq AI to analyze a call for scam indicators."""
    masked = phone[:4] + "****" + phone[-2:] if len(phone) >= 6 else "******"

    prompt = f"""You are Raksha, a digital safety guardian AI. Analyze the following call details for scam indicators.

Respond ONLY in valid JSON format with this exact structure:
{{
  "verdict": "Scam" | "Suspicious" | "Safe",
  "confidence": 0-100,
  "red_flags": ["list of specific red flags found"],
  "advice": "specific advice for the user",
  "risk_factors": ["list of risk factors"],
  "explanation": "brief explanation of the analysis"
}}

Call Details:
- Phone Number (masked): {masked}
- Number of calls received: {call_count}
- Caller description: """ + json.dumps(description) + """

Respond in English only, with the JSON structure above."""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert specializing in phone scam and vishing detection for Indian users."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=800
        )

        content = response.choices[0].message.content
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            return None
    except Exception as e:
        st.error(f"Analysis error: {str(e)}")
        return None

# ==================== UI HELPERS ====================
def get_badge_class(verdict: str):
    verdict = verdict.lower()
    if "scam" in verdict or "high" in verdict:
        return "scam-high"
    elif "suspicious" in verdict or "medium" in verdict:
        return "scam-medium"
    elif "safe" in verdict or "low" in verdict:
        return "scam-safe"
    else:
        return "scam-low"

def display_result(result: dict, ui: dict):
    if not result:
        st.error(ui["parse_error"])
        return

    verdict = result.get("verdict", "Unknown")
    confidence = result.get("confidence", 0)
    badge_class = get_badge_class(verdict)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div style="text-align: center; margin: 1rem 0;">
                <div class="scam-badge {badge_class}" style="font-size: 1.5rem; padding: 1rem 2rem;">
                    {ui.get("verdict", "Verdict")}: {verdict}
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.metric(ui.get("confidence", "Confidence"), f"{confidence}%")

    st.divider()

    if "red_flags" in result and result["red_flags"]:
        st.subheader(f"🚩 {ui.get('red_flags', 'Red Flags')}")
        for flag in result["red_flags"]:
            st.markdown(f"- {flag}")

    if "risk_factors" in result and result["risk_factors"]:
        st.subheader(f"⚠️ {ui.get('risk_factors', 'Risk Factors')}")
        for factor in result["risk_factors"]:
            st.markdown(f"- {factor}")

    if "explanation" in result and result["explanation"]:
        st.subheader(f"ℹ️ {ui.get('explanation', 'Explanation')}")
        st.info(result["explanation"])

    if "advice" in result and result["advice"]:
        st.subheader(f"💡 {ui.get('advice', 'Advice')}")
        st.success(result["advice"])

# ==================== SESSION STATE ====================
if "messages_checked" not in st.session_state:
    st.session_state.messages_checked = 0
if "scams_caught" not in st.session_state:
    st.session_state.scams_caught = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_current" not in st.session_state:
    st.session_state.quiz_current = 0
if "quiz_answered" not in st.session_state:
    st.session_state.quiz_answered = False

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="font-size: 2.5rem; margin: 0;">🛡️</h1>
            <h2 style="margin-top: 0.5rem; color: #1e40af;">Raksha</h2>
            <p style="color: #64748b; font-size: 0.9rem;">{UI_TRANSLATIONS['en']['mission_text']}</p>
        </div>
    """, unsafe_allow_html=True)

    selected_language = st.selectbox(
        UI_TRANSLATIONS["en"]["language_label"],
        options=list(LANGUAGE_OPTIONS.keys()),
        index=0
    )
    lang_code = LANGUAGE_OPTIONS[selected_language]
    T = TRANSLATIONS[lang_code]
    UI = UI_TRANSLATIONS[lang_code]

    st.divider()

    st.markdown(f"### {UI['stats']}")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(UI["messages_checked"], st.session_state.messages_checked)
    with col2:
        st.metric(UI["scams_caught"], st.session_state.scams_caught)

    st.divider()

    st.markdown(f"### {UI['why_raksha']}")
    st.markdown(f"{UI['why_1']}")
    st.markdown(f"{UI['why_2']}")
    st.markdown(f"{UI['why_3']}")
    st.markdown(f"{UI['why_4']}")

    st.divider()

    st.markdown(f"<p style='text-align: center; color: #64748b; font-size: 0.85rem;'>{UI['made_for']}</p>", unsafe_allow_html=True)

# ==================== MAIN CONTENT ====================
st.markdown(f"""
    <div class="hero-banner">
        <h1>{UI['hero_title']}</h1>
        <p>{UI['hero_subtitle']}</p>
    </div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    f"💬 {T['message_checker']}",
    f"🔗 {T['link_inspector']}",
    f"📞 {T['call_checker']}",
    f"🎓 {T['learn_quiz']}"
])

# ==================== TAB 1: MESSAGE CHECKER ====================
with tab1:
    st.header(T["message_checker"])
    st.markdown(f"<p style='color: #64748b;'>{UI['paste_any']}</p>", unsafe_allow_html=True)

    # Example buttons
    st.markdown(f"**{UI['try_example']}**")
    examples = EXAMPLE_MESSAGES.get(lang_code, EXAMPLE_MESSAGES["en"])
    cols = st.columns(3)
    for i, ex in enumerate(examples):
        with cols[i]:
            if st.button(f"{['🎰', '🏦', '📦'][i]} {UI[['fake_lottery', 'fake_bank', 'fake_delivery'][i]]}", key=f"ex_{i}"):
                st.session_state["msg_input"] = ex

    msg_input = st.text_area(
        T["paste_message"],
        value=st.session_state.get("msg_input", ""),
        height=150,
        key="msg_text_area"
    )

    if st.button(T["analyze_btn"], type="primary", use_container_width=True):
        if not msg_input.strip():
            st.warning(UI["enter_message"])
        else:
            with st.spinner("Analyzing..."):
                result = analyze_message_ai(msg_input, lang_code)
                st.session_state.messages_checked += 1
                if result and result.get("verdict", "").lower() in ["scam", "suspicious"]:
                    st.session_state.scams_caught += 1
                display_result(result, UI)

# ==================== TAB 2: LINK INSPECTOR ====================
with tab2:
    st.header(T["link_inspector"])
    st.markdown(f"<p style='color: #64748b;'>{UI['url_description']}</p>", unsafe_allow_html=True)

    url_input = st.text_input(T["paste_url"], placeholder="https://example.com")

    if st.button(T["analyze_url"], type="primary", use_container_width=True):
        if not url_input.strip():
            st.warning(UI["enter_url"])
        else:
            with st.spinner("Analyzing URL..."):
                result = analyze_url_ai(url_input, lang_code)
                st.session_state.messages_checked += 1
                if result and result.get("verdict", "").lower() in ["scam", "suspicious"]:
                    st.session_state.scams_caught += 1
                display_result(result, UI)

# ==================== TAB 3: CALL CHECKER ====================
with tab3:
    st.header(T["call_checker"])
    st.markdown(f"<p style='color: #64748b;'>{UI['call_checker_description']}</p>", unsafe_allow_html=True)

    phone_input = st.text_input(T["phone_number"], placeholder="9876543210 or +919876543210")
    call_count = st.number_input(T["call_count"], min_value=1, max_value=100, value=1)
    call_desc = st.text_area(
        UI["call_description_label"],
        placeholder=UI["call_description_placeholder"],
        height=100
    )

    st.markdown(f"<p style='font-size: 0.8rem; color: #64748b;'>{UI['privacy_notice']}</p>", unsafe_allow_html=True)

    if st.button(T["analyze_call"], type="primary", use_container_width=True):
        if not phone_input.strip():
            st.warning(UI["enter_phone"])
        else:
            with st.spinner(UI["checking_call"]):
                # Validate phone
                clean_phone = re.sub(r"[^\d+]", "", phone_input)
                if not (len(clean_phone) == 10 or (clean_phone.startswith("+91") and len(clean_phone) == 13) or (clean_phone.startswith("91") and len(clean_phone) == 12)):
                    st.error(UI["invalid_phone"])
                else:
                    # Telecom lookup
                    telecom = lookup_telecom_info(clean_phone)

                    if telecom:
                        with st.expander(UI["telecom_intelligence"]):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**{UI['number_valid']}:** {UI['yes'] if telecom['valid'] else UI['no']}")
                                st.write(f"**{UI['carrier']}:** {telecom['carrier']}")
                                st.write(f"**{UI['line_type']}:** {telecom['line_type']}")
                                st.write(f"**{UI['line_status']}:** {telecom['line_status']}")
                            with col2:
                                st.write(f"**{UI['country']}:** {telecom['country']}")
                                st.write(f"**{UI['region']}:** {telecom['region']}")
                                st.write(f"**{UI['registered_city']}:** {telecom['city']}")
                                st.write(f"**{UI['timezone']}:** {telecom['timezone']}")
                        st.caption(UI["telecom_not_verdict"])
                    else:
                        st.info(UI["lookup_unavailable"])

                    # AI Analysis
                    result = analyze_call_ai(clean_phone, call_desc, call_count, lang_code)
                    st.session_state.messages_checked += 1
                    if result and result.get("verdict", "").lower() in ["scam", "suspicious"]:
                        st.session_state.scams_caught += 1
                    display_result(result, UI)

# ==================== TAB 4: LEARN & QUIZ ====================
with tab4:
    st.header(T["quiz_title"])
    st.markdown(f"<p style='color: #64748b;'>{UI['quiz_description']}</p>", unsafe_allow_html=True)

    quiz_data = QUIZ_DATA.get(lang_code, QUIZ_DATA["en"])

    if st.session_state.quiz_current >= len(quiz_data):
        # Quiz completed
        score = st.session_state.quiz_score
        total = len(quiz_data)
        percentage = (score / total) * 100

        st.balloons()
        st.markdown(f"""
            <div style="text-align: center; padding: 2rem; background: white; border-radius: 20px; box-shadow: 0 12px 30px rgba(0,0,0,0.08);">
                <h1 style="font-size: 3rem; margin: 0;">{'🎉' if percentage == 100 else '🏆'}</h1>
                <h2>{UI['score']}: {score}/{total}</h2>
                <p style="font-size: 1.2rem; color: #64748b;">{percentage:.0f}%</p>
                <p style="font-size: 1.1rem; margin-top: 1rem;">{UI['perfect_score'] if percentage == 100 else ''}</p>
            </div>
        """, unsafe_allow_html=True)

        if st.button("🔄 Restart Quiz", type="primary"):
            st.session_state.quiz_current = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_answered = False
            st.rerun()
    else:
        current_q = quiz_data[st.session_state.quiz_current]

        st.progress((st.session_state.quiz_current) / len(quiz_data))
        st.subheader(f"{UI['question']} {st.session_state.quiz_current + 1}/{len(quiz_data)}")
        st.markdown(f"<p style='font-size: 1.1rem; font-weight: 600; color: #1e293b;'>{current_q['question']}</p>", unsafe_allow_html=True)

        answer = st.radio("Select your answer:", current_q["options"], key=f"q_{st.session_state.quiz_current}")

        if not st.session_state.quiz_answered:
            if st.button(UI["submit_answer"], type="primary"):
                st.session_state.quiz_answered = True
                selected_idx = current_q["options"].index(answer)
                if selected_idx == current_q["correct"]:
                    st.session_state.quiz_score += 1
                    st.success(f"{UI['correct']} {current_q['explanation']}")
                else:
                    st.error(f"{UI['incorrect']} {current_q['explanation']}")
                st.rerun()
        else:
            selected_idx = current_q["options"].index(answer)
            if selected_idx == current_q["correct"]:
                st.success(f"{UI['correct']}")
            else:
                st.error(f"{UI['incorrect']}")
            st.info(current_q["explanation"])

            if st.button("Next Question →", type="primary"):
                st.session_state.quiz_current += 1
                st.session_state.quiz_answered = False
                st.rerun()

# ==================== FOOTER ====================
st.divider()
st.markdown(f"""
    <div style="text-align: center; padding: 2rem 0; color: #64748b;">
        <p style="font-size: 0.9rem;">{UI['footer']}</p>
        <p style="font-size: 0.8rem; margin-top: 0.5rem;">{UI['footer_model']}</p>
        <div style="margin-top: 1rem;">
            <a href="https://cybercrime.gov.in" target="_blank" class="report-btn">{UI['report']}</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# Floating Action Button for reporting
st.markdown(f"""
    <a href="https://cybercrime.gov.in" target="_blank" class="fab-report" title="{UI['report']}">🚨</a>
""", unsafe_allow_html=True)
