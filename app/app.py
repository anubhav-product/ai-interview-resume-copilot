import streamlit as st
from pypdf import PdfReader
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Page config
st.set_page_config(page_title="AI Resume Screening Copilot")

st.title("AI Resume & Interview Screening Copilot")
st.write(
    "This tool helps recruiters and candidates get structured insights from resumes. "
    "It is a decision-support system and does not automate hiring decisions."
)

# -------- Helper Functions --------

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text


def analyze_resume(resume_text, job_description):
    prompt = f"""
You are an AI hiring assistant.

Analyze the resume against the job description.

Return the output STRICTLY in the following markdown format:

### Matching Skills
- List skills from the resume that directly match the job description

### Strengths
- Key strengths of the candidate relevant to the role

### Skill Gaps
- Important missing or weak skills compared to the job description

### Interview Focus Areas
- Areas the interviewer should probe further during interviews

Do NOT provide hiring recommendations or scores.

Resume:
{resume_text}

Job Description:
{job_description}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content


# -------- UI --------

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description", height=200)

if st.button("Analyze"):
    if resume_file and job_description:
        with st.spinner("Analyzing resume against job description..."):
            resume_text = extract_text_from_pdf(resume_file)
            analysis = analyze_resume(resume_text, job_description)

        st.subheader("AI Analysis")
        st.markdown(analysis)

        st.info(
            "⚠️ This analysis is intended to support human decision-making "
            "and should not be used as an automated hiring decision."
        )
    else:
        st.warning("Please upload a resume and paste a job description.")
