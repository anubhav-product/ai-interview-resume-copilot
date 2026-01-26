from flask import Flask, render_template, request, jsonify, send_file
from pypdf import PdfReader
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from io import BytesIO
import json
from functools import wraps
import uuid

# Environment Setup
load_dotenv()

# Get API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY or not OPENAI_API_KEY.startswith("sk-"):
    raise ValueError("❌ Invalid or missing OPENAI_API_KEY in .env file")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Flask Setup
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Rate Limiting
MAX_REQUESTS_PER_HOUR = 5
MAX_REQUESTS_PER_DAY = 20
MAX_TOKENS_PER_REQUEST = 1000

# In-memory usage log (use database in production)
usage_log = {}

def get_client_id():
    """Get unique client identifier from request"""
    return request.remote_addr

def check_rate_limit(client_id):
    """Check if client has exceeded rate limits"""
    now = datetime.now()
    
    if client_id not in usage_log:
        usage_log[client_id] = []
    
    # Clean old entries (older than 1 day)
    usage_log[client_id] = [
        entry for entry in usage_log[client_id]
        if entry > now - timedelta(days=1)
    ]
    
    # Check hourly limit
    hourly_count = len([e for e in usage_log[client_id] if e > now - timedelta(hours=1)])
    if hourly_count >= MAX_REQUESTS_PER_HOUR:
        return False, f"⏰ Hourly limit ({MAX_REQUESTS_PER_HOUR}/hour) reached. Try again after 1 hour."
    
    # Check daily limit
    daily_count = len([e for e in usage_log[client_id] if e > now - timedelta(days=1)])
    if daily_count >= MAX_REQUESTS_PER_DAY:
        return False, f"📊 Daily limit ({MAX_REQUESTS_PER_DAY}/day) reached. Try again tomorrow."
    
    return True, f"✅ Usage: {hourly_count + 1}/{MAX_REQUESTS_PER_HOUR} this hour, {daily_count + 1}/{MAX_REQUESTS_PER_DAY} today"

def log_api_usage(client_id):
    """Log API usage for rate limiting"""
    if client_id not in usage_log:
        usage_log[client_id] = []
    usage_log[client_id].append(datetime.now())

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception as e:
        return None

