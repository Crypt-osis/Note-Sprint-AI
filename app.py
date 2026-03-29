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

bg_main = "linear-gradient(135deg, #0f172a, #111827)"
text_color = "white"
subtext_color = "#d1d5db"
card_bg = "rgba(255,255,255,0.06)"
sidebar_bg = "rgba(15,23,42,0.95)"

st.markdown(f"""
<style>
    .stApp {{
        background: {bg_main};
        color: {text_color};
        overflow-x: hidden;
    }}

    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
        animation: pageFade 0.9s ease;
    }}

    .stApp::before,
    .stApp::after {{
        content: "";
        position: fixed;
        width: 380px;
        height: 380px;
        border-radius: 999px;
        filter: blur(90px);
        z-index: -1;
        opacity: 0.22;
        pointer-events: none;
        animation: floatBlob 12s ease-in-out infinite;
    }}

    .stApp::before {{
        background: #3b82f6;
        top: -80px;
        left: -100px;
    }}

    .stApp::after {{
        background: #8b5cf6;
        bottom: -100px;
        right: -80px;
        animation-delay: 3s;
    }}

    .hero {{
        position: relative;
        overflow: hidden;
        padding: 2.4rem 2.2rem 2rem 2.2rem;
        border-radius: 28px;
        background:
            radial-gradient(circle at top left, rgba(59,130,246,0.25), transparent 35%),
            radial-gradient(circle at bottom right, rgba(168,85,247,0.22), transparent 35%),
            linear-gradient(135deg, rgba(255,255,255,0.07), rgba(255,255,255,0.03));
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 18px 50px rgba(0,0,0,0.22);
        margin-bottom: 1.7rem;
        animation: fadeInUp 0.9s ease, pulseGlow 4s infinite ease-in-out, floatSoft 6s ease-in-out infinite;
        backdrop-filter: blur(14px);
    }}

    .hero::before {{
        content: "";
        position: absolute;
        top: 0;
        left: -120%;
        width: 40%;
        height: 100%;
        background: linear-gradient(120deg, transparent, rgba(255,255,255,0.14), transparent);
        animation: shineSweep 4.5s infinite linear;
    }}

    .hero h1 {{
        font-size: 2.7rem;
        margin-bottom: 0.55rem;
        font-weight: 900;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6, #60a5fa);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 6s ease infinite;
    }}

    .hero p {{
        font-size: 1.06rem;
        color: {subtext_color};
        margin-bottom: 0.2rem;
        animation: fadeInUp 1.1s ease;
    }}

    .section-title {{
        font-size: 1.55rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: {text_color};
        animation: fadeInUp 0.8s ease;
    }}

    .custom-card {{
        position: relative;
        overflow: hidden;
        background: rgba(255,255,255,0.055);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        box-shadow: 0 12px 30px rgba(0,0,0,0.14);
        animation: fadeInUp 0.75s ease;
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
        backdrop-filter: blur(12px);
        color: {text_color};
    }}

    .custom-card:hover {{
        transform: translateY(-6px) scale(1.015);
        box-shadow: 0 18px 40px rgba(0,0,0,0.2);
        border-color: rgba(96,165,250,0.35);
    }}

    .custom-card::before {{
        content: "";
        position: absolute;
        top: 0;
        left: -120%;
        width: 40%;
        height: 100%;
        background: linear-gradient(120deg, transparent, rgba(255,255,255,0.08), transparent);
        animation: shineSweep 5s infinite linear;
    }}

    .custom-card h3 {{
        font-size: 1.15rem;
        font-weight: 800;
        margin-bottom: 0.75rem;
        color: {text_color};
    }}

    .custom-card ul {{
        padding-left: 1.2rem;
        margin: 0;
        color: {subtext_color};
        line-height: 2;
    }}

    .custom-card ul li {{
        margin-bottom: 0.2rem;
    }}

    .custom-card p {{
        color: {subtext_color};
        margin: 0;
        line-height: 1.7;
    }}

    /* ---- LEFT COLUMN CONTAINER (wraps Streamlit widgets) ---- */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: rgba(255,255,255,0.055) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 20px !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: 0 12px 30px rgba(0,0,0,0.14) !important;
        padding: 1rem !important;
        transition: transform 0.25s ease, box-shadow 0.25s ease !important;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
        transform: translateY(-4px) scale(1.008) !important;
        box-shadow: 0 18px 40px rgba(0,0,0,0.2) !important;
        border-color: rgba(96,165,250,0.35) !important;
    }}

    .flashcard {{
        background:
            radial-gradient(circle at top left, rgba(59,130,246,0.18), transparent 35%),
            radial-gradient(circle at bottom right, rgba(168,85,247,0.16), transparent 35%),
            rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 24px;
        padding: 1.35rem;
        margin-bottom: 1rem;
        min-height: 180px;
        box-shadow: 0 14px 34px rgba(0,0,0,0.16);
        animation: fadeInUp 0.8s ease;
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
        transform-style: preserve-3d;
        backdrop-filter: blur(12px);
    }}

    .flashcard:hover {{
        transform: perspective(1000px) rotateX(6deg) rotateY(-6deg) translateY(-6px) scale(1.02);
        box-shadow: 0 22px 45px rgba(59,130,246,0.22);
        border-color: rgba(139,92,246,0.35);
    }}

    .flashcard-title {{
        font-size: 1.4rem;
        font-weight: 800;
        margin-bottom: 0.8rem;
        color: {text_color};
    }}

    /* ---- SUMMARY CARDS ---- */
    .summary-card {{
        position: relative;
        overflow: hidden;
        background:
            radial-gradient(circle at top left, rgba(59,130,246,0.18), transparent 35%),
            radial-gradient(circle at bottom right, rgba(168,85,247,0.16), transparent 35%),
            rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 24px;
        padding: 1.5rem 1.7rem;
        margin-bottom: 1.1rem;
        box-shadow: 0 14px 34px rgba(0,0,0,0.16);
        animation: fadeInUp 0.8s ease;
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
        transform-style: preserve-3d;
        backdrop-filter: blur(12px);
    }}

    .summary-card:hover {{
        transform: perspective(1000px) rotateX(4deg) rotateY(-4deg) translateY(-6px) scale(1.015);
        box-shadow: 0 22px 45px rgba(59,130,246,0.22);
        border-color: rgba(139,92,246,0.35);
    }}

    .summary-card::before {{
        content: "";
        position: absolute;
        top: 0;
        left: -120%;
        width: 40%;
        height: 100%;
        background: linear-gradient(120deg, transparent, rgba(255,255,255,0.09), transparent);
        animation: shineSweep 5s infinite linear;
    }}

    .summary-card h3 {{
        font-size: 1.2rem;
        font-weight: 800;
        margin-bottom: 0.75rem;
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .summary-card ul {{
        padding-left: 1.2rem;
        margin: 0;
        color: {subtext_color};
        line-height: 2;
    }}

    .summary-card ul li {{
        margin-bottom: 0.2rem;
    }}

    /* ---- KEY TERM CARDS ---- */
    .keyterm-card {{
        position: relative;
        overflow: hidden;
        background:
            radial-gradient(circle at top right, rgba(168,85,247,0.18), transparent 35%),
            radial-gradient(circle at bottom left, rgba(59,130,246,0.15), transparent 35%),
            rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 24px;
        padding: 1.35rem;
        margin-bottom: 1rem;
        box-shadow: 0 14px 34px rgba(0,0,0,0.16);
        animation: fadeInUp 0.8s ease;
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
        transform-style: preserve-3d;
        backdrop-filter: blur(12px);
    }}

    .keyterm-card:hover {{
        transform: perspective(1000px) rotateX(6deg) rotateY(6deg) translateY(-6px) scale(1.02);
        box-shadow: 0 22px 45px rgba(139,92,246,0.22);
        border-color: rgba(96,165,250,0.35);
    }}

    .keyterm-card::before {{
        content: "";
        position: absolute;
        top: 0;
        left: -120%;
        width: 40%;
        height: 100%;
        background: linear-gradient(120deg, transparent, rgba(255,255,255,0.09), transparent);
        animation: shineSweep 5.5s infinite linear;
    }}

    .keyterm-card h3 {{
        font-size: 1.15rem;
        font-weight: 800;
        margin-bottom: 0.6rem;
        background: linear-gradient(90deg, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .keyterm-card p {{
        color: {subtext_color};
        margin: 0;
        line-height: 1.7;
    }}

    .quiz-box {{
        background: rgba(255,255,255,0.05);
        border-left: 4px solid #60a5fa;
        padding: 1rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        box-shadow: 0 8px 22px rgba(0,0,0,0.12);
        animation: fadeInUp 0.7s ease;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}

    .quiz-box:hover {{
        transform: translateX(4px);
        box-shadow: 0 14px 28px rgba(59,130,246,0.16);
    }}

    .answer-box {{
        background: rgba(34,197,94,0.12);
        border: 1px solid rgba(34,197,94,0.25);
        padding: 0.7rem 0.9rem;
        border-radius: 14px;
        margin-top: 0.7rem;
        color: #22c55e;
        font-weight: 700;
        animation: fadeInUp 0.4s ease;
    }}

    .stButton > button {{
        width: 100%;
        border-radius: 16px;
        height: 3.3em;
        font-size: 1rem;
        font-weight: 800;
        border: none;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899, #3b82f6);
        background-size: 250% 250%;
        color: white;
        box-shadow: 0 10px 24px rgba(59,130,246,0.28);
        animation: gradientShift 6s ease infinite, pulseGlow 2.8s infinite ease-in-out;
        transition: transform 0.16s ease, box-shadow 0.16s ease, filter 0.16s ease;
    }}

    .stButton > button:hover {{
        transform: translateY(-3px) scale(1.015);
        box-shadow: 0 16px 32px rgba(139,92,246,0.35);
        filter: brightness(1.05);
    }}

    .stButton > button:active {{
        transform: scale(0.985);
    }}

    .stDownloadButton > button {{
        width: 100%;
        border-radius: 16px;
        height: 3em;
        font-size: 1rem;
        font-weight: 800;
        background: linear-gradient(90deg, #10b981, #14b8a6, #06b6d4, #10b981);
        background-size: 250% 250%;
        color: white;
        border: none;
        box-shadow: 0 10px 24px rgba(16,185,129,0.24);
        animation: gradientShift 7s ease infinite, floatSoft 4s ease-in-out infinite;
        transition: transform 0.16s ease, box-shadow 0.16s ease;
    }}

    .stDownloadButton > button:hover {{
        transform: translateY(-3px) scale(1.015);
        box-shadow: 0 16px 30px rgba(16,185,129,0.32);
    }}

    section[data-testid="stSidebar"] {{
        background: {sidebar_bg};
        border-right: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(14px);
    }}

    textarea {{
        border-radius: 18px !important;
        background: rgba(255,255,255,0.04) !important;
        transition: all 0.2s ease !important;
    }}

    textarea:focus {{
        box-shadow: 0 0 0 2px rgba(96,165,250,0.35) !important;
    }}

    section[data-testid="stFileUploader"] {{
        background: rgba(255,255,255,0.035);
        border-radius: 18px;
        padding: 1rem;
        border: 1px dashed rgba(255,255,255,0.16);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        animation: fadeInUp 0.8s ease;
    }}

    section[data-testid="stFileUploader"]:hover {{
        transform: translateY(-3px);
        box-shadow: 0 14px 30px rgba(59,130,246,0.12);
    }}

    [data-testid="metric-container"] {{
        background: {card_bg};
        border: 1px solid rgba(255,255,255,0.08);
        padding: 1rem;
        border-radius: 18px;
        box-shadow: 0 10px 26px rgba(0,0,0,0.12);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        animation: fadeInUp 0.7s ease;
        backdrop-filter: blur(10px);
    }}

    [data-testid="metric-container"]:hover {{
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 16px 34px rgba(59,130,246,0.16);
        border-color: rgba(96,165,250,0.28);
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background: rgba(255,255,255,0.035);
        padding: 0.5rem;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 1rem;
        animation: fadeInUp 0.8s ease;
    }}

    .stTabs [data-baseweb="tab"] {{
        border-radius: 14px !important;
        padding: 0.7rem 1rem !important;
        transition: all 0.22s ease !important;
    }}

    .stTabs [aria-selected="true"] {{
        background: linear-gradient(90deg, rgba(59,130,246,0.22), rgba(139,92,246,0.22)) !important;
        box-shadow: 0 8px 22px rgba(59,130,246,0.14);
        transform: translateY(-2px);
    }}

    [data-testid="stProgressBar"] > div > div > div {{
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899) !important;
        background-size: 250% 250%;
        animation: gradientShift 4s ease infinite;
        border-radius: 999px;
    }}

    @keyframes pageFade {{
        from {{ opacity: 0; transform: translateY(8px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(18px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes floatSoft {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-5px); }}
        100% {{ transform: translateY(0px); }}
    }}
    @keyframes floatBlob {{
        0% {{ transform: translate(0px, 0px) scale(1); }}
        50% {{ transform: translate(30px, -20px) scale(1.08); }}
        100% {{ transform: translate(0px, 0px) scale(1); }}
    }}
    @keyframes pulseGlow {{
        0% {{ box-shadow: 0 0 0px rgba(139,92,246,0.0), 0 0 0px rgba(59,130,246,0.0); }}
        50% {{ box-shadow: 0 0 28px rgba(139,92,246,0.35), 0 0 36px rgba(59,130,246,0.22); }}
        100% {{ box-shadow: 0 0 0px rgba(139,92,246,0.0), 0 0 0px rgba(59,130,246,0.0); }}
    }}
    @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    @keyframes shineSweep {{
        0% {{ transform: translateX(-120%); }}
        100% {{ transform: translateX(220%); }}
    }}
</style>
""", unsafe_allow_html=True)

