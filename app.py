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

# ---------- FIXED DARK THEME ----------
bg_main = "linear-gradient(135deg, #0f172a, #111827)"
text_color = "white"
subtext_color = "#d1d5db"
card_bg = "rgba(255,255,255,0.06)"
sidebar_bg = "rgba(15,23,42,0.95)"

# ---------- CUSTOM CSS ----------
st.markdown(f"""
<style>
    .stApp {{
        background: {bg_main};
        color: {text_color};
    }}

    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}

    .hero {{
        padding: 2rem 2rem 1.5rem 2rem;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(59,130,246,0.18), rgba(168,85,247,0.18));
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 10px 30px rgba(0,0,0,0.18);
        margin-bottom: 1.5rem;
    }}

    .hero h1 {{
        font-size: 2.4rem;
        margin-bottom: 0.5rem;
        color: {text_color};
    }}

    .hero p {{
        font-size: 1.05rem;
        color: {subtext_color};
        margin-bottom: 0.2rem;
    }}

    .custom-card {{
        background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1rem 1rem;
    margin-bottom: 1rem;
    }}

    .flashcard {{
        background: linear-gradient(135deg, rgba(59,130,246,0.18), rgba(168,85,247,0.18));
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 20px;
        padding: 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        min-height: 180px;
    }}

    .flashcard-title {{
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
    }}

    .section-title {{
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: {text_color};
    }}

    .quiz-box {{
        background: rgba(255,255,255,0.05);
        border-left: 4px solid #60a5fa;
        padding: 1rem;
        border-radius: 14px;
        margin-bottom: 1rem;
    }}

    .answer-box {{
        background: rgba(34,197,94,0.12);
        border: 1px solid rgba(34,197,94,0.25);
        padding: 0.65rem 0.85rem;
        border-radius: 12px;
        margin-top: 0.7rem;
        color: #16a34a;
        font-weight: 600;
    }}

    .stButton > button {{
        width: 100%;
        border-radius: 14px;
        height: 3.2em;
        font-size: 1rem;
        font-weight: 700;
        border: none;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        color: white;
        box-shadow: 0 8px 20px rgba(59,130,246,0.3);
    }}

    .stDownloadButton > button {{
        width: 100%;
        border-radius: 14px;
        height: 3em;
        font-size: 1rem;
        font-weight: 700;
        background: linear-gradient(90deg, #10b981, #059669);
        color: white;
        border: none;
    }}

    section[data-testid="stSidebar"] {{
        background: {sidebar_bg};
        border-right: 1px solid rgba(255,255,255,0.08);
    }}

    textarea {{
        border-radius: 16px !important;
    }}

    section[data-testid="stFileUploader"] {{
        background: rgba(255,255,255,0.03);
        border-radius: 16px;
        padding: 1rem;
        border: 1px dashed rgba(255,255,255,0.15);
    }}

    [data-testid="metric-container"] {{
        background: {card_bg};
        border: 1px solid rgba(255,255,255,0.08);
        padding: 1rem;
        border-radius: 16px;
    }}
</style>
""", unsafe_allow_html=True)

# ---------- HERO ----------
st.markdown("""
<div class="hero">
    <h1>📚 NoteSprint AI</h1>
    <p>AI-powered study notes summariser, flashcards, and quiz generator.</p>
</div>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("⚙️ Study Pack Settings")

difficulty = st.sidebar.selectbox(
    "Quiz Difficulty",
    ["Easy", "Medium", "Hard"]
)

num_questions = st.sidebar.slider(
    "Number of Questions",
    5, 100, 10, step=5
)

show_answers = st.sidebar.toggle(
    "Show Answers by Default",
    value=False
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 💡 Demo Tip")
st.sidebar.info("Paste a clean textbook paragraph or lecture notes for the best output.")

st.sidebar.markdown("### 🛠 Included Features")
st.sidebar.markdown("""
- Structured Summary  
- Key Terms  
- Flashcards  
- AI Quiz Generator  
- PDF Export  
""")

# ---------- INPUT AREA ----------
st.markdown('<div class="section-title">📥 Input Your Study Material</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1], gap="large")

user_text = ""

with col1:
    input_method = st.radio("Choose input method:", ["Paste Text", "Upload File"], horizontal=True)

    if input_method == "Paste Text":
        user_text = st.text_area(
            "Paste your notes here:",
            height=300,
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

    st.markdown("### Ready to generate your revision pack?")
    if st.button("🚀 Generate Study Pack", use_container_width=True):
        if not user_text.strip():
            st.warning("Please provide some study material first.")
        else:
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

with col2:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 📌 Quick Overview")
    st.markdown("""
This tool helps students:
- revise faster
- understand key concepts
- test themselves instantly
- download notes for offline study
""")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Best Use Cases")
    st.markdown("""
- Exam revision  
- Last-minute prep  
- Lecture note cleanup  
- Quick self-testing  
""")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- RESULTS ----------
if "result" in st.session_state:
    result = st.session_state["result"]

    st.markdown("---")
    st.markdown('<div class="section-title">📊 Your Generated Study Pack</div>', unsafe_allow_html=True)

    # Metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Summary Sections", len(result.get("summary", [])))
    with m2:
        st.metric("Key Terms", len(result.get("keyTerms", [])))
    with m3:
        st.metric("Quiz Questions", len(result.get("quiz", [])))

    st.markdown("")

    # ---------- TABS ----------
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📝 Summary", "📖 Key Terms", "🃏 Flashcards", "❓ Quiz", "📄 Export"]
    )

    # ---------- TAB 1: SUMMARY ----------
    with tab1:
        for section in result.get("summary", []):
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown(f"### {section['heading']}")
            for point in section["points"]:
                st.markdown(f"- {point}")
            st.markdown('</div>', unsafe_allow_html=True)

    # ---------- TAB 2: KEY TERMS ----------
    with tab2:
        key_terms = result.get("keyTerms", [])
        if key_terms:
            cols = st.columns(2)
            for i, item in enumerate(key_terms):
                with cols[i % 2]:
                    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                    st.markdown(f"### {item['term']}")
                    st.write(item['definition'])
                    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- TAB 3: FLASHCARDS ----------
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
                        <p>Think of the definition before revealing it.</p>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button(f"Reveal Answer — {item['term']}", key=f"flash_{i}"):
                        st.success(item["definition"])

    # ---------- TAB 4: QUIZ ----------
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

    # ---------- TAB 5: EXPORT ----------
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
