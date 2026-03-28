import streamlit as st
from ai_utils import generate_study_pack
from file_utils import extract_text_from_txt, extract_text_from_pdf
from pdf_utils import create_pdf



st.set_page_config(page_title="AI Study Notes Summariser", page_icon="📚", layout="wide")

st.title("📚 AI Study Notes Summariser & Quiz Generator")
st.write("Upload or paste your notes and generate a smart revision pack instantly.")

# Sidebar settings
st.sidebar.header("⚙️ Settings")
provider = st.sidebar.selectbox("Choose AI Provider", ["Gemini", "OpenAI"])
difficulty = st.sidebar.selectbox("Quiz Difficulty", ["Easy", "Medium", "Hard"])
num_questions = st.sidebar.slider("Number of Questions", 5, 10, 5)

# Input section
st.subheader("📥 Input Your Study Material")
input_method = st.radio("Choose input method:", ["Paste Text", "Upload File"])

user_text = ""

if input_method == "Paste Text":
    user_text = st.text_area("Paste your notes here:", height=250)
else:
    uploaded_file = st.file_uploader("Upload a TXT or PDF file", type=["txt", "pdf"])
    if uploaded_file:
        if uploaded_file.type == "text/plain":
            user_text = extract_text_from_txt(uploaded_file)
        elif uploaded_file.type == "application/pdf":
            user_text = extract_text_from_pdf(uploaded_file)

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

# Display results
if "result" in st.session_state:
    result = st.session_state["result"]

    st.subheader("📝 Summary")
    for section in result.get("summary", []):
        st.markdown(f"### {section['heading']}")
        for point in section["points"]:
            st.markdown(f"- {point}")

    st.subheader("📖 Key Terms")
    for item in result.get("keyTerms", []):
        st.markdown(f"**{item['term']}** — {item['definition']}")

    st.subheader("❓ Quiz")
    for i, q in enumerate(result.get("quiz", []), start=1):
        st.markdown(f"**Q{i}. {q['question']}**")
        for option in q["options"]:
            st.markdown(f"- {option}")
        st.markdown(f"✅ **Answer:** {q['answer']}")
        st.markdown("---")

    pdf_file = create_pdf(result)

    st.download_button(
        label="📄 Download PDF",
        data=pdf_file,
        file_name="study_pack.pdf",
        mime="application/pdf"
    )
