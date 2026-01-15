# AI Architecture – Resume Screening MVP

## Overview
The system uses a Large Language Model (LLM) to analyze resumes against a job description and generate structured, explainable insights to support recruiter decision-making.

## Inputs
- Resume text (PDF or plain text)
- Job description text

## Processing Flow
1. Resume text is extracted from the uploaded file
2. Job description is provided by the user
3. Relevant sections of the resume are passed to the LLM
4. The LLM performs:
   - Skill extraction
   - Experience relevance analysis
   - Gap identification
5. Output is generated in a structured format

## Role of LLM
- Semantic understanding of resumes and job descriptions
- Natural language reasoning for skill matching
- Generation of human-readable summaries

## Guardrails
- LLM outputs are constrained to a fixed structure
- No hiring recommendations or scores are produced
- Sensitive attributes (gender, caste, age) are ignored

## Human-in-the-Loop
The system is designed as a decision-support tool. Recruiters make final hiring decisions.

## Limitations
- Not designed for production-scale hiring
- No long-term data storage
- No automated ranking or rejection
