import streamlit as st
from pypdf import PdfReader

st.set_page_config(page_title="AI Resume Screening Copilot")

st.title("AI Resume & Interview Screening Copilot")
st.write("Upload a resume and paste a job description to get structured insights.")

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description")

if st.button("Analyze"):
    if resume_file and job_description:
        resume_text = extract_text_from_pdf(resume_file)

        st.subheader("Extracted Resume Text (Preview)")
        st.write(resume_text[:1500] + "...")
    else:
        st.warning("Please upload a resume and enter a job description.")
