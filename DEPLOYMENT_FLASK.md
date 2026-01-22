# 🚀 Deployment Guide - Flask Version

**Good News!** We've migrated from Streamlit to Flask with a professional animated UI. Your app is now ready to deploy on **PythonAnywhere** for FREE!

## ✨ What's New

✅ Professional animated UI with smooth transitions  
✅ Drag & drop file upload  
✅ Tab-based results display  
✅ Dark mode ready CSS  
✅ Mobile responsive design  
✅ TXT & Markdown export  
✅ Better performance  
✅ Ready for production deployment  

---

## 🎯 Deploy to PythonAnywhere (FREE)

### Step 1: Create Account
1. Go to https://www.pythonanywhere.com
2. Sign up for **free account**
3. Verify email

### Step 2: Clone Repository
1. Go to Dashboard → Web
2. Click "Add a new web app"
3. Choose "Flask"
4. In the code editor, replace with:

```bash
# In Bash console:
git clone https://github.com/anubhav-product/ai-interview-resume-copilot.git
cd ai-interview-resume-copilot/app
```

### Step 3: Configure WSGI File
PythonAnywhere will generate a WSGI file. Edit it to:

```python
import sys
path = '/home/{username}/ai-interview-resume-copilot/app'
if path not in sys.path:
    sys.path.append(path)

from main import app
application = app
```

### Step 4: Set Environment Variables
1. Go to Web → (your app) → Environment variables
2. Add:
```
OPENAI_API_KEY=sk-your-key-here
```

### Step 5: Install Dependencies
In Bash console:
```bash
cd /home/{username}/ai-interview-resume-copilot/app
pip install -r requirements.txt
```

### Step 6: Reload Web App
1. Go to Web section
2. Click "Reload app"
3. Your app will be live at: `https://{username}.pythonanywhere.com`

---

## 🏠 Run Locally

### Prerequisites
- Python 3.8+
- pip

### Installation
```bash
cd app
pip install -r requirements.txt
```

### Set API Key
Create `.env` file in `app/` folder:
```
OPENAI_API_KEY=sk-your-key-here
```

### Run
```bash
python main.py
```

Open: http://localhost:5000

---

## 📊 Project Structure

```
app/
├── main.py                 # Flask app (entry point)
├── requirements.txt        # Python dependencies
├── .env                    # API keys (NOT in git)
├── templates/
│   └── index.html         # HTML template
└── static/
    ├── css/
    │   └── style.css      # Professional animations & styling
    └── js/
        └── script.js      # Interactive features
```

---

## 🎨 Features Implemented

### UI/UX
- **Modern Design**: Gradient backgrounds, smooth transitions
- **Animations**: Fade-in, slide-in, bounce, pulse effects
- **Responsive**: Works on desktop, tablet, mobile
- **Dark-ready**: CSS variables for easy theming

### Functionality
- **File Upload**: Drag & drop PDF support
- **Job Description**: Real-time word count
- **Model Selection**: Choose between GPT-3.5 & GPT-4
- **Results Display**: Tab-based (Report, Summary, Export)
- **Export Options**: TXT, Markdown formats
- **Rate Limiting**: 5 requests/hour, 20/day

### Performance
- **Minimal JS**: No heavy frameworks
- **Optimized CSS**: Variable system for fast rendering
- **Fast API**: Flask is lightweight
- **Efficient PDF parsing**: pypdf library

---

## 🔧 Troubleshooting

### Issue: "API Key not found"
**Solution**: 
1. Create `.env` file in `app/` folder
2. Add: `OPENAI_API_KEY=sk-your-key`
3. Restart app

### Issue: "File upload not working"
**Solution**:
1. Check file is PDF
2. Max file size: 5MB
3. Check browser console for errors

### Issue: "Analysis failing"
**Solution**:
1. Check API key is valid (https://platform.openai.com/api-keys)
2. Check rate limits (5/hour, 20/day)
3. Try GPT-3.5 instead of GPT-4

---

## 📚 Alternative Deployment Options

1. **Railway.app**: 
   - Connect GitHub repo
   - Auto deploys
   - Free tier available

2. **Render.com**:
   - Simple deployment
   - GitHub integration
   - Free tier generous

3. **Replit**:
   - Easiest setup
   - Community standard
   - Free hosting

---

## 🔐 Security Notes

⚠️ **NEVER** commit `.env` file  
✅ Use environment variables in production  
✅ Rotate API keys regularly  
✅ Rate limit to prevent abuse  
✅ Validate all file uploads  

---

## 📝 Next Steps

1. ✅ Deploy to PythonAnywhere
2. Get domain name (optional)
3. Share link with recruiters
4. Monitor usage
5. Upgrade model as needed

---

## ❓ Need Help?

- Flask Docs: https://flask.palletsprojects.com
- PythonAnywhere Help: https://help.pythonanywhere.com
- OpenAI API: https://platform.openai.com/docs

**Happy deploying! 🚀**
