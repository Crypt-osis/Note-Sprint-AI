import streamlit as st
import time
from ai_utils import generate_study_pack
from file_utils import extract_text_from_txt, extract_text_from_pdf
from pdf_utils import create_pdf

st.set_page_config(
    page_title="NoteSprint AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  THEME STATE
# ─────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"

IS_DARK = st.session_state["theme"] == "dark"

# ─────────────────────────────────────────────
#  THEME TOKENS
# ─────────────────────────────────────────────
if IS_DARK:
    BG_MAIN          ="linear-gradient(315deg, #04010F, #302B38)"
    BLOB_1           = "#3b82f6"
    BLOB_2           = "#8b5cf6"
    TEXT             = "#ffffff"
    SUBTEXT          = "#d1d5db"
    CARD_BG          = "rgba(255,255,255,0.055)"
    CARD_BORDER      = "rgba(255,255,255,0.1)"
    CARD_SHADOW      = "0 12px 30px rgba(0,0,0,0.14)"
    CARD_HOVER_SH    = "0 18px 40px rgba(0,0,0,0.2)"
    HERO_BG1         = "rgba(59,130,246,0.25)"
    HERO_BG2         = "rgba(168,85,247,0.22)"
    HERO_GLASS       = "rgba(255,255,255,0.07)"
    HERO_GLASS2      = "rgba(255,255,255,0.03)"
    HERO_BORDER      = "rgba(255,255,255,0.12)"
    FLASH_BG1        = "rgba(59,130,246,0.18)"
    FLASH_BG2        = "rgba(168,85,247,0.16)"
    FLASH_BASE       = "rgba(255,255,255,0.05)"
    FLASH_BORDER     = "rgba(255,255,255,0.1)"
    QUIZ_BG          = "rgba(255,255,255,0.05)"
    UPLOAD_BG        = "rgba(255,255,255,0.035)"
    UPLOAD_BORDER    = "rgba(255,255,255,0.16)"
    TAB_LIST_BG      = "rgba(255,255,255,0.035)"
    TAB_LIST_BORDER  = "rgba(255,255,255,0.08)"
    TAB_ACTIVE       = "linear-gradient(90deg,rgba(59,130,246,0.22),rgba(139,92,246,0.22))"
    METRIC_BG        = "rgba(255,255,255,0.06)"
    METRIC_BORDER    = "rgba(255,255,255,0.08)"
    SECTION_TITLE    = "#ffffff"
    SHINE            = "rgba(255,255,255,0.08)"
    SHINE_HERO       = "rgba(255,255,255,0.14)"
    WRAPPER_BG       = "rgba(255,255,255,0.055)"
    WRAPPER_BORDER   = "rgba(255,255,255,0.1)"
    ANSWER_COLOR     = "#22c55e"
else:
    BG_MAIN          = "linear-gradient(135deg, #e8f0fe, #f3e8ff)"
    BLOB_1           = "#93c5fd"
    BLOB_2           = "#c4b5fd"
    TEXT             = "#0f172a"
    SUBTEXT          = "#374151"
    CARD_BG          = "rgba(255,255,255,0.85)"
    CARD_BORDER      = "rgba(99,102,241,0.22)"
    CARD_SHADOW      = "0 8px 24px rgba(99,102,241,0.10)"
    CARD_HOVER_SH    = "0 16px 36px rgba(99,102,241,0.20)"
    HERO_BG1         = "rgba(59,130,246,0.14)"
    HERO_BG2         = "rgba(168,85,247,0.12)"
    HERO_GLASS       = "rgba(255,255,255,0.60)"
    HERO_GLASS2      = "rgba(255,255,255,0.40)"
    HERO_BORDER      = "rgba(99,102,241,0.22)"
    FLASH_BG1        = "rgba(59,130,246,0.10)"
    FLASH_BG2        = "rgba(168,85,247,0.09)"
    FLASH_BASE       = "rgba(255,255,255,0.88)"
    FLASH_BORDER     = "rgba(99,102,241,0.22)"
    QUIZ_BG          = "rgba(255,255,255,0.78)"
    UPLOAD_BG        = "rgba(255,255,255,0.68)"
    UPLOAD_BORDER    = "rgba(99,102,241,0.28)"
    TAB_LIST_BG      = "rgba(255,255,255,0.68)"
    TAB_LIST_BORDER  = "rgba(99,102,241,0.18)"
    TAB_ACTIVE       = "linear-gradient(90deg,rgba(59,130,246,0.18),rgba(139,92,246,0.18))"
    METRIC_BG        = "rgba(255,255,255,0.85)"
    METRIC_BORDER    = "rgba(99,102,241,0.22)"
    SECTION_TITLE    = "#1e1b4b"
    SHINE            = "rgba(255,255,255,0.55)"
    SHINE_HERO       = "rgba(255,255,255,0.65)"
    WRAPPER_BG       = "rgba(255,255,255,0.85)"
    WRAPPER_BORDER   = "rgba(99,102,241,0.22)"
    ANSWER_COLOR     = "#16a34a"

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
    .stApp {{
        background: {BG_MAIN} !important;
        color: {TEXT} !important;
        overflow-x: hidden;
    }}
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
        animation: pageFade 0.9s ease;
    }}

    .stApp::before, .stApp::after {{
        content: "";
        position: fixed;
        width: 380px; height: 380px;
        border-radius: 999px;
        filter: blur(90px);
        z-index: -1;
        opacity: 0.25;
        pointer-events: none;
        animation: floatBlob 12s ease-in-out infinite;
    }}
    .stApp::before {{ background: {BLOB_1}; top: -80px; left: -100px; }}
    .stApp::after  {{ background: {BLOB_2}; bottom: -100px; right: -80px; animation-delay: 3s; }}

    .hero {{
        position: relative; overflow: hidden;
        padding: 2.4rem 2.2rem 2rem;
        border-radius: 28px;
        background:
            radial-gradient(circle at top left, {HERO_BG1}, transparent 35%),
            radial-gradient(circle at bottom right, {HERO_BG2}, transparent 35%),
            linear-gradient(135deg, {HERO_GLASS}, {HERO_GLASS2});
        border: 1px solid {HERO_BORDER};
        box-shadow: 0 18px 50px rgba(0,0,0,0.12);
        margin-bottom: 1.7rem;
        animation: fadeInUp 0.9s ease, pulseGlow 4s infinite ease-in-out, floatSoft 6s ease-in-out infinite;
        backdrop-filter: blur(14px);
    }}
    .hero::before {{
        content: "";
        position: absolute; top: 0; left: -120%;
        width: 40%; height: 100%;
        background: linear-gradient(120deg, transparent, {SHINE_HERO}, transparent);
        animation: shineSweep 4.5s infinite linear;
    }}
    .hero h1 {{
        font-size: 2.7rem; margin-bottom: 0.55rem;
        font-weight: 900; letter-spacing: -0.5px;
        background: linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6, #60a5fa);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 6s ease infinite;
    }}
    .hero p {{ font-size: 1.06rem; color: {SUBTEXT}; margin-bottom: 0.2rem; }}

    .section-title {{
        font-size: 1.55rem; font-weight: 800;
        margin-bottom: 1rem; color: {SECTION_TITLE};
        animation: fadeInUp 0.8s ease;
    }}

    .custom-card {{
        position: relative; overflow: hidden;
        background: {CARD_BG};
        border: 1px solid {CARD_BORDER};
        border-radius: 20px; padding: 1.4rem 1.6rem; margin-bottom: 1rem;
        box-shadow: {CARD_SHADOW};
        animation: fadeInUp 0.75s ease;
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
        backdrop-filter: blur(12px);
        color: {TEXT};
    }}
    .custom-card:hover {{
        transform: translateY(-6px) scale(1.015);
        box-shadow: {CARD_HOVER_SH};
        border-color: rgba(96,165,250,0.4);
    }}
    .custom-card::before {{
        content: "";
        position: absolute; top: 0; left: -120%;
        width: 40%; height: 100%;
        background: linear-gradient(120deg, transparent, {SHINE}, transparent);
        animation: shineSweep 5s infinite linear;
    }}
    .custom-card h3 {{ font-size: 1.15rem; font-weight: 800; margin-bottom: 0.75rem; color: {TEXT}; }}
    .custom-card ul {{ padding-left: 1.2rem; margin: 0; color: {SUBTEXT}; line-height: 2; }}
    .custom-card p {{ color: {SUBTEXT}; margin: 0; line-height: 1.7; }}

    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: {WRAPPER_BG} !important;
        border: 1px solid {WRAPPER_BORDER} !important;
        border-radius: 20px !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: {CARD_SHADOW} !important;
        padding: 1rem !important;
        transition: transform 0.25s ease, box-shadow 0.25s ease !important;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
        transform: translateY(-4px) scale(1.008) !important;
        box-shadow: {CARD_HOVER_SH} !important;
        border-color: rgba(96,165,250,0.35) !important;
    }}

    /* ===== CYBERPUNK INPUT ===== */
    div[data-testid="stTextArea"] label p {{
        font-size: 0px !important;
        margin-bottom: 0 !important;
    }}
    .cyber-label {{
        display: inline-block;
        margin-bottom: 10px;
        padding: 6px 14px;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 700;
        color: #c4b5fd;
        background: rgba(139, 92, 246, 0.12);
        border: 1px solid rgba(168, 85, 247, 0.35);
        box-shadow: 0 0 12px rgba(168,85,247,0.18);
        letter-spacing: 0.4px;
        animation: floatGlow 2.8s ease-in-out infinite;
    }}
    .cyber-chips {{
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-bottom: 12px;
    }}
    .cyber-chip {{
        padding: 8px 14px;
        border-radius: 999px;
        background: rgba(255,255,255,0.05);
        color: rgba(255,255,255,0.88);
        font-size: 13px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 0 10px rgba(168,85,247,0.08);
    }}
    div[data-testid="stTextArea"] {{
        position: relative;
        border-radius: 26px;
        padding: 2px;
        background: linear-gradient(135deg, rgba(59,130,246,0.95), rgba(168,85,247,0.95), rgba(236,72,153,0.95));
        box-shadow: 0 0 14px rgba(139,92,246,0.35), 0 0 32px rgba(59,130,246,0.18);
        animation: neonPulse 3s ease-in-out infinite;
        overflow: hidden;
        margin-top: 6px;
    }}
    div[data-testid="stTextArea"] > div {{
        background: rgba(15, 23, 42, 0.92) !important;
        backdrop-filter: blur(18px);
        border-radius: 24px !important;
        padding: 18px !important;
    }}
    div[data-testid="stTextArea"] textarea {{
        background: transparent !important;
        color: #ffffff !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        font-size: 15px !important;
        line-height: 1.8 !important;
        border-radius: 18px !important;
        min-height: 280px !important;
        resize: vertical !important;
        padding: 10px 4px 10px 4px !important;
        caret-color: #a855f7 !important;
        font-family: "Inter", sans-serif !important;
    }}
    div[data-testid="stTextArea"] textarea::placeholder {{
        color: rgba(255,255,255,0.42) !important;
        font-size: 14px !important;
        line-height: 1.7 !important;
    }}
    div[data-testid="stTextArea"]:has(textarea:focus) {{
        box-shadow: 0 0 18px rgba(168,85,247,0.55), 0 0 38px rgba(59,130,246,0.22), 0 0 60px rgba(236,72,153,0.12);
        transform: translateY(-2px) scale(1.005);
        transition: all 0.25s ease;
    }}
    div[data-testid="stTextArea"] textarea::-webkit-scrollbar {{ width: 8px; }}
    div[data-testid="stTextArea"] textarea::-webkit-scrollbar-track {{ background: rgba(255,255,255,0.04); border-radius: 999px; }}
    div[data-testid="stTextArea"] textarea::-webkit-scrollbar-thumb {{ background: linear-gradient(180deg, #3b82f6, #a855f7, #ec4899); border-radius: 999px; }}
    .cyber-helper {{
        margin-top: 10px;
        font-size: 13px;
        color: rgba(255,255,255,0.55);
        padding-left: 4px;
    }}

    .flashcard, .summary-card, .keyterm-card {{
        background: radial-gradient(circle at top left, {FLASH_BG1}, transparent 35%), radial-gradient(circle at bottom right, {FLASH_BG2}, transparent 35%), {FLASH_BASE};
        border: 1px solid {FLASH_BORDER};
        border-radius: 24px; padding: 1.35rem; margin-bottom: 1rem;
        box-shadow: 0 14px 34px rgba(0,0,0,0.10);
        animation: fadeInUp 0.8s ease;
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
        transform-style: preserve-3d; backdrop-filter: blur(12px);
    }}
    .flashcard:hover, .summary-card:hover, .keyterm-card:hover {{
        transform: perspective(1000px) rotateX(4deg) rotateY(-4deg) translateY(-6px) scale(1.015);
        box-shadow: 0 22px 45px rgba(59,130,246,0.22);
        border-color: rgba(139,92,246,0.35);
    }}
    .flashcard-title {{ font-size: 1.4rem; font-weight: 800; margin-bottom: 0.8rem; color: {TEXT}; }}
    .summary-card h3 {{
        font-size: 1.2rem; font-weight: 800; margin-bottom: 0.75rem;
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }}
    .summary-card ul {{ padding-left: 1.2rem; margin: 0; color: {SUBTEXT}; line-height: 2; }}
    .keyterm-card h3 {{
        font-size: 1.15rem; font-weight: 800; margin-bottom: 0.6rem;
        background: linear-gradient(90deg, #a78bfa, #f472b6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }}
    .keyterm-card p {{ color: {SUBTEXT}; margin: 0; line-height: 1.7; }}

    .quiz-box {{
        background: {QUIZ_BG};
        border-left: 4px solid #60a5fa;
        padding: 1rem; border-radius: 16px; margin-bottom: 1rem;
        box-shadow: 0 8px 22px rgba(0,0,0,0.08);
        animation: fadeInUp 0.7s ease;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        color: {TEXT};
    }}
    .quiz-box:hover {{ transform: translateX(4px); box-shadow: 0 14px 28px rgba(59,130,246,0.16); }}
    .answer-box {{
        background: rgba(34,197,94,0.12);
        border: 1px solid rgba(34,197,94,0.25);
        padding: 0.7rem 0.9rem; border-radius: 14px; margin-top: 0.7rem;
        color: {ANSWER_COLOR}; font-weight: 700;
        animation: fadeInUp 0.4s ease;
    }}

    .stButton > button {{
        width: 100%; border-radius: 16px; height: 3.3em;
        font-size: 1rem; font-weight: 800; border: none;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899, #3b82f6);
        background-size: 250% 250%; color: white;
        box-shadow: 0 10px 24px rgba(59,130,246,0.28);
        animation: gradientShift 6s ease infinite, pulseGlow 2.8s infinite ease-in-out;
        transition: transform 0.16s ease, box-shadow 0.16s ease, filter 0.16s ease;
    }}
    .stButton > button:hover {{ transform: translateY(-3px) scale(1.015); box-shadow: 0 16px 32px rgba(139,92,246,0.35); filter: brightness(1.05); }}
    .stButton > button:active {{ transform: scale(0.985); }}

    .stDownloadButton > button {{
        width: 100%; border-radius: 16px; height: 3em;
        font-size: 1rem; font-weight: 800; border: none;
        background: linear-gradient(90deg, #10b981, #14b8a6, #06b6d4, #10b981);
        background-size: 250% 250%; color: white;
        box-shadow: 0 10px 24px rgba(16,185,129,0.24);
        animation: gradientShift 7s ease infinite, floatSoft 4s ease-in-out infinite;
    }}

    section[data-testid="stSidebar"] {{
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(18px) saturate(180%);
        -webkit-backdrop-filter: blur(18px) saturate(180%);
        border-right: 1px solid rgba(255, 255, 255, 0.14) !important;
        box-shadow: 8px 0 32px rgba(31, 38, 135, 0.18);
        position: relative;
        overflow: hidden;
    }}
    section[data-testid="stSidebar"]::before {{
        content: "";
        position: absolute;
        top: 0; left: -120%;
        width: 60%; height: 100%;
        background: linear-gradient(120deg, transparent, rgba(255,255,255,0.12), transparent);
        animation: sidebarShine 6s linear infinite;
        pointer-events: none;
    }}
    section[data-testid="stSidebar"] * {{ color: {TEXT} !important; }}

    section[data-testid="stFileUploader"] {{
        background: {UPLOAD_BG};
        border-radius: 18px; padding: 1rem;
        border: 1px dashed {UPLOAD_BORDER};
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        animation: fadeInUp 0.8s ease;
    }}
    section[data-testid="stFileUploader"]:hover {{ transform: translateY(-3px); box-shadow: 0 14px 30px rgba(59,130,246,0.12); }}

    [data-testid="metric-container"] {{
        background: {METRIC_BG};
        border: 1px solid {METRIC_BORDER};
        padding: 1rem; border-radius: 18px;
        box-shadow: {CARD_SHADOW};
        animation: fadeInUp 0.7s ease; backdrop-filter: blur(10px);
        color: {TEXT} !important;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px; background: {TAB_LIST_BG}; padding: 0.5rem;
        border-radius: 18px; border: 1px solid {TAB_LIST_BORDER};
        margin-bottom: 1rem; animation: fadeInUp 0.8s ease;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 14px !important; padding: 0.7rem 1rem !important;
        transition: all 0.22s ease !important; color: {TEXT} !important;
    }}
    .stTabs [aria-selected="true"] {{
        background: {TAB_ACTIVE} !important;
        box-shadow: 0 8px 22px rgba(59,130,246,0.14);
        transform: translateY(-2px);
    }}

    [data-testid="stProgressBar"] > div > div > div {{
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899) !important;
        background-size: 250% 250%;
        animation: gradientShift 4s ease infinite;
        border-radius: 999px;
    }}

    .stApp, .stApp p, .stApp label, .stApp span,
    .stApp div, .stApp h1, .stApp h2, .stApp h3,
    .stApp h4, .stApp h5, .stApp h6 {{ color: {TEXT}; }}

    a[href^="#"], h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {{ display: none !important; }}
    [data-testid="stMarkdownContainer"] a {{ text-decoration: none !important; }}

    @keyframes pageFade   {{ from {{ opacity:0; transform:translateY(8px); }} to {{ opacity:1; transform:translateY(0); }} }}
    @keyframes fadeInUp   {{ from {{ opacity:0; transform:translateY(18px); }} to {{ opacity:1; transform:translateY(0); }} }}
    @keyframes floatSoft  {{ 0%,100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-5px); }} }}
    @keyframes floatBlob  {{ 0%,100% {{ transform:translate(0,0) scale(1); }} 50% {{ transform:translate(30px,-20px) scale(1.08); }} }}
    @keyframes pulseGlow  {{ 0%,100% {{ box-shadow: 0 0 0px rgba(139,92,246,0), 0 0 0px rgba(59,130,246,0); }} 50% {{ box-shadow: 0 0 28px rgba(139,92,246,.35), 0 0 36px rgba(59,130,246,.22); }} }}
    @keyframes gradientShift {{ 0% {{ background-position:0% 50%; }} 50% {{ background-position:100% 50%; }} 100% {{ background-position:0% 50%; }} }}
    @keyframes shineSweep    {{ 0% {{ transform:translateX(-120%); }} 100% {{ transform:translateX(220%); }} }}
    @keyframes neonPulse {{ 0% {{ box-shadow: 0 0 14px rgba(139,92,246,0.35), 0 0 32px rgba(59,130,246,0.18); }} 50% {{ box-shadow: 0 0 18px rgba(168,85,247,0.55), 0 0 42px rgba(236,72,153,0.20); }} 100% {{ box-shadow: 0 0 14px rgba(139,92,246,0.35), 0 0 32px rgba(59,130,246,0.18); }} }}
    @keyframes floatGlow {{ 0% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-2px); }} 100% {{ transform: translateY(0px); }} }}
    @keyframes sidebarShine {{ 0% {{ transform:translateX(-120%); }} 100% {{ transform:translateX(260%); }} }}
