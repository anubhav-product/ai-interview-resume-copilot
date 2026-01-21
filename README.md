# ai-interview-resume-copilot
AI-powered interview and resume screening copilot – PRD, architecture, metrics, and product decisions

## 🚀 Quick Links
- **Live Demo:** Deploy FREE on [Streamlit Cloud](https://share.streamlit.io)
- **[Deployment Guide](./DEPLOYMENT.md)** - 5-minute setup

## Running the App Locally

This project uses environment variables to manage API keys securely.

Create a `.env` file inside the `app/` directory with the following content:

```
OPENAI_API_KEY=your_api_key_here
```

The `.env` file is intentionally excluded from version control.

Then run:
```bash
cd app
pip install -r requirements.txt
streamlit run app.py
```

Visit `http://localhost:8501`

## 🎯 Features
- ✅ Upload resume (PDF) & paste job description
- ✅ AI-powered analysis using GPT-4/GPT-3.5
- ✅ Rate limiting (5/hour, 20/day) to control costs
- ✅ Export results as PDF, TXT, or Markdown
- ✅ Free deployment on Streamlit Cloud

## 🛡️ Cost Controls
- **Rate Limiting**: Prevents API abuse
- **Token Limits**: Max 1000 tokens per request
- **File Limits**: Max 10MB uploads
- **Set Spending Limits**: Configure on OpenAI dashboard
