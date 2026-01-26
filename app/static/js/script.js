// ==================== DOM ELEMENTS ====================
const resumeInput = document.getElementById('resumeInput');
const resumeDropZone = document.getElementById('resumeDropZone');
const jobDescription = document.getElementById('jobDescription');
const analyzeBtn = document.getElementById('analyzeBtn');
const resetBtn = document.getElementById('resetBtn');
const modelSelect = document.getElementById('modelSelect');
const wordCount = document.getElementById('wordCount');
const nextToJD = document.getElementById('nextToJD');
const backToResume = document.getElementById('backToResume');
const nextToThankYou = document.getElementById('nextToThankYou');
const startOver = document.getElementById('startOver');
const downloadPdf = document.getElementById('downloadPdf');
const downloadTxt = document.getElementById('downloadTxt');
const downloadMd = document.getElementById('downloadMd');

let currentAnalysis = null;
let currentStep = 1;

// ==================== STEP NAVIGATION ====================

function goToStep(stepNumber) {
    // Hide all steps
    document.querySelectorAll('.step-section').forEach(section => {
        section.style.display = 'none';
    });
    
    // Show current step
    const stepElement = document.getElementById(`step${stepNumber}`);
    if (stepElement) {
        stepElement.style.display = 'block';
        stepElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    // Update progress indicator
    document.querySelectorAll('.step-item').forEach((item, index) => {
        if (index < stepNumber) {
            item.classList.add('completed');
            item.classList.remove('active');
        } else if (index === stepNumber - 1) {
            item.classList.add('active');
            item.classList.remove('completed');
        } else {
            item.classList.remove('active', 'completed');
        }
    });
    
    currentStep = stepNumber;
}

// ==================== EVENT LISTENERS ====================

// Resume file input
resumeInput.addEventListener('change', handleResumeSelect);

// Resume drag and drop
resumeDropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    resumeDropZone.classList.add('drag-over');
});

resumeDropZone.addEventListener('dragleave', () => {
    resumeDropZone.classList.remove('drag-over');
});

resumeDropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    resumeDropZone.classList.remove('drag-over');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        resumeInput.files = files;
        handleResumeSelect();
    }
});

// Click on drop zone to browse
resumeDropZone.addEventListener('click', () => {
    resumeInput.click();
});

// Job description word count
jobDescription.addEventListener('input', () => {
    const count = jobDescription.value.trim().split(/\s+/).filter(w => w.length > 0).length;
    wordCount.textContent = count;
});

// Navigation buttons
nextToJD.addEventListener('click', () => goToStep(2));
backToResume.addEventListener('click', () => goToStep(1));
nextToThankYou.addEventListener('click', () => goToStep(4));
startOver.addEventListener('click', handleReset);

// Analyze button
analyzeBtn.addEventListener('click', handleAnalyze);

// Reset button
resetBtn.addEventListener('click', handleReset);

// Tab switching
document.querySelectorAll('.glass-tab').forEach(btn => {
    btn.addEventListener('click', (e) => {
        const button = e.target.closest('.glass-tab');
        if (!button) return;
        
        const tabName = button.dataset.tab;
        
        // Remove active from all tabs
        document.querySelectorAll('.glass-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        
        // Hide all panels
        document.querySelectorAll('.tab-panel').forEach(panel => {
            panel.classList.remove('active');
        });
        
        // Activate clicked tab
        button.classList.add('active');
        
        // Show corresponding panel
        const panel = document.getElementById(`${tabName}-tab`);
        if (panel) {
            panel.classList.add('active');
        }
    });
});

// Legacy tab switching for old tabs (if any)
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        const tabName = e.target.dataset.tab || e.target.closest('.tab-btn').dataset.tab;
        switchTab(tabName);
    });
});

// Download buttons
if (downloadPdf) {
    downloadPdf.addEventListener('click', () => downloadAnalysis('pdf'));
}
if (downloadTxt) {
    downloadTxt.addEventListener('click', () => downloadAnalysis('txt'));
}
if (downloadMd) {
    downloadMd.addEventListener('click', () => downloadAnalysis('md'));
}

// ==================== FILE HANDLING ====================

