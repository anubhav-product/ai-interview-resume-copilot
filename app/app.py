import streamlit as st

st.set_page_config(page_title="AI Resume Screening Copilot")

st.title("AI Resume & Interview Screening Copilot")

st.write("Upload a resume and paste a job description to get structured insights.")

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description")

if st.button("Analyze"):
    if resume_file and job_description:
        st.success("Analysis will appear here (LLM integration coming next).")
    else:
        st.warning("Please upload a resume and enter a job description.")