</style>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<div class="hero">
    <h1>📚 NoteSprint AI</h1>
    <p>Turn messy notes into clean summaries, flashcards, quizzes, and revision PDFs in seconds.</p>
    <p style="margin-top:0.6rem; font-size:0.95rem; opacity:0.85;">
        ⚡ Fast • 🎯 Smart • 🧠 Student-focused
    </p>
</div>
""", unsafe_allow_html=True)

# SIDEBAR
st.sidebar.title("⚙️ Settings")

toggle_label = "☀️ Light Mode" if IS_DARK else "🌙 Dark Mode"
if st.sidebar.button(toggle_label, use_container_width=True):
    st.session_state["theme"] = "light" if IS_DARK else "dark"
    st.rerun()

st.sidebar.markdown("---")
difficulty = st.sidebar.segmented_control("Quiz Difficulty", ["Easy", "Medium", "Hard"], default="Medium")
num_questions = st.sidebar.slider("Number of Questions", 5, 100, 10, step=5)
show_answers = st.sidebar.toggle("Show Answers by Default", value=False)
st.sidebar.markdown("---")
st.sidebar.caption("Tip: Use clean lecture notes or textbook text for best results.")

# MAIN WORKSPACE
st.markdown('<div class="section-title">📥 Input Your Study Material</div>', unsafe_allow_html=True)
left, right = st.columns([2.2, 1], gap="large")
user_text = ""

with left:
    with st.container(border=True):
        input_method = st.radio("Choose input method:", ["Paste Text", "Upload File"], horizontal=True)

        if input_method == "Paste Text":
            st.markdown("""
            <div class="cyber-chips">
                <div class="cyber-chip">⚡ AI-ready</div>
                <div class="cyber-chip">📚 Notes / Textbook / Lecture</div>
                <div class="cyber-chip">🧠 Best for revision</div>
            </div>
            <div class="cyber-label">✍️ Smart Notes Input</div>
            """, unsafe_allow_html=True)

            user_text = st.text_area(
                "notes_input_hidden_label",
                placeholder="Paste your class notes, textbook chapter, lecture summary, or study material here...\n\nExample:\n• Photosynthesis process\n• Important definitions\n• Key exam concepts\n• Formulas / diagrams explained",
                height=320,
                key="notes_input"
            )

            st.markdown("""
            <div class="cyber-helper">
            💡 Tip: Cleaner and longer notes = better summaries, flashcards, and quizzes.
            </div>
            """, unsafe_allow_html=True)
        else:
            uploaded_file = st.file_uploader("Upload a TXT or PDF file", type=["txt", "pdf"])
            if uploaded_file:
                if uploaded_file.type == "text/plain":
                    user_text = extract_text_from_txt(uploaded_file)
                elif uploaded_file.type == "application/pdf":
                    user_text = extract_text_from_pdf(uploaded_file)
                if user_text:
                    st.success("File uploaded and text extracted successfully!")
                    with st.expander("Preview Extracted Text"):
                        st.write(user_text[:3000])

        st.markdown("""
        <div style="margin-top: 18px; margin-bottom: 12px; font-size: 1.15rem; font-weight: 800; color: white; letter-spacing: 0.3px;">
        ⚡ Generate your AI Study Pack
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Generate Study Pack", use_container_width=True):
            if not user_text.strip():
                st.warning("Please provide some study material first.")
            else:
                st.markdown("""
                <div class="custom-card" style="text-align:center; padding:1rem;">
                    <h4 style="margin-bottom:0.4rem;">🤖 AI is building your study pack...</h4>
                    <p>Summaries • Flashcards • Quiz • PDF</p>
                </div>
                """, unsafe_allow_html=True)

                progress = st.progress(0, text="Starting AI generation...")
                try:
                    time.sleep(0.4); progress.progress(20, text="📚 Reading and understanding notes...")
                    time.sleep(0.8); progress.progress(45, text="📝 Creating structured summary...")
                    time.sleep(0.8); progress.progress(70, text="📖 Extracting key terms...")
                    time.sleep(0.8); progress.progress(85, text="❓ Generating quiz questions...")

                    result = generate_study_pack(user_text, difficulty, num_questions)

                    progress.progress(100, text="✅ Study pack ready!")
                    time.sleep(0.5); progress.empty()

                    st.session_state["result"] = result
                    st.success("Study pack generated successfully!")
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

