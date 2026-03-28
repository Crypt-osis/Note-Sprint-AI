import streamlit as st
from ai_utils import generate_study_pack
from file_utils import extract_text_from_txt, extract_text_from_pdf
from pdf_utils import create_pdf

st.set_page_config(
    page_title="NoteSprint AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
    /* App background */
    .stApp {
        background: linear-gradient(135deg, #0f172a, #111827);
        color: white;
    }

    /* Main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* Hero section */
    .hero {
        padding: 2rem 2rem 1.5rem 2rem;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(59,130,246,0.18), rgba(168,85,247,0.18));
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        font-size: 2.4rem;
        margin-bottom: 0.5rem;
        color: white;
    }

    .hero p {
        font-size: 1.05rem;
        color: #d1d5db;
        margin-bottom: 0.2rem;
    }

    

    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: white;
    }

    .mini-label {
        font-size: 0.9rem;
        color: #cbd5e1;
        margin-bottom: 0.3rem;
    }

    /* Quiz box */
    .quiz-box {
        background: rgba(255,255,255,0.05);
        border-left: 4px solid #60a5fa;
        padding: 1rem;
        border-radius: 14px;
        margin-bottom: 1rem;
    }

    .answer-box {
        background: rgba(34,197,94,0.12);
        border: 1px solid rgba(34,197,94,0.25);
        padding: 0.65rem 0.85rem;
        border-radius: 12px;
        margin-top: 0.7rem;
        color: #bbf7d0;
        font-weight: 600;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 14px;
        height: 3.2em;
        font-size: 1rem;
        font-weight: 700;
        border: none;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        color: white;
        box-shadow: 0 8px 20px rgba(59,130,246,0.3);
    }

    .stDownloadButton > button {
        width: 100%;
        border-radius: 14px;
        height: 3em;
        font-size: 1rem;
        font-weight: 700;
        background: linear-gradient(90deg, #10b981, #059669);
        color: white;
        border: none;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(15,23,42,0.95);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* Text area */
    textarea {
        border-radius: 16px !important;
    }

    /* File uploader */
    section[data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.03);
        border-radius: 16px;
        padding: 1rem;
        border: 1px dashed rgba(255,255,255,0.15);
    }

    /* Metric cards look */
    [data-testid="metric-container"] {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 1rem;
        border-radius: 16px;
    }

</style>
""", unsafe_allow_html=True)

# ---------- HERO ----------
st.markdown("""
<div class="hero">
    <h1>📚 NoteSprint AI</h1>
    <p><i>Built for students who want faster revision and smarter self-testing.</i></p>
    <p>Turn long, messy notes into a smart revision pack in seconds.</p>
    <p>Get <b>summaries</b>, <b>key terms</b>, <b>MCQ quizzes</b>, and a downloadable <b>PDF</b>.</p>
</div>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("⚙️ Customise Your Study Pack")
difficulty = st.sidebar.selectbox("Quiz Difficulty", ["Easy", "Medium", "Hard"])
num_questions = st.sidebar.slider("Number of Questions", 5, 10, 5)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Demo Tip")
st.sidebar.info("Use textbook paragraphs or class notes for the best output.")

st.sidebar.markdown("### 🛠 Features")
st.sidebar.markdown("""
- Structured Summary  
- Key Terms  
- AI Quiz Generator  
- PDF Export  
""")

# ---------- INPUT AREA ----------
st.markdown('<div class="section-title">📥 Input Your Study Material</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1], gap="large")

with col1:
    input_method = st.radio("Choose input method:", ["Paste Text", "Upload File"], horizontal=True)

    user_text = ""

    if input_method == "Paste Text":
        user_text = st.text_area(
            "Paste your notes here:",
            height=300,
            placeholder="Paste your class notes, textbook chapter, or study material here..."
        )

        if st.button("📄 Load Sample Notes"):
            sample_text = """
Photosynthesis is the process by which green plants prepare their own food using sunlight, carbon dioxide, and water. 
Chlorophyll, present in leaves, helps absorb sunlight. During this process, oxygen is released as a by-product. 
Photosynthesis is essential because it provides food for plants and oxygen for living organisms.
"""
            st.session_state["sample_text"] = sample_text
            st.rerun()

        if "sample_text" in st.session_state:
            user_text = st.session_state["sample_text"]
            st.text_area("Loaded Sample Notes:", value=user_text, height=220, disabled=True)

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

# ---------- GENERATE BUTTON ----------
st.markdown("")

if st.button("🚀 Generate Study Pack"):
    if not user_text.strip():
        st.warning("Please provide some study material first.")
    else:
        with st.spinner("Generating your study pack..."):
            try:
                result = generate_study_pack(user_text, difficulty, num_questions)
                st.session_state["result"] = result
                st.success("Study pack generated successfully!")

            except Exception as e:
                st.error(f"Something went wrong: {e}")

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

    # Summary Section
    st.markdown('<div class="section-title">📝 Summary</div>', unsafe_allow_html=True)
    for section in result.get("summary", []):
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown(f"### {section['heading']}")
        for point in section["points"]:
            st.markdown(f"- {point}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Key Terms Section
    st.markdown('<div class="section-title">📖 Key Terms</div>', unsafe_allow_html=True)
    key_terms = result.get("keyTerms", [])

    if key_terms:
        cols = st.columns(2)
        for i, item in enumerate(key_terms):
            with cols[i % 2]:
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.markdown(f"### {item['term']}")
                st.write(item['definition'])
                st.markdown('</div>', unsafe_allow_html=True)

    # Quiz Section
    st.markdown('<div class="section-title">❓ Quiz</div>', unsafe_allow_html=True)
    for i, q in enumerate(result.get("quiz", []), start=1):
        st.markdown(f"""
        <div class="quiz-box">
            <h4>Q{i}. {q['question']}</h4>
        </div>
        """, unsafe_allow_html=True)

        for option in q["options"]:
            st.markdown(f"- {option}")

        st.markdown(f"""
        <div class="answer-box">
            ✅ Answer: {q['answer']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")

    # PDF Download
    pdf_file = create_pdf(result)

    st.markdown("---")
    st.markdown('<div class="section-title">📄 Export</div>', unsafe_allow_html=True)

    st.download_button(
        label="📥 Download Revision PDF",
        data=pdf_file,
        file_name="study_pack.pdf",
        mime="application/pdf"
    )