function handleResumeSelect() {
    const file = resumeInput.files[0];
    if (file) {
        const resumeInfo = document.getElementById('resumeInfo');
        const resumeFileName = document.getElementById('resumeFileName');
        const uploadArea = resumeDropZone;

        // Check file type
        if (file.type !== 'application/pdf') {
            alert('Please upload a PDF file');
            resumeInput.value = '';
            return;
        }

        // Check file size (max 5MB)
        if (file.size > 5 * 1024 * 1024) {
            alert('File size must be less than 5MB');
            resumeInput.value = '';
            return;
        }

        // Display file info
        uploadArea.style.display = 'none';
        resumeInfo.style.display = 'block';
        resumeFileName.textContent = `📄 ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
        
        // Show next button
        nextToJD.style.display = 'block';
    }
}

// ==================== ANALYZE ====================

async function handleAnalyze() {
    // Validate inputs
    if (!resumeInput.files[0]) {
        alert('Please upload a resume');
        goToStep(1);
        return;
    }

    if (!jobDescription.value.trim()) {
        alert('Please enter a job description');
        return;
    }

    // Prepare form data
    const formData = new FormData();
    formData.append('resume', resumeInput.files[0]);
    formData.append('job_description', jobDescription.value);
    formData.append('model', modelSelect.value);

    // Show loading state
    analyzeBtn.disabled = true;
    const btnText = analyzeBtn.querySelector('.btn-text');
    const btnLoader = analyzeBtn.querySelector('.btn-loader');
    btnText.textContent = 'Analyzing...';
    btnLoader.classList.remove('hidden');

    try {
        // Call API
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Analysis failed');
        }

        // Store analysis for export
        currentAnalysis = data.analysis;

        // Display results
        displayResults(data);
        
        // Go to results step
        goToStep(3);

    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        // Reset button state
        analyzeBtn.disabled = false;
        btnText.textContent = 'Analyze Resume';
        btnLoader.classList.add('hidden');
    }
}

function displayResults(data) {
    console.log('displayResults called with:', data);
    const { analysis, model, timestamp } = data;

    // Format the analysis for better display
    const formattedAnalysis = formatAnalysisText(analysis);
    
    const analysisContent = document.getElementById('analysisContent');
    
    if (analysisContent) {
        analysisContent.innerHTML = formattedAnalysis;
    }

    // Update metadata
    const resultModel = document.getElementById('resultModel');
    const resultTime = document.getElementById('resultTime');
    
    if (resultModel) resultModel.textContent = model;
    if (resultTime) resultTime.textContent = new Date(timestamp).toLocaleTimeString();
}

function formatAnalysisText(text) {
    // Convert markdown-style text to HTML with proper formatting
    let html = text;
    
    // Headers (must come before other replacements)
    html = html.replace(/^### (.*?)$/gm, '<h3 style="color: #5eead4; font-size: 1.1rem; font-weight: 700; margin: 1.5rem 0 0.75rem 0; padding-bottom: 0.5rem; border-bottom: 2px solid rgba(94, 234, 212, 0.3);">$1</h3>');
    html = html.replace(/^## (.*?)$/gm, '<h2 style="color: #2dd4bf; font-size: 1.3rem; font-weight: 700; margin: 2rem 0 1rem 0; padding: 0.5rem; background: linear-gradient(135deg, rgba(20, 184, 166, 0.2), rgba(20, 184, 166, 0.1)); border-left: 4px solid #14b8a6; border-radius: 4px;">$1</h2>');
    html = html.replace(/^# (.*?)$/gm, '<h1 style="color: #14b8a6; font-size: 1.5rem; font-weight: 800; margin: 2rem 0 1rem 0; padding: 0.75rem; background: linear-gradient(135deg, rgba(20, 184, 166, 0.25), rgba(20, 184, 166, 0.15)); border-radius: 8px;">$1</h1>');
    
    // Bold text
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong style="color: #5eead4; font-weight: 700;">$1</strong>');
    html = html.replace(/__(.*?)__/g, '<strong style="color: #5eead4; font-weight: 700;">$1</strong>');
    
    // Italic
    html = html.replace(/\*(.*?)\*/g, '<em style="color: #cbd5e1;">$1</em>');
    html = html.replace(/_(.*?)_/g, '<em style="color: #cbd5e1;">$1</em>');
    
    // Code/inline highlights
    html = html.replace(/`(.*?)`/g, '<code style="background: rgba(20, 184, 166, 0.2); color: #5eead4; padding: 0.2rem 0.4rem; border-radius: 4px; font-family: monospace; font-size: 0.9em; border: 1px solid rgba(20, 184, 166, 0.3);">$1</code>');
    
    // Bullet points (unordered)
    html = html.replace(/^[\*\-\•] (.*?)$/gm, '<li style="margin-left: 1.5rem; margin-bottom: 0.5rem; color: #e2e8f0; line-height: 1.6;">$1</li>');
    
    // Numbered lists
    html = html.replace(/^\d+\. (.*?)$/gm, '<li style="margin-left: 1.5rem; margin-bottom: 0.5rem; color: #e2e8f0; line-height: 1.6;">$1</li>');
    
    // Wrap consecutive list items
    html = html.replace(/(<li.*?<\/li>\s*)+/g, function(match) {
        return '<ul style="margin: 0.75rem 0; padding-left: 0;">' + match + '</ul>';
    });
    
    // Add line breaks for paragraphs
    html = html.replace(/\n\n/g, '</p><p style="margin: 0.75rem 0; line-height: 1.7; color: #e2e8f0;">');
    html = '<p style="margin: 0.75rem 0; line-height: 1.7; color: #e2e8f0;">' + html + '</p>';
    
    // Clean up empty paragraphs
    html = html.replace(/<p[^>]*>\s*<\/p>/g, '');
    
    // Add spacing after sections
    html = html.replace(/<\/h1>/g, '</h1><div style="margin-bottom: 1rem;"></div>');
    html = html.replace(/<\/h2>/g, '</h2><div style="margin-bottom: 0.75rem;"></div>');
    html = html.replace(/<\/h3>/g, '</h3><div style="margin-bottom: 0.5rem;"></div>');
    
    return html;
}

function parseMarkdown(markdown) {
    let html = markdown;

    // Headers
    html = html.replace(/^### (.*?)$/gm, '<h3>$1</h3>');
    html = html.replace(/^## (.*?)$/gm, '<h2>$1</h2>');
    html = html.replace(/^# (.*?)$/gm, '<h1>$1</h1>');

    // Bold
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/__(.*?)__/g, '<strong>$1</strong>');

    // Italic
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    html = html.replace(/_(.*?)_/g, '<em>$1</em>');

    // Lists
    html = html.replace(/^\* (.*?)$/gm, '<li>$1</li>');
    html = html.replace(/^- (.*?)$/gm, '<li>$1</li>');
    html = html.replace(/^\d+\. (.*?)$/gm, '<li>$1</li>');

    // Wrap list items
    html = html.replace(/(<li>.*?<\/li>)/s, (match) => {
        return '<ul>' + match + '</ul>';
    });

    // Cleanup multiple ul tags
    html = html.replace(/<\/ul>\s*<ul>/g, '');

    // Code blocks
    html = html.replace(/`(.*?)`/g, '<code>$1</code>');

    // Line breaks
    html = html.replace(/\n\n/g, '</p><p>');
    html = '<p>' + html + '</p>';

    return html;
}

function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    const tabContent = document.getElementById(`${tabName}-tab`);
    if (tabContent) {
        tabContent.classList.add('active');
    }

    // Mark button as active
    const activeBtn = document.querySelector(`[data-tab="${tabName}"]`);
    if (activeBtn) {
        activeBtn.classList.add('active');
    }
}

// ==================== DOWNLOAD ====================

function downloadAnalysis(format) {
    if (!currentAnalysis) {
        alert('No analysis to download');
        return;
    }

    if (format === 'pdf') {
        // For PDF, call the backend API
        const data = {
            analysis: currentAnalysis,
            summary: 'Analysis Summary',
            model: document.getElementById('resultModel')?.textContent || 'gpt-3.5-turbo',
            format: 'pdf'
        };

        fetch('/api/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `resume_analysis_${new Date().toISOString().split('T')[0]}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            // Show thank you message after PDF download
            setTimeout(() => {
                goToStep(4);
            }, 800);
        })
        .catch(error => {
            console.error('PDF download failed:', error);
            alert('Failed to generate PDF. Please try TXT or MD format.');
        });
        return;
    }

    const element = document.createElement('a');
    const timestamp = new Date().toISOString().split('T')[0];
    const content = currentAnalysis;
    const mimeType = format === 'txt' ? 'text/plain' : 'text/markdown';
    const filename = `resume_analysis_${timestamp}.${format}`;

    element.setAttribute('href', 'data:' + mimeType + ';charset=utf-8,' + encodeURIComponent(content));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

