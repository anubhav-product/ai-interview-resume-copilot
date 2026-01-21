import streamlit as st
from pypdf import PdfReader
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from io import BytesIO
import json
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
except ImportError:
    pass

# Environment Setup
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("❌ OpenAI API key not found. Create .env file in app/ folder with OPENAI_API_KEY=your_key")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

# Rate Limiting Configuration
MAX_REQUESTS_PER_HOUR = 5  # Free tier limit
MAX_REQUESTS_PER_DAY = 20
MAX_TOKENS_PER_REQUEST = 1000  # Cost control

def get_user_id():
    """Get unique user identifier based on session"""
    return str(st.session_state.get("session_id", st.get_option("server.startupScript")))

def check_rate_limit():
    """Check if user has exceeded rate limits"""
    now = datetime.now()
    
    if "usage_log" not in st.session_state:
        st.session_state.usage_log = []
    
    # Clean old entries
    st.session_state.usage_log = [
        entry for entry in st.session_state.usage_log 
        if entry["timestamp"] > now - timedelta(days=1)
    ]
    
    # Check hourly limit
    hourly_count = len([e for e in st.session_state.usage_log if e["timestamp"] > now - timedelta(hours=1)])
    if hourly_count >= MAX_REQUESTS_PER_HOUR:
        return False, f"⏰ Hourly limit ({MAX_REQUESTS_PER_HOUR}/hour) reached. Try again after 1 hour."
    
    # Check daily limit
    daily_count = len([e for e in st.session_state.usage_log if e["timestamp"] > now - timedelta(days=1)])
    if daily_count >= MAX_REQUESTS_PER_DAY:
        return False, f"📊 Daily limit ({MAX_REQUESTS_PER_DAY}/day) reached. Try again tomorrow."
    
    return True, f"✅ Usage: {hourly_count + 1}/{MAX_REQUESTS_PER_HOUR} this hour, {daily_count + 1}/{MAX_REQUESTS_PER_DAY} today"

def log_api_usage():
    """Log API usage for rate limiting"""
    if "usage_log" not in st.session_state:
        st.session_state.usage_log = []
    st.session_state.usage_log.append({"timestamp": datetime.now()})

# Page Config
st.set_page_config(page_title="AI Resume Screening Copilot", page_icon="📄", layout="wide", initial_sidebar_state="expanded")