def analyze_resume(resume_text, job_description, model="gpt-3.5-turbo"):
    """Analyze resume using OpenAI API"""
    prompt = f"""
You are an expert ATS (Applicant Tracking System) consultant and career coach. Provide a comprehensive, professional resume analysis.

**IMPORTANT**: Your analysis should be detailed, actionable, and extensive.

# COMPREHENSIVE RESUME ANALYSIS

## 1. EXECUTIVE SUMMARY
Provide an overall assessment of the resume's strengths and alignment with the job description.

## 2. ATS COMPATIBILITY ANALYSIS
### Overall ATS Score: X/100
- **Keyword Match Score**: X/100 - Analysis of keyword density and relevance
- **Format Compatibility**: Assessment of ATS-friendly formatting
- **Critical Issues**: List any formatting problems that will cause ATS rejection
- **Immediate Fixes**: Top 3 urgent changes needed

## 3. DETAILED SKILLS ANALYSIS

### Required Skills Checklist
For each skill in the job description:
- ✓ Skill Name - (Present/Missing)
- Evidence in resume (if present)
- Recommendation for improvement

### Missing Critical Skills (HIGH PRIORITY)
List skills from JD not found in resume and explain their importance

### Transferable Skills to Highlight
Identify skills from resume that apply to this role

## 4. EXPERIENCE ALIGNMENT

### Relevant Experience Breakdown
- Match percentage: X%
- Strongest alignments
- Experience gaps
- Suggestions to reframe existing experience

### Achievement Quantification
- Current quantified achievements found
- Recommendations for adding metrics
- Example bullet point improvements

## 5. KEYWORD OPTIMIZATION STRATEGY

### Current Keywords Present (Matching JD)
List all matching keywords

### CRITICAL Missing Keywords
- Keyword | Importance | Where to Add | How to Incorporate Naturally

### Keyword Density Recommendations
- Optimal placement strategy
- Sections needing keyword enrichment

## 6. ATS-FRIENDLY FORMATTING CHECKLIST
- ✓/✗ Standard section headers
- ✓/✗ Simple, clean font
- ✓/✗ No tables/text boxes/graphics
- ✓/✗ Consistent formatting
- ✓/✗ Proper file format (PDF/Word)
- ✓/✗ Appropriate length (1-2 pages)

### Formatting Improvements Needed
List specific changes

## 7. CONTENT ENHANCEMENT RECOMMENDATIONS

### Professional Summary Rewrite
Provide an improved summary tailored to the job (3-4 sentences with keywords)

### Work Experience Optimization
For top 2-3 positions:
- Current bullet analysis
- Improved version with action verbs and metrics
- Missing impact statements

### Skills Section Enhancement
- Technical skills to add
- Soft skills to emphasize
- Certifications needed

## 8. IMMEDIATE ACTION PLAN

### This Week (CRITICAL):
1. [Specific actionable task]
2. [Specific actionable task]
3. [Specific actionable task]

### Next Week (IMPORTANT):
1. [Specific actionable task]
2. [Specific actionable task]

### Month 1 (ENHANCEMENT):
1. [Specific actionable task]
2. [Specific actionable task]

## 9. COMPETITIVE POSITIONING
- Your unique value proposition for this role
- How to differentiate from other candidates
- Key talking points for interviews

## 10. POTENTIAL RED FLAGS & SOLUTIONS
- Employment gaps (if any) - how to address
- Career transition challenges - how to frame
- Overqualification/underqualification concerns
- Recommended explanations

## 11. INTERVIEW PREPARATION INSIGHTS
Based on your resume:
- Expected interview questions (5-7)
- Key achievements to emphasize
- Stories to prepare (STAR method)

## 12. MATCH ASSESSMENT
- Overall Match Score: X/100
- Match Breakdown:
  * Skills Match: X%
  * Experience Match: X%  
  * Education Match: X%
  * Cultural Fit Indicators: X%

## 13. FINAL RECOMMENDATIONS
- Top 3 strengths to emphasize
- Top 3 areas needing immediate improvement
- Timeline to optimize resume (realistic)
- Success probability if applied today: X%

Resume Content:
{resume_text[:3000]}

Job Description:
{job_description[:2000]}

Provide detailed, specific, actionable analysis following this framework."""
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert ATS consultant and career coach providing detailed, actionable resume analysis. Be specific, comprehensive, and professional."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        error_str = str(e).lower()
        
        if "403" in str(e) or "forbidden" in error_str or ("invalid" in error_str and "api" in error_str):
            return "❌ API Authentication Error: Your API key is invalid or expired. Get a new key from https://platform.openai.com/api-keys"
        elif "429" in str(e):
            return "❌ Rate Limited: OpenAI quota exceeded. Wait a moment and try again."
        elif "model" in error_str:
            return f"❌ Model Not Available: '{model}' not found. Try: gpt-3.5-turbo, gpt-4"
        elif "connection" in error_str or "timeout" in error_str:
            return "❌ Connection Error: Can't reach OpenAI API. Check your internet."
        else:
            return f"❌ API Error: {error_str[:200]}"

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for resume analysis"""
    try:
        client_id = get_client_id()
        
        # Check rate limit
        can_proceed, usage_msg = check_rate_limit(client_id)
        if not can_proceed:
            return jsonify({'success': False, 'error': usage_msg}), 429
        
        # Get form data
        if 'resume' not in request.files:
            return jsonify({'success': False, 'error': 'Resume file not provided'}), 400
        
        if 'job_description' not in request.form:
            return jsonify({'success': False, 'error': 'Job description not provided'}), 400
        
        resume_file = request.files['resume']
        job_description = request.form.get('job_description', '').strip()
        model = request.form.get('model', 'gpt-3.5-turbo')
        
        if not job_description:
            return jsonify({'success': False, 'error': 'Job description cannot be empty'}), 400
        
        # Extract resume text
        resume_text = extract_text_from_pdf(resume_file)
        if not resume_text:
            return jsonify({'success': False, 'error': 'Could not extract text from PDF'}), 400
        
        # Analyze resume
        analysis = analyze_resume(resume_text, job_description, model=model)
        
        # Log usage
        log_api_usage(client_id)
        
        # Check for errors in analysis
        if analysis.startswith("❌"):
            return jsonify({'success': False, 'error': analysis}), 400
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'model': model,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500

@app.route('/api/download', methods=['POST'])
def api_download():
    """Download analysis as text"""
    try:
        data = request.get_json()
        analysis = data.get('analysis', '')
        format_type = data.get('format', 'txt')
        
        if format_type == 'txt':
            buffer = BytesIO(analysis.encode())
            return send_file(
                buffer,
                mimetype='text/plain',
                as_attachment=True,
                download_name=f'analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            )
        elif format_type == 'md':
            buffer = BytesIO(analysis.encode())
            return send_file(
                buffer,
                mimetype='text/markdown',
                as_attachment=True,
                download_name=f'analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
            )
        elif format_type == 'pdf':
            # Professional PDF generation
            from generate_pdf import generate_professional_pdf
            summary = data.get('summary', 'Analysis Summary')
            model = data.get('model', 'gpt-3.5-turbo')
            timestamp = datetime.now()
            pdf_buffer = generate_professional_pdf(analysis, summary, model, timestamp)
            return send_file(
                pdf_buffer,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
            )
        else:
            return jsonify({'error': 'Invalid format'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
