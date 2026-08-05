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
# SESSION STATE — impact counters + example-fill flags
# ---------------------------------------------------------
for key, default in {
    "messages_checked": 0,
    "scams_caught": 0,
    "suspicious_caught": 0,
    "links_checked": 0,
    "dangerous_links": 0,
    "calls_checked": 0,
    "spam_calls_caught": 0,
    "example_text": "",
    "last_result": None,
    "last_link_result": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

def parse_verdict(result_text):
    """Pull the Verdict line out of the AI's reply. Returns one of
    SAFE / SUSPICIOUS / SCAM / None."""
    match = re.search(r"Verdict:\s*([A-Za-z /]+)", result_text)
    if not match:
        # Fallback: look for keywords anywhere in the text
        upper = result_text.upper()
        if "LIKELY SCAM" in upper or "DANGEROUS" in upper or "SPAM" in upper:
            return "SCAM"
        if "SUSPICIOUS" in upper:
            return "SUSPICIOUS"
        if "SAFE" in upper or "LEGITIMATE" in upper:
            return "SAFE"
        return None
    verdict_raw = match.group(1).upper().strip()
    if any(k in verdict_raw for k in ["LIKELY SCAM", "SCAM", "DANGEROUS", "SPAM"]):
        return "SCAM"
    if "SUSPICIOUS" in verdict_raw:
        return "SUSPICIOUS"
    if "SAFE" in verdict_raw or "LEGITIMATE" in verdict_raw:
        return "SAFE"
    return None

def parse_confidence(result_text):
    """Pull a 'Confidence: 90%' style line out of the AI's reply."""
    match = re.search(r"Confidence:\s*(\d{1,3})\s*%", result_text)
    if match:
        return min(int(match.group(1)), 100)
    return None

def render_verdict(result_text):
    """Color-coded verdict box: red / yellow / green.
    Plus confidence indicator with colored progress bar."""
    verdict = parse_verdict(result_text)

    # — Color-coded verdict boxes —
    if verdict == "SCAM":
        st.error("🚨 **LIKELY SCAM / SPAM DETECTED**")
        st.markdown(
            f"""<div style="background:#FEE2E2; border-left:5px solid #DC2626;
            border-radius:10px; padding:1.2rem 1.4rem; margin-top:0.5rem;
            color:#991B1B; font-size:1rem; line-height:1.7;">{result_text}</div>""",
            unsafe_allow_html=True,
        )
    elif verdict == "SUSPICIOUS":
        st.warning("⚠️ **SUSPICIOUS — Be Careful**")
        st.markdown(
            f"""<div style="background:#FEF3C7; border-left:5px solid #D97706;
            border-radius:10px; padding:1.2rem 1.4rem; margin-top:0.5rem;
            color:#92400E; font-size:1rem; line-height:1.7;">{result_text}</div>""",
            unsafe_allow_html=True,
        )
    elif verdict == "SAFE":
        st.success("✅ **SAFE — Looks Legitimate**")
        st.markdown(
            f"""<div style="background:#D1FAE5; border-left:5px solid #059669;
            border-radius:10px; padding:1.2rem 1.4rem; margin-top:0.5rem;
            color:#065F46; font-size:1rem; line-height:1.7;">{result_text}</div>""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="result-box">{result_text}</div>',
            unsafe_allow_html=True,
        )

    # — Confidence indicator —
    confidence = parse_confidence(result_text)
    if confidence is not None:
        if verdict == "SCAM":
            conf_color = "#DC2626"
        elif verdict == "SUSPICIOUS":
            conf_color = "#D97706"
        else:
            conf_color = "#059669"
        st.markdown(
            f"""<div style="margin-top:1rem; padding:0.6rem 1rem;
            background:#F8FAFC; border-radius:8px; border:1px solid #E2E8F0;">
            <span style="font-weight:700; font-size:1rem;">🎯 Confidence Level:
            <span style="color:{conf_color}; font-size:1.2rem;">{confidence}%</span></span>
            </div>""",
            unsafe_allow_html=True,
        )
        st.progress(confidence / 100)

    return verdict

# ---------------------------------------------------------
# TRANSLATIONS — every UI string, per language
# ---------------------------------------------------------
TEXT = {
    "English": {
        "hero_title": "🛡️ Raksha — Family Digital Safety Guardian",
        "hero_sub": "Protecting families from online fraud — checks scam messages, inspects suspicious links, verifies spam calls, and teaches people to spot fraud themselves. Built for real families. Works in English, Hindi, Telugu, Tamil, and Kannada.",
        "mission_title": "🛡️ Our Mission",
        "mission_text": "Thousands of Indian families lose money to online scams every day. Elders are the biggest targets. Raksha protects, inspects, and teaches — in the family's own language.",
        "lang_label": "🌐 Choose your language",
        "lang_caption": "Raksha will reply in this language:",
        "why_title": "Why Raksha wins",
        "why_bullets": "✅ Real problem, real mission\n\n✅ 4 working tools, not 1\n\n✅ 5 Indian languages supported\n\n✅ One clean ask_ai() helper reused everywhere",
        "model_caption": "Model: llama-3.3-70b-versatile via Groq",
        "tab1": "📩 Message Checker",
        "tab2": "🔗 Link Inspector",
        "tab3": "📞 Call Verifier",
        "tab4": "🎓 Learn & Quiz",
        "t1_subheader": "Is this message a scam?",
        "t1_caption": "Paste any SMS, WhatsApp, or email you're unsure about.",
        "t1_placeholder": "e.g. Congratulations! You won Rs 10,00,000 in KBC lottery. Pay Rs 5000 fee to claim...",
        "t1_label": "Suspicious message:",
        "t1_button": "🔍 Check Message",
        "t1_warning": "Please paste a message first.",
        "t1_spinner": "Analyzing message...",
        "t1_examples_label": "🚀 Try an example (one click demo!):",
        "t1_ex_lottery": "🎰 Fake Lottery",
        "t1_ex_bank": "🏦 Fake Bank Alert",
        "t1_ex_delivery": "📦 Fake Delivery",
        "t1_tally": "🛡️ {checked} messages checked, {caught} scams caught, {suspicious} suspicious flagged",
        "t1_links_tally": "🔗 {links} links inspected, {dangerous} dangerous found",
        "t2_subheader": "Is this link safe to open?",
        "t2_caption": "Paste any suspicious link or website address — we won't open it, just inspect it.",
        "t2_placeholder": "e.g. http://sbi-secure-login.xyz/verify-account",
        "t2_label": "Suspicious link:",
        "t2_button": "🔍 Inspect Link",
        "t2_warning": "Please paste a link first.",
        "t2_spinner": "Inspecting link...",
        # Tab 3: Call Verifier
        "t3_subheader": "📞 Is this call / number spam?",
        "t3_caption": "Enter a phone number AND describe what the caller said. Raksha will analyze the patterns.",
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
        "t3_calls_tally": "📞 {calls} calls verified, {spam} spam detected",
        # Tab 4: Learn & Quiz
        "t4_subheader": "Learn to spot scams",
        "t4_caption": "Press the button for a practice example and its red flags.",
        "t4_button": "🎓 Give me a scam example",
        "t4_spinner": "Creating a practice example...",
        "footer": "🛡️ Raksha — Protects. Inspects. Verifies. Teaches. Built with one reusable ask_ai() helper across all four tools.",
    },
    "Hindi": {
        "hero_title": "🛡️ रक्षा — पारिवारिक डिजिटल सुरक्षा रक्षक",
        "hero_sub": "ऑनलाइन धोखाधड़ी से परिवारों की सुरक्षा — संदिग्ध संदेशों की जांच, लिंक की जांच, स्पैम कॉल की पहचान, और धोखाधड़ी पहचानना सिखाता है। असली परिवारों के लिए बनाया गया।",
        "mission_title": "🛡️ हमारा मिशन",
        "mission_text": "हर दिन हज़ारों भारतीय परिवार ऑनलाइन धोखाधड़ी में पैसा गंवाते हैं। बुज़ुर्ग सबसे बड़े निशाने पर होते हैं। रक्षा सुरक्षा करता है, जांचता है, और सिखाता है।",
        "lang_label": "🌐 अपनी भाषा चुनें",
        "lang_caption": "रक्षा इस भाषा में जवाब देगा:",
        "why_title": "रक्षा क्यों जीतता है",
        "why_bullets": "✅ असली समस्या, असली मिशन\n\n✅ 4 काम करने वाले टूल\n\n✅ 5 भारतीय भाषाएँ\n\n✅ एक साफ ask_ai() हेल्पर",
        "model_caption": "मॉडल: llama-3.3-70b-versatile, Groq द्वारा",
        "tab1": "📩 संदेश जांचक",
        "tab2": "🔗 लिंक निरीक्षक",
        "tab3": "📞 कॉल सत्यापक",
        "tab4": "🎓 सीखें और प्रश्नोत्तरी",
        "t1_subheader": "क्या यह संदेश धोखाधड़ी है?",
        "t1_caption": "कोई भी संदिग्ध SMS, WhatsApp, या ईमेल यहाँ पेस्ट करें।",
        "t1_placeholder": "जैसे: बधाई हो! आपने KBC लॉटरी में 10,00,000 रुपये जीते हैं...",
        "t1_label": "संदिग्ध संदेश:",
        "t1_button": "🔍 संदेश जांचें",
        "t1_warning": "कृपया पहले एक संदेश पेस्ट करें।",
        "t1_spinner": "संदेश की जांच हो रही है...",
        "t1_examples_label": "🚀 एक उदाहरण आज़माएं:",
        "t1_ex_lottery": "🎰 फर्जी लॉटरी",
        "t1_ex_bank": "🏦 फर्जी बैंक अलर्ट",
        "t1_ex_delivery": "📦 फर्जी डिलीवरी",
        "t1_tally": "🛡️ {checked} संदेश जांचे, {caught} धोखाधड़ी पकड़ी, {suspicious} संदिग्ध",
        "t1_links_tally": "🔗 {links} लिंक जांचे, {dangerous} खतरनाक",
        "t2_subheader": "क्या यह लिंक सुरक्षित है?",
        "t2_caption": "कोई भी संदिग्ध लिंक पेस्ट करें — हम उसे नहीं खोलेंगे।",
        "t2_placeholder": "जैसे: http://sbi-secure-login.xyz/verify-account",
        "t2_label": "संदिग्ध लिंक:",
        "t2_button": "🔍 लिंक जांचें",
        "t2_warning": "कृपया पहले एक लिंक पेस्ट करें।",
        "t2_spinner": "लिंक की जांच हो रही है...",
        "t3_subheader": "📞 क्या यह कॉल स्पैम है?",
        "t3_caption": "फ़ोन नंबर दर्ज करें और बताएं कि कॉलर ने क्या कहा। रक्षा पैटर्न का विश्लेषण करेगा।",
        "t3_number_label": "फ़ोन नंबर:",
        "t3_number_placeholder": "+91 9876543210",
        "t3_context_label": "कॉलर ने क्या कहा? (कॉल का वर्णन करें):",
        "t3_context_placeholder": "जैसे: किसी ने कॉल करके कहा कि वे SBI बैंक से हैं और मेरा खाता ब्लॉक हो जाएगा। उन्होंने OTP और कार्ड डिटेल्स मांगी...",
        "t3_button": "📞 कॉल सत्यापित करें",
        "t3_warning": "कृपया फ़ोन नंबर और कॉल का विवरण दर्ज करें।",
        "t3_spinner": "कॉल पैटर्न का विश्लेषण हो रहा है...",
        "t3_examples_label": "🚀 एक उदाहरण कॉल आज़माएं:",
        "t3_ex_bank_call": "🏦 फर्जी बैंक कॉल",
        "t3_ex_insurance": "📋 फर्जी बीमा",
        "t3_ex_police": "🚔 फर्जी पुलिस/CBI",
        "t3_calls_tally": "📞 {calls} कॉल सत्यापित, {spam} स्पैम पकड़ी",
        "t4_subheader": "धोखाधड़ी पहचानना सीखें",
        "t4_caption": "अभ्यास उदाहरण के लिए बटन दबाएं।",
        "t4_button": "🎓 एक धोखाधड़ी उदाहरण दें",
        "t4_spinner": "अभ्यास उदाहरण बनाया जा रहा है...",
        "footer": "🛡️ रक्षा — सुरक्षा करता है। जांचता है। सत्यापित करता है। सिखाता है।",
    },
    "Telugu": {
        "hero_title": "🛡️ రక్ష — కుటుంబ డిజిటల్ భద్రతా రక్షకుడు",
        "hero_sub": "ఆన్లైన్ మోసాల నుండి కుటుంబాలను రక్షిస్తుంది — సందేశాలు, లింక్లు, స్పామ్ కాల్స్ తనిఖీ చేస్తుంది, మోసాన్ని గుర్తించడం నేర్పిస్తుంది.",
        "mission_title": "🛡️ మా లక్ష్యం",
        "mission_text": "ప్రతిరోజూ వేలాది భారతీయ కుటుంబాలు ఆన్లైన్ మోసాలలో డబ్బు కోల్పోతున్నాయి. వృద్ధులు అత్యధికంగా లక్ష్యంగా ఉంటారు.",
        "lang_label": "🌐 మీ భాషను ఎంచుకోండి",
        "lang_caption": "రక్ష ఈ భాషలో సమాధానం ఇస్తుంది:",
        "why_title": "రక్ష ఎందుకు గెలుస్తుంది",
        "why_bullets": "✅ నిజమైన సమస్య\n\n✅ 4 పనిచేసే సాధనాలు\n\n✅ 5 భాషలు\n\n✅ ఒకే ask_ai() హెల్పర్",
        "model_caption": "మోడల్: llama-3.3-70b-versatile, Groq ద్వారా",
        "tab1": "📩 సందేశ తనిఖీ",
        "tab2": "🔗 లింక్ పరిశీలన",
        "tab3": "📞 కాల్ సత్యాపన",
        "tab4": "🎓 నేర్చుకోండి & క్విజ్",
        "t1_subheader": "ఈ సందేశం మోసమా?",
        "t1_caption": "మీకు అనుమానం ఉన్న SMS, WhatsApp, లేదా ఇమెయిల్ పేస్ట్ చేయండి.",
        "t1_placeholder": "ఉదా: అభినందనలు! KBC లాటరీలో రూ. 10,00,000 గెలుచుకున్నారు...",
        "t1_label": "అనుమానాస్పద సందేశం:",
        "t1_button": "🔍 సందేశాన్ని తనిఖీ చేయండి",
        "t1_warning": "దయచేసి ముందుగా సందేశం పేస్ట్ చేయండి.",
        "t1_spinner": "సందేశాన్ని విశ్లేషిస్తోంది...",
        "t1_examples_label": "🚀 ఒక ఉదాహరణ ప్రయత్నించండి:",
        "t1_ex_lottery": "🎰 నకిలీ లాటరీ",
        "t1_ex_bank": "🏦 నకిలీ బ్యాంక్ అలర్ట్",
        "t1_ex_delivery": "📦 నకిలీ డెలివరీ",
        "t1_tally": "🛡️ {checked} సందేశాలు తనిఖీ, {caught} మోసాలు, {suspicious} అనుమానాస్పదం",
        "t1_links_tally": "🔗 {links} లింక్లు పరిశీలించబడ్డాయి, {dangerous} ప్రమాదకరం",
        "t2_subheader": "ఈ లింక్ సురక్షితమేనా?",
        "t2_caption": "అనుమానాస్పద లింక్ పేస్ట్ చేయండి — మేము తెరవం, పరిశీలిస్తాము.",
        "t2_placeholder": "ఉదా: http://sbi-secure-login.xyz/verify-account",
        "t2_label": "అనుమానాస్పద లింక్:",
        "t2_button": "🔍 లింక్ పరిశీలించండి",
        "t2_warning": "దయచేసి ముందుగా లింక్ పేస్ట్ చేయండి.",
        "t2_spinner": "లింక్ పరిశీలిస్తోంది...",
        "t3_subheader": "📞 ఈ కాల్ స్పామ్ అా?",
        "t3_caption": "ఫోన్ నంబర్ నమోదు చేయండి మరియు కాలర్ ఏమి చెప్పారో వివరించండి.",
        "t3_number_label": "ఫోన్ నంబర్:",
        "t3_number_placeholder": "+91 9876543210",
        "t3_context_label": "కాలర్ ఏమి చెప్పారు? (కాల్ వివరించండి):",
        "t3_context_placeholder": "ఉదా: ఎవరో కాల్ చేసి SBI బ్యాంక్ నుండి అని చెప్పారు, OTP మరియు కార్డ్ వివరాలు అడిగారు...",
        "t3_button": "📞 కాల్ సత్యాపించండి",
        "t3_warning": "దయచేసి ఫోన్ నంబర్ మరియు కాల్ వివరాలు నమోదు చేయండి.",
        "t3_spinner": "కాల్ ప్యాటర్న్ విశ్లేషిస్తోంది...",
        "t3_examples_label": "🚀 ఒక ఉదాహరణ కాల్ ప్రయత్నించండి:",
        "t3_ex_bank_call": "🏦 నకిలీ బ్యాంక్ కాల్",
        "t3_ex_insurance": "📋 నకిలీ బీమా",
        "t3_ex_police": "🚔 నకిలీ పోలీస్/CBI",
        "t3_calls_tally": "📞 {calls} కాల్స్ సత్యాపించబడ్డాయి, {spam} స్పామ్ కనుగొనబడ్డాయి",
        "t4_subheader": "మోసాన్ని గుర్తించడం నేర్చుకోండి",
        "t4_caption": "ప్రాక్టీస్ ఉదాహరణ కోసం బటన్ నొక్కండి.",
        "t4_button": "🎓 మోస ఉదాహరణ ఇవ్వండి",
        "t4_spinner": "ఉదాహరణ సృష్టిస్తోంది...",
        "footer": "🛡️ రక్ష — రక్షిస్తుంది. పరిశీలిస్తుంది. సత్యాపిస్తుంది. నేర్పిస్తుంది.",
    },
    "Tamil": {
        "hero_title": "🛡️ ரக்ஷா — குடும்ப டிஜிட்டல் பாதுகாவலர்",
        "hero_sub": "ஆன்லைன் மோசடியிலிருந்து குடும்பங்களைப் பாதுகாக்கிறது — செய்திகள், இணைப்புகள், ஸ்பேம் அழைப்புகளை சரிபார்க்கிறது, மோசடியை கண்டறிய கற்றுக்கொடுக்கிறது.",
        "mission_title": "🛡️ எங்கள் நோக்கம்",
        "mission_text": "ஒவ்வொரு நாளும் ஆயிரக்கணக்கான இந்திய குடும்பங்கள் ஆன்லைன் மோசடியில் பணத்தை இழக்கின்றன. முதியவர்களே அதிக இலக்கு.",
        "lang_label": "🌐 உங்கள் மொழியைத் தேர்ந்தெடுக்கவும்",
        "lang_caption": "ரக்ஷா இந்த மொழியில் பதிலளிக்கும்:",
        "why_title": "ரக்ஷா ஏன் வெற்றி பெறுகிறது",
        "why_bullets": "✅ உண்மையான பிரச்சனை\n\n✅ 4 செயல்படும் கருவிகள்\n\n✅ 5 மொழிகள்\n\n✅ ஒரே ask_ai() உதவியாளர்",
        "model_caption": "மாடல்: llama-3.3-70b-versatile, Groq மூலம்",
        "tab1": "📩 செய்தி சரிபார்ப்பு",
        "tab2": "🔗 இணைப்பு ஆய்வு",
        "tab3": "📞 அழைப்பு சரிபார்ப்பு",
        "tab4": "🎓 கற்றுக்கொள் & வினாடி வினா",
        "t1_subheader": "இந்த செய்தி மோசடியா?",
        "t1_caption": "சந்தேகிக்கும் எந்த SMS, WhatsApp, மின்னஞ்சலையும் ஒட்டவும்.",
        "t1_placeholder": "எ.கா: வாழ்த்துக்கள்! KBC லாட்டரியில் ரூ. 10,00,000 வென்றுள்ளீர்கள்...",
        "t1_label": "சந்தேகத்திற்குரிய செய்தி:",
        "t1_button": "🔍 செய்தியை சரிபார்க்கவும்",
        "t1_warning": "முதலில் செய்தியை ஒட்டவும்.",
        "t1_spinner": "செய்தியை பகுப்பாய்வு செய்கிறது...",
        "t1_examples_label": "🚀 எடுத்துக்காட்டை முயற்சிக்கவும்:",
        "t1_ex_lottery": "🎰 போலி லாட்டரி",
        "t1_ex_bank": "🏦 போலி வங்கி எச்சரிக்கை",
        "t1_ex_delivery": "📦 போலி டெலிவரி",
        "t1_tally": "🛡️ {checked} செய்திகள் சரிபார்க்கப்பட்டன, {caught} மோசடிகள், {suspicious} சந்தேகமானவை",
        "t1_links_tally": "🔗 {links} இணைப்புகள் ஆய்வு, {dangerous} ஆபத்தானவை",
        "t2_subheader": "இந்த இணைப்பு பாதுகாப்பானதா?",
        "t2_caption": "சந்தேகத்திற்குரிய இணைப்பை ஒட்டவும் — திறக்க மாட்டோம்.",
        "t2_placeholder": "எ.கா: http://sbi-secure-login.xyz/verify-account",
        "t2_label": "சந்தேகத்திற்குரிய இணைப்பு:",
        "t2_button": "🔍 இணைப்பை ஆய்வு செய்யவும்",
        "t2_warning": "முதலில் இணைப்பை ஒட்டவும்.",
        "t2_spinner": "இணைப்பை ஆய்வு செய்கிறது...",
        "t3_subheader": "📞 இந்த அழைப்பு ஸ்பேமா?",
        "t3_caption": "தொலைபேசி எண்ணை உள்ளிடவும் மற்றும் அழைப்பாளர் என்ன சொன்னார் என்பதை விவரிக்கவும்.",
        "t3_number_label": "தொலைபேசி எண்:",
        "t3_number_placeholder": "+91 9876543210",
        "t3_context_label": "அழைப்பாளர் என்ன சொன்னார்? (அழைப்பை விவரிக்கவும்):",
        "t3_context_placeholder": "எ.கா: SBI வங்கியிலிருந்து அழைப்பு என்று சொல்லி OTP கேட்டார்கள்...",
        "t3_button": "📞 அழைப்பை சரிபார்க்கவும்",
        "t3_warning": "தொலைபேசி எண் மற்றும் அழைப்பு விவரங்களை உள்ளிடவும்.",
        "t3_spinner": "அழைப்பு முறையை பகுப்பாய்வு செய்கிறது...",
        "t3_examples_label": "🚀 ஒரு எடுத்துக்காட்டு அழைப்பை முயற்சிக்கவும்:",
        "t3_ex_bank_call": "🏦 போலி வங்கி அழைப்பு",
        "t3_ex_insurance": "📋 போலி காப்பீடு",
        "t3_ex_police": "🚔 போலி காவல்/CBI",
        "t3_calls_tally": "📞 {calls} அழைப்புகள் சரிபார்க்கப்பட்டன, {spam} ஸ்பேம் கண்டறியப்பட்டன",
        "t4_subheader": "மோசடியை கண்டறிய கற்றுக்கொள்ளுங்கள்",
        "t4_caption": "பயிற்சி எடுத்துக்காட்டுக்கு பொத்தானை அழுத்தவும்.",
        "t4_button": "🎓 மோசடி எடுத்துக்காட்டு கொடுங்கள்",
        "t4_spinner": "எடுத்துக்காட்டை உருவாக்குகிறது...",
        "footer": "🛡️ ரக்ஷா — பாதுகாக்கிறது. ஆய்வு செய்கிறது. சரிபார்க்கிறது. கற்றுக்கொடுக்கிறது.",
    },
    "Kannada": {
        "hero_title": "🛡️ ರಕ್ಷಾ — ಕುಟುಂಬ ಡಿಜಿಟಲ್ ಸುರಕ್ಷತಾ ರಕ್ಷಕ",
        "hero_sub": "ಆನ್ಲೈನ್ ವಂಚನೆಯಿಂದ ಕುಟುಂಬಗಳನ್ನು ರಕ್ಷಿಸುತ್ತದೆ — ಸಂದೇಶಗಳು, ಲಿಂಕ್ಗಳು, ಸ್ಪ್ಯಾಮ್ ಕಾಲ್ಗಳನ್ನು ಪರಿಶೀಲಿಸುತ್ತದೆ, ವಂಚನೆಯನ್ನು ಗುರುತಿಸಲು ಕಲಿಸುತ್ತದೆ.",
        "mission_title": "🛡️ ನಮ್ಮ ಧ್ಯೇಯ",
        "mission_text": "ಪ್ರತಿದಿನ ಸಾವಿರಾರು ಭಾರತೀಯ ಕುಟುಂಬಗಳು ಆನ್ಲೈನ್ ವಂಚನೆಯಲ್ಲಿ ಹಣ ಕಳೆದುಕೊಳ್ಳುತ್ತವೆ. ಹಿರಿಯರೇ ಅತಿ ದೊಡ್ಡ ಗುರಿ.",
        "lang_label": "🌐 ನಿಮ್ಮ ಭಾಷೆ ಆರಿಸಿ",
        "lang_caption": "ರಕ್ಷಾ ಈ ಭಾಷೆಯಲ್ಲಿ ಉತ್ತರಿಸುತ್ತದೆ:",
        "why_title": "ರಕ್ಷಾ ಏಕೆ ಗೆಲ್ಲುತ್ತದೆ",
        "why_bullets": "✅ ನಿಜವಾದ ಸಮಸ್ಯೆ\n\n✅ 4 ಸಾಧನಗಳು\n\n✅ 5 ಭಾಷೆಗಳು\n\n✅ ಒಂದೇ ask_ai() ಸಹಾಯಕ",
        "model_caption": "ಮಾದರಿ: llama-3.3-70b-versatile, Groq ಮೂಲಕ",
        "tab1": "📩 ಸಂದೇಶ ಪರಿಶೀಲಕ",
        "tab2": "🔗 ಲಿಂಕ್ ಪರಿಶೀಲಕ",
        "tab3": "📞 ಕಾಲ್ ಪರಿಶೀಲಕ",
        "tab4": "🎓 ಕಲಿಯಿರಿ & ರಸಪ್ರಶ್ನೆ",
        "t1_subheader": "ಈ ಸಂದೇಶ ವಂಚನೆಯೇ?",
        "t1_caption": "ಅನುಮಾನಿಸುವ SMS, WhatsApp, ಇಮೇಲ್ ಅಂಟಿಸಿ.",
        "t1_placeholder": "ಉದಾ: KBC ಲಾಟರಿಯಲ್ಲಿ ರೂ. 10,00,000 ಗೆದ್ದಿದ್ದೀರಿ...",
        "t1_label": "ಸಂಶಯಾಸ್ಪದ ಸಂದೇಶ:",
        "t1_button": "🔍 ಸಂದೇಶ ಪರಿಶೀಲಿಸಿ",
        "t1_warning": "ಮೊದಲು ಸಂದೇಶ ಅಂಟಿಸಿ.",
        "t1_spinner": "ಸಂದೇಶ ವಿಶ್ಲೇಷಿಸುತ್ತಿದೆ...",
        "t1_examples_label": "🚀 ಉದಾಹರಣೆ ಪ್ರಯತ್ನಿಸಿ:",
        "t1_ex_lottery": "🎰 ನಕಲಿ ಲಾಟರಿ",
        "t1_ex_bank": "🏦 ನಕಲಿ ಬ್ಯಾಂಕ್ ಎಚ್ಚರಿಕೆ",
        "t1_ex_delivery": "📦 ನಕಲಿ ಡೆಲಿವರಿ",
        "t1_tally": "🛡️ {checked} ಸಂದೇಶಗಳು ಪರಿಶೀಲಿಸಲಾಗಿದೆ, {caught} ವಂಚನೆಗಳು, {suspicious} ಸಂಶಯಾಸ್ಪದ",
        "t1_links_tally": "🔗 {links} ಲಿಂಕ್ಗಳು ಪರಿಶೀಲಿಸಲಾಗಿದೆ, {dangerous} ಅಪಾಯಕಾರಿ",
        "t2_subheader": "ಈ ಲಿಂಕ್ ಸುರಕ್ಷಿತವೇ?",
        "t2_caption": "ಸಂಶಯಾಸ್ಪದ ಲಿಂಕ್ ಅಂಟಿಸಿ — ತೆರೆಯುವುದಿಲ್ಲ, ಪರಿಶೀಲಿಸುತ್ತೇವೆ.",
        "t2_placeholder": "ಉದಾ: http://sbi-secure-login.xyz/verify-account",
        "t2_label": "ಸಂಶಯಾಸ್ಪದ ಲಿಂಕ್:",
        "t2_button": "🔍 ಲಿಂಕ್ ಪರಿಶೀಲಿಸಿ",
        "t2_warning": "ಮೊದಲು ಲಿಂಕ್ ಅಂಟಿಸಿ.",
        "t2_spinner": "ಲಿಂಕ್ ಪರಿಶೀಲಿಸುತ್ತಿದೆ...",
        "t3_subheader": "📞 ಈ ಕಾಲ್ ಸ್ಪ್ಯಾಮ್ ಆಗಿದೆಯೇ?",
        "t3_caption": "ಫೋನ್ ನಂಬರ್ ನಮೂದಿಸಿ ಮತ್ತು ಕಾಲರ್ ಏನು ಹೇಳಿದರು ಎಂದು ವಿವರಿಸಿ.",
        "t3_number_label": "ಫೋನ್ ನಂಬರ್:",
        "t3_number_placeholder": "+91 9876543210",
        "t3_context_label": "ಕಾಲರ್ ಏನು ಹೇಳಿದರು? (ಕಾಲ್ ವಿವರಿಸಿ):",
        "t3_context_placeholder": "ಉದಾ: SBI ಬ್ಯಾಂಕ್ನಿಂದ ಎಂದು ಕಾಲ್ ಮಾಡಿ OTP ಕೇಳಿದರು...",
        "t3_button": "📞 ಕಾಲ್ ಪರಿಶೀಲಿಸಿ",
        "t3_warning": "ಫೋನ್ ನಂಬರ್ ಮತ್ತು ಕಾಲ್ ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ.",
        "t3_spinner": "ಕಾಲ್ ಪ್ಯಾಟರ್ನ್ ವಿಶ್ಲೇಷಿಸುತ್ತಿದೆ...",
        "t3_examples_label": "🚀 ಉದಾಹರಣೆ ಕಾಲ್ ಪ್ರಯತ್ನಿಸಿ:",
        "t3_ex_bank_call": "🏦 ನಕಲಿ ಬ್ಯಾಂಕ್ ಕಾಲ್",
        "t3_ex_insurance": "📋 ನಕಲಿ ವಿಮೆ",
        "t3_ex_police": "🚔 ನಕಲಿ ಪೊಲೀಸ್/CBI",
        "t3_calls_tally": "📞 {calls} ಕಾಲ್ಗಳು ಪರಿಶೀಲಿಸಲಾಗಿದೆ, {spam} ಸ್ಪ್ಯಾಮ್ ಪತ್ತೆ",
        "t4_subheader": "ವಂಚನೆಯನ್ನು ಗುರುತಿಸಲು ಕಲಿಯಿರಿ",
        "t4_caption": "ಅಭ್ಯಾಸ ಉದಾಹರಣೆಗಾಗಿ ಬಟನ್ ಒತ್ತಿ.",
        "t4_button": "🎓 ವಂಚನೆ ಉದಾಹರಣೆ ನೀಡಿ",
        "t4_spinner": "ಉದಾಹರಣೆ ರಚಿಸುತ್ತಿದೆ...",
        "footer": "🛡️ ರಕ್ಷಾ — ರಕ್ಷಿಸುತ್ತದೆ. ಪರಿಶೀಲಿಸುತ್ತದೆ. ಸತ್ಯಾಪಿಸುತ್ತದೆ. ಕಲಿಸುತ್ತದೆ.",
    },
}

LANGUAGES = ["English", "Hindi", "Telugu", "Tamil", "Kannada"]

# ---------------------------------------------------------
# Pre-loaded sample scams
# ---------------------------------------------------------
EXAMPLES = {
    "lottery": "Congratulations! Your mobile number has won Rs 25,00,000 in the KBC Lucky Draw 2026. To claim your prize, pay a processing fee of Rs 4,999 via UPI to unlock ID KBC2026 within 24 hours or the prize will be cancelled.",
    "bank": "Dear Customer, your SBI account will be BLOCKED today due to KYC expiry. Update immediately by clicking http://sbi-kyc-verify.xyz and entering your card number, CVV and OTP to avoid suspension.",
    "delivery": "Your Amazon package could not be delivered due to an unpaid customs fee of Rs 49. Click http://indpost-delivery.co to pay now and reschedule delivery, or your parcel will be returned.",
}

# Pre-loaded sample spam calls
CALL_EXAMPLES = {
    "bank_call": {
        "number": "+91 8800123456",
        "context": "Someone called saying they are from SBI Bank's fraud department. They said my account has been compromised and I need to immediately share my OTP and debit card CVV number to 'secure' my account. They said if I don't do it in 10 minutes, all my money will be stolen. They were very aggressive and didn't let me hang up.",
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
# Language picker FIRST
# ---------------------------------------------------------
with st.sidebar:
    lang_label_default = "🌐 Choose your language"
    selected_language = st.selectbox(
        lang_label_default, LANGUAGES, index=0, key="lang_select"
    )
    L = TEXT[selected_language]

# ---------------------------------------------------------
# DESIGN LAYER
# ---------------------------------------------------------
st.markdown("""
<style>
.hero {
    background: linear-gradient(135deg, #1E3A5F 0%, #2D6A4F 50%, #40916C 100%);
    padding: 2.5rem 2rem;
    border-radius: 18px;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(30, 58, 95, 0.25);
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero h1 {
    color: white; font-size: 2.3rem; margin: 0; font-weight: 800;
    letter-spacing: -0.5px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.hero p {
    color: #D8F3DC; font-size: 1.05rem; margin-top: 0.5rem; margin-bottom: 0;
}
div[data-testid="stTabs"] button {
    font-size: 1.05rem; font-weight: 600; padding: 0.6rem 1.2rem;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    border-bottom: 3px solid #2D6A4F;
    color: #1E3A5F;
}
.result-box {
    background: #F2F5FA;
    border-left: 5px solid #1E63D0;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-top: 1rem;
    color: #1A1A2E;
    line-height: 1.7;
}
.tally-box {
    background: linear-gradient(135deg, #D8F3DC, #B7E4C7);
    border: 1px solid #40916C;
    border-radius: 12px;
    padding: 0.8rem 1.2rem;
    margin-bottom: 1rem;
    font-weight: 600;
    color: #1B4332;
    box-shadow: 0 2px 8px rgba(45, 106, 79, 0.15);
}
.stats-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.8rem;
    margin-bottom: 1rem;
}
.stat-card {
    background: white;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    border: 1px solid #E2E8F0;
}
.stat-card .number {
    font-size: 1.8rem;
    font-weight: 800;
    color: #1E3A5F;
}
.stat-card .label {
    font-size: 0.8rem;
    color: #64748B;
    margin-top: 0.2rem;
}
.call-info-box {
    background: linear-gradient(135deg, #EEF2FF, #E0E7FF);
    border-left: 5px solid #6366F1;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}
.call-info-box h4 { color: #4338CA; margin: 0 0 0.5rem 0; }
.call-info-box p { color: #3730A3; margin: 0.2rem 0; font-size: 0.95rem; }
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

    # Impact dashboard in sidebar
    st.markdown("### 📊 Impact Dashboard")
    total_checks = (st.session_state.messages_checked
                    + st.session_state.links_checked
                    + st.session_state.calls_checked)
    total_threats = (st.session_state.scams_caught
                     + st.session_state.dangerous_links
                     + st.session_state.spam_calls_caught)
    st.markdown(
        f"""<div class="stats-grid">
            <div class="stat-card">
                <div class="number">{total_checks}</div>
                <div class="label">Total Checks</div>
            </div>
            <div class="stat-card">
                <div class="number" style="color:#DC2626;">{total_threats}</div>
                <div class="label">Threats Found</div>
            </div>
            <div class="stat-card">
                <div class="number" style="color:#D97706;">{st.session_state.suspicious_caught}</div>
                <div class="label">Suspicious</div>
            </div>
            <div class="stat-card">
                <div class="number" style="color:#6366F1;">{st.session_state.calls_checked}</div>
                <div class="label">Calls Verified</div>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# TABS  (now 4!)
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([L["tab1"], L["tab2"], L["tab3"], L["tab4"]])

# ---------------------------------------------------------
# Tab 1: Message Checker
# ---------------------------------------------------------
with tab1:
    st.subheader(L["t1_subheader"])
    st.caption(L["t1_caption"])

    # Tally banner
    if st.session_state.messages_checked > 0:
        st.markdown(
            f'<div class="tally-box">{L["t1_tally"].format(checked=st.session_state.messages_checked, caught=st.session_state.scams_caught, suspicious=st.session_state.suspicious_caught)}</div>',
            unsafe_allow_html=True,
        )

    # "Try an example" buttons
    st.markdown(f"**{L['t1_examples_label']}**")
    ex_col1, ex_col2, ex_col3 = st.columns(3)
    with ex_col1:
        if st.button(L["t1_ex_lottery"], use_container_width=True, key="ex_lottery"):
            st.session_state.example_text = EXAMPLES["lottery"]
    with ex_col2:
        if st.button(L["t1_ex_bank"], use_container_width=True, key="ex_bank"):
            st.session_state.example_text = EXAMPLES["bank"]
    with ex_col3:
        if st.button(L["t1_ex_delivery"], use_container_width=True, key="ex_delivery"):
            st.session_state.example_text = EXAMPLES["delivery"]

    default_msg = st.session_state.get("example_text", "")

    message = st.text_area(
        L["t1_label"], height=160, key="msg_input",
        placeholder=L["t1_placeholder"],
        value=default_msg,
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        check_clicked = st.button(L["t1_button"], use_container_width=True, type="primary")

    if check_clicked:
        if not message.strip():
            st.warning(L["t1_warning"])
        else:
            system = (
                "You are Raksha, a scam-detection guardian for Indian families. "
                "Analyze the message and reply EXACTLY in this format:\n\n"
                "Verdict: SAFE / SUSPICIOUS / LIKELY SCAM\n"
                "Risk: Low / Medium / High\n"
                "Confidence: <number>%\n"
                "Warning signs: <list the exact red flags you found>\n"
                "What to do: <simple advice>\n\n"
                "IMPORTANT: Always include the Confidence line with a percentage. "
                f"Use very simple, everyday language. Reply entirely in {selected_language}."
            )
            with st.spinner(L["t1_spinner"]):
                result = ask_ai(system, message)

            verdict = render_verdict(result)

            st.session_state.messages_checked += 1
            if verdict == "SCAM":
                st.session_state.scams_caught += 1
            elif verdict == "SUSPICIOUS":
                st.session_state.suspicious_caught += 1

            st.session_state.example_text = ""

# ---------------------------------------------------------
# Tab 2: Link Inspector
# ---------------------------------------------------------
with tab2:
    st.subheader(L["t2_subheader"])
    st.caption(L["t2_caption"])

    if st.session_state.links_checked > 0:
        st.markdown(
            f'<div class="tally-box">{L["t1_links_tally"].format(links=st.session_state.links_checked, dangerous=st.session_state.dangerous_links)}</div>',
            unsafe_allow_html=True,
        )

    link = st.text_area(
        L["t2_label"], height=100, key="link_input",
        placeholder=L["t2_placeholder"]
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        inspect_clicked = st.button(L["t2_button"], use_container_width=True, type="primary")

    if inspect_clicked:
        if not link.strip():
            st.warning(L["t2_warning"])
        else:
            system = (
                "You are Raksha, a link-safety guardian for Indian families. "
                "Analyze the link and reply EXACTLY in this format:\n\n"
                "Verdict: SAFE / SUSPICIOUS / DANGEROUS\n"
                "Confidence: <number>%\n"
                "Reasons: <red flags like fake/lookalike domain, misspelled "
                "brand, strange characters, urgency>\n"
                "Advice: <what the person should do>\n\n"
                "IMPORTANT: Always include the Confidence line with a percentage. "
                "Never tell the user to open the link. "
                f"Use very simple, everyday language. Reply entirely in {selected_language}."
            )
            with st.spinner(L["t2_spinner"]):
                result = ask_ai(system, link)

            verdict = render_verdict(result)

            st.session_state.links_checked += 1
            if verdict == "SCAM":
                st.session_state.dangerous_links += 1

# ---------------------------------------------------------
# Tab 3: Call Verifier / Number Checker  <<
