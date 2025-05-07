import pdfplumber
import re
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_qa_from_pdf(pdf_path):
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

def mask_sensitive_data(answer):
    answer = re.sub(r"https://[a-zA-Z0-9./]+", lambda m: re.sub(r"[a-zA-Z0-9]", "x", m.group()), answer)
    def mask_json(match):
        try:
            data = json.loads(match.group())
            if 'ID' in data: data['ID'] = "X"
            if 'Name' in data: data['Name'] = "XXX"
            if 'Contact' in data: data['Contact'] = re.sub(r"(?<=\d{1})\d{6}(?=\d{2})", "X" * 6, data['Contact'])
            return json.dumps(data, indent=2)
        except: return match.group()
    answer = re.sub(r'{[^{}]+}', mask_json, answer)
    return answer

def chatbot(query, questions, answers, vectorizer, tfidf_matrix):
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix)
    best_match_index = similarities.argmax()
    return mask_sensitive_data(answers[best_match_index])

# MAIN PROGRAM
if __name__ == "__main__":
    questions, answers = extract_qa_from_pdf("qa_dataset.pdf")
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(questions)

    user_input = input("Ask your API-related question: ")
    response = chatbot(user_input, questions, answers, vectorizer, tfidf_matrix)
    print("\n📦 Masked Answer:\n")
    print(response)
