# 🚀 Quick Start Guide

## Local Testing (5 minutes)

### 1. Install Dependencies
```bash
cd app
pip install -r requirements.txt
```

### 2. Add API Key
Create `app/.env`:
```
OPENAI_API_KEY=sk-your-key-here
```

Get your free key: https://platform.openai.com/api-keys

### 3. Run Locally
```bash
python main.py
```

Visit: **http://localhost:5000** 🎉

---

## Deploy to PythonAnywhere (FREE - No Credit Card!)

### Quick Setup (10 minutes)

1. **Create Account**: https://www.pythonanywhere.com (free tier)

2. **Clone Your Repo**:
   - Bash Console → `git clone https://github.com/anubhav-product/ai-interview-resume-copilot.git`

3. **Install Packages**:
   ```bash
   cd ai-interview-resume-copilot/app
   pip install --user -r requirements.txt
   ```

4. **Add Web App**:
   - Web → Add new web app → Choose Flask
   - Select Python 3.9+

5. **Configure WSGI**:
   Edit the WSGI file to:
   ```python
   import sys
   path = '/home/your-username/ai-interview-resume-copilot/app'
   if path not in sys.path:
       sys.path.append(path)
   from main import app
   application = app
   ```

6. **Set Environment Variable**:
   - Web → Environment variables
   - Add: `OPENAI_API_KEY=sk-your-key`

7. **Reload & Done!** ✅
   - Your URL: `https://your-username.pythonanywhere.com`

---

## 🎨 What You Get

✨ **Professional UI with:**
- Smooth animations
- Drag-and-drop uploads
- Real-time feedback
- Tab-based results
- Export to TXT/MD
- Mobile responsive
- Fast & lightweight

---

## File Structure

```
app/
├── main.py              ← Flask app (run this!)
├── requirements.txt     ← Install these
├── .env                 ← Your API key
├── templates/
│   └── index.html      ← Beautiful UI
└── static/
    ├── css/style.css   ← Animations
    └── js/script.js    ← Interactions
```

---

## 🔑 Get Your API Key

1. Go to: https://platform.openai.com
2. Login (or signup - free $5 credit!)
3. Click your profile → "API keys"
4. Create new secret key
5. Copy and paste into `.env` file

---

## ⚡ Common Issues

**Q: "API key not found"**  
A: Create `.env` file with `OPENAI_API_KEY=sk-...`

**Q: "Python not found"**  
A: Use `python3` instead of `python`

**Q: "File upload not working"**  
A: Check file is PDF and < 5MB

**Q: "Still getting errors?"**  
A: Check browser console (F12) for messages

---

## 📞 Support

- **Local issues?** Run with debug: `FLASK_ENV=development python main.py`
- **PythonAnywhere issues?** Check error log in Web tab
- **API issues?** Visit: https://platform.openai.com/account/api-keys

---

## 🎯 Next Steps

1. ✅ Run locally to test
2. ✅ Get API key from OpenAI
3. ✅ Deploy to PythonAnywhere
4. ✅ Share your URL with recruiters!
5. ✅ Monitor usage in dashboard

**That's it! You're ready to go! 🚀**

---

*For detailed setup, see [DEPLOYMENT_FLASK.md](DEPLOYMENT_FLASK.md)*
