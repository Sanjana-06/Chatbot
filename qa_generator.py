from fpdf import FPDF

qa_pairs = [
    {
        "question": "Why is `https://api.example.com/user/101` returning 403 Forbidden?",
        "answer": """403 means access is denied. Check your token. Sample response:

https://api.example.com/user/101  
{  
    "ID": 101,  
    "Name": "Alice",  
    "Contact": "9876543210"  
}"""
    },
    {
        "question": "What causes `https://api.example.com/login` to return 401?",
        "answer": """401 Unauthorized often indicates invalid credentials. Example:

https://api.example.com/login  
{  
    "error": "Invalid email or password",  
    "status": 401  
}"""
    },
    # 👉 Add more Q&A here (up to 20)
]

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=12)

for pair in qa_pairs:
    pdf.multi_cell(0, 10, f"Question: {pair['question']}\n\nAnswer:\n{pair['answer']}\n\n---\n")

pdf.output("qa_dataset.pdf")
