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
    """Feature 2: color-coded verdict box, red/yellow/green.
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
        "footer": "🛡️ रक्षा — सुरक्षा करता है। जांचता है। सिखाता है। तीनों टूल में एक ही ask_ai() हेल्पर के साथ बनाया गया।",
    },
    "Telugu": {
        "hero_title": "🛡️ రక్ష — కుటుంబ డిజిటల్ భద్రతా రక్షకుడు",
        "hero_sub": "ఆన్‌లైన్ మోసాల నుండి కుటుంబాలను రక్షిస్తుంది — అనుమానాస్పద సందేశాలను తనిఖీ చేస్తుంది, లింక్‌లను పరిశీలిస్తుంది, మోసాన్ని గుర్తించడం నేర్పిస్తుంది. నిజమైన కుటుంబాల కోసం రూపొందించబడింది. ఆంగ్లం, హిందీ, తెలుగు, తమిళం, కన్నడలో అందుబాటులో ఉంది.",
        "mission_title": "🛡️ మా లక్ష్యం",
        "mission_text": "ప్రతిరోజూ వేలాది భారతీయ కుటుంబాలు ఆన్‌లైన్ మోసాలలో డబ్బు కోల్పోతున్నాయి. వృద్ధులు అత్యధికంగా లక్ష్యంగా ఉంటారు. రక్ష రక్షిస్తుంది, పరిశీలిస్తుంది, కుటుంబం సొంత భాషలో నేర్పిస్తుంది.",
        "lang_label": "🌐 మీ భాషను ఎంచుకోండి",
        "lang_caption": "రక్ష ఈ భాషలో సమాధానం ఇస్తుంది:",
        "why_title": "రక్ష ఎందుకు గెలుస్తుంది",
        "why_bullets": "✅ నిజమైన సమస్య, నిజమైన లక్ష్యం\n\n✅ 1 కాదు, 3 పనిచేసే సాధనాలు\n\n✅ 5 భారతీయ భాషలకు మద్దతు\n\n✅ ఒకే ask_ai() హెల్పర్ అన్నిచోట్లా వాడబడింది",
        "model_caption": "మోడల్: llama-3.3-70b-versatile, Groq ద్వారా",
        "tab1": "📩 సందేశ తనిఖీ",
        "tab2": "🔗 లింక్ పరిశీలన",
        "tab3": "🎓 నేర్చుకోండి & క్విజ్",
        "t1_subheader": "ఈ సందేశం మోసమా?",
        "t1_caption": "మీకు అనుమానం ఉన్న ఏదైనా SMS, WhatsApp, లేదా ఇమెయిల్‌ను పేస్ట్ చేయండి.",
        "t1_placeholder": "ఉదా: అభినందనలు! మీరు KBC లాటరీలో రూ. 10,00,000 గెలుచుకున్నారు. క్లెయిమ్ చేయడానికి రూ. 5000 ఫీజు పంపండి...",
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
        "t2_caption": "ఏదైనా అనుమానాస్పద లింక్ లేదా వెబ్‌సైట్ చిరునామాను పేస్ట్ చేయండి — మేము దానిని తెరవం, కేవలం పరిశీలిస్తాము.",
        "t2_placeholder": "ఉదా: http://sbi-secure-login.xyz/verify-account",
        "t2_label": "అనుమానాస్పద లింక్:",
        "t2_button": "🔍 లింక్‌ను పరిశీలించండి",
        "t2_warning": "దయచేసి ముందుగా ఒక లింక్‌ను పేస్ట్ చేయండి.",
        "t2_spinner": "లింక్‌ను పరిశీలిస్తోంది...",
        "t3_subheader": "మోసాన్ని గుర్తించడం నేర్చుకోండి",
        "t3_caption": "ప్రాక్టీస్ ఉదాహరణ మరియు దాని హెచ్చరిక సంకేతాల కోసం బటన్ నొక్కండి.",
        "t3_button": "🎓 నాకు ఒక మోస ఉదాహరణ ఇవ్వండి",
        "t3_spinner": "ప్రాక్టీస్ ఉదాహరణను సృష్టిస్తోంది...",
        "footer": "🛡️ రక్ష — రక్షిస్తుంది. పరిశీలిస్తుంది. నేర్పిస్తుంది. మూడు సాధనాలలో ఒకే ask_ai() హెల్పర్‌తో నిర్మించబడింది.",
    },
    "Tamil": {
        "hero_title": "🛡️ ரக்ஷா — குடும்ப டிஜிட்டல் பாதுகாவலர்",
        "hero_sub": "ஆன்லைன் மோசடியிலிருந்து குடும்பங்களைப் பாதுகாக்கிறது — சந்தேகத்திற்குரிய செய்திகளை சரிபார்க்கிறது, இணைப்புகளை ஆய்வு செய்கிறது, மோசடியை கண்டறிய கற்றுக்கொடுக்கிறது. உண்மையான குடும்பங்களுக்காக உருவாக்கப்பட்டது. ஆங்கிலம், இந்தி, தெலுங்கு, தமிழ், கன்னடம் ஆகியவற்றில் கிடைக்கிறது.",
        "mission_title": "🛡️ எங்கள் நோக்கம்",
        "mission_text": "ஒவ்வொரு நாளும் ஆயிரக்கணக்கான இந்திய குடும்பங்கள் ஆன்லைன் மோசடியில் பணத்தை இழக்கின்றன. முதியவர்களே அதிக இலக்கு. ரக்ஷா பாதுகாக்கிறது, ஆய்வு செய்கிறது, குடும்பத்தின் சொந்த மொழியில் கற்றுக்கொடுக்கிறது.",
        "lang_label": "🌐 உங்கள் மொழியைத் தேர்ந்தெடுக்கவும்",
        "lang_caption": "ரக்ஷா இந்த மொழியில் பதிலளிக்கும்:",
        "why_title": "ரக்ஷா ஏன் வெற்றி பெறுகிறது",
        "why_bullets": "✅ உண்மையான பிரச்சனை, உண்மையான நோக்கம்\n\n✅ 1 அல்ல, 3 செயல்படும் கருவிகள்\n\n✅ 5 இந்திய மொழிகள் ஆதரிக்கப்படுகின்றன\n\n✅ ஒரே ask_ai() உதவியாளர் எல்லா இடங்களிலும் பயன்படுத்தப்படுகிறது",
        "model_caption": "மாடல்: llama-3.3-70b-versatile, Groq மூலம்",
        "tab1": "📩 செய்தி சரிபார்ப்பு",
        "tab2": "🔗 இணைப்பு ஆய்வு",
        "tab3": "🎓 கற்றுக்கொள் & வினாடி வினா",
        "t1_subheader": "இந்த செய்தி மோசடியா?",
        "t1_caption": "நீங்கள் சந்தேகிக்கும் எந்த SMS, WhatsApp, அல்லது மின்னஞ்சலையும் ஒட்டவும்.",
        "t1_placeholder": "எ.கா: வாழ்த்துக்கள்! நீங்கள் KBC லாட்டரியில் ரூ. 10,00,000 வென்றுள்ளீர்கள். பெற ரூ. 5000 கட்டணத்தை அனுப்பவும்...",
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
        "t2_caption": "சந்தேகத்திற்குரிய இணைப்பு அல்லது இணையதள முகவரியை ஒட்டவும் — நாங்கள் அதைத் திறக்க மாட்டோம், ஆய்வு மட்டுமே செய்வோம்.",
        "t2_placeholder": "எ.கா: http://sbi-secure-login.xyz/verify-account",
        "t2_label": "சந்தேகத்திற்குரிய இணைப்பு:",
        "t2_button": "🔍 இணைப்பை ஆய்வு செய்யவும்",
        "t2_warning": "முதலில் ஒரு இணைப்பை ஒட்டவும்.",
        "t2_spinner": "இணைப்பை ஆய்வு செய்கிறது...",
        "t3_subheader": "மோசடியை கண்டறிய கற்றுக்கொள்ளுங்கள்",
        "t3_caption": "பயிற்சி எடுத்துக்காட்டு மற்றும் அதன் எச்சரிக்கை அறிகுறிகளுக்கு பொத்தானை அழுத்தவும்.",
        "t3_button": "🎓 எனக்கு ஒரு மோசடி எடுத்துக்காட்டு கொடுங்கள்",
        "t3_spinner": "பயிற்சி எடுத்துக்காட்டை உருவாக்குகிறது...",
        "footer": "🛡️ ரக்ஷா — பாதுகாக்கிறது. ஆய்வு செய்கிறது. கற்றுக்கொடுக்கிறது. மூன்று கருவிகளிலும் ஒரே ask_ai() உதவியாளருடன் கட்டமைக்கப்பட்டது.",
    },
    "Kannada": {
        "hero_title": "🛡️ ರಕ್ಷಾ — ಕುಟುಂಬ ಡಿಜಿಟಲ್ ಸುರಕ್ಷತಾ ರಕ್ಷಕ",
        "hero_sub": "ಆನ್‌ಲೈನ್ ವಂಚನೆಯಿಂದ ಕುಟುಂಬಗಳನ್ನು ರಕ್ಷಿಸುತ್ತದೆ — ಸಂಶಯಾಸ್ಪದ ಸಂದೇಶಗಳನ್ನು ಪರಿಶೀಲಿಸುತ್ತದೆ, ಲಿಂಕ್‌ಗಳನ್ನು ಪರಿಶೀಲಿಸುತ್ತದೆ, ವಂಚನೆಯನ್ನು ಗುರುತಿಸಲು ಕಲಿಸುತ್ತದೆ. ನಿಜವಾದ ಕುಟುಂಬಗಳಿಗಾಗಿ ನಿರ್ಮಿಸಲಾಗಿದೆ. ಇಂಗ್ಲಿಷ್, ಹಿಂದಿ, ತೆಲುಗು, ತಮಿಳು, ಕನ್ನಡದಲ್ಲಿ ಲಭ್ಯವಿದೆ.",
        "mission_title": "🛡️ ನಮ್ಮ ಧ್ಯೇಯ",
        "mission_text": "ಪ್ರತಿದಿನ ಸಾವಿರಾರು ಭಾರತೀಯ ಕುಟುಂಬಗಳು ಆನ್‌ಲೈನ್ ವಂಚನೆಯಲ್ಲಿ ಹಣ ಕಳೆದುಕೊಳ್ಳುತ್ತವೆ. ಹಿರಿಯರೇ ಅತಿ ದೊಡ್ಡ ಗುರಿ. ರಕ್ಷಾ ರಕ್ಷಿಸುತ್ತದೆ, ಪರಿಶೀಲಿಸುತ್ತದೆ, ಕುಟುಂಬದ ಸ್ವಂತ ಭಾಷೆಯಲ್ಲಿ ಕಲಿಸುತ್ತದೆ.",
        "lang_label": "🌐 ನಿಮ್ಮ ಭಾಷೆಯನ್ನು ಆರಿಸಿ",
        "lang_caption": "ರಕ್ಷಾ ಈ ಭಾಷೆಯಲ್ಲಿ ಉತ್ತರಿಸುತ್ತದೆ:",
        "why_title": "ರಕ್ಷಾ ಏಕೆ ಗೆಲ್ಲುತ್ತದೆ",
        "why_bullets": "✅ ನಿಜವಾದ ಸಮಸ್ಯೆ, ನಿಜವಾದ ಧ್ಯೇಯ\n\n✅ 1 ಅಲ್ಲ, 3 ಕೆಲಸ ಮಾಡುವ ಸಾಧನಗಳು\n\n✅ 5 ಭಾರತೀಯ ಭಾಷೆಗಳಿಗೆ ಬೆಂಬಲ\n\n✅ ಒಂದೇ ask_ai() ಸಹಾಯಕವನ್ನು ಎಲ್ಲೆಡೆ ಬಳಸಲಾಗಿದೆ",
        "model_caption": "ಮಾದರಿ: llama-3.3-70b-versatile, Groq ಮೂಲಕ",
        "tab1": "📩 ಸಂದೇಶ ಪರಿಶೀಲಕ",
        "tab2": "🔗 ಲಿಂಕ್ ಪರಿಶೀಲಕ",
        "tab3": "🎓 ಕಲಿಯಿರಿ & ರಸಪ್ರಶ್ನೆ",
        "t1_subheader": "ಈ ಸಂದೇಶ ವಂಚನೆಯೇ?",
        "t1_caption": "ನೀವು ಅನುಮಾನಿಸುವ ಯಾವುದೇ SMS, WhatsApp, ಅಥವಾ ಇಮೇಲ್ ಅನ್ನು ಅಂಟಿಸಿ.",
        "t1_placeholder": "ಉದಾ: ಅಭಿನಂದನೆಗಳು! ನೀವು KBC ಲಾಟರಿಯಲ್ಲಿ ರೂ. 10,00,000 ಗೆದ್ದಿದ್ದೀರಿ. ಪಡೆಯಲು ರೂ. 5000 ಶುಲ್ಕ ಕಳುಹಿಸಿ...",
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
        "t2_caption": "ಯಾವುದೇ ಸಂಶಯಾಸ್ಪದ ಲಿಂಕ್ ಅಥವಾ ವೆಬ್‌ಸೈಟ್ ವಿಳಾಸವನ್ನು ಅಂಟಿಸಿ — ನಾವು ಅದನ್ನು ತೆರೆಯುವುದಿಲ್ಲ, ಕೇವಲ ಪರಿಶೀಲಿಸುತ್ತೇವೆ.",
        "t2_placeholder": "ಉದಾ: http://sbi-secure-login.xyz/verify-account",
        "t2_label": "ಸಂಶಯಾಸ್ಪದ ಲಿಂಕ್:",
        "t2_button": "🔍 ಲಿಂಕ್ ಅನ್ನು ಪರಿಶೀಲಿಸಿ",
        "t2_warning": "ದಯವಿಟ್ಟು ಮೊದಲು ಲಿಂಕ್ ಅನ್ನು ಅಂಟಿಸಿ.",
        "t2_spinner": "ಲಿಂಕ್ ಅನ್ನು ಪರಿಶೀಲಿಸುತ್ತಿದೆ...",
        "t3_subheader": "ವಂಚನೆಯನ್ನು ಗುರುತಿಸಲು ಕಲಿಯಿರಿ",
        "t3_caption": "ಅಭ್ಯಾಸ ಉದಾಹರಣೆ ಮತ್ತು ಅದರ ಎಚ್ಚರಿಕೆ ಚಿಹ್ನೆಗಳಿಗಾಗಿ ಬಟನ್ ಒತ್ತಿ.",
        "t3_button": "🎓 ನನಗೆ ಒಂದು ವಂಚನೆ ಉದಾಹರಣೆ ನೀಡಿ",
        "t3_spinner": "ಅಭ್ಯಾಸ ಉದಾಹರಣೆಯನ್ನು ರಚಿಸುತ್ತಿದೆ...",
        "footer": "🛡️ ರಕ್ಷಾ — ರಕ್ಷಿಸುತ್ತದೆ. ಪರಿಶೀಲಿಸುತ್ತದೆ. ಕಲಿಸುತ್ತದೆ. ಮೂರು ಸಾಧನಗಳಲ್ಲೂ ಒಂದೇ ask_ai() ಸಹಾಯಕದೊಂದಿಗೆ ನಿರ್ಮಿಸಲಾಗಿದೆ.",
    },
}

LANGUAGES = ["English", "Hindi", "Telugu", "Tamil", "Kannada"]

# ---------------------------------------------------------
# Feature 3: pre-loaded sample scams (English text; the AI is told to
# translate/explain in the selected language regardless of input language)
# ---------------------------------------------------------
EXAMPLES = {
    "lottery": "Congratulations! Your mobile number has won Rs 25,00,000 in the KBC Lucky Draw 2026. To claim your prize, pay a processing fee of Rs 4,999 via UPI to unlock ID KBC2026 within 24 hours or the prize will be cancelled.",
    "bank": "Dear Customer, your SBI account will be BLOCKED today due to KYC expiry. Update immediately by clicking http://sbi-kyc-verify.xyz and entering your card number, CVV and OTP to avoid suspension.",
    "delivery": "Your Amazon package could not be delivered due to an unpaid customs fee of Rs 49. Click http://indpost-delivery.co to pay now and reschedule delivery, or your parcel will be returned.",
}

# ---------------------------------------------------------
# Language must be picked BEFORE we render anything else
# ---------------------------------------------------------
with st.sidebar:
    lang_label_default = "🌐 Choose your language"
    selected_language = st.selectbox(
        lang_label_default, LANGUAGES, index=0, key="lang_select"
    )
    L = TEXT[selected_language]

# ---------------------------------------------------------
# DESIGN LAYER — light, trustworthy blue-green theme
# ---------------------------------------------------------
st.markdown("""
<style>
.hero {
    background: linear-gradient(90deg, #4F9DF7, #6FC3A0);
    padding: 2.2rem 2rem;
    border-radius: 18px;
    margin-bottom: 1.5rem;
    box-shadow: 0 6px 20px rgba(79, 157, 247, 0.18);
}
.hero h1 {
    color: white; font-size: 2.3rem; margin: 0; font-weight: 800;
    letter-spacing: -0.5px;
}
.hero p {
    color: #eaf6f0; font-size: 1.05rem; margin-top: 0.5rem; margin-bottom: 0;
}
div[data-testid="stTabs"] button {
    font-size: 1.05rem; font-weight: 600; padding: 0.6rem 1.2rem;
}
.result-box {
    background: #F2F5FA;
    border-left: 5px solid #1E63D0;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-top: 1rem;
    color: #1A1A2E;
}
.tally-box {
    background: #EAF6F0;
    border: 1px solid #6FC3A0;
    border-radius: 10px;
    padding: 0.7rem 1rem;
    margin-bottom: 1rem;
    font-weight: 600;
    color: #1A1A2E;
}
.footer-tag {
    text-align: center; color: #6b7280; font-size: 0.85rem;
    margin-top: 2.5rem; padding-top: 1rem;
    border-top: 1px solid #e5e7eb;
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
# SIDEBAR — rest of the sidebar content (below language picker)
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
    # Feature 1: impact tally, always visible in the sidebar too
    st.markdown(
        f'<div class="tally-box">{L["t1_tally"].format(checked=st.session_state.messages_checked, caught=st.session_state.scams_caught)}</div>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs([L["tab1"], L["tab2"], L["tab3"]])

# ---------------------------------------------------------
# PART B — Tab 1: Message Checker
# ---------------------------------------------------------
with tab1:
    st.subheader(L["t1_subheader"])
    st.caption(L["t1_caption"])

    # Feature 1: tally banner at the top of the tab (the judge-facing number)
    st.markdown(
        f'<div class="tally-box">{L["t1_tally"].format(checked=st.session_state.messages_checked, caught=st.session_state.scams_caught)}</div>',
        unsafe_allow_html=True,
    )

    # Feature 3: "Try an example" buttons
    st.markdown(f"**{L['t1_examples_label']}**")
    ex_col1, ex_col2, ex_col3 = st.columns(3)
    with ex_col1:
        if st.button(L["t1_ex_lottery"], use_container_width=True):
            st.session_state.msg = EXAMPLES["lottery"]
            st.rerun()
    with ex_col2:
        if st.button(L["t1_ex_bank"], use_container_width=True):
            st.session_state.msg = EXAMPLES["bank"]
            st.rerun()
    with ex_col3:
        if st.button(L["t1_ex_delivery"], use_container_width=True):
            st.session_state.msg = EXAMPLES["delivery"]
            st.rerun()

    message = st.text_area(
        L["t1_label"], height=160, key="msg",
        placeholder=L["t1_placeholder"]
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        check_clicked = st.button(L["t1_button"], use_container_width=True)

    if check_clicked:
        if not message.strip():
            st.warning(L["t1_warning"])
        else:
            system = (
                "You are Raksha, a scam-detection guardian. Reply as:\n"
                "Verdict: SAFE / SUSPICIOUS / LIKELY SCAM\n"
                "Risk: Low / Medium / High\n"
                "Confidence: a percentage from 0 to 100 showing how sure you are\n"
                "Warning signs: the exact red flags you found\n"
                "What to do: simple advice.\n"
                f"Use very simple, everyday language. Reply entirely in {selected_language}, "
                "regardless of what language the input message is in."
            )
            with st.spinner(L["t1_spinner"]):
                result = ask_ai(system, message)

            verdict = render_verdict(result)

            # Feature 1: update the impact tally
            st.session_state.messages_checked += 1
            if verdict == "SCAM":
                st.session_state.scams_caught += 1

# ---------------------------------------------------------
# PART C — Tab 2: Link Inspector
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
        inspect_clicked = st.button(L["t2_button"], use_container_width=True)

    if inspect_clicked:
        if not link.strip():
            st.warning(L["t2_warning"])
        else:
            system = (
                "You are Raksha, a link-safety guardian. Reply as:\n"
                "Verdict: SAFE / SUSPICIOUS / DANGEROUS\n"
                "Confidence: a percentage from 0 to 100 showing how sure you are\n"
                "Reasons: red flags (fake or lookalike domain, misspelled "
                "brand, strange characters, urgency).\n"
                "Advice: what the person should do.\n"
                "Never tell the user to open the link. "
                f"Use very simple, everyday language. Reply entirely in {selected_language}, "
                "regardless of what language the input link/text is in."
            )
            with st.spinner(L["t2_spinner"]):
                result = ask_ai(system, link)

            render_verdict(result)

# ---------------------------------------------------------
# PART D — Tab 3: Learn & Quiz
# ---------------------------------------------------------
with tab3:
    st.subheader(L["t3_subheader"])
    st.write(L["t3_caption"])

    topics = ["lottery/prize", "fake delivery/OTP", "bank KYC update",
              "job offer", "fake tech support", "UPI refund scam"]

    if st.button(L["t3_button"], use_container_width=False):
        chosen = random.choice(topics)
        system = (
            "You are Raksha, a friendly teacher. Create ONE realistic "
            "scam message that targets Indian families, then list its "
            "red flags in simple points. Keep it short and educational. "
            f"Write the entire example and explanation in {selected_language}."
        )
        with st.spinner(L["t3_spinner"]):
            result = ask_ai(system, f"Give one {chosen} scam example with red flags.")
        st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown(f'<div class="footer-tag">{L["footer"]}</div>', unsafe_allow_html=True)
