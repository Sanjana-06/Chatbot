# 🔐 API Chatbot with PDF QA Extraction, Masking & Feedback Logging

A Python-based interactive chatbot designed to answer API-related questions extracted from structured PDF documents. It ensures data privacy by masking sensitive information, employs intelligent NLP techniques for question matching, and logs user feedback for continuous improvement.

---

## 🚀 Features

- 📄 **PDF QA Extraction**  
  Automatically extracts question-answer pairs from consistently structured PDF documents.

- 🔐 **Sensitive Data Masking**  
  Masks personally identifiable information (PII) such as:
  - Card numbers
  - Emails
  - Social Security Numbers (SSNs)
  - Phone numbers
  - Dates of Birth
  - Passwords, etc.

- 🤖 **Intelligent Matching**  
  Uses **TF-IDF** and **cosine similarity** to find the most relevant answer based on user input.

- 🗃 **Logging System**  
  Structured logs for different actions:
  - `feedback.logs`: Stores user feedback.
  - `maskedQ.logs`: Tracks masked queries.
  - `error.logs`: Captures exceptions and errors.

- 📬 **Feedback Loop**  
  Collects user feedback on chatbot responses to improve future interactions.

---

## 🧰 Tech Stack

| Category         | Tool/Library                             |
|------------------|-------------------------------------------|
| PDF Extraction   | `pdfplumber`                              |
| NLP              | `scikit-learn` (`TfidfVectorizer`, `cosine_similarity`) |
| Regex Parsing    | `re`                                      |
| Logging          | Python built-in `logging` module          |
| Data Handling    | `json`, `os`, `datetime`                  |

---

## 🧠 How It Works

1. **PDF Q&A Extraction**  
   - Uses regex to extract questions and answers from structured PDFs.
   - Recognizes patterns like `1. Question:` and `Answer:`.

2. **TF-IDF Initialization**  
   - Converts extracted questions into TF-IDF vectors.
   - Computes cosine similarity to find the best match for user queries.

3. **Sensitive Data Masking**  
   - Applies regex-based rules to mask sensitive fields in both questions and answers.

4. **User Interaction**  
   - Accepts user input via CLI.
   - Returns the most relevant answer with masked sensitive data.

5. **Feedback Collection**  
   - After each interaction, asks for feedback.
   - Stores it in `feedback.logs` for future analysis.

---

## ⚠️ Limitations

- Assumes consistent structure in the source PDF (e.g., standard Q&A format).
- Input must be ASCII-compatible (no special encoding).
- Static similarity threshold (`0.3`) may require tuning for varied datasets.
- Regex-based masking may miss certain edge-case patterns.

---

## 🌱 Future Enhancements

- [ ] GUI integration using **Tkinter** or **Streamlit**.
- [ ] Dynamic PDF upload support for live dataset loading.
- [ ] Multi-language question understanding.
- [ ] Integrate NLP models like **BERT** for advanced semantic matching.
- [ ] Automated feedback analysis for self-improving responses.

---
