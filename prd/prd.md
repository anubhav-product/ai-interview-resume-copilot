# AI Interview & Resume Screening Copilot

## 1. Product Overview

The AI Interview & Resume Screening Copilot is an AI-powered decision-support product designed to help recruiters screen candidates more efficiently and help candidates receive structured, actionable interview feedback.

### Target Users
- Recruiters and hiring managers at startups and mid-sized companies
- Early-career and mid-level job candidates preparing for interviews

### Value Proposition
- For recruiters: Faster, more consistent resume screening and structured interview preparation
- For candidates: Clear identification of skill gaps and actionable feedback to improve interview performance

---

## 2. Problem Statement

### Recruiter Problems
Recruiters, especially in startups and high-growth teams, receive a high volume of resumes for each role. Manual screening is time-consuming, inconsistent, and prone to bias, often resulting in missed qualified candidates and delayed hiring decisions.

Existing tools rely heavily on keyword matching or rigid filters, which fail to capture transferable skills and true role fit.

### Candidate Problems
Candidates frequently receive rejections without structured or actionable feedback. This makes it difficult for them to understand why they were rejected or how to improve for future interviews.

Most interview preparation platforms provide generic advice rather than role-specific, personalized guidance.

---

## 3. User Personas

### Persona 1: Recruiter
- Role: Recruiter or Hiring Manager at a startup (10–200 employees)
- Goals:
  - Quickly identify high-signal candidates
  - Maintain consistent interview standards
  - Reduce time-to-hire
- Pain Points:
  - Resume overload
  - Subjective screening decisions
  - Inconsistent interview questions
- Success Criteria:
  - Faster shortlisting
  - Clear, explainable candidate evaluations
  - Reduced screening effort

### Persona 2: Candidate
- Role: Early-career or mid-level job seeker
- Goals:
  - Understand interview expectations
  - Identify strengths and skill gaps
  - Improve interview performance
- Pain Points:
  - Rejections without feedback
  - Unclear preparation strategy
- Success Criteria:
  - Actionable feedback
  - Role-specific preparation guidance

---

## 4. Why AI? (Decision Justification)

Manual resume screening and interview preparation do not scale efficiently due to volume and variability in candidate profiles.

Large Language Models enable semantic understanding of resumes and job descriptions, allowing for:
- Skill and experience matching beyond keywords
- Generation of structured, role-specific interview questions
- Personalized feedback summaries

AI is used as a decision-support system rather than a replacement for human judgment. Final hiring decisions remain with recruiters.

---

## 5. Product Goals & Non-Goals

### Goals
- Reduce time spent on resume screening for recruiters
- Improve consistency and structure in interview preparation
- Provide candidates with clear, actionable feedback

### Non-Goals
- Fully automated hiring decisions
- Predicting candidate success or performance
- Replacing human interviews

---

## 6. Core User Flows

### Recruiter Flow
1. Upload job description
2. Upload candidate resumes
3. View AI-generated skill match summaries
4. Receive suggested interview questions
5. Shortlist candidates for interviews

### Candidate Flow
1. Upload resume
2. Select target job description
3. Receive skill-gap analysis
4. Get role-specific interview questions
5. View structured feedback summary

---

## 7. MVP Feature Set

### Included in MVP (v1)
- Resume and job description parsing
- Skill and experience matching
- Interview question generation
- Candidate feedback summaries

### Excluded from MVP
- Video interview analysis
- Automated hiring recommendations
- Applicant tracking system (ATS) integration

---

## 8. AI System Design (High-Level)

- Large Language Model for text understanding and generation
- Retrieval-Augmented Generation (RAG) using job descriptions and resumes
- Prompt constraints to ensure structured outputs
- Guardrails to reduce hallucinations and bias

---

## 9. Metrics & Success Criteria

### Product Metrics
- Number of resumes screened per recruiter
- Feature usage rate

### AI Quality Metrics
- Relevance of skill matching
- Accuracy of generated interview questions
- Hallucination or error rate

### Business Metrics
- Reduction in screening time
- Recruiter satisfaction score

---

## 10. Risks & Mitigations

- Hallucinations: Use grounding via RAG and structured prompts
- Bias: Avoid sensitive attributes and monitor outputs
- Data Privacy: Do not store resumes beyond session scope
- Cost Overruns: Apply token limits and caching strategies

---

## 11. Tradeoffs & Key Decisions

- Accuracy vs latency: Favor slightly slower but higher-quality outputs
- Automation vs control: Keep humans in the loop
- Cost vs scale: Limit scope to high-value features in MVP

---

## 12. Roadmap

### v1 (MVP)
- Resume screening
- Interview question generation
- Feedback summaries

### v2
- Recruiter dashboards
- Custom interview frameworks
- Feedback analytics

### v3
- ATS integrations
- Team collaboration features
- Advanced evaluation metrics

---

## 13. Open Questions & Assumptions

- Will recruiters trust AI-generated evaluations?
- How much feedback do candidates actually want?
- What level of explainability is required for adoption?

---

## 14. Implementation Notes

- Current MVP is a Flask web app served via WSGI.
- Deployment target: PythonAnywhere (see deployment docs).
- Secrets are provided via environment variables (e.g., `OPENAI_API_KEY`).
- Rate limiting and token caps are enforced to control costs.