with right:
    st.markdown("""
    <div class="custom-card">
        <h3>🔗 What this app does</h3>
        <ul>
            <li>Summarises long notes</li>
            <li>Extracts key terms</li>
            <li>Creates flashcards</li>
            <li>Generates MCQ quizzes</li>
            <li>Exports revision PDF</li>
        </ul>
    </div>
    <div class="custom-card">
        <h3>🎯 Best for</h3>
        <ul>
            <li>Exam revision</li>
            <li>Last-minute prep</li>
            <li>Lecture notes</li>
            <li>Quick self-testing</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# RESULTS
if "result" in st.session_state:
    result = st.session_state["result"]
    if not result:
        st.stop()

    st.markdown("---")
    st.markdown('<div class="section-title">📊 Your Generated Study Pack</div>', unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    with m1: st.metric("Summary Sections", len(result.get("summary", [])))
    with m2: st.metric("Key Terms", len(result.get("keyTerms", [])))
    with m3: st.metric("Quiz Questions", len(result.get("quiz", [])))

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Summary", "📖 Key Terms", "🃏 Flashcards", "❓ Quiz", "📄 Export"])

    with tab1:
        for section in result.get("summary", []):
            st.markdown(f"""
            <div class="summary-card">
                <h3>{section['heading']}</h3>
                <ul>{''.join(f"<li>{p}</li>" for p in section['points'])}</ul>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        key_terms = result.get("keyTerms", [])
        if key_terms:
            cols = st.columns(2)
            for i, item in enumerate(key_terms):
                with cols[i % 2]:
                    st.markdown(f"""
                    <div class="keyterm-card">
                        <h3>{item['term']}</h3>
                        <p>{item['definition']}</p>
                    </div>
                    """, unsafe_allow_html=True)

    with tab3:
        st.markdown("### 🃏 Flashcard Revision Mode")
        st.write("Test yourself by revealing each definition only after you think of the answer.")
        key_terms = result.get("keyTerms", [])
        if key_terms:
            cols = st.columns(2)
            for i, item in enumerate(key_terms):
                with cols[i % 2]:
                    st.markdown(f"""
                    <div class="flashcard">
                        <div class="flashcard-title">{item['term']}</div>
                        <p style="opacity:0.7;">Think of the definition before revealing it.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Reveal Answer — {item['term']}", key=f"flash_{i}"):
                        st.success(item["definition"])

    with tab4:
        st.markdown("### 🧠 Test Yourself")
        for i, q in enumerate(result.get("quiz", []), start=1):
            st.markdown(f"""
            <div class="quiz-box"><h4>Q{i}. {q['question']}</h4></div>
            """, unsafe_allow_html=True)

            selected = st.radio(f"Q{i}", q["options"], key=f"quiz_{i}", label_visibility="collapsed")

            if st.button(f"Check Answer for Q{i}", key=f"check_{i}"):
                if selected == q["answer"]:
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Incorrect. Correct answer: {q['answer']}")

            if show_answers:
                st.markdown(f'<div class="answer-box">✅ Answer: {q["answer"]}</div>', unsafe_allow_html=True)

            st.markdown("")

    with tab5:
        st.markdown("### 📄 Export Your Study Pack")
        st.write("Download your AI-generated revision notes as a PDF for offline study.")
        pdf_file = create_pdf(result)
        st.download_button(
            label="📥 Download Revision PDF",
            data=pdf_file,
            file_name="study_pack.pdf",
            mime="application/pdf"
        )
        st.info("Tip: Download this PDF before your exam for quick revision.")