# CSS Styling with Animations
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
* { font-family: 'Poppins', sans-serif; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
@keyframes slideInLeft { from { opacity: 0; transform: translateX(-30px); } to { opacity: 1; transform: translateX(0); } }
@keyframes slideInRight { from { opacity: 0; transform: translateX(30px); } to { opacity: 1; transform: translateX(0); } }
@keyframes pulse { 0%, 100% { box-shadow: 0 0 0 0 rgba(31, 119, 230, 0.7); } 50% { box-shadow: 0 0 0 10px rgba(31, 119, 230, 0); } }
@keyframes gradientShift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
.main-header { font-size: 2.5rem; background: linear-gradient(135deg, #1f77e6, #5b9ef3, #1f77e6); background-size: 200% 200%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: 700; animation: fadeIn 0.8s, gradientShift 3s infinite; }
.subtitle { font-size: 1rem; color: #555; margin-bottom: 2rem; animation: fadeIn 1s 0.2s backwards; }
.input-card { background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%); border-left: 4px solid #1f77e6; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(31, 119, 230, 0.1); animation: slideInLeft 0.6s; transition: all 0.3s; }
.input-card:hover { box-shadow: 0 8px 25px rgba(31, 119, 230, 0.2); transform: translateY(-5px); }
.input-card h3 { color: #1f77e6; font-weight: 700; margin-bottom: 15px; }
.stButton > button { width: 100%; height: 55px; font-size: 18px; font-weight: 700; border-radius: 10px; background: linear-gradient(135deg, #1f77e6 0%, #1560c0 100%); color: white; border: none; box-shadow: 0 4px 15px rgba(31, 119, 230, 0.3); animation: fadeIn 1.2s 0.4s backwards; }
.stButton > button:hover { background: linear-gradient(135deg, #1560c0 0%, #0f4a9e 100%); box-shadow: 0 8px 25px rgba(31, 119, 230, 0.5); transform: translateY(-3px); }
.stDownloadButton > button { background: linear-gradient(135deg, #4caf50 0%, #45a049 100%) !important; }
h2 { color: #1f77e6; font-weight: 700; border-bottom: 3px solid #1f77e6; padding-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">📄 AI Resume & Interview Screening Copilot</h1>', unsafe_allow_html=True)

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text: text += page_text
    return text

def generate_pdf_report(analysis, candidate_name="Candidate", model_used="gpt-4"):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
        
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#1f77e6'), alignment=TA_CENTER)
        heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#1560c0'))
        
        story.append(Paragraph("📄 Resume Screening Analysis Report", title_style))
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y')}<br/><b>Model:</b> {model_used}", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph("⚠️ This is a decision-support tool only. Always use with human judgment.", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        for line in analysis.split('\n'):
            if line.startswith('###'): 
                story.append(Paragraph(line.replace('###', '').strip(), heading_style))
            elif line.strip(): 
                story.append(Paragraph(line.strip(), styles['Normal']))
        
        doc.build(story)
        pdf_buffer.seek(0)
        return pdf_buffer
    except: return None

def analyze_resume(resume_text, job_description, model="gpt-4"):
    prompt = f"""
You are an AI career assistant. Analyze the resume against job description in markdown format:
### Job Readiness Indicator
- Strong/Developing/Early with 1-2 line explanation
### Matching Skills
- List matching skills
### Strengths
- Key strengths
### Skill Gaps
- Skill / Why it matters / How to improve
### Suggested Job Roles
- Role / Why fits / Skills to strengthen
### Interview Focus Areas
- Topics to probe

Resume: {resume_text[:2000]}
Job Description: {job_description[:1000]}
"""
    try:
        response = client.chat.completions.create(
            model=model, 
            messages=[
                {"role": "system", "content": "You are helpful."}, 
                {"role": "user", "content": prompt}
            ], 
            max_tokens=MAX_TOKENS_PER_REQUEST,
            temperature=0.7
        )
        log_api_usage()
        return response.choices[0].message.content
    except Exception as e:
        if "429" in str(e): st.error("❌ API Quota Exceeded. Check https://platform.openai.com/account/billing")
        elif "model" in str(e).lower(): st.error("❌ Model not available. Try gpt-3.5-turbo")
        else: st.error(f"❌ Error: {str(e)}")
        return None

# Sidebar
st.sidebar.markdown("---\n### ⚙️ Settings")
model = st.sidebar.selectbox("🤖 Select Model:", ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"])
st.sidebar.markdown("---\n### 📖 How to Use:\n1. Upload resume (PDF)\n2. Paste job description\n3. Click Analyze\n4. Download results")
st.sidebar.caption("Made with ❤️ for better hiring")

# Main UI
st.markdown("---")
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="input-card"><h3>📋 Resume</h3></div>', unsafe_allow_html=True)
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    if resume_file: 
        st.success(f"✅ {resume_file.name}")
        st.caption(f"📊 {resume_file.size/1024:.1f} KB")

with col2:
    st.markdown('<div class="input-card"><h3>💼 Job Description</h3></div>', unsafe_allow_html=True)
    job_description = st.text_area("Paste Job Description", height=200, placeholder="✨ Paste job description...")
    if job_description: st.caption(f"📝 {len(job_description.split())} words")

st.markdown("---")

# Display usage info
col_usage_1, col_usage_2, col_usage_3 = st.columns(3)
with col_usage_1:
    can_proceed, usage_msg = check_rate_limit()
    st.info(usage_msg)

col_btn_1, col_btn_2, col_btn_3 = st.columns([2, 1, 2])
with col_btn_2:
    analyze_clicked = st.button("🚀 Analyze", use_container_width=True, disabled=not can_proceed)

if analyze_clicked:
    if resume_file and job_description:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.markdown("⏳ Step 1/3: Extracting resume...")
        progress_bar.progress(33)
        resume_text = extract_text_from_pdf(resume_file)
        
        status_text.markdown("⏳ Step 2/3: Analyzing with AI...")
        progress_bar.progress(66)
        analysis = analyze_resume(resume_text, job_description, model=model)
        
        progress_bar.progress(100)
        status_text.markdown("✅ Analysis complete!")
        import time; time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()

        if analysis:
            st.markdown("---\n## 📊 AI Analysis Results")
            tab1, tab2, tab3 = st.tabs(["📖 Full Report", "💾 Export", "📋 Summary"])
            
            with tab1:
                st.markdown('<div style="background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%); padding: 25px; border-radius: 12px; border-left: 5px solid #1f77e6;">', unsafe_allow_html=True)
                st.markdown(analysis)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with tab2:
                pdf_file = generate_pdf_report(analysis, model_used=model)
                col_txt, col_md, col_pdf = st.columns(3)
                with col_txt:
                    st.download_button("📥 Download TXT", data=analysis, file_name="analysis.txt", mime="text/plain", use_container_width=True)
                with col_md:
                    st.download_button("📄 Download MD", data=analysis, file_name="analysis.md", mime="text/markdown", use_container_width=True)
                with col_pdf:
                    if pdf_file:
                        st.download_button("📋 Download PDF", data=pdf_file, file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf", mime="application/pdf", use_container_width=True)
            
            with tab3:
                st.markdown(f'<div style="background: #e3f2fd; padding: 20px; border-radius: 12px;"><h4>📌 Summary</h4><p>✅ Analysis complete<br>🤖 Model: {model}<br>📊 Resume analyzed<br>💡 Full insights ready</p></div>', unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown('<div style="background: #fff3cd; padding: 20px; border-radius: 12px; border-left: 5px solid #ff9800;"><h4>⚠️ Disclaimer</h4><ul><li>Decision-support tool only</li><li>Always combine with human judgment</li><li>Verify findings through interviews</li><li>Never as final decision</li></ul></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="background: #ffebee; padding: 20px; border-radius: 12px; border-left: 5px solid #f44336; text-align: center;"><h4>❌ Missing Information</h4><p>Upload resume AND paste job description</p></div>', unsafe_allow_html=True)
