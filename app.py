import streamlit as st
from ocr_google import extract_text_google

def score_answers(student_text, answer_key):
    student_lines = student_text.strip().split('\n')
    key_lines = answer_key.strip().split('\n')
    score = 0
    feedback = []
    for i in range(min(len(student_lines), len(key_lines))):
        if key_lines[i].lower().strip() in student_lines[i].lower():
            score += 1
            feedback.append(f"Q{i+1}: ✅ Correct")
        else:
            feedback.append(f"Q{i+1}: ❌ Incorrect")
    grade = "A" if score >= len(key_lines) * 0.8 else "B" if score >= len(key_lines) * 0.5 else "C"
    return score, grade, feedback

st.title("📚 SmartCampus AI Paper Evaluation")

st.markdown("Upload your files below to evaluate student answers using Google Vision OCR.")

answer_key_file = st.file_uploader("📄 Upload Answer Key (TXT)", type=["txt"])
answer_sheet_file = st.file_uploader("📝 Upload Student Answer Sheet (Image or PDF)", type=["jpg", "jpeg", "png", "pdf"])

api_key_path = "smartcampus-evaluator-ae282b7acc76.json"  # Replace with your actual JSON key filename

if st.button("🚀 Evaluate"):
    if answer_key_file and answer_sheet_file:
        answer_key = answer_key_file.read().decode("utf-8")
        student_text = extract_text_google(answer_sheet_file, api_key_path)
        score, grade, feedback = score_answers(student_text, answer_key)
        st.subheader(f"🔢 Score: {score}")
        st.subheader(f"🏅 Grade: {grade}")
        st.write("🗒️ Feedback:")
        for f in feedback:
            st.write(f)
    else:
        st.warning("Please upload both the answer key and the student answer sheet.")