# ---------- HERO ----------
st.markdown("""
<div class="hero">
    <h1>📚 NoteSprint AI</h1>
    <p>Turn messy notes into clean summaries, flashcards, quizzes, and revision PDFs in seconds.</p>
    <p style="margin-top: 0.6rem; font-size: 0.95rem; opacity: 0.85;">
        ⚡ Fast • 🎯 Smart • 🧠 Student-focused
    </p>
</div>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("⚙️ Settings")

difficulty = st.sidebar.selectbox("Quiz Difficulty", ["Easy", "Medium", "Hard"])
num_questions = st.sidebar.slider("Number of Questions", 5, 100, 10, step=5)
show_answers = st.sidebar.toggle("Show Answers by Default", value=False)

st.sidebar.markdown("---")
st.sidebar.caption("Tip: Use clean lecture notes or textbook text for best results.")

# ---------- MAIN WORKSPACE ----------
st.markdown('<div class="section-title">📥 Input Your Study Material</div>', unsafe_allow_html=True)

left, right = st.columns([2.2, 1], gap="large")

user_text = ""

with left:
    # st.container(border=True) lets Streamlit widgets sit inside a styled card
    with st.container(border=True):
        input_method = st.radio(
            "Choose input method:",
            ["Paste Text", "Upload File"],
            horizontal=True
        )

        if input_method == "Paste Text":
            user_text = st.text_area(
                "Paste your notes here:",
                height=320,
                placeholder="Paste your notes, lecture content, textbook chapter, or study material here..."
            )
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

        st.markdown("### Generate your study pack")
        if st.button("🚀 Generate Study Pack", use_container_width=True):
            if not user_text.strip():
                st.warning("Please provide some study material first.")
            else:
                st.markdown("""
                <div class="custom-card" style="text-align:center; padding: 1rem;">
                    <h4 style="margin-bottom: 0.4rem;">🤖 AI is building your study pack...</h4>
                    <p>Summaries • Flashcards • Quiz • PDF</p>
                </div>
                """, unsafe_allow_html=True)

                progress = st.progress(0, text="Starting AI generation...")

                try:
                    time.sleep(0.4)
                    progress.progress(20, text="📚 Reading and understanding notes...")
                    time.sleep(0.8)
                    progress.progress(45, text="📝 Creating structured summary...")
                    time.sleep(0.8)
                    progress.progress(70, text="📖 Extracting key terms...")
                    time.sleep(0.8)
                    progress.progress(85, text="❓ Generating quiz questions...")

                    result = generate_study_pack(user_text, difficulty, num_questions)

                    progress.progress(100, text="✅ Study pack ready!")
                    time.sleep(0.5)
                    progress.empty()

                    st.session_state["result"] = result
                    st.success("Study pack generated successfully!")

                except Exception as e:
                    st.error(f"Something went wrong: {e}")

# ---------- RIGHT COLUMN — pure HTML cards (no widgets, so divs work fine) ----------
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

# ---------- RESULTS ----------
if "result" in st.session_state:
    result = st.session_state["result"]

    st.markdown("---")
    st.markdown('<div class="section-title">📊 Your Generated Study Pack</div>', unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Summary Sections", len(result.get("summary", [])))
    with m2:
        st.metric("Key Terms", len(result.get("keyTerms", [])))
    with m3:
        st.metric("Quiz Questions", len(result.get("quiz", [])))

    st.markdown("")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📝 Summary", "📖 Key Terms", "🃏 Flashcards", "❓ Quiz", "📄 Export"]
    )

    with tab1:
        for section in result.get("summary", []):
            st.markdown(f"""
            <div class="summary-card">
                <h3>{section['heading']}</h3>
                <ul>
                    {''.join(f"<li>{p}</li>" for p in section['points'])}
                </ul>
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
            <div class="quiz-box">
                <h4>Q{i}. {q['question']}</h4>
            </div>
            """, unsafe_allow_html=True)

            selected = st.radio(
                f"Choose your answer for Q{i}",
                q["options"],
                key=f"quiz_{i}",
                label_visibility="collapsed"
            )

            if st.button(f"Check Answer for Q{i}", key=f"check_{i}"):
                if selected == q["answer"]:
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Incorrect. Correct answer: {q['answer']}")

            if show_answers:
                st.markdown(f"""
                <div class="answer-box">
                    ✅ Answer: {q['answer']}
                </div>
                """, unsafe_allow_html=True)

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

        st.markdown("")
        st.info("Tip: Download this PDF before your exam for quick revision.")
