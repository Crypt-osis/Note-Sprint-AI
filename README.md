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

## Workflow Diagram

<img width="1408" height="768" alt="Gemini_Generated_Image_b0fclzb0fclzb0fc" src="https://github.com/user-attachments/assets/e11e3aba-01eb-43e7-995a-37a7b04ae246" />


## 📌 Project Architecture — NoteSprint AI

## 🏗️ System Architecture

1) Input Stage

   The user provides study material in one of three ways:

   typed/pasted notes
   .txt file upload
   PDF upload
   
3) Preprocessing Stage

   The app converts the uploaded file into clean readable text.

   For example:

   .txt → direct reading
   .pdf → text extraction using Python PDF libraries

   This ensures the AI receives usable study content.

4) Prompt Engineering Stage

   The extracted text is placed into separate prompts depending on the task:

   Summary prompt
   Flashcard prompt
   Quiz prompt

   This is important because each output type needs different instructions.

4) AI Generation Stage

   The app sends the processed prompts to Google Gemini API, which returns:

   structured summary
   revision flashcards
   MCQ quiz questions
   
6) Presentation + Export Stage

   The results are displayed inside the app using Streamlit UI.

   Students can then:

   read the output
   revise from it
   download it as a PDF

## ✅ Architecture Diagram


<img width="1024" height="1536" alt="ChatGPT Image Mar 31, 2026, 11_05_05 AM" src="https://github.com/user-attachments/assets/a612b60b-751f-4f73-9e6e-48b9c48a5072" />


## 🏗️ Architecture Notes

NoteSprint AI is built as a lightweight AI-powered study assistant using a modular architecture.

### Main Modules:
- **Input Module** → accepts pasted notes, `.txt`, and PDF files
- **Text Extraction Module** → extracts readable text from uploaded files
- **Prompt Engineering Module** → formats text into task-specific prompts
- **LLM Module** → sends prompts to Google Gemini API
- **Output Module** → displays summary, flashcards, and quiz
- **Export Module** → generates downloadable PDF output

### Data Flow:
User Input → Text Processing → Prompt Engineering → Gemini API → Output Rendering → PDF Export

### Architecture Style:
- Simple monolithic web app
- AI API-integrated pipeline
- Lightweight and hackathon-friendly design
---

## 🧪 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/Crypt-osis/Note-Sprint-AI.git
cd Note-Sprint-AI
```

## ⚙️ Setup Instructions
1. Clone the repository
```
   git clone https://github.com/your-username/NoteSprint-AI.git
   cd NoteSprint-AI
```

2.Create a virtual environment
```
   python -m venv venv
```
3. Activate it
Windows
```
   venv\Scripts\activate
```
Mac/Linux
```
   source venv/bin/activate
```

4. Install dependencies
```
   pip install -r requirements.txt
```
6. Add your API key
   Create a .env file in the root folder and add:
```
   GOOGLE_API_KEY=your_api_key_here
```
▶️ Run Locally
```
streamlit run app.py
```

## ❓ FAQ

### 1) What does this project do?
NoteSprint AI helps students convert long lecture notes, textbook excerpts, or uploaded study material into concise, revision-friendly study resources such as summaries, flashcards, and quizzes.

---

### 2) What kind of input does the app accept?
The app accepts:
- Pasted text notes
- `.txt` files
- Text-based PDF files

---

### 3) Can I upload scanned PDFs or image-based PDFs?
Not reliably. The current version works best with **text-based PDFs**. If a PDF is scanned like an image, text extraction may fail or produce incomplete output.

---

### 4) What outputs does the app generate?
The app can generate:
- Topic-wise bullet-point summaries
- Flashcards for quick revision
- Multiple-choice quiz questions
- Downloadable PDF study material

---

### 5) Which AI model is used in this project?
This project uses the **Google Gemini API** to generate educational outputs from the provided study content.

---

### 6) Do I need an API key to run the app locally?
Yes. You need a valid **Google Gemini API key** and must add it to your `.env` file.

Example:

```env
GOOGLE_API_KEY=your_api_key_here
```
---

7) Why am I getting an “API key not valid” error?

This usually happens if:

the API key is incorrect
the Gemini API is not enabled
the .env file is missing or not loaded properly

Make sure your key is active and correctly configured.

---

8) Is this project free to use?

The code is open-source for hackathon/demo purposes, but actual API usage depends on your Google Gemini API quota and usage limits.

---

9) Can this project work for any subject?

Yes. It is designed to work with most educational text such as:

Biology
Physics
History
Computer Science
Lecture notes
Exam revision material

Output quality depends on the clarity and quality of the input text.

---

10) Does the app store user notes or personal data?

No. In the current version, user input is processed only for generating study outputs and is not permanently stored by the app.
