import pdfplumber
import re
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

# ========== Log Initialization ==========
def initialize_logs():
    log_files = ["feedback.logs", "maskedQ.logs", "error.logs"]
    for log_file in log_files:
        if not os.path.exists(log_file):
            with open(log_file, "w") as f:
                f.write(f"{log_file} created at {datetime.now()}\n")

initialize_logs()

# ========== PDF Extraction ==========
def extract_qa_from_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        qa_blocks = text.split("---")
        questions, answers = [], []
        for block in qa_blocks:
            if "Question:" in block and "Answer:" in block:
                q = block.split("Question:")[1].split("Answer:")[0].strip()
                a = block.split("Answer:")[1].strip()
                questions.append(q)
                answers.append(a)
        return questions, answers
    except Exception as e:
        log_error(f"PDF extraction error: {str(e)}")
        return [], []

# ========== Masking ==========
def mask_sensitive_data(text):
    try:
        text = re.sub(r"https://[a-zA-Z0-9./]+", lambda m: re.sub(r"[a-zA-Z0-9]", "x", m.group()), text)

        # Mask sensitive fields
        patterns = {
            "card_number": r"\b(?:\d[ -]*?){13,16}\b",
            "cvv": r"\b\d{3,4}\b",
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "password": r"(?i)\"?(password|pin|token|otp)\"?\s*[:=]\s*\"?.+?\"?",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b",
            "mobile": r"\b\d{10}\b",
            "dob": r"\b\d{2}[/-]\d{2}[/-]\d{4}\b",
            "transaction_id": r"\btransaction_id\s*[:=]\s*\"?.+?\"?",
            "address": r"\b\d{1,5}\s+\w+(\s\w+)*,\s\w+(\s\w+)*",
            "user_id": r"\buser_id\s*[:=]\s*\"?.+?\"?",
            "customer_id": r"\bcustomer_id\s*[:=]\s*\"?.+?\"?",
            "account_number": r"\b\d{9,18}\b",
        }

        for key, pattern in patterns.items():
            if key in ["card_number"]:
                text = re.sub(pattern, lambda m: "**** **** **** " + m.group()[-4:], text)
            elif key in ["cvv", "pin", "otp"]:
                text = re.sub(pattern, "***", text)
            elif key == "ssn":
                text = re.sub(pattern, "***-**-1234", text)
            elif key == "password" or key == "token":
                text = re.sub(pattern, '"password": "****"', text)
            elif key == "email":
                text = re.sub(pattern, lambda m: m.group()[0] + "***@" + m.group().split('@')[1], text)
            elif key == "mobile":
                text = re.sub(pattern, "******" + text[-4:], text)
            elif key == "dob":
                text = re.sub(pattern, "XX/XX/XXXX", text)
            elif key in ["transaction_id", "user_id", "customer_id"]:
                text = re.sub(pattern, f'"{key}": "XXXXXX"', text)
            elif key == "address":
                text = re.sub(pattern, "XXX, XXX", text)
            elif key == "account_number":
                text = re.sub(pattern, "XXXXXX" + text[-4:], text)
        return text
    except Exception as e:
        log_error(f"Masking error: {str(e)}")
        return text

def mask_user_input(q):
    return re.sub(r"https://[a-zA-Z0-9./]+", lambda m: re.sub(r"[a-zA-Z0-9]", "x", m.group()), q)

# ========== Logging ==========
def log_feedback(question, feedback):
    with open("feedback.logs", "a") as f:
        f.write(f"{datetime.now()} | Question: {question}\nFeedback: {feedback}\n\n")

def log_masked_input(masked_q):
    with open("maskedQ.logs", "a") as f:
        f.write(f"{datetime.now()} | Masked Input: {masked_q}\n")

def log_error(error_msg):
    with open("error.logs", "a") as f:
        f.write(f"{datetime.now()} | ERROR: {error_msg}\n")

# ========== Chatbot Core ==========
def chatbot(query, questions, answers, vectorizer, tfidf_matrix):
    try:
        masked_q = mask_user_input(query)
        log_masked_input(masked_q)

        query_vec = vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, tfidf_matrix)

        print("Similarities: ", similarities)  # Debug: Log similarities to check if they make sense

        # Ensure we get the best match using highest similarity index
        best_index = similarities.argmax()
        
        # If the best similarity is below a threshold, it means we couldn't find a good match
        if similarities[0][best_index] < 0.3:
            return "Sorry, I couldn't find a relevant answer. Please try again with more details."

        return mask_sensitive_data(answers[best_index])
    except Exception as e:
        log_error(f"Chatbot processing error: {str(e)}")
        return "Sorry, something went wrong while processing your question."

# ========== MAIN ==========
if __name__ == "__main__":
    try:
        questions, answers = extract_qa_from_pdf("qa_dataset.pdf")
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(questions)

        while True:
            user_input = input("\n🔹 Ask your API-related question (or type 'exit' to quit):\n> ")
            if user_input.lower() in ["exit", "quit"]:
                print("👋 Exiting the chatbot.")
                break

            # Get the response from the chatbot
            response = chatbot(user_input, questions, answers, vectorizer, tfidf_matrix)
            print("\n📦 Masked Answer:\n", response)

            # Ask for feedback
            feedback = input("\n💬 Was this helpful? (yes/no/comment):\n> ")
            log_feedback(user_input, feedback)

    except Exception as e:
        log_error(f"Startup error: {str(e)}")
