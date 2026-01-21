# 🚀 Deployment Guide - Streamlit Cloud (Free)

## Quick Deploy to Web (5 minutes)

### Step 1: Push Code to GitHub
```bash
git add .
git commit -m "Add rate limiting and deployment config"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud (FREE)

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Click **"New app"**
3. Select:
   - Repository: `anubhav-product/ai-interview-resume-copilot`
   - Branch: `main`
   - Main file path: `app/app.py`
4. Click **Deploy**

### Step 3: Add API Key as Secret
1. In Streamlit Cloud dashboard, click your app
2. Click **Settings** (⚙️) → **Secrets**
3. Add:
```
OPENAI_API_KEY = "your_openai_key_here"
```
4. Save - your app will auto-restart

**Your app is now LIVE!** 🎉 Share the URL with others

---

## Cost Controls Implemented

✅ **Rate Limiting:**
- 5 requests/hour per user
- 20 requests/day per user
- 1000 max tokens per request

✅ **Input Limits:**
- Max 10MB file upload
- Resume text truncated to 2000 chars
- Job description truncated to 1000 chars

✅ **Model Selection:**
- Users can choose `gpt-3.5-turbo` (cheaper than gpt-4)
- Default safe token limits

---

## Monitoring Usage

Check OpenAI usage:
1. Go to [platform.openai.com/account/billing](https://platform.openai.com/account/billing)
2. Set spending limits under **Billing** → **Usage limits**
3. Recommend: Set to $10-20/month max

---

## Optional: Custom Domain (Paid)

For custom domain like `resume-copilot.com`:
- Use Streamlit Sharing (free domain: `app-name.streamlit.app`)
- Or upgrade to Streamlit Community Cloud Pro ($20/month) for custom domains

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| API Key not working | Verify key is in Secrets, not `.env` |
| Rate limit errors | Users are at limit, they'll see countdown |
| App won't deploy | Check `app/app.py` exists and `requirements.txt` is correct |
| Upload fails | PDF too large (max 10MB) or corrupted |

---

## Local Testing Before Deploy

```bash
cd app
streamlit run app.py
```

Visit `http://localhost:8501`

---

## Next Steps

- Monitor usage at [platform.openai.com](https://platform.openai.com)
- Share the live URL with others
- Adjust rate limits in `app.py` if needed (lines 27-28)
- Consider switching to cheaper model (gpt-3.5-turbo) if costs are high
