🔐 API Chatbot with PDF QA Extraction, Masking & Feedback Logging
A Python-based interactive chatbot that answers API-related questions extracted from a structured PDF document. It ensures privacy by masking sensitive data, uses TF-IDF and cosine similarity for accurate question matching, and supports user feedback with structured logs.


🚀 Features
📄 PDF QA Extraction: Automatically extracts questions and answers from structured PDFs.

🔐 Sensitive Data Masking: Masks fields like card numbers, email, SSN, phone, DOB, etc.

🤖 Intelligent Matching: Uses TF-IDF & cosine similarity for relevant answer detection.

🗃 Logging System:

feedback.logs: User feedback history

maskedQ.logs: Tracks masked queries

error.logs: Captures exceptions

📬 Feedback Loop: Collects feedback for each response to continuously improve quality.

🧰 Tech Stack
Category	Tool/Library
PDF Extraction	pdfplumber
NLP	scikit-learn (TfidfVectorizer, cosine_similarity)
Regex Parsing	re
Logging	Built-in logging via custom file-based logs
Data Handling	json, os, datetime


🧠 How It Works
Extract Q&A from PDF:

Uses regex to split questions and answers based on patterns like 1. Question: and Answer:.

Initialize TF-IDF:

Builds a similarity matrix from extracted questions.

Masking Engine:

Identifies and obfuscates fields like card numbers, emails, passwords, mobile numbers, etc.

User Interaction:

Takes user input, finds the best matching question using cosine similarity, and responds with the masked answer.

Feedback Collection:

Prompts user for feedback and logs it in feedback.logs.


⚠️ Limitations
Assumes consistent structure in the Q&A PDF.

Requires internet-safe input encoding (ASCII-like).

Similarity threshold is static (0.3) and might require tuning for larger datasets.

Masking uses regex and may not cover edge-case patterns.

🌱 Future Enhancements
Add GUI for chatbot interface (Tkinter or Streamlit).

Integrate PDF upload feature for dynamic dataset loading.

Support for multiple languages.

Train with actual NLP models like BERT for better understanding.

Automatic feedback analysis to improve response accuracy.



