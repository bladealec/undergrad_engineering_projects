import re
import json
from PyPDF2 import PdfReader
from docx import Document
import nltk

# Predefined skills list (expand as needed)
SKILLS = ["Python", "JavaScript", "SQL", "HTML", "CSS", "Java", "C++", "Machine Learning"]

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_details(text):
    details = {}
    
    # Extract email
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    details["Email"] = email_match.group() if email_match else "Not found"

    # Extract phone number
    phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    details["Phone"] = phone_match.group() if phone_match else "Not found"

    # Extract skills
    found_skills = [skill for skill in SKILLS if skill.lower() in text.lower()]
    details["Skills"] = found_skills if found_skills else "Not found"

    # Extract education
    if "bachelor" in text.lower():
        details["Education"] = "Bachelor's Degree"
    elif "master" in text.lower():
        details["Education"] = "Master's Degree"
    else:
        details["Education"] = "Not found"

    return details

def main():
    file_path = input("Enter the path to the resume (PDF or DOCX): ")
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        print("Unsupported file format. Please use PDF or DOCX.")
        return

    details = extract_details(text)

    # Save to JSON
    with open("resume_details.json", "w") as json_file:
        json.dump(details, json_file, indent=4)
    
    print("Extracted details saved to resume_details.json")
    print(details)

if __name__ == "__main__":
    main()
