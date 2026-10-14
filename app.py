
import re
from pathlib import Path

import joblib
import streamlit as st
import streamlit.components.v1 as components

# ==================================================
# PAGE CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="TrustCheck AI | Scam Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

MODEL_PATH = Path(__file__).parent / "models" / "fake_job_detector.pkl"

# ==================================================
# RESPONSIVE DESIGN AND ANIMATIONS
# ==================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html {
        scroll-behavior: smooth;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(145deg, #f7f9ff, #eef4ff 55%, #f8faff);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    @keyframes fadeSlideUp {
        from {
            opacity: 0;
            transform: translateY(22px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes progressGlow {
        0% { filter: brightness(1); }
        50% { filter: brightness(1.2); }
        100% { filter: brightness(1); }
    }

    .hero {
        background: linear-gradient(125deg, #111b3c, #244b91 65%, #3979d7);
        color: white;
        padding: 34px;
        border-radius: 24px;
        margin-bottom: 24px;
        box-shadow: 0 15px 35px rgba(25, 57, 115, 0.16);
        animation: fadeSlideUp 0.65s ease-out both;
    }

    .hero h1 {
        font-size: clamp(28px, 4vw, 43px);
        line-height: 1.15;
        margin: 12px 0;
        color: white;
        font-weight: 800;
    }

    .hero p {
        color: #dce8ff;
        font-size: 16px;
        line-height: 1.7;
        max-width: 700px;
    }

    .eyebrow {
        display: inline-block;
        background: rgba(255,255,255,.14);
        border: 1px solid rgba(255,255,255,.24);
        border-radius: 30px;
        padding: 7px 12px;
        font-size: 12px;
        letter-spacing: 1px;
        font-weight: 700;
    }

    .section-card {
        background: white;
        padding: 22px;
        border: 1px solid #e2e9f5;
        border-radius: 20px;
        box-shadow: 0 6px 24px rgba(33, 60, 110, 0.05);
        margin-bottom: 18px;
        animation: fadeSlideUp 0.5s ease-out both;
        transition: box-shadow 0.25s ease;
    }

    .section-card:hover {
        box-shadow: 0 10px 28px rgba(33, 60, 110, 0.09);
    }

    .section-card h3 {
        color: #17264a;
        margin-top: 0;
    }

    .feature {
        background: white;
        padding: 18px;
        border: 1px solid #e2e9f5;
        border-radius: 16px;
        min-height: 125px;
        margin-bottom: 10px;
        animation: fadeSlideUp 0.6s ease-out both;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }

    .feature:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 28px rgba(33, 60, 110, 0.12);
    }

    .feature-icon {
        font-size: 25px;
    }

    .feature h4 {
        margin: 8px 0 5px 0;
        color: #17264a;
    }

    .feature p {
        font-size: 13px;
        color: #66738a;
        line-height: 1.6;
    }

    .result-card {
        padding: 25px;
        border-radius: 20px;
        background: white;
        border: 1px solid #e2e9f5;
        margin-top: 18px;
        scroll-margin-top: 30px;
        animation: fadeSlideUp 0.65s ease-out both;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }

    .result-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 28px rgba(33, 60, 110, 0.10);
    }

    .risk-high {
        background: #fff0f0;
        border-left: 6px solid #dc2626;
    }

    .risk-medium {
        background: #fff8e8;
        border-left: 6px solid #d97706;
    }

    .risk-low {
        background: #eafaf1;
        border-left: 6px solid #159447;
    }

    .small-note {
        color: #64748b;
        font-size: 12px;
        line-height: 1.6;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        border-radius: 12px;
        min-height: 48px;
        font-weight: 700;
        border: 0;
        background: linear-gradient(110deg, #2454b7, #397ce4);
        color: white;
        width: 100%;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 7px 18px rgba(37, 99, 235, 0.20);
    }

    div[data-testid="stTextArea"] textarea {
        border-radius: 13px;
        border: 1px solid #d7e1f0;
        background: #fbfdff;
        font-size: 15px;
        line-height: 1.65;
    }

    div[data-testid="stTextArea"] textarea:focus {
        border-color: #397ce4;
        box-shadow: 0 0 0 2px #dbeafe;
    }

    div[data-testid="stProgress"] > div > div {
        transition: width 1s ease-in-out;
        animation: progressGlow 1.4s ease-in-out;
    }

    div[data-testid="stRadio"] > div {
        gap: 12px;
    }

    @media (max-width: 640px) {
        .block-container {
            padding: 1rem 0.8rem 2rem 0.8rem;
        }

        .hero {
            padding: 23px 18px;
            border-radius: 18px;
        }

        .section-card {
            padding: 16px;
        }

        .result-card {
            padding: 18px;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
            scroll-behavior: auto !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==================================================
# MODEL LOADING
# ==================================================
@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)


# ==================================================
# WARNING SIGN RULES
# ==================================================
JOB_RULES = [
    (
        "Requests an upfront fee",
        r"\b(registration fee|security fee|application fee|"
        r"joining fee|pay to get (?:the )?job|processing fee|"
        r"training fee|pay .*?to secure)\b",
        24,
    ),
    (
        "Requests banking or payment details",
        r"\b(bank account details|credit card details|"
        r"send money|transfer money|payment details|"
        r"share your otp|one.time password)\b",
        25,
    ),
    (
        "Requests sensitive identity information",
        r"\b(aadhaar|aadhar|pan card|passport number|"
        r"social security number)\b",
        15,
    ),
    (
        "Pushes communication to WhatsApp",
        r"\b(whatsapp only|contact us on whatsapp|"
        r"message us on whatsapp)\b",
        10,
    ),
    (
        "Promises guaranteed selection",
        r"\b(guaranteed (?:job|selection|employment)|"
        r"100% placement guaranteed|no interview required)\b",
        18,
    ),
    (
        "Uses urgency or pressure",
        r"\b(act immediately|limited vacancies|"
        r"apply immediately|urgent hiring|"
        r"offer expires today|hurry up)\b",
        8,
    ),
]

MESSAGE_RULES = [
    (
        "Requests an upfront payment",
        r"\b(pay now|send money|processing fee|"
        r"claim fee|release fee|prize fee|"
        r"pay to receive|transfer money)\b",
        25,
    ),
    (
        "Requests OTPs, passwords, or banking details",
        r"\b(share your otp|send otp|verify your otp|"
        r"password|bank details|card number|"
        r"cvv|pin number|account credentials)\b",
        25,
    ),
    (
        "Contains a web link",
        r"(https?://|www\.)",
        12,
    ),
    (
        "Promises a prize or unexpected reward",
        r"\b(you have won|you won|claim your prize|"
        r"lucky winner|free gift|lottery winner|"
        r"won a lottery|cash prize)\b",
        18,
    ),
    (
        "Uses urgent account warnings",
        r"\b(account blocked|account suspended|"
        r"account will be closed|verify immediately|"
        r"action required immediately|"
        r"your account is locked)\b",
        18,
    ),
    (
        "Makes unrealistic money or job promises",
        r"\b(easy money|earn money instantly|"
        r"guaranteed returns|double your money|"
        r"work from home earn|no experience high salary)\b",
        15,
    ),
    (
        "Pressures you to act quickly",
        r"\b(act now|limited time|urgent response|"
        r"expires today|last chance|hurry)\b",
        8,
    ),
    (
        "Uses a shortened web link",
        r"\b(?:bit\.ly|tinyurl\.com|t\.co|"
        r"cutt\.ly|is\.gd)/\S+",
        15,
    ),
]


def find_flags(text, rules):
    flags = []
    total = 0

    for label, pattern, weight in rules:
        if re.search(pattern, text, re.IGNORECASE):
            flags.append(label)
            total += weight

    return flags, min(total, 100)


def risk_details(score):
    if score >= 60:
        return (
            "HIGH RISK",
            "risk-high",
            "Do not proceed until independently verified.",
        )
    elif score >= 30:
        return (
            "CAUTION",
            "risk-medium",
            "Check the details carefully before responding.",
        )
    return (
        "LOWER DETECTED RISK",
        "risk-low",
        "No strong warning pattern was detected.",
    )


# ==================================================
# HEADER
# ==================================================
st.markdown(
    """
    <div class="hero">
        <span class="eyebrow">🛡️ AI-POWERED SAFETY TOOL</span>
        <h1>TrustCheck AI</h1>
        <p>
            Check suspicious job advertisements and messages in seconds.
            Identify warning signs, understand potential risks, and make
            safer decisions before you click, reply, or share information.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==================================================
# FEATURE CARDS
# ==================================================
feature1, feature2, feature3 = st.columns(3)

with feature1:
    st.markdown(
        """
        <div class="feature">
            <div class="feature-icon">💼</div>
            <h4>Fake Job Detector</h4>
            <p>Analyze job and internship descriptions using your trained ML model.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with feature2:
    st.markdown(
        """
        <div class="feature">
            <div class="feature-icon">📩</div>
            <h4>Spam Message Detector</h4>
            <p>Check suspicious SMS, WhatsApp messages, emails, and scam texts.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with feature3:
    st.markdown(
        """
        <div class="feature">
            <div class="feature-icon">🔎</div>
            <h4>Warning Sign Report</h4>
            <p>See detected warning patterns and practical safety recommendations.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("")

# ==================================================
# DETECTOR SELECTION
# ==================================================
st.markdown("### Choose what you want to check")

mode = st.radio(
    "Detection mode",
    ["💼 Job Advertisement", "📩 Spam / Fake Message"],
    horizontal=True,
    label_visibility="collapsed",
)

if mode == "💼 Job Advertisement":
    heading = "Analyze a job or internship"
    description = (
        "Paste the complete job advertisement below. "
        "You do not need to enter a job title or company name separately."
    )
    placeholder = (
        "Paste the complete job advertisement here...\n\n"
        "Include the description, requirements, salary, application process, "
        "and any payment requests if available."
    )
    rules = JOB_RULES
else:
    heading = "Check a suspicious message"
    description = (
        "Paste an SMS, WhatsApp message, email, or other text you want to check."
    )
    placeholder = (
        "Paste the suspicious message here...\n\n"
        "Example: Congratulations! You have won a prize. "
        "Pay a processing fee to claim your reward."
    )
    rules = MESSAGE_RULES

st.markdown(
    f"""
    <div class="section-card">
        <h3>{heading}</h3>
        <p style="color:#64748b; line-height:1.7;">{description}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==================================================
# INPUT FORM
# ==================================================
with st.form("detector_form"):
    text_to_check = st.text_area(
        "Paste text",
        placeholder=placeholder,
        height=230,
        label_visibility="collapsed",
        max_chars=30000,
    )

    submitted = st.form_submit_button("🔍 Analyze for Scam Risk")

# ==================================================
# ANALYSIS
# ==================================================
if submitted:
    if len(text_to_check.strip()) < 10:
        st.warning("Please paste a longer job advertisement or message to analyze.")

    else:
        flags, rule_score = find_flags(text_to_check, rules)

        ml_probability = None
        model_prediction = None
        model_available = False

        # Job advertisements use the trained ML model.
        if mode == "💼 Job Advertisement":
            try:
                model = load_model()

                if model is not None:
                    probabilities = model.predict_proba([text_to_check])[0]
                    classes = list(
                        model.named_steps["classifier"].classes_
                    )
                    fraud_index = classes.index(1)

                    ml_probability = float(
                        probabilities[fraud_index]
                    ) * 100

                    model_prediction = int(
                        model.predict([text_to_check])[0]
                    )
                    model_available = True

                else:
                    st.warning(
                        "The trained job model was not found. "
                        "Showing rule-based warning checks only."
                    )

            except Exception as error:
                st.warning(
                    "The machine-learning model could not be loaded. "
                    "Showing rule-based warning checks only."
                )

                with st.expander("Technical details"):
                    st.code(str(error))

        # Combine ML output and rules for job advertisements.
        # This score is a heuristic, not a calibrated probability.
        if mode == "💼 Job Advertisement" and model_available:
            risk_score = round(
                min(100, 0.75 * ml_probability + 0.25 * rule_score)
            )
        else:
            risk_score = rule_score

        risk_label, risk_class, recommendation = risk_details(risk_score)

        # Anchor and automatic smooth scrolling.
        st.markdown(
            '<div id="analysis-results"></div>',
            unsafe_allow_html=True,
        )

        components.html(
            """
            <script>
            function scrollToAnalysis() {
                const parentDocument = window.parent.document;
                const target = parentDocument.getElementById(
                    "analysis-results"
                );

                if (target) {
                    target.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });
                }
            }

            setTimeout(scrollToAnalysis, 300);
            setTimeout(scrollToAnalysis, 700);
            </script>
            """,
            height=0,
        )

        st.markdown("---")
        st.markdown("## Analysis results")
        st.caption(
            "✨ Analysis complete — review your results below."
        )

        left, right = st.columns([1, 1.3], gap="large")

        with left:
            st.markdown(
                f"""
                <div class="result-card {risk_class}">
                    <p style="margin:0; color:#526078;">
                        Overall assessment
                    </p>
                    <h2 style="margin:8px 0; color:#17264a;">
                        {risk_label}
                    </h2>
                    <p style="margin:0;">
                        Risk indicator: <b>{risk_score}/100</b>
                    </p>
                    <p style="margin-top:12px;">
                        {recommendation}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.progress(risk_score / 100)

            st.caption(
                "This score is a screening indicator, not a verified "
                "probability that the content is fraudulent."
            )

        with right:
            st.markdown("### 🚩 Detected warning signs")

            if flags:
                for flag in flags:
                    st.markdown(f"- ⚠️ {flag}")
            else:
                st.success(
                    "No warning patterns from the current checks were detected."
                )

            if mode == "💼 Job Advertisement" and model_available:
                st.markdown("### 🤖 Machine-learning assessment")

                st.metric(
                    "Model-estimated fraud score",
                    f"{ml_probability:.1f}%",
                )

                if model_prediction == 1:
                    st.write(
                        "The model classified this advertisement as "
                        "potentially fraudulent."
                    )
                else:
                    st.write(
                        "The model classified this advertisement as "
                        "likely legitimate."
                    )

        st.markdown(
            """
            <div class="section-card">
                <h3>🔐 Recommended safety actions</h3>
                <ul>
                    <li>Never pay money to secure a job or claim an unexpected prize.</li>
                    <li>Never share OTPs, passwords, or sensitive banking details.</li>
                    <li>Verify employers using their independently located official website.</li>
                    <li>Do not click suspicious links or download unexpected attachments.</li>
                    <li>Be cautious of urgent demands, unrealistic rewards, and guaranteed offers.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("How this assessment works"):
            if mode == "💼 Job Advertisement" and model_available:
                st.write(
                    "The job detector combines a trained TF-IDF and "
                    "Logistic Regression model with keyword-based warning checks. "
                    "The displayed risk indicator is a heuristic combination, "
                    "not a calibrated probability."
                )

            elif mode == "💼 Job Advertisement":
                st.write(
                    "Only the keyword-based warning checks ran because "
                    "the trained model was unavailable."
                )

            else:
                st.write(
                    "The message detector uses keyword and pattern-based "
                    "checks. It does not yet use a separately trained SMS spam "
                    "classification model, so it can miss scams or flag "
                    "legitimate messages."
                )

        st.caption(
            "Important: This tool provides an initial screening only. "
            "A low score does not prove that a job or message is safe."
        )

# ==================================================
# FOOTER
# ==================================================
st.markdown("---")
st.markdown(
    """
    <p style="text-align:center; color:#718096; font-size:12px;">
        TrustCheck AI · Fake Job & Spam Message Detection<br>
        Built with Python, Streamlit, scikit-learn and rule-based checks
    </p>
    """,
    unsafe_allow_html=True,
)
