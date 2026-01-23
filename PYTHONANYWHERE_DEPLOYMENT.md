# 🚀 PythonAnywhere Deployment Guide

## Pre-Deployment Checklist ✅

- ✅ Flask app tested locally
- ✅ All files in place (main.py, templates/, static/)
- ✅ requirements.txt updated
- ✅ Code pushed to GitHub
- ✅ API key ready (from OpenAI)

---

## Step-by-Step Deployment (10 minutes)

### 1️⃣ Create PythonAnywhere Account

- Go to: **https://www.pythonanywhere.com**
- Click **"Start exploring PythonAnywhere"** (FREE tier)
- Sign up with your email
- Verify email

### 2️⃣ Open Bash Console

- After login, click **"Bash console"** (right side)
- You'll see a terminal

### 3️⃣ Clone Your Repository

```bash
git clone https://github.com/anubhav-product/ai-interview-resume-copilot.git
cd ai-interview-resume-copilot
```

### 4️⃣ Install Python Packages

```bash
pip install --user -r app/requirements.txt
```

Wait for installation to complete (1-2 minutes).

### 5️⃣ Create WSGI Configuration File

Go back to PythonAnywhere dashboard:
1. Click **"Web"** (top menu)
2. Click **"Add a new web app"**
3. Choose **"Flask"**
4. Choose **"Python 3.9"** (or latest available)
5. Accept defaults

### 6️⃣ Edit WSGI File

Click on the WSGI file that was created:
- Path: `/var/www/your-username_pythonanywhere_com_wsgi.py`

**Replace the entire content with (virtualenv users):**

```python
import sys
import os

project_home = '/home/your-username/ai-interview-resume-copilot/app'
if project_home not in sys.path:
  sys.path.insert(0, project_home)

# Activate your virtualenv
activate_this = '/home/your-username/.virtualenvs/your-venv-name/bin/activate_this.py'
with open(activate_this) as file_:
  exec(file_.read(), dict(__file__=activate_this))

os.environ['FLASK_ENV'] = 'production'

from main import app as application
```

**If you are NOT using a virtualenv, remove the activate_this block:**

```python
import sys
import os

project_home = '/home/your-username/ai-interview-resume-copilot/app'
if project_home not in sys.path:
  sys.path.insert(0, project_home)

os.environ['FLASK_ENV'] = 'production'

from main import app as application
```

### 7️⃣ Set Environment Variables

1. In **Web** tab, scroll down to **"Environment variables"**
2. Click **"New environment variable"**
3. Add your OpenAI API key:
   - **Variable name:** `OPENAI_API_KEY`
   - **Value:** `sk-your-actual-key-here`
4. Save

### 8️⃣ Configure Source Code

1. In **Web** tab, find **"Source code:"**
2. Click to edit and set: `/home/your-username/ai-interview-resume-copilot/app`

### 9️⃣ Configure Working Directory

1. In **Web** tab, find **"Working directory:"**
2. Click to edit and set: `/home/your-username/ai-interview-resume-copilot/app`

### 🔟 Reload Web App

1. Click the green **"Reload your-username.pythonanywhere.com"** button
2. Wait 10 seconds

### ✅ Done!

Your app is now live at: **https://your-username.pythonanywhere.com**

---

## Troubleshooting

### "Module not found" error
**Solution:** Run `pip install --user -r app/requirements.txt` again in bash console

### "API key not found" error
**Solution:** 
1. Check **Web** → **Environment variables**
2. Make sure `OPENAI_API_KEY` is set correctly
3. Reload the web app

### "ModuleNotFoundError: No module named 'main'"
**Solution:**
1. Check Source code path: `/home/your-username/ai-interview-resume-copilot/app`
2. Check Working directory: `/home/your-username/ai-interview-resume-copilot/app`
3. Reload

### "It's working" page but app doesn't load
**Solution:**
1. Check error log: **Web** → **Error log**
2. Look for specific errors
3. Common: Wrong WSGI file path or missing environment variable

### App is slow
**Solution:** This is normal on free tier. Upgrade to Premium for faster response.

---

## File Locations Reference

| File | Location |
|------|----------|
| Flask App | `/home/your-username/ai-interview-resume-copilot/app/main.py` |
| Templates | `/home/your-username/ai-interview-resume-copilot/app/templates/` |
| Static Files | `/home/your-username/ai-interview-resume-copilot/app/static/` |
| WSGI File | `/home/your-username/flask_app.py` |

---

## Post-Deployment

### 1. Test Your App
- Go to: `https://your-username.pythonanywhere.com`
- Try uploading a resume PDF
- Check if analysis works

### 2. Monitor Usage
- Check API calls in OpenAI dashboard
- Watch rate limits (5/hour, 20/day)

### 3. Custom Domain (Optional)
- Go to **Web** tab
- Add custom domain (requires domain purchase)

### 4. Enable HTTPS
- Already enabled on PythonAnywhere ✅

---

## Useful Commands

```bash
# Check installed packages
pip list --user

# Check OpenAI + httpx versions
python -c "import openai, httpx; print(openai.__version__, httpx.__version__)"

# View error log (in bash console)
cat /var/log/your-username.pythonanywhere.com.error.log

# Check Flask version
python -c "import flask; print(flask.__version__)"

# Test API locally before deploying
curl -X POST http://localhost:5000/api/analyze
```

---

## Support

- **PythonAnywhere Docs:** https://help.pythonanywhere.com/
- **Flask Docs:** https://flask.palletsprojects.com/
- **OpenAI API Docs:** https://platform.openai.com/docs/

---

## Security Notes

- Never commit `.env` files (already in `.gitignore`)
- Use environment variables on production
- Change secret key in production:
  ```python
  app.secret_key = 'your-secret-key-here'
  ```
- Keep API key private (use env variables)

---

**You're all set! Your AI Resume Copilot is now live! 🚀**