// ==================== RESET ====================

function handleReset() {
    // Clear inputs
    resumeInput.value = '';
    jobDescription.value = '';
    wordCount.textContent = '0';

    // Clear file info
    const resumeInfo = document.getElementById('resumeInfo');
    const uploadArea = resumeDropZone;
    resumeInfo.style.display = 'none';
    uploadArea.style.display = 'block';
    nextToJD.style.display = 'none';

    // Clear analysis
    currentAnalysis = null;

    // Go back to step 1
    goToStep(1);
}

// ==================== ERROR HANDLING ====================

function showError(message) {
    alert('Error: ' + message);
}

// ==================== UTILITY FUNCTIONS ====================

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Add smooth scroll behavior
document.addEventListener('DOMContentLoaded', () => {
    // Add animation to elements on scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
            }
        });
    }, {
        threshold: 0.1
    });

    document.querySelectorAll('[class*="section"]').forEach(el => {
        observer.observe(el);
    });
});

// Prevent multiple submissions
let isSubmitting = false;

async function submitAnalysis() {
    if (isSubmitting) return;
    isSubmitting = true;

    try {
        await handleAnalyze();
    } finally {
        isSubmitting = false;
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to analyze
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        if (!analyzeBtn.disabled) {
            handleAnalyze();
        }
    }

    // Escape to close error
    if (e.key === 'Escape') {
        errorSection.style.display = 'none';
    }
});

// ==================== RESPONSIVE BEHAVIOR ====================

// Adjust for mobile
if (window.innerWidth < 768) {
    document.querySelector('.section-grid').style.gridTemplateColumns = '1fr';
}

// Handle window resize
window.addEventListener('resize', () => {
    if (window.innerWidth < 768) {
        document.querySelector('.section-grid').style.gridTemplateColumns = '1fr';
    } else {
        document.querySelector('.section-grid').style.gridTemplateColumns = '1fr 1fr';
    }
});

// ==================== INITIALIZATION ====================

console.log('✅ AI Resume Copilot loaded');
