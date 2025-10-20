import streamlit as st
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

def extract_text_from_pdf(pdf_file):
    images = convert_from_path(pdf_file.name)
    full_text = ""
    for img in images:
        full_text += pytesseract.image_to_string(img) + "\n"
    return full_text

def extract_text_from_image(image_file):
    img = Image.open(image_file)
    return pytesseract.image_to_string(img)

def score_answers(student_text, answer_key):
    student_lines = student_text.strip().split('\n')
    key_lines = answer_key.strip().split('\n')
    score = 0
    feedback = []
    for i in range(min(len(student_lines), len(key_lines))):
        if key_lines[i].lower().strip() in student_lines[i].lower():
            score += 1
            feedback.append(f"Q{i+1}: Correct")
        else:
            feedback.append(f"Q{i+1}: Incorrect")
    grade = "A" if score >= len(key_lines) * 0.8 else "B" if score >= len(key_lines) * 0.5 else "C"
    return score, grade, feedback

st.title("SmartCampus AI Paper Evaluation")

question_file = st.file_uploader("Upload Question Paper (PDF or TXT)")
answer_key_file = st.file_uploader("Upload Answer Key (TXT)")
answer_sheet_file = st.file_uploader("Upload Student Answer Sheet (PDF or Image)")

if st.button("Evaluate"):
    if answer_key_file and answer_sheet_file:
        answer_key = answer_key_file.read().decode("utf-8")
        if answer_sheet_file.name.endswith(".pdf"):
            student_text = extract_text_from_pdf(answer_sheet_file)
        else:
            student_text = extract_text_from_image(answer_sheet_file)
        score, grade, feedback = score_answers(student_text, answer_key)
        st.subheader(f"Score: {score}")
        st.subheader(f"Grade: {grade}")
        st.write("Feedback:")
        for f in feedback:
            st.write(f)
