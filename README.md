# 📚 NoteSprint AI

**NoteSprint AI** is an AI-powered study assistant that transforms long, messy notes into a complete revision pack in seconds.

It helps students save time by automatically generating:

- 📝 Structured summaries  
- 📖 Key terms and definitions  
- 🃏 Flashcards for active recall  
- ❓ Multiple-choice quizzes  
- 📄 Downloadable PDF revision notes  

---

## 🚀 Problem Statement

Students often spend too much time converting long lecture notes or textbook content into revision material.

Manual revision is:
- time-consuming
- repetitive
- inefficient before exams

**NoteSprint AI** solves this by instantly turning raw notes into a clean, interactive study pack.

---

## ✨ Features

### 📥 Input Support
- Paste study notes directly
- Upload `.txt` and `.pdf` files

### 📝 Smart Summary
- Converts raw notes into structured, easy-to-read revision points

### 📖 Key Terms
- Extracts important concepts and definitions

### 🃏 Flashcard Mode
- Lets students actively test themselves using reveal-based flashcards

### ❓ AI Quiz Generator
- Generates multiple-choice questions based on the uploaded notes
- Adjustable difficulty levels
- Adjustable number of questions

### 📄 PDF Export
- Download the full study pack as a revision PDF

---

## 🛠 Tech Stack

- **Frontend/UI:** Streamlit
- **Language:** Python
- **AI Model:** Google Gemini API
- **PDF Reading:** PyPDF2
- **PDF Export:** ReportLab

---

## ⚙️ How It Works

1. User pastes notes or uploads a PDF/TXT file  
2. The app extracts the text  
3. Gemini AI analyzes the content  
4. The app generates:
   - summary
   - key terms
   - flashcards
   - quiz
5. User can export the study pack as a PDF

---

## 🧪 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/Crypt-osis/Note-Sprint-AI.git
cd Note-Sprint-AI
